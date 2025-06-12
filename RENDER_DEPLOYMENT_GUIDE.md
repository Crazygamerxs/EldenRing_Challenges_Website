# 🚀 Render.com Deployment Guide

## Elden Ring Challenges Website → eldenringchallenge.xyz

### 🎉 **Ready for FREE Deployment!**

Your website is now fully configured for deployment on Render.com with your custom domain `eldenringchallenge.xyz`.

---

## 📋 **Pre-Deployment Checklist**

### ✅ **Files Created/Updated:**

- `render.yaml` - Render deployment configuration
- `build.sh` - Automated build script
- `mybackend/mybackend/settings_render.py` - Production settings for your domain
- `mybackend/requirements.txt` - Updated with all dependencies
- `myfrontend/src/components/common/BottomBar.js` - Added disclaimer
- All React components - Fixed hardcoded URLs (36 files updated)

### ✅ **Features Ready:**

- **Domain**: eldenringchallenge.xyz + www.eldenringchallenge.xyz
- **SSL**: Automatic HTTPS certificates
- **Database**: PostgreSQL (free for 90 days)
- **Security**: Enhanced middleware, rate limiting, security headers
- **Disclaimer**: Fan site notice in bottom bar

---

## 🌐 **Step-by-Step Deployment**

### **Step 1: Prepare Your Repository**

1. **Commit all changes to Git:**

   ```bash
   git add .
   git commit -m "Prepare for Render deployment with eldenringchallenge.xyz"
   git push origin main
   ```

2. **Make build script executable:**
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build script executable"
   git push origin main
   ```

### **Step 2: Set Up Render Account**

1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** (free account)
3. **Connect your GitHub repository**

### **Step 3: Create PostgreSQL Database**

1. **In Render Dashboard:**

   - Click "New +"
   - Select "PostgreSQL"
   - Name: `eldenring-db`
   - Region: `Oregon (US West)`
   - Plan: **Free** (90 days free)
   - Click "Create Database"

2. **Copy Database URL:**
   - Once created, copy the "External Database URL"
   - You'll need this for the web service

### **Step 4: Deploy Web Service**

1. **In Render Dashboard:**

   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select your repository

2. **Configure Service:**

   - **Name**: `eldenring-challenges`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn mybackend.wsgi:application`

3. **Environment Variables:**

   ```
   DJANGO_SETTINGS_MODULE = mybackend.settings_render
   DATABASE_URL = [paste your PostgreSQL URL from Step 3]
   SECRET_KEY = [Render will auto-generate this]
   PYTHON_VERSION = 3.11.0
   ```

4. **Advanced Settings:**

   - **Plan**: Free
   - **Health Check Path**: `/api/health/`
   - **Auto-Deploy**: Yes

5. **Click "Create Web Service"**

### **Step 5: Configure Custom Domain**

1. **In your web service settings:**

   - Go to "Settings" tab
   - Scroll to "Custom Domains"
   - Add: `eldenringchallenge.xyz`
   - Add: `www.eldenringchallenge.xyz`

2. **Configure DNS (at your domain registrar):**

   ```
   Type: CNAME
   Name: eldenringchallenge.xyz
   Value: [your-render-app].onrender.com

   Type: CNAME
   Name: www
   Value: [your-render-app].onrender.com
   ```

### **Step 6: Wait for Deployment**

- **Build time**: ~5-10 minutes
- **Watch logs** in Render dashboard
- **SSL certificates** will be automatically provisioned

---

## 🎯 **Post-Deployment Setup**

### **Step 1: Access Your Site**

- **Temporary URL**: `https://[your-app].onrender.com`
- **Final URL**: `https://eldenringchallenge.xyz` (after DNS propagation)

### **Step 2: Create Admin Account**

The build script automatically creates:

- **Username**: `admin`
- **Email**: `admin@eldenringchallenge.xyz`
- **Password**: `EldenRing2024!`

**⚠️ IMPORTANT**: Change this password immediately!

### **Step 3: Access Admin Panel**

- Go to: `https://eldenringchallenge.xyz/admin`
- Login with admin credentials
- **Change password** in User settings

### **Step 4: Test Everything**

- ✅ Home page loads
- ✅ Challenges display
- ✅ User registration works
- ✅ Login/logout functions
- ✅ Admin panel accessible
- ✅ Disclaimer shows in footer

---

## 💰 **Cost Breakdown (FREE!)**

### **Render Free Tier:**

- **Web Service**: FREE (with limitations)
  - 750 hours/month (enough for 24/7)
  - Sleeps after 15 minutes of inactivity
  - Wakes up automatically on request
- **PostgreSQL**: FREE for 90 days, then $7/month
- **SSL Certificate**: FREE
- **Custom Domain**: FREE
- **Bandwidth**: 100GB/month FREE

### **Total Monthly Cost:**

- **First 90 days**: $0.00
- **After 90 days**: $7.00/month (just for database)

---

## 🔧 **Configuration Details**

### **Production Settings (`settings_render.py`):**

- ✅ Debug disabled
- ✅ Allowed hosts configured for your domain
- ✅ PostgreSQL database
- ✅ Enhanced security middleware
- ✅ CORS configured for your domain
- ✅ Static files with WhiteNoise
- ✅ Logging optimized for Render

### **Security Features:**

- ✅ Rate limiting (login, signup, submissions)
- ✅ Failed login tracking
- ✅ Security headers (CSP, HSTS, etc.)
- ✅ HTTPS redirect
- ✅ Enhanced session security

### **Performance Optimizations:**

- ✅ Static file compression
- ✅ Database connection pooling
- ✅ Efficient caching
- ✅ Optimized middleware stack

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. Build Fails**

- Check build logs in Render dashboard
- Ensure `build.sh` is executable
- Verify all dependencies in `requirements.txt`

#### **2. Database Connection Error**

- Verify `DATABASE_URL` environment variable
- Check PostgreSQL service is running
- Ensure database URL format is correct

#### **3. Static Files Not Loading**

- Check `collectstatic` ran successfully in build logs
- Verify WhiteNoise configuration
- Clear browser cache

#### **4. Domain Not Working**

- Check DNS propagation (can take 24-48 hours)
- Verify CNAME records are correct
- Ensure SSL certificate is provisioned

### **Debug Commands:**

```bash
# Check deployment logs
# (Available in Render dashboard)

# Test database connection
python manage.py dbshell

# Verify static files
python manage.py collectstatic --dry-run

# Check migrations
python manage.py showmigrations
```

---

## 🔄 **Updates & Maintenance**

### **Deploying Updates:**

1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically redeploys (if auto-deploy enabled)

### **Manual Deployment:**

- Go to Render dashboard
- Click "Manual Deploy" → "Deploy latest commit"

### **Database Backups:**

- Render provides automatic backups for paid plans
- For free tier, consider periodic data exports

---

## 📊 **Monitoring & Analytics**

### **Render Dashboard:**

- View deployment logs
- Monitor resource usage
- Check uptime statistics
- Review error logs

### **Django Admin:**

- Monitor user registrations
- Review challenge submissions
- Check system health at `/admin`

### **Health Check:**

- Endpoint: `https://eldenringchallenge.xyz/api/health/`
- Returns JSON with system status

---

## 🎮 **Your Live Website Features**

### **Public Features:**

- ✅ Challenge browsing and filtering
- ✅ User registration and authentication
- ✅ Leaderboards and statistics
- ✅ Challenge submission system
- ✅ Responsive design for mobile/desktop

### **Admin Features:**

- ✅ Challenge management
- ✅ User administration
- ✅ Submission review and approval
- ✅ Site settings configuration
- ✅ Security monitoring

### **Legal Compliance:**

- ✅ Fan site disclaimer
- ✅ FromSoftware trademark acknowledgment
- ✅ Server cost transparency

---

## 🎉 **Success!**

Your Elden Ring Challenges website is now live at:

- **🌐 https://eldenringchallenge.xyz**
- **🛡️ Secure HTTPS with SSL**
- **⚡ Fast global CDN**
- **🔒 Enterprise-level security**
- **💰 FREE hosting (90 days)**

**Admin Access:**

- **URL**: https://eldenringchallenge.xyz/admin
- **Username**: admin
- **Password**: EldenRing2024! (change immediately!)

**Remember to:**

1. Change the admin password
2. Set up your domain DNS
3. Test all functionality
4. Monitor the deployment logs

**🎮 May the challenges guide your way, Tarnished!**
