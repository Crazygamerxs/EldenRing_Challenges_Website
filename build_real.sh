#!/usr/bin/env bash
# Render.com build script for Elden Ring Challenges Website
# This script builds both React frontend and Django backend

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd mybackend
pip install -r requirements.txt

# Install Node.js dependencies and build React
echo "⚛️ Building React frontend..."
cd ../myfrontend
npm install --only=production
npm run build

# Copy React build to Django static directory
echo "📁 Copying React build to Django static directory..."
rm -rf ../mybackend/static/*
cp -r build/* ../mybackend/static/

# Return to Django directory
cd ../mybackend

# Collect static files
echo "🗂️ Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist (optional)
echo "👤 Setting up admin user..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@eldenringchallenge.xyz', 'EldenRing2024!')
    print("✅ Admin user created: admin / EldenRing2024!")
else:
    print("ℹ️ Admin user already exists")
EOF

echo "✅ Build completed successfully!"
echo "🌐 Ready to deploy to eldenringchallenge.xyz"
