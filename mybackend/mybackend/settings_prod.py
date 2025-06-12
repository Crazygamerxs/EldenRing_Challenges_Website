"""
Production settings for mybackend project.
"""

import os
from pathlib import Path
from .settings import *

# Build paths inside the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Production hosts - configurable via environment variable
ALLOWED_HOSTS = [
    os.environ.get('DOMAIN_NAME', 'localhost'),
    f"www.{os.environ.get('DOMAIN_NAME', 'localhost')}",
    'localhost',  # For local testing
    '127.0.0.1',
    '0.0.0.0',  # For Docker/container deployments
]

# Database - PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'eldenring_prod'),
        'USER': os.environ.get('DB_USER', 'eldenring_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'prefer',  # Use SSL if available
        },
    }
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files

# Additional static files directories
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Your custom static files
    BASE_DIR / 'build' / 'static',  # React build static files
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this for static files
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.SiteSettingsMiddleware',
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings for production
domain_name = os.environ.get('DOMAIN_NAME', 'localhost')
if domain_name != 'localhost':
    CORS_ALLOWED_ORIGINS = [
        f"https://{domain_name}",
        f"https://www.{domain_name}",
        f"http://{domain_name}",  # For development/testing
        f"http://www.{domain_name}",
    ]
else:
    # Local development/testing
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

CORS_ALLOW_CREDENTIALS = True

# CSRF settings for production
if domain_name != 'localhost':
    CSRF_TRUSTED_ORIGINS = [
        f"https://{domain_name}",
        f"https://www.{domain_name}",
        f"http://{domain_name}",
        f"http://www.{domain_name}",
    ]
else:
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (enable when you have SSL certificate)
USE_HTTPS = os.environ.get('USE_HTTPS', 'False').lower() == 'true'
if USE_HTTPS:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Session and CSRF cookie settings
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# Email configuration (reuse your existing Gmail setup)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'ringrunnerhelp@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'cyiqmpfvbomjvnkk')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', f'noreply@{domain_name}')

# Cache configuration (optional but recommended)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Template configuration for React
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # React build templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Performance optimizations
if not DEBUG:
    # Disable admin docs in production
    INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'django.contrib.admindocs']
    
    # Add compression middleware
    MIDDLEWARE.insert(1, 'django.middleware.gzip.GZipMiddleware')

# Secret key from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-_)qm!2+p2^e_ilfm-#3rwvbs!(d&l&e-t18-nk75iky5#n0lz(')

# Frontend URL for production
FRONTEND_URL = f"http://{domain_name}:8000" if domain_name == 'localhost' else f"https://{domain_name}"
