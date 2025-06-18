#!/usr/bin/env bash
# Fixed build script that properly integrates React with Django

set -o errexit

echo "🚀 Building React + Django for production..."

# Build React frontend
echo "⚛️ Building React frontend..."
cd myfrontend
npm install
npm run build

# Move to Django directory
cd ../mybackend

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Clean and setup directories
echo "🧹 Setting up Django directories..."
rm -rf static staticfiles templates
mkdir -p static templates

# Copy the ACTUAL React build files
echo "📁 Copying React build files..."

# Copy the entire React build static directory
if [ -d "../myfrontend/build/static" ]; then
    cp -r ../myfrontend/build/static/* static/
    echo "✅ All React static files copied"
else
    echo "❌ React build/static directory not found!"
    exit 1
fi

# Copy other React assets to static (favicon, manifest, etc.)
echo "📄 Copying React root assets..."
find ../myfrontend/build -maxdepth 1 -type f \( -name "*.ico" -o -name "*.png" -o -name "*.json" -o -name "*.txt" \) -exec cp {} static/ \; 2>/dev/null || true

# Copy and modify the ACTUAL React index.html
echo "📄 Processing React index.html for Django..."
if [ -f "../myfrontend/build/index.html" ]; then
    # Copy the real index.html and modify it for Django static files
    cp ../myfrontend/build/index.html templates/index.html
    
    # Add Django static load at the top
    sed -i '1i{% load static %}' templates/index.html
    
    # Replace static file paths with Django static tags - FIXED SYNTAX
    sed -i 's|="/static/css/|="{% static '"'"'css/|g' templates/index.html
    sed -i 's|="/static/js/|="{% static '"'"'js/|g' templates/index.html
    sed -i 's|\.css"|.css'"'"' %}"|g' templates/index.html
    sed -i 's|\.js"|.js'"'"' %}"|g' templates/index.html
    sed -i 's|="/favicon\.ico"|="{% static '"'"'favicon.ico'"'"' %}"|g' templates/index.html
    sed -i 's|="/logo192\.png"|="{% static '"'"'logo192.png'"'"' %}"|g' templates/index.html
    sed -i 's|="/logo512\.png"|="{% static '"'"'logo512.png'"'"' %}"|g' templates/index.html
    sed -i 's|="/manifest\.json"|="{% static '"'"'manifest.json'"'"' %}"|g' templates/index.html
    
    echo "✅ React index.html processed for Django"
else
    echo "❌ React index.html not found!"
    exit 1
fi

# Show what files were actually copied
echo "📋 Static files structure:"
find static -type f | head -20

echo "📄 Generated Django template:"
head -20 templates/index.html

# Set proper permissions for static files
echo "🔧 Setting file permissions..."
find static -type f -name "*.js" -exec chmod 644 {} \;
find static -type f -name "*.css" -exec chmod 644 {} \;

# DATABASE MIGRATIONS
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=mybackend.settings_render

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --settings=mybackend.settings_render

# Create default superuser
echo "👤 Creating default superuser..."
python manage.py shell --settings=mybackend.settings_render << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user(
        email='admin@eldenring.com',
        username='admin',
        password='admin123'
    )
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print('✅ Default superuser created: admin/admin123')
else:
    print('ℹ️ Superuser already exists')
EOF

echo "✅ Build complete!"
echo "📄 React app properly integrated with Django"
echo "👤 Default admin credentials: admin/admin123"
echo "🗄️ Database migrations completed"