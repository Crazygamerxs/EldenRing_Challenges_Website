#!/usr/bin/env bash
# Better build script with proper MIME type handling

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
mkdir -p static staticfiles templates

# Copy React static files with proper structure
echo "📁 Copying React static files..."
cp -r ../myfrontend/build/static/* static/

# Copy other React assets
find ../myfrontend/build -maxdepth 1 -type f \( -name "*.ico" -o -name "*.png" -o -name "*.json" -o -name "*.txt" \) -exec cp {} static/ \; 2>/dev/null || true

# Create a simpler Django template that definitely loads React
echo "📄 Creating optimized Django template..."
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
    <link href="{% static 'css/main.b4e3a3ca.css' %}" rel="stylesheet">
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    
    <!-- Load React scripts -->
    <script>
        console.log('🚀 Loading React app...');
        console.log('Environment: production');
    </script>
    <script src="{% static 'js/main.2447be8d.js' %}"></script>
    <script src="{% static 'js/488.2c2c4401.chunk.js' %}"></script>
    <script>
        console.log('✅ React scripts loaded');
        // Check if React mounted
        setTimeout(() => {
            const root = document.getElementById('root');
            if (root && root.innerHTML.trim() === '') {
                console.error('❌ React failed to mount!');
            } else {
                console.log('✅ React mounted successfully!');
            }
        }, 1000);
    </script>
</body>
</html>
EOF

# Run Django setup
echo "🗄️ Setting up Django..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "✅ Build complete!"
echo "📄 Template created with debug logging"