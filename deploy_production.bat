@echo off
REM deploy_production.bat - Windows batch file for production deployment

echo 🚀 Starting Elden Ring Challenges Production Deployment

REM Check if environment file exists
if not exist ".env.production" (
    echo ❌ .env.production file not found!
    echo Please create .env.production file with your configuration.
    pause
    exit /b 1
)

REM Step 1: Install Python dependencies
echo 📦 Installing Python dependencies...
cd mybackend
pip install -r requirements.txt

REM Step 2: Build React frontend
echo 🎨 Building React frontend...
cd ..\myfrontend

REM Install npm dependencies
echo 📦 Installing npm dependencies...
call npm ci

REM Build React app
echo 🔨 Building React app...
call npm run build

cd ..

REM Step 3: Integrate React with Django
echo 🔧 Integrating React with Django...

REM Remove old build
if exist "mybackend\build" rmdir /s /q "mybackend\build"
if exist "mybackend\templates\index.html" del "mybackend\templates\index.html"

REM Copy React build to Django
xcopy "myfrontend\build" "mybackend\build" /e /i /y

REM Create templates directory and copy index.html
if not exist "mybackend\templates" mkdir "mybackend\templates"
copy "mybackend\build\index.html" "mybackend\templates\"

REM Step 4: Database setup
echo 🗃️ Setting up database...
cd mybackend

REM Load environment variables (Windows doesn't have export, so we'll use set)
for /f "usebackq tokens=1,2 delims==" %%a in ("..\\.env.production") do (
    if not "%%a"=="" if not "%%a:~0,1%%"=="#" set %%a=%%b
)

REM Run migrations
echo 🔄 Running database migrations...
python manage.py migrate --settings=mybackend.settings_prod

REM Create superuser
echo 👤 Setting up admin user...
python manage.py shell --settings=mybackend.settings_prod < nul
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists') | python manage.py shell --settings=mybackend.settings_prod

REM Collect static files
echo 📋 Collecting static files...
python manage.py collectstatic --noinput --settings=mybackend.settings_prod

REM Run security checks
echo 🔒 Running security checks...
python manage.py check --deploy --settings=mybackend.settings_prod

echo ✅ Deployment completed successfully!
echo 🌐 Your app is ready to serve
echo 📝 Next steps:
echo    1. Start the production server: start_server.bat
echo    2. Visit: http://localhost:8000
echo    3. Admin panel: http://localhost:8000/admin (admin/admin123)

cd ..
pause
