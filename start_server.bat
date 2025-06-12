@echo off
REM start_server.bat - Windows batch file to start production server

echo 🚀 Starting Elden Ring Challenges Production Server

REM Load environment variables
if not exist ".env.production" (
    echo ❌ .env.production file not found!
    echo Please create .env.production file with your configuration.
    pause
    exit /b 1
)

echo 📋 Loading environment variables...
for /f "usebackq tokens=1,2 delims==" %%a in (".env.production") do (
    if not "%%a"=="" if not "%%a:~0,1%%"=="#" set %%a=%%b
)

REM Check database connection
echo 🗃️ Checking database connection...
cd mybackend
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings_prod'); import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('✅ Database connection successful')" 2>nul
if errorlevel 1 (
    echo ❌ Cannot connect to PostgreSQL database!
    echo Please ensure PostgreSQL is running and database credentials are correct.
    echo Check your .env.production file for database configuration.
    pause
    exit /b 1
)

REM Create logs directory
if not exist "logs" mkdir "logs"

REM Start the production server
echo 🌐 Starting Gunicorn server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Start Gunicorn with production settings
set DJANGO_SETTINGS_MODULE=mybackend.settings_prod
gunicorn mybackend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --worker-class sync --worker-connections 1000 --max-requests 1000 --max-requests-jitter 100 --timeout 30 --keep-alive 2 --log-level info --access-logfile logs/access.log --error-logfile logs/error.log --capture-output --enable-stdio-inheritance

pause
