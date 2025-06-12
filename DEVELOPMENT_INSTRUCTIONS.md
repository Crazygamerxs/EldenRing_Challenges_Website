# Elden Ring Challenges Website - Development Instructions

This guide explains how to run the Elden Ring Challenges Website in different environments and configurations.

## 🚀 Quick Production Deployment (NEW)

**For single-server production deployment with Django serving both API and React frontend:**

### Prerequisites

- PostgreSQL installed and running
- Python 3.8+ and Node.js 16+

### Setup Steps

1. **Create PostgreSQL database:**

   ```sql
   CREATE DATABASE eldenring_prod;
   CREATE USER eldenring_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE eldenring_prod TO eldenring_user;
   ```

2. **Configure environment:**

   ```bash
   # Edit .env.production with your settings
   DOMAIN_NAME=yourdomain.com  # or localhost for testing
   DB_PASSWORD=your_secure_password
   ```

3. **Deploy and start:**

   ```bash
   # Windows
   deploy_production.bat
   start_server.bat

   # Linux/macOS
   ./deploy_production.sh
   ./start_server.sh
   ```

4. **Access application:**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin (admin/admin123)
   - API: http://localhost:8000/api/

### What Each Script Does

- **`deploy_production.bat/.sh`**: Complete deployment (builds React, integrates with Django, sets up database, collects static files)
- **`start_server.bat/.sh`**: Starts production server with Gunicorn
- **`build_frontend.sh`**: Just builds and integrates React (optional)

### Key Files

- `mybackend/mybackend/settings_prod.py` - Production Django settings
- `.env.production` - Environment variables template
- `myfrontend/src/utils/api.js` - Smart API URL handling for dev/prod

**📖 For detailed production setup, see `PRODUCTION_DEPLOYMENT_GUIDE.md`**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Local Development with SQLite](#local-development-with-sqlite)
3. [Local Development with PostgreSQL](#local-development-with-postgresql)
4. [Production with Supabase PostgreSQL](#production-with-supabase-postgresql)
5. [Environment Management](#environment-management)
6. [Common Commands](#common-commands)
7. [Troubleshooting](#troubleshooting)

## Project Overview

The project consists of:

- **Backend**: Django REST API (`mybackend/`)
- **Frontend**: React application (`myfrontend/`)
- **Database Options**: SQLite (development) or PostgreSQL (production)

### Settings Files

- `mybackend/mybackend/settings.py` - Default local development (SQLite)
- `mybackend/mybackend/settings_supabase.py` - Production with Supabase PostgreSQL
- `mybackend/mybackend/settings_production.py` - General production settings
- `mybackend/mybackend/settings_local_prod.py` - Local production testing

## Local Development with SQLite

**Best for**: Quick development, testing, and getting started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Setup Steps

#### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd EldenRing_Challenges_Website

# Create Python virtual environment
python -m venv Home_venv

# Activate virtual environment
# Windows:
Home_venv\Scripts\activate
# macOS/Linux:
source Home_venv/bin/activate
```

#### 2. Install Backend Dependencies

```bash
cd mybackend
pip install -r requirements.txt
```

#### 3. Setup Database and Initial Data

```bash
# Run migrations (creates SQLite database)
python manage.py migrate

# Create admin user
python ../create_default_admin.py

# Populate with challenge data
python add_complete_challenges.py
```

#### 4. Start Backend Server

```bash
# Start Django development server
python manage.py runserver
# Backend will be available at: http://localhost:8000
```

#### 5. Setup and Start Frontend

```bash
# Open new terminal, navigate to frontend
cd myfrontend

# Install dependencies
npm install

# Start React development server
npm start
# Frontend will be available at: http://localhost:3000
```

#### 6. Access the Application

- **Website**: http://localhost:3000
- **Django Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

**Default Admin Credentials:**

- Email: `admin@eldenring.com`
- Password: `EldenRing123!`

### SQLite Database Location

The SQLite database is stored at: `mybackend/db.sqlite3`

## Local Development with PostgreSQL

**Best for**: Testing production-like environment locally

### Prerequisites

- PostgreSQL installed locally
- All prerequisites from SQLite setup

### Setup Steps

#### 1. Install PostgreSQL

**Windows:**

- Download from https://www.postgresql.org/download/windows/
- Install with default settings

**macOS:**

```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2. Create Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE eldenring_challenges;
CREATE USER eldenring_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eldenring_challenges TO eldenring_user;
\q
```

#### 3. Configure Environment

Create `mybackend/.env.local`:

```env
# Local PostgreSQL
DB_NAME=eldenring_challenges
DB_USER=eldenring_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Django settings
SECRET_KEY=your-local-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

#### 4. Install PostgreSQL Python Package

```bash
cd mybackend
pip install psycopg2-binary
```

#### 5. Run with PostgreSQL Settings

```bash
# Set environment variables and run migrations
export DJANGO_SETTINGS_MODULE=mybackend.settings_production
python manage.py migrate

# Create admin user
python ../create_default_admin.py

# Populate with data
python add_complete_challenges.py

# Start server
python manage.py runserver
```

## Production with Supabase PostgreSQL

**Best for**: Production deployment and testing production data

### Prerequisites

- Supabase account and project
- Database credentials from Supabase dashboard

### Setup Steps

#### 1. Get Supabase Credentials

From your Supabase project dashboard:

1. Go to Settings → Database
2. Copy the connection details

#### 2. Configure Production Environment

Update `mybackend/.env.prod`:

```env
# Supabase PostgreSQL
DB_NAME=postgres
DB_USER=postgres.your_project_ref
DB_PASSWORD=your_supabase_password
DB_HOST=your-project-ref.supabase.co
DB_PORT=6543

# Django settings
SECRET_KEY=your-super-long-production-secret-key-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost

# Frontend URL
FRONTEND_URL=https://yourdomain.com

# Email settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### 3. Run Production Setup

```bash
cd mybackend

# Option 1: Use the migration scripts (if you have existing data)
python scripts/setup_production_fixed.py

# Option 2: Fresh setup
export DJANGO_SETTINGS_MODULE=mybackend.settings_supabase
python manage.py migrate
python ../create_default_admin.py
python add_complete_challenges.py
```

#### 4. Verify Setup

```bash
# Run verification script
python scripts/verify_migration_fixed.py
```

## Environment Management

### Settings Files Explained

| File                     | Purpose                  | Database            | Use Case                            |
| ------------------------ | ------------------------ | ------------------- | ----------------------------------- |
| `settings.py`            | Default development      | SQLite              | Local development                   |
| `settings_supabase.py`   | Production               | Supabase PostgreSQL | Production deployment               |
| `settings_production.py` | General production       | PostgreSQL          | Production with any PostgreSQL      |
| `settings_local_prod.py` | Local production testing | PostgreSQL          | Testing production settings locally |

### Switching Between Environments

#### Method 1: Environment Variable

```bash
# Use SQLite (default)
python manage.py runserver

# Use Supabase
export DJANGO_SETTINGS_MODULE=mybackend.settings_supabase
python manage.py runserver

# Use local PostgreSQL
export DJANGO_SETTINGS_MODULE=mybackend.settings_production
python manage.py runserver
```

#### Method 2: Command Line Flag

```bash
# Use specific settings file
python manage.py runserver --settings=mybackend.settings_supabase
python manage.py migrate --settings=mybackend.settings_supabase
```

### Environment Variables

Create these files as needed:

- `mybackend/.env` - Local development
- `mybackend/.env.prod` - Production
- `myfrontend/.env.local` - Frontend local
- `myfrontend/.env.production` - Frontend production

## Common Commands

### Database Management

```bash
# Run migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Reset database (SQLite only)
rm db.sqlite3
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load data from fixtures
python manage.py loaddata fixture_file.json

# Export data to fixtures
python manage.py dumpdata app_name > fixture_file.json
```

### Development Helpers

```bash
# Check current data
python scripts/check_dev_data.py

# Export development data
python scripts/export_dev_data_fixed.py

# Start Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Frontend Commands

```bash
cd myfrontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**SQLite Issues:**

```bash
# Check if database file exists
ls -la mybackend/db.sqlite3

# If missing, run migrations
python manage.py migrate
```

**PostgreSQL Issues:**

```bash
# Test connection
python -c "
import psycopg2
conn = psycopg2.connect(
    host='localhost',
    database='eldenring_challenges',
    user='eldenring_user',
    password='your_password'
)
print('Connection successful!')
"
```

**Supabase Issues:**

- Check credentials in `.env.prod`
- Verify Supabase project is active
- Check firewall/network settings

#### 2. Migration Issues

```bash
# Reset migrations (development only)
rm mybackend/api/migrations/0*.py
python manage.py makemigrations
python manage.py migrate

# Fake migrations (if tables already exist)
python manage.py migrate --fake-initial
```

#### 3. Missing Dependencies

```bash
# Reinstall backend dependencies
cd mybackend
pip install -r requirements.txt

# Reinstall frontend dependencies
cd myfrontend
rm -rf node_modules package-lock.json
npm install
```

#### 4. Port Conflicts

```bash
# Use different ports
python manage.py runserver 8001  # Backend on 8001
npm start -- --port 3001         # Frontend on 3001
```

#### 5. Environment Variable Issues

```bash
# Check if environment variables are loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.prod')
print('DB_HOST:', os.environ.get('DB_HOST'))
print('DB_NAME:', os.environ.get('DB_NAME'))
"
```

### Data Migration Issues

If you need to migrate data between environments:

```bash
# Export from current environment
python scripts/export_dev_data_fixed.py

# Switch to target environment and import
python scripts/setup_production_fixed.py

# Verify migration
python scripts/verify_migration_fixed.py
```

### Performance Issues

```bash
# Check database queries (development)
# Add to settings.py:
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

## Quick Start Commands

### For New Development (SQLite)

```bash
# Setup
python -m venv Home_venv
Home_venv\Scripts\activate  # Windows
cd mybackend
pip install -r requirements.txt
python manage.py migrate
python ../create_default_admin.py
python add_complete_challenges.py

# Run
python manage.py runserver  # Terminal 1
cd ../myfrontend && npm start  # Terminal 2
```

### For Production Testing (Supabase)

```bash
# Setup environment
cd mybackend
# Edit .env.prod with your Supabase credentials

# Deploy
python scripts/setup_production_fixed.py
python scripts/verify_migration_fixed.py

# Run
export DJANGO_SETTINGS_MODULE=mybackend.settings_supabase
python manage.py runserver
```

## Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **React Documentation**: https://reactjs.org/docs/
- **Supabase Documentation**: https://supabase.com/docs
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

For more specific migration instructions, see `MIGRATION_GUIDE.md`.
