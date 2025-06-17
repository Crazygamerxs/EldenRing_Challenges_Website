#!/usr/bin/env bash
# Start script for Render.com deployment

set -o errexit

echo "🚀 Starting Elden Ring Challenges Website..."
echo "📍 Current directory: $(pwd)"
echo "📁 Directory contents:"
ls -la

# Change to the mybackend directory where wsgi.py is located
cd mybackend

echo "📍 Changed to directory: $(pwd)"
echo "📁 Backend directory contents:"
ls -la

# Set up environment
export DJANGO_SETTINGS_MODULE=mybackend.settings_render

# Check if wsgi.py exists
if [ -f "mybackend/wsgi.py" ]; then
    echo "✅ Found wsgi.py at: $(pwd)/mybackend/wsgi.py"
else
    echo "❌ wsgi.py not found!"
    exit 1
fi

# Start Gunicorn
echo "🔥 Starting Gunicorn..."
exec gunicorn mybackend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 30 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --log-level info \
    --access-logfile - \
    --error-logfile -