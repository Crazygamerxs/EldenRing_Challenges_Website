#!/usr/bin/env python
"""
Security Monitoring Script for EldenRing Challenges Website
Monitors security logs and sends alerts for suspicious activities
"""

import os
import sys
import re
import datetime
import logging
from pathlib import Path
from collections import defaultdict, Counter

# Add the parent directory to the path so we can import Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_production')
import django
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/django/security_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityMonitor:
    def __init__(self):
        self.log_files = [
            '/var/log/django/security.log',
            '/var/log/django/django.log',
            '/var/log/nginx/access.log',  # If using Nginx
            '/var/log/apache2/access.log'  # If using Apache
        ]
        
        # Security patterns to monitor
        self.suspicious_patterns = {
            'sql_injection': [
                r'union\s+select',
                r'drop\s+table',
                r'insert\s+into',
                r'delete\s+from',
                r'update\s+set',
                r'exec\s*\(',
                r'script\s*>',
                r'<\s*script'
            ],
            'xss_attempts': [
                r'<script[^>]*>',
                r'javascript:',
                r'onload\s*=',
                r'onerror\s*=',
                r'onclick\s*=',
                r'eval\s*\(',
                r'document\.cookie'
            ],
            'path_traversal': [
                r'\.\./\.\.',
                r'\.\.\\\.\.\\',
                r'/etc/passwd',
                r'/etc/shadow',
                r'\.\.%2f',
                r'\.\.%5c'
            ],
            'brute_force': [
                r'Invalid username or password',
                r'Authentication failed',
                r'Login failed',
                r'Rate limit exceeded'
            ],
            'admin_access': [
                r'admin access attempt',
                r'unauthorized admin',
                r'admin login failed'
            ]
        }
        
        # Thresholds for alerts
        self.thresholds = {
            'failed_logins_per_ip': 10,
            'suspicious_requests_per_ip': 5,
            'admin_access_attempts': 3,
            'time_window_minutes': 60
        }
    
    def read_log_file(self, log_file, since_time):
        """Read log file and return lines since specified time"""
        try:
            if not os.path.exists(log_file):
                return []
            
            lines = []
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    # Try to extract timestamp from line
                    if self.is_line_recent(line, since_time):
                        lines.append(line.strip())
            
            return lines
        except Exception as e:
            logger.error(f"Error reading log file {log_file}: {e}")
            return []
    
    def is_line_recent(self, line, since_time):
        """Check if log line is from recent time period"""
        try:
            # Try different timestamp formats
            timestamp_patterns = [
                r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',  # Django format
                r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',  # Apache format
                r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'     # Nginx format
            ]
            
            for pattern in timestamp_patterns:
                match = re.search(pattern, line)
                if match:
                    timestamp_str = match.group(1)
                    try:
                        # Parse timestamp (simplified - you may need to adjust formats)
                        if '-' in timestamp_str:
                            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        else:
                            # Handle other formats as needed
                            continue
                        
                        return timestamp >= since_time
                    except ValueError:
                        continue
            
            # If no timestamp found, assume it's recent
            return True
            
        except Exception:
            return True
    
    def analyze_security_events(self, log_lines):
        """Analyze log lines for security events"""
        events = {
            'failed_logins': defaultdict(list),
            'suspicious_requests': defaultdict(list),
            'admin_attempts': [],
            'attack_patterns': defaultdict(list)
        }
        
        for line in log_lines:
            line_lower = line.lower()
            
            # Extract IP address
            ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', line)
            ip = ip_match.group(1) if ip_match else 'unknown'
            
            # Check for failed logins
            if any(pattern in line_lower for pattern in self.suspicious_patterns['brute_force']):
                events['failed_logins'][ip].append(line)
            
            # Check for admin access attempts
            if any(pattern in line_lower for pattern in self.suspicious_patterns['admin_access']):
                events['admin_attempts'].append((ip, line))
            
            # Check for attack patterns
            for attack_type, patterns in self.suspicious_patterns.items():
                if attack_type in ['brute_force', 'admin_access']:
                    continue
                
                for pattern in patterns:
                    if re.search(pattern, line_lower):
                        events['attack_patterns'][attack_type].append((ip, line))
                        events['suspicious_requests'][ip].append(line)
                        break
        
        return events
    
    def generate_alerts(self, events):
        """Generate security alerts based on events"""
        alerts = []
        
        # Check failed login thresholds
        for ip, failed_attempts in events['failed_logins'].items():
            if len(failed_attempts) >= self.thresholds['failed_logins_per_ip']:
                alerts.append({
                    'type': 'brute_force',
                    'severity': 'high',
                    'ip': ip,
                    'count': len(failed_attempts),
                    'message': f"Potential brute force attack from {ip}: {len(failed_attempts)} failed login attempts"
                })
        
        # Check suspicious request thresholds
        for ip, requests in events['suspicious_requests'].items():
            if len(requests) >= self.thresholds['suspicious_requests_per_ip']:
                alerts.append({
                    'type': 'suspicious_activity',
                    'severity': 'medium',
                    'ip': ip,
                    'count': len(requests),
                    'message': f"Suspicious activity from {ip}: {len(requests)} potentially malicious requests"
                })
        
        # Check admin access attempts
        if len(events['admin_attempts']) >= self.thresholds['admin_access_attempts']:
            alerts.append({
                'type': 'admin_access',
                'severity': 'high',
                'count': len(events['admin_attempts']),
                'message': f"Multiple unauthorized admin access attempts: {len(events['admin_attempts'])} attempts"
            })
        
        # Check for specific attack patterns
        for attack_type, attacks in events['attack_patterns'].items():
            if attacks:
                unique_ips = len(set(ip for ip, _ in attacks))
                alerts.append({
                    'type': attack_type,
                    'severity': 'medium',
                    'count': len(attacks),
                    'unique_ips': unique_ips,
                    'message': f"{attack_type.replace('_', ' ').title()} attempts detected: {len(attacks)} attempts from {unique_ips} unique IPs"
                })
        
        return alerts
    
    def send_security_alert(self, alerts):
        """Send security alert email"""
        if not alerts:
            return
        
        try:
            subject = f"EldenRing Challenges - Security Alert ({len(alerts)} issues)"
            
            message_parts = [
                f"Security monitoring detected {len(alerts)} potential security issues:",
                "",
                "ALERTS:",
                "=" * 50
            ]
            
            for alert in alerts:
                message_parts.extend([
                    f"Type: {alert['type'].upper()}",
                    f"Severity: {alert['severity'].upper()}",
                    f"Message: {alert['message']}",
                    f"Time: {datetime.datetime.now()}",
                    "-" * 30
                ])
            
            message_parts.extend([
                "",
                "Please investigate these security events immediately.",
                "",
                "This is an automated security alert from the EldenRing Challenges monitoring system."
            ])
            
            message = "\n".join(message_parts)
            
            # Only send email if configured
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [os.environ.get('NOTIFICATION_EMAIL', 'admin@yourdomain.com')],
                    fail_silently=False,
                )
                logger.info(f"Security alert email sent for {len(alerts)} issues")
            else:
                logger.warning("Email not configured, security alert not sent")
                logger.warning(f"Security Alert:\n{message}")
            
        except Exception as e:
            logger.error(f"Failed to send security alert email: {e}")
    
    def run_monitoring(self):
        """Run the security monitoring process"""
        logger.info("Starting security monitoring")
        
        # Monitor events from the last hour
        since_time = datetime.datetime.now() - datetime.timedelta(
            minutes=self.thresholds['time_window_minutes']
        )
        
        all_log_lines = []
        
        # Read all log files
        for log_file in self.log_files:
            lines = self.read_log_file(log_file, since_time)
            all_log_lines.extend(lines)
            logger.info(f"Read {len(lines)} recent lines from {log_file}")
        
        if not all_log_lines:
            logger.info("No recent log entries found")
            return
        
        # Analyze security events
        events = self.analyze_security_events(all_log_lines)
        
        # Generate alerts
        alerts = self.generate_alerts(events)
        
        if alerts:
            logger.warning(f"Generated {len(alerts)} security alerts")
            self.send_security_alert(alerts)
        else:
            logger.info("No security issues detected")
        
        # Log summary
        logger.info(f"Security monitoring completed. Analyzed {len(all_log_lines)} log lines")

def main():
    """Main function"""
    monitor = SecurityMonitor()
    monitor.run_monitoring()

if __name__ == "__main__":
    main()
