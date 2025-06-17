#!/usr/bin/env bash
# Clean Django + React build script for Render

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

# Copy ALL React build files to Django static
echo "📁 Copying React build to Django..."
cp -r ../myfrontend/build/* static/

# Move index.html to templates (Django needs it there)
mv static/index.html templates/

# Run Django setup
echo "🗄️ Setting up Django..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "✅ Build complete!"
echo "📂 Static files: $(ls static/ | wc -l) items"
echo "📄 Template: $(ls templates/)"