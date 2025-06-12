#!/usr/bin/env bash
# Startup script for Render deployment

echo "🚀 Starting Elden Ring Challenges Website..."
echo "📍 Current directory: $(pwd)"
echo "📂 Directory contents:"
ls -la

echo "🔍 Checking mybackend directory:"
ls -la mybackend/

echo "🔍 Checking mybackend/mybackend directory:"
ls -la mybackend/mybackend/

echo "🐍 Setting up Python path..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)/mybackend"
echo "🐍 Python path: $PYTHONPATH"

echo "🔧 Starting Gunicorn with correct path..."
cd mybackend
exec gunicorn mybackend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers $WEB_CONCURRENCY \
    --max-requests $MAX_REQUESTS \
    --max-requests-jitter $MAX_REQUESTS_JITTER \
    --timeout $TIMEOUT \
    --keep-alive $KEEP_ALIVE \
    --preload
