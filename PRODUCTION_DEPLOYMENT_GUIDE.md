# Production Deployment Guide

## Elden Ring Challenges Website

This guide provides step-by-step instructions for deploying your Django + React application to production using a single Django server with WhiteNoise for static file serving.

## 🎯 Overview

**What this deployment does:**

- ✅ Serves both Django API and React frontend from a single Django server
- ✅ Uses PostgreSQL for production database
- ✅ WhiteNoise for efficient static file serving
- ✅ Gunicorn as production WSGI server
- ✅ Environment-based configuration
- ✅ Automated deployment scripts

**Production Architecture:**

```
[Client Browser] → [Django + Gunicorn :8000] → [PostgreSQL Database]
                           ↓
                    [WhiteNoise serves React static files]
```

## 📋 Prerequisites

### 1. System Requirements

- Python 3.8+ installed
- Node.js 16+ and npm installed
- PostgreSQL 12+ installed and running
- Git (for version control)

### 2. PostgreSQL Setup

**Install PostgreSQL:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Windows (using chocolatey)
choco install postgresql

# macOS (using homebrew)
brew install postgresql
```

**Create Database and User:**

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE eldenring_prod;
CREATE USER eldenring_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE eldenring_prod TO eldenring_user;
ALTER USER eldenring_user CREATEDB;
\q
```

## 🚀 Deployment Steps

### Step 1: Environment Configuration

1. **Copy the environment template:**

```bash
cp .env.production .env.production.local
```

2. **Edit `.env.production.local` with your settings:**

```bash
# Domain Configuration
DOMAIN_NAME=yourdomain.com  # Change this to your actual domain

# HTTPS Configuration (set to True when you have SSL)
USE_HTTPS=False

# Generate a new secret key for production
SECRET_KEY=your_new_secret_key_here

# Database Configuration
DB_NAME=eldenring_prod
DB_USER=eldenring_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (update if needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

3. **Generate a new Django secret key:**

```bash
cd mybackend
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
cd mybackend
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
cd myfrontend
npm install
cd ..
```

### Step 3: Deploy Application

**Run the deployment script:**

```bash
# Make scripts executable (Linux/macOS)
chmod +x deploy_production.sh
chmod +x start_server.sh
chmod +x build_frontend.sh

# Deploy to production
./deploy_production.sh
```

**What the deployment script does:**

1. 📦 Installs Python dependencies
2. 🎨 Builds React frontend with production optimizations
3. 🔧 Integrates React build with Django
4. 🗃️ Sets up PostgreSQL database and runs migrations
5. 👤 Creates admin user (admin/admin123)
6. 📋 Collects static files
7. 🔒 Runs security checks

### Step 4: Start Production Server

```bash
./start_server.sh
```

**Server will be available at:**

- Frontend: http://localhost:8000
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## 🔧 Manual Deployment (Alternative)

If you prefer to run steps manually:

### 1. Build Frontend

```bash
./build_frontend.sh
```

### 2. Setup Database

```bash
cd mybackend
export $(cat ../.env.production.local | grep -v '^#' | xargs)
python manage.py migrate --settings=mybackend.settings_prod
python manage.py collectstatic --noinput --settings=mybackend.settings_prod
```

### 3. Start Server

```bash
gunicorn mybackend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --env DJANGO_SETTINGS_MODULE=mybackend.settings_prod
```

## 🔄 Development vs Production

### Development Workflow (Current)

```bash
# Terminal 1: Django API
cd mybackend && python manage.py runserver localhost:8888

# Terminal 2: React Frontend
cd myfrontend && npm start
```

### Production Workflow (New)

```bash
# Deploy changes
./deploy_production.sh

# Start production server
./start_server.sh
```

## 🛠️ Configuration Details

### Environment Variables

| Variable      | Description              | Default        | Required |
| ------------- | ------------------------ | -------------- | -------- |
| `DOMAIN_NAME` | Your domain name         | localhost      | Yes      |
| `USE_HTTPS`   | Enable HTTPS redirects   | False          | No       |
| `SECRET_KEY`  | Django secret key        | (dev key)      | Yes      |
| `DB_NAME`     | PostgreSQL database name | eldenring_prod | Yes      |
| `DB_USER`     | PostgreSQL username      | eldenring_user | Yes      |
| `DB_PASSWORD` | PostgreSQL password      | -              | Yes      |
| `DB_HOST`     | PostgreSQL host          | localhost      | No       |
| `DB_PORT`     | PostgreSQL port          | 5432           | No       |

### Static Files

**Development:**

- React dev server serves frontend
- Django serves API and static files

**Production:**

- Django serves everything via WhiteNoise
- React build integrated into Django static files
- Compressed and optimized static file serving

### Security Features

- ✅ CSRF protection
- ✅ XSS protection headers
- ✅ Content type sniffing protection
- ✅ Clickjacking protection
- ✅ HTTPS redirect (when enabled)
- ✅ Secure cookies (when HTTPS enabled)
- ✅ HSTS headers (when HTTPS enabled)

## 🔍 Troubleshooting

### Common Issues

**1. Database Connection Error**

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U eldenring_user -d eldenring_prod
```

**2. Static Files Not Loading**

```bash
# Rebuild frontend and collect static files
./build_frontend.sh
```

**3. Permission Errors**

```bash
# Make scripts executable
chmod +x *.sh
```

**4. Port Already in Use**

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Logs

**Django Logs:**

```bash
tail -f mybackend/logs/django.log
```

**Gunicorn Logs:**

```bash
tail -f mybackend/logs/access.log
tail -f mybackend/logs/error.log
```

## 🌐 Domain Setup (Optional)

### 1. Update Environment

```bash
# In .env.production.local
DOMAIN_NAME=yourdomain.com
USE_HTTPS=True
```

### 2. DNS Configuration

Point your domain to your server's IP address:

```
A record: yourdomain.com → your.server.ip
A record: www.yourdomain.com → your.server.ip
```

### 3. SSL Certificate (Recommended)

```bash
# Install Certbot
sudo apt install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### 4. Nginx Reverse Proxy (Optional)

For production with SSL, consider using Nginx:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Performance Optimization

### 1. Database Optimization

```bash
# Create database indexes (if needed)
cd mybackend
python manage.py dbshell --settings=mybackend.settings_prod
```

### 2. Static File Caching

WhiteNoise automatically handles:

- Gzip compression
- Static file versioning
- Browser caching headers

### 3. Gunicorn Tuning

Adjust workers based on your server:

```bash
# Formula: (2 x CPU cores) + 1
--workers 5  # For 2 CPU cores
```

## 🔄 Updates and Maintenance

### Deploying Updates

```bash
# Pull latest changes
git pull origin main

# Redeploy
./deploy_production.sh

# Restart server
./start_server.sh
```

### Database Backups

```bash
# Create backup
pg_dump -h localhost -U eldenring_user eldenring_prod > backup_$(date +%Y%m%d).sql

# Restore backup
psql -h localhost -U eldenring_user eldenring_prod < backup_20241201.sql
```

## 🎉 Success!

Your Elden Ring Challenges website is now running in production mode!

**Access your application:**

- **Frontend:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin (admin/admin123)
- **API:** http://localhost:8000/api/

**Key Benefits:**

- ✅ Single server deployment
- ✅ Production-ready configuration
- ✅ Efficient static file serving
- ✅ Secure by default
- ✅ Easy to maintain and update

For support or questions, refer to the Django and React documentation or check the troubleshooting section above.
