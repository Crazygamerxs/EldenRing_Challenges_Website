#!/bin/bash
# deploy_production.sh - Complete production deployment script for Elden Ring Challenges Website

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Elden Ring Challenges Production Deployment${NC}"

# Check if environment is specified
ENV=${1:-production}
echo -e "${YELLOW}📋 Deploying to: $ENV${NC}"

# Load environment variables
if [ -f ".env.production" ]; then
    echo -e "${YELLOW}📋 Loading environment variables...${NC}"
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo -e "${RED}❌ .env.production file not found!${NC}"
    echo "Please create .env.production file with your configuration."
    exit 1
fi

# Step 1: Install/Update Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
cd mybackend
pip install -r requirements.txt

# Step 2: Build React frontend
echo -e "${YELLOW}🎨 Building React frontend...${NC}"
cd ../myfrontend

# Install npm dependencies
echo -e "${YELLOW}📦 Installing npm dependencies...${NC}"
npm ci

# Build React app with production optimizations
echo -e "${YELLOW}🔨 Building React app...${NC}"
npm run build

cd ..

# Step 3: Integrate React with Django
echo -e "${YELLOW}🔧 Integrating React with Django...${NC}"

# Remove old build
if [ -d "mybackend/build" ]; then
    rm -rf mybackend/build
fi

if [ -f "mybackend/templates/index.html" ]; then
    rm -f mybackend/templates/index.html
fi

# Copy React build to Django
cp -r myfrontend/build mybackend/

# Create templates directory and copy index.html
mkdir -p mybackend/templates
cp mybackend/build/index.html mybackend/templates/

# Step 4: Database setup
echo -e "${YELLOW}🗃️  Setting up database...${NC}"
cd mybackend

# Wait for database to be ready (if using PostgreSQL)
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
max_attempts=30
attempt=1
while ! python manage.py dbshell --settings=mybackend.settings_prod <<< '\q' 2>/dev/null; do
    if [ $attempt -eq $max_attempts ]; then
        echo -e "${RED}❌ Database connection failed after $max_attempts attempts${NC}"
        echo "Please check your PostgreSQL installation and .env.production configuration"
        exit 1
    fi
    echo "Database not ready, waiting... (attempt $attempt/$max_attempts)"
    sleep 2
    ((attempt++))
done

echo -e "${GREEN}✅ Database connection successful${NC}"

# Run migrations
echo -e "${YELLOW}🔄 Running database migrations...${NC}"
python manage.py migrate --settings=mybackend.settings_prod

# Create superuser if it doesn't exist
echo -e "${YELLOW}👤 Setting up admin user...${NC}"
python manage.py shell --settings=mybackend.settings_prod << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser created: admin/admin123")
else:
    print("✅ Superuser already exists")
EOF

# Step 5: Collect static files
echo -e "${YELLOW}📋 Collecting static files...${NC}"
python manage.py collectstatic --noinput --settings=mybackend.settings_prod

# Step 6: Run security checks
echo -e "${YELLOW}🔒 Running security checks...${NC}"
python manage.py check --deploy --settings=mybackend.settings_prod

# Step 7: Test the setup
echo -e "${YELLOW}🧪 Testing setup...${NC}"
python manage.py check --settings=mybackend.settings_prod

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Your app is ready to serve${NC}"
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "   1. Start the production server: ./start_server.sh"
echo "   2. Visit: http://localhost:8000"
echo "   3. Admin panel: http://localhost:8000/admin (admin/admin123)"
echo ""
echo -e "${YELLOW}📋 Production URLs:${NC}"
echo "   Frontend: http://localhost:8000"
echo "   API: http://localhost:8000/api/"
echo "   Admin: http://localhost:8000/admin/"

cd ..
