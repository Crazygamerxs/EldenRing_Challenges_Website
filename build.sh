#!/usr/bin/env bash
# Fixed production build script for Render.com

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd mybackend
pip install -r requirements.txt

# Build React frontend
echo "⚛️ Building React frontend..."
cd ../myfrontend
npm install
npm run build

# Debug: Check what was built
echo "📋 Checking React build contents..."
ls -la build/
echo "📋 Static files in build:"
ls -la build/static/

# Copy built frontend to Django static files properly
echo "📁 Setting up Django static files structure..."
cd ../mybackend

# Create necessary directories
mkdir -p static
mkdir -p staticfiles
mkdir -p templates

# Copy the React build files
echo "📁 Copying React build files..."
cp -r ../myfrontend/build/static/* static/

# Create custom Django template instead of using React's index.html
echo "📄 Creating custom Django template..."
cat > templates/index.html << 'EOF'
{% load static %}
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <link rel="icon" href="{% static 'favicon.ico' %}"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <meta name="theme-color" content="#000000"/>
    <meta name="description" content="Elden Ring Challenges - Test your skills"/>
    <link rel="apple-touch-icon" href="{% static 'logo192.png' %}"/>
    <link rel="manifest" href="{% static 'manifest.json' %}"/>
    <title>Elden Ring Challenges</title>
    
    <!-- Load CSS files dynamically -->
    {% for css_file in css_files %}
    <link href="{% static css_file %}" rel="stylesheet">
    {% endfor %}
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    
    <!-- Load JS files dynamically -->
    {% for js_file in js_files %}
    <script defer="defer" src="{% static js_file %}"></script>
    {% endfor %}
</body>
</html>
EOF

# Debug: Check what was copied
echo "📋 Django static files:"
ls -la static/
echo "📋 Django templates:"
ls -la templates/

# Run Django migrations
echo "🗄️ Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Debug: Check collected static files
echo "📋 Collected static files:"
ls -la staticfiles/

echo "✅ Build completed successfully!"