#!/usr/bin/env bash
# Production build script for Render.com - Elden Ring Challenges Website

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd mybackend
pip install -r requirements.txt

# Build React frontend
echo "⚛️ Building React frontend..."
cd ../myfrontend
npm install --only=production
npm run build

# Copy built frontend to Django static files
echo "📁 Copying frontend build to Django static files..."
cd ..
rm -rf mybackend/static/*
cp -r myfrontend/build/* mybackend/static/

# Return to Django directory for final setup
cd mybackend

# Run Django migrations
echo "🗄️ Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Set up Python path for Gunicorn
echo "🔧 Setting up Python path for deployment..."
cd ..
export PYTHONPATH="${PYTHONPATH}:$(pwd)/mybackend"

echo "✅ Build completed successfully!"
echo "📍 Current directory: $(pwd)"
echo "🐍 Python path: $PYTHONPATH"
