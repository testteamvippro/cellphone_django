# 🍓 Logo Installation Instructions

## How to Add Your Logo

Your templates have been updated to use the new "Dâu Store" logo. Follow these simple steps:

### Step 1: Save the Logo Image

1. **Save the attached logo image** as `logo.png`
2. **Place it in this folder**: `store/static/store/images/`
3. The full path should be: `c:\PersonalStored\1___MyCode\cellphone_django\store\static\store\images\logo.png`

### Step 2: Verify the Logo

The logo will automatically appear in:
- ✅ **Website Header** - Top navigation bar
- ✅ **Admin Panel** - Admin header
- ✅ **All Pages** - Consistent branding

### What's Been Updated

✅ **Template Files:**
- [store/templates/store/base.html](store/templates/store/base.html) - Main website logo
- [store/templates/admin/base_site.html](store/templates/admin/base_site.html) - Admin panel logo
- [store/templates/admin/store_dashboard.html](store/templates/admin/store_dashboard.html) - Dashboard branding

✅ **Branding Changes:**
- Site name: **CellphoneS** → **Dâu Store**
- Email: **support@cellphones.vn** → **support@daustore.vn**
- Copyright: **2024 CellphoneS** → **2026 Dâu Store**
- Admin header: **Cellphone Store Admin** → **🍓 Dâu Store Admin**

### Logo Specifications

- **File name**: `logo.png`
- **Location**: `store/static/store/images/logo.png`
- **Recommended size**: The logo will automatically scale to height 48px
- **Format**: PNG with transparent or dark background
- **Current logo**: Features strawberry icon with "DẨU STORE" text in gold/beige color

### Quick Copy Command

If the logo is in your Downloads folder, you can copy it using:

```powershell
# Create the images directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "c:\PersonalStored\1___MyCode\cellphone_django\store\static\store\images"

# Copy from Downloads (adjust the path if your logo is elsewhere)
Copy-Item "$env:USERPROFILE\Downloads\logo.png" -Destination "c:\PersonalStored\1___MyCode\cellphone_django\store\static\store\images\logo.png"
```

### Testing

After placing the logo:

1. **Start the server**:
   ```powershell
   python manage.py runserver
   ```

2. **Visit**: http://localhost:8000/
   - You should see the logo in the header

3. **Visit Admin**: http://localhost:8000/admin/
   - You should see the logo in the admin panel header

### Troubleshooting

**Logo not appearing?**
- ✅ Check file name is exactly `logo.png` (case-sensitive on some systems)
- ✅ Check file location: `store/static/store/images/logo.png`
- ✅ Clear browser cache (Ctrl+F5)
- ✅ Run `python manage.py collectstatic` for production

**Logo too big/small?**
- Edit the height in [base.html](store/templates/store/base.html): Change `h-12` (48px) to desired size
- Edit the height in [base_site.html](store/templates/admin/base_site.html): Change `height: 40px` to desired size

---

## All Done! 🎉

Your "Dâu Store" branding is now applied throughout the entire website and admin panel!
