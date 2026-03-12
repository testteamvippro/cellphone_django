# 🚀 Quick Deploy to Railway

## Deploy in 3 Steps:

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login and Initialize
```bash
railway login
cd cellphone_django
railway init
```

### 3. Deploy!
```bash
railway up
```

Railway will:
- ✅ Detect it's a Django project
- ✅ Automatically provision PostgreSQL
- ✅ Install dependencies from requirements.txt
- ✅ Run migrations
- ✅ Collect static files
- ✅ Give you a live URL

### 4. Set Environment Variables (in Railway Dashboard)

```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=.railway.app
```

### 5. Load Sample Data (Optional)
```bash
railway run python manage.py load_sample_data
railway run python manage.py create_superuser_auto
```

### 6. Get Your URL
```bash
railway domain
```

---

## Alternative: Deploy to Render (Also Free!)

### 1. Create a Render account at https://render.com

### 2. New Web Service → Connect GitHub repo

### 3. Configure:
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command**: `gunicorn cellphone_store.wsgi`
- **Add PostgreSQL** database from Render dashboard

### 4. Set Environment Variables:
- `SECRET_KEY`: Your secret key
- `DEBUG`: False
- `ALLOWED_HOSTS`: .onrender.com
- `DATABASE_URL`: (Auto-filled by Render)

### 5. After Deploy:
```bash
# In Render Shell
python manage.py migrate
python manage.py load_sample_data
python manage.py create_superuser_auto
```

---

## Your App is Now Live! 🎉

Access:
- **Frontend**: https://your-app.railway.app/ (or .onrender.com)
- **Admin**: https://your-app.railway.app/admin/
  - Username: `admin`
  - Password: `admin123` (Change this!)

---

## Troubleshooting

### Static files not loading?
```bash
railway run python manage.py collectstatic --noinput
```

### Database issues?
Check that `DATABASE_URL` is set correctly in Railway/Render dashboard

### Need to see logs?
```bash
railway logs
```

---

**Files Created for Deployment:**
- ✅ `Procfile` - Tells Railway/Render how to run the app
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Updated for production environment
- ✅ `.gitignore` - Don't commit sensitive files

**Ready to deploy!** 🚀
