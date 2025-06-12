#!/bin/bash
# build_frontend.sh - Script to build React and integrate with Django

set -e  # Exit on any error

echo "🚀 Starting frontend build process..."

# Step 1: Build React app
echo "📦 Building React application..."
cd myfrontend
npm run build
cd ..

# Step 2: Copy React build to Django
echo "📂 Copying React build to Django..."

# Remove existing build directory in Django
if [ -d "mybackend/build" ]; then
    rm -rf mybackend/build
fi

# Copy React build to Django backend
cp -r myfrontend/build mybackend/

# Step 3: Update Django to serve React
echo "🔧 Configuring Django to serve React..."

# Create/update Django template directory for React
mkdir -p mybackend/templates

# Copy index.html to Django templates
cp mybackend/build/index.html mybackend/templates/

# Step 4: Collect static files
echo "📋 Collecting static files..."
cd mybackend

# Load environment variables
if [ -f "../.env.production" ]; then
    export $(cat ../.env.production | grep -v '^#' | xargs)
fi

python manage.py collectstatic --noinput --settings=mybackend.settings_prod
cd ..

echo "✅ Frontend build complete!"
echo "📁 React build is now integrated with Django"
echo "🌐 Django will serve React app at root URL"
