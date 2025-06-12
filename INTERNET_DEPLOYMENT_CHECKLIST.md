# Internet Deployment Checklist

## Elden Ring Challenges Website

This checklist covers everything you need to do before deploying your website to the internet.

## 🌐 Pre-Deployment Checklist

### 1. 🏗️ Server Setup

**Get a VPS/Server:**

- [ ] Purchase VPS (DigitalOcean, Linode, AWS EC2, etc.)
- [ ] Choose Ubuntu 20.04+ or similar Linux distribution
- [ ] Minimum specs: 2GB RAM, 1 CPU, 25GB storage
- [ ] Note your server's IP address

**Server Access:**

- [ ] Set up SSH key authentication
- [ ] Test SSH connection: `ssh root@your-server-ip`
- [ ] Create non-root user with sudo privileges

### 2. 🌍 Domain Setup

**Domain Registration:**

- [ ] Purchase domain name (Namecheap, GoDaddy, etc.)
- [ ] Configure DNS A records:
  ```
  A record: yourdomain.com → your-server-ip
  A record: www.yourdomain.com → your-server-ip
  ```
- [ ] Wait for DNS propagation (up to 24 hours)
- [ ] Test with: `ping yourdomain.com`

### 3. 🗄️ Database Setup

**PostgreSQL Options:**

**Option A: Server PostgreSQL (Recommended)**

- [ ] Install PostgreSQL on your server
- [ ] Create production database and user
- [ ] Configure PostgreSQL for remote connections (if needed)
- [ ] Set strong password for database user

**Option B: Managed Database (Easier)**

- [ ] Set up managed PostgreSQL (DigitalOcean, AWS RDS, etc.)
- [ ] Note connection details (host, port, username, password)
- [ ] Configure firewall to allow your server's IP

### 4. 🔐 Security Configuration

**SSL Certificate:**

- [ ] Install Certbot: `sudo apt install certbot python3-certbot-nginx`
- [ ] Get SSL certificate: `sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com`
- [ ] Test auto-renewal: `sudo certbot renew --dry-run`

**Firewall Setup:**

- [ ] Configure UFW firewall:
  ```bash
  sudo ufw allow ssh
  sudo ufw allow 80
  sudo ufw allow 443
  sudo ufw enable
  ```

**Server Security:**

- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Disable root login via SSH
- [ ] Change default SSH port (optional)
- [ ] Set up fail2ban for SSH protection

### 5. ⚙️ Environment Configuration

**Update .env.production:**

```env
# Domain Configuration
DOMAIN_NAME=yourdomain.com
USE_HTTPS=True

# Generate new secret key
SECRET_KEY=your-super-long-production-secret-key-minimum-50-characters

# Database Configuration
DB_NAME=eldenring_prod
DB_USER=eldenring_user
DB_PASSWORD=your-very-secure-database-password
DB_HOST=localhost  # or your managed database host
DB_PORT=5432

# Email Configuration (for password resets)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Debug Mode (MUST be False in production)
DEBUG=False
```

**Generate New Secret Key:**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 6. 📧 Email Setup (Optional but Recommended)

**Gmail App Password:**

- [ ] Enable 2-factor authentication on Gmail
- [ ] Generate app password: Google Account → Security → App passwords
- [ ] Use app password in EMAIL_HOST_PASSWORD

**Alternative Email Services:**

- [ ] SendGrid, Mailgun, or AWS SES for production email
- [ ] Update EMAIL_HOST and credentials accordingly

### 7. 🚀 Server Software Installation

**Install Required Software:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL (if using server database)
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

### 8. 📁 Code Deployment

**Upload Your Code:**

```bash
# Option 1: Git clone (recommended)
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Option 2: SCP upload
scp -r /local/path/to/project user@server-ip:/home/user/
```

**Set Up Project:**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd mybackend
pip install -r requirements.txt
cd ../myfrontend
npm install
cd ..
```

### 9. 🌐 Nginx Configuration

**Create Nginx Config:**

```bash
sudo nano /etc/nginx/sites-available/eldenring
```

**Basic Nginx Config:**

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/mybackend/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/mybackend/media/;
    }
}
```

**Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/eldenring /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. 🔄 Process Management

**Create Systemd Service:**

```bash
sudo nano /etc/systemd/system/eldenring.service
```

**Service Configuration:**

```ini
[Unit]
Description=Elden Ring Challenges Website
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/your/project/mybackend
ExecStart=/path/to/your/project/venv/bin/gunicorn mybackend.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=on-failure
Environment="DJANGO_SETTINGS_MODULE=mybackend.settings_prod"

[Install]
WantedBy=multi-user.target
```

**Enable and Start Service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable eldenring
sudo systemctl start eldenring
sudo systemctl status eldenring
```

### 11. 🧪 Testing & Verification

**Pre-Launch Tests:**

- [ ] Test database connection
- [ ] Verify static files are served correctly
- [ ] Test admin panel access
- [ ] Check all main pages load
- [ ] Test user registration and login
- [ ] Verify email functionality (password reset)
- [ ] Test challenge submission process
- [ ] Check responsive design on mobile

**Performance Tests:**

- [ ] Run Django security check: `python manage.py check --deploy`
- [ ] Test SSL certificate: https://www.ssllabs.com/ssltest/
- [ ] Check page load speeds
- [ ] Test under load (optional)

### 12. 📊 Monitoring & Backups

**Set Up Monitoring:**

- [ ] Configure log rotation
- [ ] Set up basic monitoring (htop, disk space alerts)
- [ ] Monitor application logs: `sudo journalctl -u eldenring -f`

**Database Backups:**

```bash
# Create backup script
#!/bin/bash
pg_dump -h localhost -U eldenring_user eldenring_prod > /backups/eldenring_$(date +%Y%m%d_%H%M%S).sql

# Set up cron job for daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup-script.sh
```

### 13. 🚀 Go Live!

**Final Steps:**

- [ ] Update DOMAIN_NAME in .env.production
- [ ] Set USE_HTTPS=True
- [ ] Run deployment script: `./deploy_production.sh`
- [ ] Start production server
- [ ] Test everything works with your domain
- [ ] Announce your launch! 🎉

## 🔧 Quick Commands Reference

**Deploy to Server:**

```bash
# Upload .env.production with your settings
scp .env.production user@server:/path/to/project/

# Run deployment
./deploy_production.sh

# Start server
sudo systemctl start eldenring
```

**Update Deployment:**

```bash
git pull origin main
./deploy_production.sh
sudo systemctl restart eldenring
```

**Check Logs:**

```bash
# Application logs
sudo journalctl -u eldenring -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## 🆘 Common Issues

**Domain not working:**

- Check DNS propagation: `dig yourdomain.com`
- Verify A records point to correct IP
- Check Nginx configuration

**SSL certificate issues:**

- Ensure domain points to server before running certbot
- Check firewall allows ports 80 and 443
- Verify Nginx configuration syntax

**Database connection errors:**

- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify database credentials in .env.production
- Test connection manually

**Static files not loading:**

- Run `python manage.py collectstatic`
- Check Nginx static file configuration
- Verify file permissions

## 📚 Additional Resources

- **DigitalOcean Tutorials**: https://www.digitalocean.com/community/tutorials
- **Let's Encrypt Documentation**: https://letsencrypt.org/docs/
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- **Nginx Documentation**: https://nginx.org/en/docs/

---

**🎯 Remember:** Test everything on a staging environment first if possible!
