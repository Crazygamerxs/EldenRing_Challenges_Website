#!/usr/bin/env python
"""
Database Backup Script for EldenRing Challenges Website
Run this script regularly to create database backups
"""

import os
import sys
import subprocess
import datetime
import logging
from pathlib import Path

# Add the parent directory to the path so we can import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_production')
import django
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.core.mail import send_mail

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/django/backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = Path(os.environ.get('BACKUP_STORAGE_PATH', '/var/backups/eldenring_challenges'))
        self.retention_days = int(os.environ.get('BACKUP_RETENTION_DAYS', 30))
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_database_backup(self):
        """Create a PostgreSQL database backup"""
        try:
            db_config = settings.DATABASES['default']
            
            # Build pg_dump command
            backup_file = self.backup_dir / f"eldenring_db_backup_{self.timestamp}.sql"
            
            cmd = [
                'pg_dump',
                f"--host={db_config['HOST']}",
                f"--port={db_config['PORT']}",
                f"--username={db_config['USER']}",
                f"--dbname={db_config['NAME']}",
                '--verbose',
                '--clean',
                '--no-owner',
                '--no-privileges',
                f"--file={backup_file}"
            ]
            
            # Set password via environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = db_config['PASSWORD']
            
            logger.info(f"Starting database backup to {backup_file}")
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database backup completed successfully: {backup_file}")
                
                # Compress the backup
                self.compress_backup(backup_file)
                return True
            else:
                logger.error(f"Database backup failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Database backup error: {e}")
            return False
    
    def compress_backup(self, backup_file):
        """Compress the backup file"""
        try:
            compressed_file = f"{backup_file}.gz"
            
            cmd = ['gzip', str(backup_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Backup compressed: {compressed_file}")
            else:
                logger.error(f"Compression failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Compression error: {e}")
    
    def create_media_backup(self):
        """Create a backup of media files"""
        try:
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                logger.info("No media directory found, skipping media backup")
                return True
            
            backup_file = self.backup_dir / f"eldenring_media_backup_{self.timestamp}.tar.gz"
            
            cmd = [
                'tar',
                '-czf',
                str(backup_file),
                '-C',
                str(Path(media_root).parent),
                Path(media_root).name
            ]
            
            logger.info(f"Starting media backup to {backup_file}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Media backup completed successfully: {backup_file}")
                return True
            else:
                logger.error(f"Media backup failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Media backup error: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        try:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
            
            for backup_file in self.backup_dir.glob("*backup_*.sql.gz"):
                if backup_file.stat().st_mtime < cutoff_date.timestamp():
                    backup_file.unlink()
                    logger.info(f"Removed old backup: {backup_file}")
            
            for backup_file in self.backup_dir.glob("*backup_*.tar.gz"):
                if backup_file.stat().st_mtime < cutoff_date.timestamp():
                    backup_file.unlink()
                    logger.info(f"Removed old backup: {backup_file}")
                    
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
    
    def send_notification(self, success, error_message=None):
        """Send backup notification email"""
        try:
            if success:
                subject = "EldenRing Challenges - Backup Successful"
                message = f"Database backup completed successfully at {datetime.datetime.now()}"
            else:
                subject = "EldenRing Challenges - Backup Failed"
                message = f"Database backup failed at {datetime.datetime.now()}\nError: {error_message}"
            
            # Only send email if configured
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [os.environ.get('NOTIFICATION_EMAIL', 'admin@yourdomain.com')],
                    fail_silently=True,
                )
                logger.info("Backup notification email sent")
            
        except Exception as e:
            logger.error(f"Failed to send notification email: {e}")
    
    def run_backup(self):
        """Run the complete backup process"""
        logger.info("Starting backup process")
        
        db_success = self.create_database_backup()
        media_success = self.create_media_backup()
        
        if db_success and media_success:
            logger.info("All backups completed successfully")
            self.cleanup_old_backups()
            self.send_notification(True)
            return True
        else:
            error_msg = "Database backup failed" if not db_success else "Media backup failed"
            logger.error(f"Backup process failed: {error_msg}")
            self.send_notification(False, error_msg)
            return False

def main():
    """Main function"""
    backup = DatabaseBackup()
    success = backup.run_backup()
    
    if success:
        logger.info("Backup process completed successfully")
        sys.exit(0)
    else:
        logger.error("Backup process failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
