#!/usr/bin/env python3
"""
Frontend Build Script for Elden Ring Challenges Website
Builds React frontend and integrates it with Django backend for unified deployment.
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

class FrontendBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / 'myfrontend'
        self.backend_dir = self.root_dir / 'mybackend'
        self.build_dir = self.frontend_dir / 'build'
        self.templates_dir = self.backend_dir / 'templates'
        self.static_dir = self.backend_dir / 'static'
        
    def check_prerequisites(self):
        """Check if all required directories and tools exist."""
        print("🔍 Checking prerequisites...")
        
        issues = []
        
        # Check directories
        if not self.frontend_dir.exists():
            issues.append(f"Frontend directory not found: {self.frontend_dir}")
        
        if not self.backend_dir.exists():
            issues.append(f"Backend directory not found: {self.backend_dir}")
        
        if not (self.frontend_dir / 'package.json').exists():
            issues.append("package.json not found in frontend directory")
        
        # Check for npm
        try:
            subprocess.run(['npm', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            issues.append("npm not found. Please install Node.js and npm")
        
        if issues:
            print("❌ Prerequisites not met:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        print("✅ All prerequisites met!")
        return True
    
    def build_react_app(self):
        """Build the React application for production."""
        print("🔄 Building React application...")
        
        try:
            # Change to frontend directory
            os.chdir(self.frontend_dir)
            
            # Run npm build
            result = subprocess.run(['npm', 'run', 'build'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ React build failed:")
                print(result.stderr)
                return False
            
            print("✅ React build completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error building React app: {str(e)}")
            return False
        finally:
            # Change back to root directory
            os.chdir(self.root_dir)
    
    def prepare_django_directories(self):
        """Create necessary Django directories for frontend integration."""
        print("🔄 Preparing Django directories...")
        
        try:
            # Create templates directory
            self.templates_dir.mkdir(exist_ok=True)
            
            # Create static directory if it doesn't exist
            self.static_dir.mkdir(exist_ok=True)
            
            print("✅ Django directories prepared!")
            return True
            
        except Exception as e:
            print(f"❌ Error preparing directories: {str(e)}")
            return False
    
    def copy_build_files(self):
        """Copy React build files to Django directories."""
        print("🔄 Copying build files to Django...")
        
        try:
            if not self.build_dir.exists():
                print(f"❌ Build directory not found: {self.build_dir}")
                return False
            
            # Copy index.html to templates
            index_src = self.build_dir / 'index.html'
            index_dst = self.templates_dir / 'index.html'
            
            if index_src.exists():
                shutil.copy2(index_src, index_dst)
                print(f"✅ Copied index.html to {index_dst}")
            else:
                print("❌ index.html not found in build directory")
                return False
            
            # Copy static files
            build_static = self.build_dir / 'static'
            if build_static.exists():
                # Remove existing frontend static files
                frontend_static = self.static_dir / 'frontend'
                if frontend_static.exists():
                    shutil.rmtree(frontend_static)
                
                # Copy new static files
                shutil.copytree(build_static, frontend_static)
                print(f"✅ Copied static files to {frontend_static}")
            
            # Copy other assets (favicon, manifest, etc.)
            for file_name in ['favicon.ico', 'logo192.png', 'logo512.png', 'manifest.json', 'robots.txt']:
                src_file = self.build_dir / file_name
                if src_file.exists():
                    dst_file = self.static_dir / file_name
                    shutil.copy2(src_file, dst_file)
                    print(f"✅ Copied {file_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error copying build files: {str(e)}")
            return False
    
    def fix_static_paths(self):
        """Fix static file paths in index.html for Django."""
        print("🔄 Fixing static file paths...")
        
        try:
            index_file = self.templates_dir / 'index.html'
            
            if not index_file.exists():
                print("❌ index.html not found in templates directory")
                return False
            
            # Read the file
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add Django template tags
            if '{% load static %}' not in content:
                content = '{% load static %}\n' + content
            
            # Replace static file paths
            replacements = [
                ('/static/css/', '{% static "frontend/css/" %}'),
                ('/static/js/', '{% static "frontend/js/" %}'),
                ('/static/media/', '{% static "frontend/media/" %}'),
                ('href="/static/', 'href="{% static "frontend/'),
                ('src="/static/', 'src="{% static "frontend/'),
                ('/favicon.ico', '{% static "favicon.ico" %}'),
                ('/logo192.png', '{% static "logo192.png" %}'),
                ('/logo512.png', '{% static "logo512.png" %}'),
                ('/manifest.json', '{% static "manifest.json" %}'),
            ]
            
            for old_path, new_path in replacements:
                content = content.replace(old_path, new_path)
            
            # Fix any remaining static references
            content = content.replace('"static/', '"{% static "frontend/')
            content = content.replace("'static/", "'{% static \"frontend/")
            
            # Write the modified content back
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Static file paths fixed!")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing static paths: {str(e)}")
            return False
    
    def create_build_info(self):
        """Create a build info file with timestamp and details."""
        try:
            from datetime import datetime
            
            build_info = {
                'build_timestamp': datetime.now().isoformat(),
                'frontend_integrated': True,
                'react_build_dir': str(self.build_dir),
                'django_templates_dir': str(self.templates_dir),
                'django_static_dir': str(self.static_dir),
                'note': 'Frontend built and integrated with Django backend'
            }
            
            info_file = self.backend_dir / 'frontend_build_info.json'
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(build_info, f, indent=2)
            
            print(f"✅ Build info saved to {info_file}")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not create build info: {str(e)}")
            return True  # Non-critical error
    
    def cleanup_old_builds(self):
        """Clean up old build artifacts."""
        print("🔄 Cleaning up old builds...")
        
        try:
            # Remove old build directory contents (but keep the directory)
            if self.build_dir.exists():
                for item in self.build_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            
            print("✅ Old builds cleaned up!")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not clean up old builds: {str(e)}")
            return True  # Non-critical error

def main():
    print("🚀 Starting frontend build and integration...")
    print("=" * 60)
    
    builder = FrontendBuilder()
    
    # Check prerequisites
    if not builder.check_prerequisites():
        print("\n❌ Build failed due to missing prerequisites")
        return False
    
    print("\n" + "=" * 60)
    
    # Build React app
    if not builder.build_react_app():
        print("\n❌ Build failed during React compilation")
        return False
    
    print("\n" + "=" * 60)
    
    # Prepare Django directories
    if not builder.prepare_django_directories():
        print("\n❌ Build failed during Django directory preparation")
        return False
    
    # Copy build files
    if not builder.copy_build_files():
        print("\n❌ Build failed during file copying")
        return False
    
    # Fix static paths
    if not builder.fix_static_paths():
        print("\n❌ Build failed during path fixing")
        return False
    
    # Create build info
    builder.create_build_info()
    
    print("\n" + "=" * 60)
    print("✅ Frontend build and integration completed successfully!")
    print("\n🎉 Your React frontend is now integrated with Django!")
    print("\nNext steps:")
    print("1. Start your Django server:")
    print("   cd mybackend")
    print("   python manage.py runserver")
    print("2. Visit http://localhost:8000 to see your integrated app")
    print("3. Your API endpoints are still available at /api/...")
    print("\nFor production deployment:")
    print("- Use --settings=mybackend.settings_production for PostgreSQL")
    print("- Use --settings=mybackend.settings_supabase for Supabase")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
