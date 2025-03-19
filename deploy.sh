#!/bin/bash

# Elden Ring Challenges Website Deployment Script
# This script automates the deployment process for the Elden Ring Challenges website

# Exit on error
set -e

# Display help message
show_help() {
    echo "Elden Ring Challenges Website Deployment Script"
    echo ""
    echo "Usage: ./deploy.sh [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help                 Show this help message"
    echo "  -e, --env <environment>    Specify environment (dev, prod) [default: dev]"
    echo "  -s, --skip-build           Skip the build step"
    echo "  -c, --clean                Clean build artifacts before building"
    echo ""
    echo "Example:"
    echo "  ./deploy.sh --env prod     Deploy to production environment"
    echo ""
}

# Default values
ENVIRONMENT="dev"
SKIP_BUILD=false
CLEAN=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -s|--skip-build)
            SKIP_BUILD=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate environment
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    echo "Error: Invalid environment. Must be 'dev' or 'prod'."
    exit 1
fi

echo "=== Elden Ring Challenges Website Deployment ==="
echo "Environment: $ENVIRONMENT"
echo "Skip Build: $SKIP_BUILD"
echo "Clean: $CLEAN"
echo "================================================"

# Set environment-specific variables
if [[ "$ENVIRONMENT" == "prod" ]]; then
    DJANGO_SETTINGS="mybackend.settings_prod"
    API_URL="https://eldenring.biz/api"
    STATIC_ROOT="mybackend/static"
else
    DJANGO_SETTINGS="mybackend.settings"
    API_URL="http://localhost:8888/api"
    STATIC_ROOT="mybackend/static"
fi

# Create .env file for React
create_env_file() {
    echo "Creating .env file for React..."
    # Make sure the directory exists
    mkdir -p myfrontend
    
    # Create the .env file
    cat > myfrontend/.env <<EOL
REACT_APP_API_URL=$API_URL
REACT_APP_ENV=$ENVIRONMENT
EOL
    echo "Created .env file with the following content:"
    cat myfrontend/.env
}

# Clean build artifacts
if [[ "$CLEAN" == true ]]; then
    echo "Cleaning build artifacts..."
    rm -rf myfrontend/build
    rm -rf mybackend/build
    rm -rf mybackend/static/css
    rm -rf mybackend/static/js
    rm -rf mybackend/static/media
    echo "Clean completed."
fi

# Build React frontend
if [[ "$SKIP_BUILD" == false ]]; then
    echo "Building React frontend..."
    cd myfrontend
    
    # Create environment file
    create_env_file
    
    # Install dependencies
    echo "Installing frontend dependencies..."
    npm install
    
    # Build the React app
    echo "Building frontend..."
    npm run build
    
    # Copy build files to Django static directory
    echo "Copying build files to Django static directory..."
    cd ..
    mkdir -p mybackend/build
    cp -r myfrontend/build/* mybackend/build/
    
    echo "Frontend build completed."
fi

# Set up Django backend
echo "Setting up Django backend..."
cd mybackend

# Activate virtual environment
if [[ -f "../Home_venv/Scripts/activate" ]]; then
    echo "Activating virtual environment..."
    source "../Home_venv/Scripts/activate"
fi

# Install Python dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Set Django settings module
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if in production and doesn't exist
if [[ "$ENVIRONMENT" == "prod" ]]; then
    echo "Checking if superuser exists..."
    python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '$DJANGO_SETTINGS_MODULE')
import django
django.setup()
from api.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    User.objects.create_superuser('admin', 'admin@eldenring.biz', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"
fi

cd ..

# Production-specific steps
if [[ "$ENVIRONMENT" == "prod" ]]; then
    echo "Performing production-specific steps..."
    
    # Check if Gunicorn is installed
    if ! command -v gunicorn &> /dev/null; then
        echo "Installing Gunicorn..."
        pip install gunicorn
    fi
    
    # Create systemd service file for Gunicorn
    echo "Creating systemd service file for Gunicorn..."
    cat > eldenring.service <<EOL
[Unit]
Description=Elden Ring Challenges Website
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)/mybackend
ExecStart=$(which gunicorn) --workers 3 --bind 0.0.0.0:8000 mybackend.wsgi:application
Restart=on-failure
Environment="DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"

[Install]
WantedBy=multi-user.target
EOL
    
    echo "Created systemd service file with the following content:"
    cat eldenring.service
    
    echo "To install the service, run:"
    echo "sudo cp eldenring.service /etc/systemd/system/"
    echo "sudo systemctl daemon-reload"
    echo "sudo systemctl enable eldenring"
    echo "sudo systemctl start eldenring"
    
    # Create Nginx configuration file
    echo "Creating Nginx configuration file..."
    cat > eldenring.nginx.conf <<EOL
server {
    listen 80;
    server_name eldenring.biz www.eldenring.biz;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $(pwd)/mybackend;
    }
    
    location /media/ {
        root $(pwd)/mybackend;
    }
    
    location / {
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://localhost:8000;
    }
}

server {
    listen 443 ssl;
    server_name eldenring.biz www.eldenring.biz;

    ssl_certificate /etc/letsencrypt/live/eldenring.biz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/eldenring.biz/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    ssl_stapling on;
    ssl_stapling_verify on;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $(pwd)/mybackend;
    }
    
    location /media/ {
        root $(pwd)/mybackend;
    }
    
    location / {
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://localhost:8000;
    }
}
EOL
    
    echo "Created Nginx configuration file with the following content:"
    cat eldenring.nginx.conf
    
    echo "To install the Nginx configuration, run:"
    echo "sudo cp eldenring.nginx.conf /etc/nginx/sites-available/eldenring"
    echo "sudo ln -s /etc/nginx/sites-available/eldenring /etc/nginx/sites-enabled/"
    echo "sudo nginx -t"
    echo "sudo systemctl restart nginx"
    
    echo "To obtain SSL certificates with Let's Encrypt, run:"
    echo "sudo apt-get install certbot python3-certbot-nginx"
    echo "sudo certbot --nginx -d eldenring.biz -d www.eldenring.biz"
fi

echo "=== Deployment completed successfully ==="
echo "To start the development server:"
echo "cd mybackend && python manage.py runserver 0.0.0.0:8888"

if [[ "$ENVIRONMENT" == "prod" ]]; then
    echo ""
    echo "For production deployment, follow the instructions above to set up:"
    echo "1. Gunicorn systemd service"
    echo "2. Nginx configuration"
    echo "3. SSL certificates with Let's Encrypt"
fi

echo ""
echo "Thank you for using the Elden Ring Challenges Website Deployment Script!"
