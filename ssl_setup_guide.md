# SSL/TLS Configuration Guide for EldenRing Challenges Website

This guide covers SSL/TLS setup for production deployment of your EldenRing Challenges website.

## 🔐 **SSL Certificate Options**

### Option 1: Let's Encrypt (Free, Recommended)

Let's Encrypt provides free SSL certificates that are automatically renewed.

#### Prerequisites:

- Domain name pointing to your server
- Certbot installed on your server

#### Installation:

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**CentOS/RHEL:**

```bash
sudo yum install certbot python3-certbot-nginx
```

#### Generate Certificate:

```bash
# For Nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# For Apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

#### Auto-renewal Setup:

```bash
# Test renewal
sudo certbot renew --dry-run

# Add to crontab for automatic renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Commercial SSL Certificate

If you prefer a commercial certificate:

1. Purchase from a trusted CA (DigiCert, Comodo, etc.)
2. Generate CSR on your server
3. Submit CSR to CA
4. Install received certificate

## 🌐 **Web Server Configuration**

### Nginx Configuration

Create `/etc/nginx/sites-available/eldenring-challenges`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server Block
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security Headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self';" always;

    # Static files
    location /static/ {
        alias /path/to/your/project/mybackend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/mybackend/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /api/health/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        access_log off;
    }

    # Rate limiting for sensitive endpoints
    location /api/login/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/signup/ {
        limit_req zone=signup burst=3 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Rate limiting zones (add to main nginx.conf)
http {
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=signup:10m rate=3r/h;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/eldenring-challenges /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Apache Configuration

Create `/etc/apache2/sites-available/eldenring-challenges-ssl.conf`:

```apache
# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    # SSL Security
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    SSLSessionTickets off

    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    # Security Headers
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"

    # Static files
    Alias /static/ /path/to/your/project/mybackend/staticfiles/
    <Directory /path/to/your/project/mybackend/staticfiles/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Directory>

    # Media files
    Alias /media/ /path/to/your/project/mybackend/media/
    <Directory /path/to/your/project/mybackend/media/>
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Directory>

    # Proxy to Django
    ProxyPreserveHost On
    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    # Set headers for Django
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPassReverseMatch ^(/.*) http://127.0.0.1:8000$1
</VirtualHost>
```

Enable required modules and site:

```bash
sudo a2enmod ssl headers expires proxy proxy_http
sudo a2ensite eldenring-challenges-ssl
sudo apache2ctl configtest
sudo systemctl reload apache2
```

## 🔧 **Django SSL Configuration**

Your `settings_production.py` already includes SSL settings, but verify these are set:

```python
# Force HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Other security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 🧪 **SSL Testing**

### 1. Test SSL Configuration

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check certificate expiration
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com 2>/dev/null | openssl x509 -noout -dates
```

### 2. Online SSL Tests

- **SSL Labs Test**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **Mozilla Observatory**: https://observatory.mozilla.org/

### 3. Expected Results

- SSL Labs Grade: A or A+
- All security headers present
- No mixed content warnings

## 🔄 **Certificate Renewal**

### Automatic Renewal (Let's Encrypt)

```bash
# Check renewal status
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run

# Manual renewal if needed
sudo certbot renew
```

### Monitoring Certificate Expiration

Add to your monitoring script:

```bash
#!/bin/bash
# Check certificate expiration
DOMAIN="yourdomain.com"
EXPIRY_DATE=$(openssl s_client -connect $DOMAIN:443 -servername $DOMAIN 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "WARNING: SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days"
    # Send alert email
fi
```

## 🚨 **Troubleshooting**

### Common Issues:

1. **Certificate not trusted**

   - Verify certificate chain is complete
   - Check intermediate certificates

2. **Mixed content warnings**

   - Ensure all resources load over HTTPS
   - Update hardcoded HTTP URLs

3. **Redirect loops**

   - Check proxy headers configuration
   - Verify `SECURE_PROXY_SSL_HEADER` setting

4. **Certificate renewal fails**
   - Check domain DNS resolution
   - Verify web server configuration
   - Check firewall rules

### Debug Commands:

```bash
# Check certificate details
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout

# Test web server config
nginx -t  # For Nginx
apache2ctl configtest  # For Apache

# Check logs
tail -f /var/log/nginx/error.log
tail -f /var/log/apache2/error.log
tail -f /var/log/letsencrypt/letsencrypt.log
```

## 📋 **SSL Security Checklist**

- [ ] SSL certificate installed and valid
- [ ] HTTP redirects to HTTPS
- [ ] HSTS header configured
- [ ] Security headers present
- [ ] Strong SSL ciphers configured
- [ ] Certificate auto-renewal working
- [ ] SSL Labs grade A or A+
- [ ] No mixed content warnings
- [ ] Certificate expiration monitoring
- [ ] Backup certificates stored securely

## 🔐 **Additional Security Measures**

### 1. Certificate Transparency Monitoring

Monitor your certificates at:

- https://crt.sh/
- https://transparencyreport.google.com/https/certificates

### 2. HSTS Preload

Submit your domain to HSTS preload list:

- https://hstspreload.org/

### 3. CAA Records

Add DNS CAA records to restrict certificate authorities:

```
yourdomain.com. CAA 0 issue "letsencrypt.org"
yourdomain.com. CAA 0 issuewild "letsencrypt.org"
yourdomain.com. CAA 0 iodef "mailto:admin@yourdomain.com"
```

This SSL setup provides enterprise-grade security for your EldenRing Challenges website!
