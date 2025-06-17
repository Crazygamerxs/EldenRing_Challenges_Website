"""
Clean Django settings for serving React build
"""
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = False  # Set to False for production

# Hosts
ALLOWED_HOSTS = [
    'eldenringchallenge.xyz',
    'www.eldenringchallenge.xyz',
    '.onrender.com',
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
    'api',
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mybackend.urls'

# Database
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
    )
}

# Security settings - temporarily relaxed for debugging
SECURE_CONTENT_TYPE_NOSNIFF = False  # Allow JS files to execute
SECURE_BROWSER_XSS_FILTER = False   # Temporarily disable

# CSRF settings - make sure they work with React
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # React needs to read this
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://eldenringchallenge.xyz',
    'https://www.eldenringchallenge.xyz',
    'https://*.onrender.com',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://eldenringchallenge.xyz",
    "https://www.eldenringchallenge.xyz",
]
CORS_ALLOW_CREDENTIALS = True

# Static files - make sure JS/CSS are served with correct MIME types
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Add this middleware order (important!)
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

# Turn on debug temporarily to see what's happening
DEBUG = True

print("✅ Django settings updated for React compatibility")