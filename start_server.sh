#!/bin/bash
# start_server.sh - Start production server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Elden Ring Challenges Production Server${NC}"

# Load environment variables
if [ -f ".env.production" ]; then
    echo -e "${YELLOW}📋 Loading environment variables...${NC}"
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo -e "${RED}❌ .env.production file not found!${NC}"
    echo "Please create .env.production file with your configuration."
    exit 1
fi

# Check if PostgreSQL is running
echo -e "${YELLOW}🗃️  Checking database connection...${NC}"
cd mybackend
if ! python manage.py dbshell --settings=mybackend.settings_prod <<< '\q' 2>/dev/null; then
    echo -e "${RED}❌ Cannot connect to PostgreSQL database!${NC}"
    echo "Please ensure PostgreSQL is running and database credentials are correct."
    echo "Check your .env.production file for database configuration."
    exit 1
fi

echo -e "${GREEN}✅ Database connection successful${NC}"

# Start the production server
echo -e "${YELLOW}🌐 Starting Gunicorn server...${NC}"
echo -e "${GREEN}Server will be available at: http://localhost:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start Gunicorn with production settings
gunicorn mybackend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --capture-output \
    --enable-stdio-inheritance \
    --env DJANGO_SETTINGS_MODULE=mybackend.settings_prod
