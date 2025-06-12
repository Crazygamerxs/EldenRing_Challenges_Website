"""
Local development settings that simulate production environment
This file inherits from settings_production.py but overrides settings for local testing
"""

from .settings_production import *
import os

# Override settings for local development testing
DEBUG = False  # Keep production-like behavior

# Allow localhost for local testing
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'localhost',
    '127.0.0.1',
    # Add your server IP if needed
    # '123.456.789.012',
]

# Disable SSL-related settings for local HTTP testing
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Update logging to use local directories instead of /var/log/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 10*1024*1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'maxBytes': 10*1024*1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',  # More verbose for local testing
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file', 'console'],  # Also log to console for local testing
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Optional: Add CORS for localhost if needed for frontend testing
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
]

# Optional: Add localhost to CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

print("🚀 Using LOCAL PRODUCTION settings with Supabase database")
print("📍 Server will be available at: http://127.0.0.1:8000")
print("🔒 Security middleware: ENABLED")
print("🗄️  Database: Supabase PostgreSQL")
