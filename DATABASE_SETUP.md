# Database Setup & Management Guide

## 🎯 Understanding Your Database System

Your Django project uses **Django ORM (Object-Relational Mapping)** as the database management system:

- ✅ **ORM = Database CRM** - Manages all database operations
- ✅ **Models** - Python classes that represent database tables
- ✅ **Migrations** - Version control for your database schema
- ✅ **QuerySets** - Python API for database queries

## 📊 Database Configuration

Your project supports two database systems:

### Development (Local)
- **Database**: SQLite3
- **File**: `db.sqlite3` (created in project root)
- **Advantages**: No installation needed, portable, fast for development

### Production (Deployment)
- **Database**: PostgreSQL
- **Connection**: Via DATABASE_URL environment variable
- **Advantages**: Scalable, robust, supports concurrent users

## 🚀 Step 1: Create Database

Run these commands in order:

```bash
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Create database tables (apply migrations)
python manage.py migrate

# You should see output like:
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, sessions, store
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying admin.0001_initial... OK
#   Applying store.0001_initial... OK
#   ...
```

**What this does:**
- Creates `db.sqlite3` file in your project root
- Creates all database tables based on your models
- Sets up Django's built-in tables (users, sessions, admin, etc.)

## 🔐 Step 2: Create Admin User

```bash
# Option A: Interactive creation
python manage.py createsuperuser
# Enter: username, email, password

# Option B: Auto-creation (uses defaults)
python manage.py create_superuser_auto
```

**Default credentials (if using auto-create):**
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

## 📦 Step 3: Load Sample Data

```bash
# Load demo products, categories, brands, etc.
python manage.py load_sample_data
```

**What this creates:**
- ✅ 3 Categories (Smartphones, Tablets, Accessories)
- ✅ 3 Brands (Apple, Samsung, Google)
- ✅ 15+ Sample Products with images
- ✅ 5 News Articles
- ✅ 2 Video Reviews
- ✅ Product specifications and colors

## 🗄️ Database Structure

Your database has these tables (models):

### Core Models
```
store_category         - Product categories
store_brand           - Phone brands
store_product         - Products/phones
store_productcolor    - Product color variants
store_productspec     - Product specifications
```

### Shopping Models
```
store_cart            - Shopping carts
store_cartitem        - Items in carts
store_order           - Customer orders
store_orderitem       - Items in orders
store_wishlist        - Customer wishlists
```

### Content Models
```
store_newsarticle     - Blog/news articles
store_videoreview     - Video reviews
```

### Django Built-in
```
auth_user             - User accounts
auth_group            - User groups
django_session        - Session data
django_admin_log      - Admin action logs
```

## 🔧 Database Management Commands

### Viewing Database
```bash
# Open Django shell (Python REPL with Django context)
python manage.py shell

# In shell, query data:
from store.models import Product, Order, Category

# Get all products
Product.objects.all()

# Get specific product
Product.objects.get(id=1)

# Filter products
Product.objects.filter(is_available=True)

# Count products
Product.objects.count()

# Exit shell
exit()
```

### Database Migrations
```bash
# After changing models.py, create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show all migrations
python manage.py showmigrations

# Revert to specific migration
python manage.py migrate store 0001
```

### Database Inspection
```bash
# Show SQL for migrations
python manage.py sqlmigrate store 0001

# Check for migration issues
python manage.py check

# Open database shell (SQLite)
python manage.py dbshell
```

## 📊 Accessing Your Data

### 1. Django Admin Panel
```
URL: http://localhost:8000/admin/
- Visual interface to manage all data
- Create, read, update, delete records
- Bulk operations
- Search and filter
```

### 2. Custom Dashboard
```
URL: http://localhost:8000/admin-dashboard/
- Analytics and statistics
- Revenue tracking
- Popular products
- Order overview
```

### 3. Django Shell
```bash
python manage.py shell
# Direct Python access to database
```

### 4. Database Browser (Optional)
- **DB Browser for SQLite**: Download from https://sqlitebrowser.org/
- Open `db.sqlite3` file
- View tables, run SQL queries

## 🔄 Common Database Operations

### Reset Database (Start Fresh)
```bash
# WARNING: Deletes all data!

# Delete database file
Remove-Item db.sqlite3

# Recreate database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data
```

### Backup Database
```bash
# SQLite backup (simple file copy)
Copy-Item db.sqlite3 -Destination "db_backup_$(Get-Date -Format 'yyyyMMdd').sqlite3"

# Or use Django dumpdata
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

### Export Data
```bash
# Export all data
python manage.py dumpdata > full_backup.json

# Export specific app
python manage.py dumpdata store > store_backup.json

# Export specific model
python manage.py dumpdata store.Product > products.json

# Pretty print JSON
python manage.py dumpdata store.Product --indent 2 > products.json
```

## 🎯 Sample Database Queries (Django Shell)

### Product Queries
```python
from store.models import Product, Category, Brand

# All products
products = Product.objects.all()

# Available products only
available = Product.objects.filter(is_available=True)

# Flash sale products
flash_sales = Product.objects.filter(is_flash_sale=True)

# Low stock products
low_stock = Product.objects.filter(stock_quantity__lt=10)

# Products by category
smartphones = Product.objects.filter(category__name='Smartphones')

# Products by brand
apple_products = Product.objects.filter(brand__name='Apple')

# Products with discount
discounted = Product.objects.filter(original_price__gt=0)

# Search by name
iphones = Product.objects.filter(name__icontains='iPhone')

# Count products
total = Product.objects.count()

# Get specific product
product = Product.objects.get(id=1)
print(f"Name: {product.name}, Price: ${product.price}")
```

### Order Queries
```python
from store.models import Order
from django.db.models import Sum, Count, Avg

# All orders
orders = Order.objects.all()

# Pending orders
pending = Order.objects.filter(status='pending')

# Orders by specific user
user_orders = Order.objects.filter(user__username='john')

# Total revenue
revenue = Order.objects.filter(
    status__in=['delivered', 'shipped']
).aggregate(Sum('total_amount'))

# Average order value
avg_order = Order.objects.aggregate(Avg('total_amount'))

# Order count by status
Order.objects.values('status').annotate(count=Count('id'))

# Recent orders (last 10)
recent = Order.objects.order_by('-created_at')[:10]
```

### Cart Queries
```python
from store.models import Cart
from django.utils import timezone
from datetime import timedelta

# Active carts
active = Cart.objects.filter(items__isnull=False).distinct()

# Abandoned carts (not updated in 7 days)
week_ago = timezone.now() - timedelta(days=7)
abandoned = Cart.objects.filter(updated_at__lt=week_ago)

# Cart by session
cart = Cart.objects.get(session_id='abc123')

# Total items in cart
cart.items.count()

# Cart total value
total = sum(item.get_subtotal() for item in cart.items.all())
```

### Category/Brand Analytics
```python
from store.models import Category, Brand
from django.db.models import Count

# Categories with product count
categories = Category.objects.annotate(
    product_count=Count('products')
)

for cat in categories:
    print(f"{cat.name}: {cat.product_count} products")

# Brands with product count
brands = Brand.objects.annotate(
    product_count=Count('products')
)

# Most popular category
popular = Category.objects.annotate(
    total_views=Sum('products__view_count')
).order_by('-total_views').first()
```

## 🔐 Database Security

### Production Best Practices
1. **Use PostgreSQL** - More secure than SQLite for production
2. **Environment Variables** - Store credentials in `.env` file
3. **Regular Backups** - Automated daily backups
4. **Access Control** - Limit database user permissions
5. **SSL Connection** - Encrypt database connections

### Environment Variables (.env)
```env
# Add to .env file (never commit to Git)
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
DEBUG=False
```

## 📈 Database Monitoring

### Check Database Size
```bash
# SQLite
Get-Item db.sqlite3 | Select-Object Name, Length

# In Django shell
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
print(f"Database size: {cursor.fetchone()[0]} bytes")
```

### Query Performance
```python
# Enable query logging in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Or use django-debug-toolbar (install separately)
```

## 🆘 Troubleshooting

### Error: "no such table"
```bash
# Solution: Run migrations
python manage.py migrate
```

### Error: "database is locked"
```bash
# Solution: Close all database connections
# Restart Django server
# Check for running Django shells
```

### Error: "unable to open database file"
```bash
# Solution: Check file permissions
# Ensure db.sqlite3 exists
# Run migrations if missing
```

### Reset Migrations (Advanced)
```bash
# WARNING: Only for development!
# 1. Delete migrations
Remove-Item store\migrations\0*.py

# 2. Delete database
Remove-Item db.sqlite3

# 3. Create new migration
python manage.py makemigrations

# 4. Apply migrations
python manage.py migrate
```

## 🎓 Learning Resources

### Django ORM Documentation
- Official Docs: https://docs.djangoproject.com/en/stable/topics/db/
- QuerySet API: https://docs.djangoproject.com/en/stable/ref/models/querysets/
- Model Field Reference: https://docs.djangoproject.com/en/stable/ref/models/fields/

### Database Tools
- **SQLite Browser**: https://sqlitebrowser.org/
- **pgAdmin** (PostgreSQL): https://www.pgadmin.org/
- **DBeaver** (Universal): https://dbeaver.io/

## ✅ Quick Start Checklist

- [ ] Activate virtual environment
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py createsuperuser`
- [ ] Run `python manage.py load_sample_data`
- [ ] Access admin at `/admin/`
- [ ] Access dashboard at `/admin-dashboard/`
- [ ] Test creating a product
- [ ] Test placing an order

## 🎉 Summary

Your database is managed by **Django ORM**, which provides:
- ✅ Database abstraction (works with SQLite, PostgreSQL, MySQL, etc.)
- ✅ Automatic table creation from Python models
- ✅ Migration system for schema changes
- ✅ Python API for all database operations
- ✅ Built-in admin interface
- ✅ Query optimization and caching

**No separate "CRM database" needed** - Django ORM handles everything! 🚀
