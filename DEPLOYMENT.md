# Deployment Guide for CellphoneS Django

This guide covers deploying your Django e-commerce application to various platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Changed `SECRET_KEY` in production
- [ ] Set `DEBUG = False`
- [ ] Updated `ALLOWED_HOSTS`
- [ ] Configured PostgreSQL (for production)
- [ ] Set up environment variables
- [ ] Changed admin password
- [ ] Configured email settings
- [ ] Set up static file serving
- [ ] Tested all functionality locally

## 🚀 Platform-Specific Guides

### 1. Railway (Recommended - Easy & Free Tier)

**Why Railway?**
- Free tier available
- Automatic PostgreSQL provisioning
- Easy deployment from Git
- Built-in SSL
- Simple environment variable management

**Steps:**

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize project** (in your project directory):
```bash
cd cellphone_django
railway init
```

4. **Add PostgreSQL database**:
```bash
railway add
# Select PostgreSQL from the list
```

5. **Create `railway.json` config**:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn cellphone_store.wsgi",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

6. **Create `Procfile`**:
```
web: gunicorn cellphone_store.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
```

7. **Add `gunicorn` to requirements.txt**:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

8. **Set environment variables** in Railway dashboard:
   - Go to your project on Railway dashboard
   - Click on Variables tab
   - Add:
```
SECRET_KEY=your-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.railway.app
DATABASE_URL=(automatically set by Railway PostgreSQL)
```

9. **Update `settings.py` for production**:
```python
import os
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```

10. **Deploy**:
```bash
railway up
```

11. **After deployment, run commands**:
```bash
railway run python manage.py load_sample_data
railway run python manage.py create_superuser_auto
```

12. **Get your URL**:
```bash
railway domain
```

---

### 2. Heroku (Established Platform)

**Why Heroku?**
- Well-documented
- Large ecosystem of add-ons
- Easy scaling
- Free tier available (with limitations)

**Steps:**

1. **Install Heroku CLI**:
   - Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login**:
```bash
heroku login
```

3. **Create Heroku app**:
```bash
heroku create cellphones-store-django
```

4. **Add PostgreSQL add-on**:
```bash
heroku addons:create heroku-postgresql:mini
```

5. **Create `Procfile`**:
```
web: gunicorn cellphone_store.wsgi
release: python manage.py migrate
```

6. **Create `runtime.txt`**:
```
python-3.11.8
```

7. **Update `requirements.txt`**:
```bash
pip freeze > requirements.txt
# Add these if missing:
# gunicorn==21.2.0
# dj-database-url==2.1.0
# whitenoise==6.6.0
```

8. **Update `settings.py`**:
```python
import dj_database_url

# Heroku database
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

9. **Set config vars**:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com
```

10. **Deploy**:
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

11. **Run post-deployment commands**:
```bash
heroku run python manage.py collectstatic --noinput
heroku run python manage.py load_sample_data
heroku run python manage.py create_superuser_auto
```

12. **Open app**:
```bash
heroku open
```

---

### 3. PythonAnywhere (Python-Specific Hosting)

**Why PythonAnywhere?**
- Python-focused hosting
- Free tier with custom domains
- SSH access
- Simple web interface

**Steps:**

1. **Sign up** at https://www.pythonanywhere.com

2. **Upload code**:
   - Option A: Use Git from Bash console
   ```bash
   git clone https://github.com/yourusername/cellphone_django.git
   ```
   - Option B: Upload via Files tab

3. **Create virtual environment** (from Bash console):
```bash
cd cellphone_django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure database**:
```bash
python manage.py migrate
python manage.py load_sample_data
python manage.py create_superuser_auto
python manage.py collectstatic
```

5. **Configure WSGI** (Web tab → WSGI configuration file):
```python
import os
import sys

# Add project directory
path = '/home/yourusername/cellphone_django'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'cellphone_store.settings'

# Load Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. **Set up static files** (Web tab):
   - URL: `/static/`
   - Directory: `/home/yourusername/cellphone_django/static/`
   - URL: `/media/`
   - Directory: `/home/yourusername/cellphone_django/media/`

7. **Set environment variables** (in WSGI file):
```python
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['DEBUG'] = 'False'
```

8. **Reload web app** (green button on Web tab)

---

### 4. DigitalOcean App Platform

**Why DigitalOcean?**
- Good performance
- Predictable pricing
- Full control over infrastructure
- Free tier available

**Steps:**

1. **Create account** at digitalocean.com

2. **Create `app.yaml`**:
```yaml
name: cellphones-django
services:
- name: web
  github:
    repo: yourusername/cellphone_django
    branch: main
  build_command: |
    pip install -r requirements.txt
    python manage.py collectstatic --noinput
  run_command: gunicorn cellphone_store.wsgi
  envs:
  - key: SECRET_KEY
    value: ${SECRET_KEY}
  - key: DEBUG
    value: "False"
databases:
- name: db
  engine: PG
  version: "12"
```

3. **Connect GitHub repo** in DigitalOcean dashboard

4. **Deploy** via dashboard

---

### 5. AWS Elastic Beanstalk

**Why AWS?**
- Enterprise-grade
- Highly scalable
- Extensive services
- Free tier (12 months)

**Steps:**

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize EB**:
```bash
eb init -p python-3.11 cellphones-django
```

3. **Create `.ebextensions/django.config`**:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: cellphone_store.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: cellphone_store.settings
```

4. **Create environment**:
```bash
eb create cellphones-env
```

5. **Set environment variables**:
```bash
eb setenv SECRET_KEY=your-secret-key DEBUG=False
```

6. **Deploy**:
```bash
eb deploy
```

---

## 🔐 Security Best Practices

### 1. Environment Variables

Never commit sensitive data to Git. Use environment variables:

**.env file** (don't commit this):
```env
SECRET_KEY=your-very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
```

**Install python-decouple**:
```bash
pip install python-decouple
```

**Update settings.py**:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

### 2. Generate Strong SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. HTTPS Configuration

```python
# In production settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 4. Database Security

- Use strong passwords
- Limit database access by IP
- Regular backups
- Use connection pooling

---

## 📊 Database Migration (SQLite → PostgreSQL)

### Export from SQLite:
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datadump.json
```

### Import to PostgreSQL:
```bash
# Configure PostgreSQL in settings.py
python manage.py migrate
python manage.py loaddata datadump.json
```

---

## 🎯 Performance Optimization

### 1. Enable Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Optimize Database Queries

```python
# Use select_related for foreign keys
products = Product.objects.select_related('category', 'brand').all()

# Use prefetch_related for many-to-many
products = Product.objects.prefetch_related('colors', 'specs').all()
```

### 3. Compress Static Files

```python
# Install whitenoise
pip install whitenoise

# Add to MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    ...
]

# Enable compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. CDN for Static Files

Use AWS S3, Cloudinary, or similar for media files.

---

## 📧 Email Configuration

### Gmail SMTP:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'CellphoneS <noreply@cellphones.com>'
```

### SendGrid:
```bash
pip install sendgrid
```

---

## 🔍 Monitoring & Logging

### Sentry for Error Tracking:
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
)
```

---

## 🆘 Common Deployment Issues

### Issue: Static files not loading
**Solution**:
```bash
python manage.py collectstatic --clear --noinput
```

### Issue: Database connection errors
**Solution**: Check `DATABASE_URL` and database credentials

### Issue: Module not found
**Solution**: Ensure all dependencies in `requirements.txt`

### Issue: Permission denied
**Solution**: Check file permissions and user access

---

## ✅ Post-Deployment Testing

1. **Test all pages** - Homepage, products, cart, checkout
2. **Test user registration** and login
3. **Test cart functionality** - Add, update, remove items
4. **Test checkout process** - Complete an order
5. **Test admin panel** - Login and manage products
6. **Test static files** - CSS, JS, images loading
7. **Test media uploads** - Product images
8. **Check logs** for errors
9. **Test on multiple devices** - Desktop, mobile, tablet
10. **Performance test** - Page load times

---

## 📱 Domain Configuration

### Custom Domain Setup:

1. **Update ALLOWED_HOSTS**:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

2. **Configure DNS** (at your domain registrar):
```
A Record: @ → Your server IP
CNAME Record: www → yourdomain.com
```

3. **SSL Certificate** (use Let's Encrypt or platform-provided)

---

**Need help?** Check the main README.md or open an issue!
