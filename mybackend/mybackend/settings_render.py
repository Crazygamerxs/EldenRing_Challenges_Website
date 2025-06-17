"""
Production Django settings for Render deployment - CSRF Fixed
"""
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = False  # Production mode

# Hosts
ALLOWED_HOSTS = [
    'eldenringchallenge.xyz',
    'www.eldenringchallenge.xyz',
    '.onrender.com',
    '127.0.0.1',
    'localhost',
]

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mybackend.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mybackend.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

# Auth
AUTH_USER_MODEL = 'api.User'
AUTHENTICATION_BACKENDS = [
    'api.backends.UsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Use WhiteNoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Security settings for production - RELAXED FOR CSRF DEBUGGING
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# SSL settings - temporarily relaxed for debugging
SECURE_SSL_REDIRECT = False  # Set to True once CSRF is working
SESSION_COOKIE_SECURE = False  # Set to True once CSRF is working
CSRF_COOKIE_SECURE = False  # Set to True once CSRF is working

# CSRF settings - configured for React
CSRF_COOKIE_HTTPONLY = False  # React needs to read this
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False  # Use cookie-based CSRF tokens
CSRF_COOKIE_AGE = 31449600  # 1 year

# Add your Render domain to trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://eldenringchallenge.xyz',
    'https://www.eldenringchallenge.xyz',
    'https://*.onrender.com',
    'http://localhost:3000',  # For local development
    'http://127.0.0.1:3000',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://eldenringchallenge.xyz",
    "https://www.eldenringchallenge.xyz",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Logging
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
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.security.csrf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print("✅ Production Django settings loaded with CSRF debugging")