#!/usr/bin/env bash
# Improved build script with better URL processing

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

# Copy and modify the ACTUAL React index.html - IMPROVED METHOD
echo "📄 Processing React index.html for Django..."
if [ -f "../myfrontend/build/index.html" ]; then
    # Copy the real index.html
    cp ../myfrontend/build/index.html templates/index.html
    
    # Use Python to properly process the HTML instead of sed
    python3 << 'PYTHON_SCRIPT'
import re

# Read the HTML file
with open('templates/index.html', 'r') as f:
    content = f.read()

# Add Django static load at the beginning
content = '{% load static %}\n' + content

# Replace static paths more carefully
# Handle CSS files
content = re.sub(r'href="/static/css/([^"]+)"', r'href="{% static \'css/\1\' %}"', content)

# Handle JS files  
content = re.sub(r'src="/static/js/([^"]+)"', r'src="{% static \'js/\1\' %}"', content)

# Handle other assets
content = re.sub(r'href="/favicon\.ico"', r'href="{% static \'favicon.ico\' %}"', content)
content = re.sub(r'href="/logo192\.png"', r'href="{% static \'logo192.png\' %}"', content)
content = re.sub(r'href="/logo512\.png"', r'href="{% static \'logo512.png\' %}"', content)
content = re.sub(r'href="/manifest\.json"', r'href="{% static \'manifest.json\' %}"', content)

# Write the processed content back
with open('templates/index.html', 'w') as f:
    f.write(content)

print("✅ HTML processing completed successfully")
PYTHON_SCRIPT

    echo "✅ React index.html processed for Django"
else
    echo "❌ React index.html not found!"
    exit 1
fi

# Show what files were actually copied
echo "📋 Static files structure:"
find static -type f | head -20

echo "📄 Generated Django template preview:"
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