#!/usr/bin/env bash
# Fixed build script with proper MIME type handling and corrected superuser creation

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
mkdir -p static/css static/js static/media templates

# Copy React static files with proper structure and permissions
echo "📁 Copying React static files with correct structure..."

# Copy CSS files
if [ -d "../myfrontend/build/static/css" ]; then
    cp -r ../myfrontend/build/static/css/* static/css/
    echo "✅ CSS files copied"
fi

# Copy JS files
if [ -d "../myfrontend/build/static/js" ]; then
    cp -r ../myfrontend/build/static/js/* static/js/
    echo "✅ JS files copied"
fi

# Copy media files if they exist
if [ -d "../myfrontend/build/static/media" ]; then
    cp -r ../myfrontend/build/static/media/* static/media/
    echo "✅ Media files copied"
fi

# Copy other React assets (favicon, manifest, etc.)
echo "📄 Copying React assets..."
find ../myfrontend/build -maxdepth 1 -type f \( -name "*.ico" -o -name "*.png" -o -name "*.json" -o -name "*.txt" \) -exec cp {} static/ \; 2>/dev/null || true

# List copied files for debugging
echo "📋 Static files structure:"
find static -type f | head -20

# Create Django template with dynamic asset references
echo "📄 Creating Django template..."
cat > templates/index.html << 'EOF'
{% load static %}
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <link rel="icon" href="{% static 'favicon.ico' %}"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <meta name="theme-color" content="#000000"/>
    <meta name="description" content="Elden Ring Challenges"/>
    <title>Elden Ring Challenges</title>
    
    <!-- Dynamically find CSS files -->
    {% for file in css_files %}
        <link href="{% static file %}" rel="stylesheet">
    {% endfor %}
    
    <!-- Fallback CSS - update the filename based on your build -->
    <link href="{% static 'css/main.b4e3a3ca.css' %}" rel="stylesheet">
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    
    <script>
        console.log('🚀 Loading React app...');
        console.log('Environment: production');
        console.log('Static URL: {% static "" %}');
    </script>
    
    <!-- Load main JS file -->
    <script type="application/javascript" src="{% static 'js/main.10191822.js' %}"></script>
    
    <!-- Load chunk files -->
    <script type="application/javascript" src="{% static 'js/488.2c2c4401.chunk.js' %}"></script>
    
    <script>
        console.log('✅ React scripts loaded');
        // Check if React mounted
        setTimeout(() => {
            const root = document.getElementById('root');
            if (root && root.innerHTML.trim() === '') {
                console.error('❌ React failed to mount!');
                console.log('Root element:', root);
                console.log('Available static files check...');
            } else {
                console.log('✅ React mounted successfully!');
            }
        }, 2000);
    </script>
</body>
</html>
EOF

# Set proper permissions for static files
echo "🔧 Setting file permissions..."
find static -type f -name "*.js" -exec chmod 644 {} \;
find static -type f -name "*.css" -exec chmod 644 {} \;

# Run Django setup
echo "🗄️ Setting up Django..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Create default superuser - FIXED VERSION
echo "👤 Creating default superuser..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    # Use create_user since create_superuser is not available in your UserManager
    user = User.objects.create_user(
        email='admin@eldenring.com',
        username='admin',
        password='admin123'
    )
    # Manually set superuser fields
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print('✅ Default superuser created: admin/admin123')
else:
    print('ℹ️ Superuser already exists')
EOF

echo "✅ Build complete!"
echo "📄 Template created with proper MIME types"
echo "👤 Default admin credentials: admin/admin123"
echo "🔍 Check static files in browser network tab"