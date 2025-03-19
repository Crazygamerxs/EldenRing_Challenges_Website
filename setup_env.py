#!/usr/bin/env python3
"""
Script to help set up environment variables for the Elden Ring Challenges Website.
This script will create a .env file based on user input.
"""

import os
import secrets
import string
from getpass import getpass

def generate_secret_key(length=50):
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_input(prompt, default=None, password=False):
    """Get user input with a default value."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    if password:
        value = getpass(prompt)
    else:
        value = input(prompt)
    
    return value if value else default

def setup_backend_env():
    """Set up the backend .env file."""
    print("\n=== Setting up backend environment variables ===\n")
    
    # Create .env file
    env_path = os.path.join('mybackend', '.env')
    
    # Check if file exists
    if os.path.exists(env_path):
        overwrite = get_input("The .env file already exists. Overwrite? (y/n)", "n")
        if overwrite.lower() != 'y':
            print("Skipping backend .env setup.")
            return
    
    # Django settings
    django_secret_key = get_input("Django secret key", generate_secret_key())
    django_debug = get_input("Django debug mode (True/False)", "False")
    django_settings_module = get_input("Django settings module", "mybackend.settings_prod")
    
    # Database settings
    use_postgres = get_input("Use PostgreSQL? (y/n)", "n")
    db_settings = {}
    if use_postgres.lower() == 'y':
        db_settings['DB_NAME'] = get_input("Database name", "eldenring")
        db_settings['DB_USER'] = get_input("Database user", "dbuser")
        db_settings['DB_PASSWORD'] = get_input("Database password", password=True)
        db_settings['DB_HOST'] = get_input("Database host", "localhost")
        db_settings['DB_PORT'] = get_input("Database port", "5432")
    
    # Email settings
    email_host = get_input("Email host", "smtp.gmail.com")
    email_port = get_input("Email port", "587")
    email_use_tls = get_input("Use TLS for email? (True/False)", "True")
    email_use_ssl = get_input("Use SSL for email? (True/False)", "False")
    email_host_user = get_input("Email host user")
    email_host_password = get_input("Email host password", password=True)
    
    # Domain settings
    domain = get_input("Domain name", "eldenring.biz")
    allowed_hosts = get_input("Allowed hosts (comma-separated)", f"{domain},www.{domain}")
    csrf_trusted_origins = get_input("CSRF trusted origins (comma-separated)", f"https://{domain},https://www.{domain}")
    cors_allowed_origins = get_input("CORS allowed origins (comma-separated)", f"https://{domain},https://www.{domain}")
    
    # Security settings
    secure_ssl_redirect = get_input("Secure SSL redirect (True/False)", "True")
    session_cookie_secure = get_input("Session cookie secure (True/False)", "True")
    csrf_cookie_secure = get_input("CSRF cookie secure (True/False)", "True")
    
    # Write to file
    with open(env_path, 'w') as f:
        f.write("# Django Settings\n")
        f.write(f"DJANGO_SECRET_KEY={django_secret_key}\n")
        f.write(f"DJANGO_DEBUG={django_debug}\n")
        f.write(f"DJANGO_SETTINGS_MODULE={django_settings_module}\n\n")
        
        if use_postgres.lower() == 'y':
            f.write("# Database Configuration\n")
            for key, value in db_settings.items():
                f.write(f"{key}={value}\n")
            f.write("\n")
        
        f.write("# Email Configuration\n")
        f.write(f"EMAIL_HOST={email_host}\n")
        f.write(f"EMAIL_PORT={email_port}\n")
        f.write(f"EMAIL_USE_TLS={email_use_tls}\n")
        f.write(f"EMAIL_USE_SSL={email_use_ssl}\n")
        f.write(f"EMAIL_HOST_USER={email_host_user}\n")
        f.write(f"EMAIL_HOST_PASSWORD={email_host_password}\n\n")
        
        f.write("# Domain Configuration\n")
        f.write(f"ALLOWED_HOSTS={allowed_hosts}\n")
        f.write(f"CSRF_TRUSTED_ORIGINS={csrf_trusted_origins}\n")
        f.write(f"CORS_ALLOWED_ORIGINS={cors_allowed_origins}\n\n")
        
        f.write("# Security Settings\n")
        f.write(f"SECURE_SSL_REDIRECT={secure_ssl_redirect}\n")
        f.write(f"SESSION_COOKIE_SECURE={session_cookie_secure}\n")
        f.write(f"CSRF_COOKIE_SECURE={csrf_cookie_secure}\n")
    
    print(f"Backend .env file created at {env_path}")

def setup_frontend_env():
    """Set up the frontend .env file."""
    print("\n=== Setting up frontend environment variables ===\n")
    
    # Create .env file
    env_path = os.path.join('myfrontend', '.env')
    
    # Check if file exists
    if os.path.exists(env_path):
        overwrite = get_input("The .env file already exists. Overwrite? (y/n)", "n")
        if overwrite.lower() != 'y':
            print("Skipping frontend .env setup.")
            return
    
    # API URL
    api_url = get_input("API URL", "https://eldenring.biz/api")
    
    # Environment
    environment = get_input("Environment (development/production)", "production")
    
    # Debug
    debug = get_input("Enable debug features (true/false)", "false")
    
    # Write to file
    with open(env_path, 'w') as f:
        f.write(f"REACT_APP_API_URL={api_url}\n")
        f.write(f"REACT_APP_ENV={environment}\n")
        f.write(f"REACT_APP_DEBUG={debug}\n")
    
    print(f"Frontend .env file created at {env_path}")

def main():
    """Main function."""
    print("=== Elden Ring Challenges Website Environment Setup ===")
    print("This script will help you set up the environment variables for the application.")
    
    setup_backend = get_input("Set up backend environment variables? (y/n)", "y")
    if setup_backend.lower() == 'y':
        setup_backend_env()
    
    setup_frontend = get_input("Set up frontend environment variables? (y/n)", "y")
    if setup_frontend.lower() == 'y':
        setup_frontend_env()
    
    print("\n=== Environment setup complete ===")
    print("You can now run the deployment script to deploy the application.")
    print("./deploy.sh --env prod")

if __name__ == "__main__":
    main()
