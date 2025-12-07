# 🚀 Pre-Deployment Checklist

## ✅ Essential Steps Before Going Live

### 1. Code Preparation

```bash
# Make build script executable
chmod +x build.sh

# Add it to git
git add build.sh
git commit -m "Make build script executable"
```

- [ ] All code tested locally
- [ ] No syntax errors
- [ ] All migrations created and applied
- [ ] Test data loads correctly
- [ ] Build script is executable

### 2. Git Repository Setup

```bash
# Initialize git (if not done)
git init

# Create .gitignore (already exists)
# Ensure these are in .gitignore:
# - db.sqlite3
# - .env
# - __pycache__/
# - *.pyc
# - /media (optional)
# - /staticfiles

# Add all files
git add .

# Commit
git commit -m "Initial commit - MMU Bicycle Rental System"

# Create repository on GitHub
# Then connect and push
git remote add origin https://github.com/YOUR_USERNAME/mmu-bicycle-rental.git
git branch -M main
git push -u origin main
```

- [ ] Git repository initialized
- [ ] .gitignore properly configured
- [ ] All files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

### 3. Environment Variables

Create a list of environment variables needed:

**Required:**
- `SECRET_KEY` - Django secret key (auto-generated)
- `DEBUG` - Set to `False`
- `DATABASE_URL` - PostgreSQL connection string
- `DJANGO_SETTINGS_MODULE` - `config.settings.production`

**Optional:**
- `EMAIL_HOST` - SMTP server
- `EMAIL_PORT` - SMTP port
- `EMAIL_HOST_USER` - Email username
- `EMAIL_HOST_PASSWORD` - Email password
- `MPESA_CONSUMER_KEY` - M-Pesa key
- `MPESA_CONSUMER_SECRET` - M-Pesa secret
- `PAYPAL_CLIENT_ID` - PayPal ID
- `PAYPAL_CLIENT_SECRET` - PayPal secret

- [ ] Environment variables documented
- [ ] Secrets prepared (don't commit!)
- [ ] Email configuration ready

### 4. Dependencies Check

```bash
# Ensure all dependencies are in requirements.txt
pip freeze > requirements-freeze.txt
diff requirements.txt requirements-freeze.txt

# Update if needed
pip install -r requirements.txt
```

- [ ] All dependencies listed
- [ ] requirements.txt up to date
- [ ] No conflicting versions

### 5. Static Files

```bash
# Test static file collection
python manage.py collectstatic --noinput

# Check that staticfiles directory is created
ls -la staticfiles/
```

- [ ] Static files collect successfully
- [ ] CSS files present
- [ ] JavaScript files present
- [ ] Images present

### 6. Database

```bash
# Create fresh migrations
python manage.py makemigrations

# Check migration status
python manage.py showmigrations

# Test migrations
python manage.py migrate
```

- [ ] All migrations created
- [ ] Migrations apply successfully
- [ ] No migration conflicts
- [ ] Initial data fixtures ready

### 7. Security Settings

Check `config/settings/production.py`:

- [ ] `DEBUG = False`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS` set
- [ ] `ALLOWED_HOSTS` configured

### 8. Media Files

- [ ] Media upload directories configured
- [ ] File size limits set
- [ ] Image validation in place
- [ ] Consider using cloud storage (Cloudinary/S3)

### 9. Testing

```bash
# Run all tests
python manage.py test

# Test key workflows
# 1. User registration
# 2. Bicycle reservation
# 3. Rental flow
# 4. Payment (if configured)
```

- [ ] All tests passing
- [ ] User flows tested
- [ ] Edge cases handled
- [ ] Error pages customized

### 10. Documentation

- [ ] README.md complete
- [ ] DEPLOYMENT_GUIDE.md ready
- [ ] API documentation (if using API)
- [ ] User guide created
- [ ] Admin guide created

---

## 🎯 Quick Deploy to Render (Step-by-Step)

### Step 1: Create GitHub Repository

1. Go to github.com
2. Click "New repository"
3. Name: `mmu-bicycle-rental`
4. Public or Private
5. Click "Create repository"

```bash
# Push your code
git remote add origin https://github.com/YOUR_USERNAME/mmu-bicycle-rental.git
git push -u origin main
```

### Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Name: `mmu-bicycle-db`
3. Database: `mmu_bicycle_rental`
4. User: `mmu_user`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click "Create Database"
8. **Copy the "Internal Database URL"** - you'll need this!

### Step 4: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `mmu-bicycle-rental`
4. Configure:
   - **Name:** `mmu-bicycle-rental`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
   - **Plan:** **Free**

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these:
   ```
   PYTHON_VERSION = 3.11.0
   DJANGO_SETTINGS_MODULE = config.settings.production
   DEBUG = False
   DATABASE_URL = [Paste the Internal Database URL from Step 3]
   SECRET_KEY = [Click "Generate" button]
   ```

6. Click "Create Web Service"

### Step 5: Wait for Deployment

- Watch the logs
- First deploy takes 5-10 minutes
- When you see "Your service is live 🎉" - it's done!

### Step 6: Create Superuser

1. Go to your web service dashboard
2. Click "Shell" tab (top right)
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts

### Step 7: Load Initial Data (Optional)

In the Shell:
```bash
python create_test_data.py
```

### Step 8: Access Your App

Your app is now live at:
```
https://mmu-bicycle-rental.onrender.com
```

Or click the URL at the top of your dashboard!

---

## 🎨 Post-Deployment Tasks

### Immediate:
- [ ] Access the site and verify it loads
- [ ] Login to admin panel
- [ ] Create test user account
- [ ] Test bicycle reservation
- [ ] Test rental flow
- [ ] Check emails (console or real)

### Soon:
- [ ] Add real station data
- [ ] Add real bicycle inventory
- [ ] Configure real email (Gmail/SendGrid)
- [ ] Setup payment processing (M-Pesa/PayPal)
- [ ] Add custom domain
- [ ] Enable SSL/HTTPS
- [ ] Setup monitoring (Sentry)
- [ ] Configure backups

### Marketing:
- [ ] Share link with MMU community
- [ ] Create user guide
- [ ] Train support staff
- [ ] Gather user feedback
- [ ] Monitor usage

---

## 🔧 Troubleshooting Common Issues

### Build Failed
```bash
# Check build.sh is executable
git ls-files -s build.sh
# Should show: 100755 (executable)

# If not:
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

### Database Connection Error
- Verify DATABASE_URL is correct
- Check database is in same region as web service
- Internal Database URL should be used (not External)

### Static Files Not Loading
- Check `STATICFILES_STORAGE` setting
- Run `python manage.py collectstatic` in shell
- Verify WhiteNoise is installed

### 502 Bad Gateway
- Check Gunicorn is starting correctly
- Review deployment logs
- Verify start command is correct

### Environment Variables Not Working
- Don't use quotes around values
- Click "Save Changes" after adding variables
- Redeploy after changing variables

---

## 💰 Cost Breakdown

### Free Tier (Render):
- **Web Service:** Free (spins down after 15min inactivity)
- **PostgreSQL:** Free (1GB storage)
- **Bandwidth:** 100GB/month free
- **Custom Domain:** Free (bring your own)
- **SSL:** Free (automatic)

**Total: $0/month** ✅

### Paid Tier (Optional):
- **Web Service:** $7/month (no spin-down)
- **PostgreSQL:** $7/month (more storage)
- **Total: $14/month**

### Domain (Optional):
- **.com domain:** ~$10/year
- **.ac.ke domain:** Contact registry

---

## 🎉 You're Ready to Deploy!

Follow the "Quick Deploy to Render" section above for the easiest path to production.

**Estimated time to deploy: 15-20 minutes**

Good luck! 🚀