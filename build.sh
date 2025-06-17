#!/usr/bin/env bash
# Simple working build script

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

# Copy ALL React build files to static
echo "📁 Copying React build files..."
cp -r ../myfrontend/build/static/* static/

# Copy and fix the React index.html
echo "📄 Fixing React index.html for Django..."
# Add Django static loading at the top and fix all /static/ paths
echo "{% load static %}" > templates/index.html
sed 's|"/static/|"{% static "|g; s|\.css"|.css" %}|g; s|\.js"|.js" %}|g' ../myfrontend/build/index.html >> templates/index.html

# Copy other React assets to static
find ../myfrontend/build -maxdepth 1 -type f \( -name "*.ico" -o -name "*.png" -o -name "*.json" -o -name "*.txt" \) -exec cp {} static/ \; 2>/dev/null || true

# Run Django setup
echo "🗄️ Setting up Django..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "✅ Build complete!"
echo "📄 Template created:"
head -10 templates/index.html