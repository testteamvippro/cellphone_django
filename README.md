# CellPhone Store - Django E-commerce

Complete e-commerce website clone of cellphones.com.vn built with Django.

## Features

- 📱 Product catalog with multiple categories (Phones, Laptops, Watches, Audio, TV)
- 🛒 Shopping cart with session persistence
- ❤️ Wishlist functionality
- ⚡ Flash sale section with countdown
- 🎨 Responsive design matching cellphones.com.vn
- 👤 User authentication & profiles
- 📦 Order management
- 🔍 Product search & filters
- 📰 News/Blog section
- 💳 Multiple payment methods
- 🎥 Video reviews section

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Load Sample Data

```bash
python manage.py load_sample_data
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

Admin Panel: http://127.0.0.1:8000/admin

## Project Structure

```
cellphone_django/
├── cellphone_store/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                 # Main app
│   ├── models.py         # Product, Cart, Order models
│   ├── views.py          # View functions
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   └── templates/        # HTML templates
│       ├── base.html
│       ├── home.html
│       ├── product_detail.html
│       └── ...
├── static/               # CSS, JS, Images
├── media/                # User uploaded files
└── manage.py
```

## Deployment

### Railway

1. Install Railway CLI
2. Run: `railway login`
3. Run: `railway init`
4. Run: `railway up`

### Heroku

1. Install Heroku CLI
2. Run: `heroku create`
3. Run: `git push heroku main`

### PythonAnywhere

1. Upload code to PythonAnywhere
2. Setup virtual environment
3. Configure WSGI file
4. Set static files path

## Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: HTML, CSS (Tailwind-inspired), JavaScript
- **Image Processing**: Pillow
- **API**: Django REST Framework

## License

MIT License
