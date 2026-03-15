# Image Upload Guide - Dâu Store

## Overview
Currently, all products are using **placeholder images** from `via.placeholder.com`. To add real product images, you have two options:

---

## Option 1: Upload via Django Admin (Recommended - Easiest)

### Step 1: Access Django Admin
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your admin credentials
3. Click on **"Products"** in the Store section

### Step 2: Edit a Product
1. Click on any product from the list
2. Scroll down to the **"Image"** field
3. Click **"Choose File"** to upload an image
4. You can also upload **Image 2** and **Image 3** for the gallery
5. Click **"Save"** at the bottom

### Step 3: Repeat for All Products
- Edit each product and upload up to 3 images
- Main image: Product front view (200x200px or larger)
- Image 2: Alternative angle
- Image 3: Another variant or color

---

## Option 2: Bulk Upload via Management Command (For Developers)

### Step 1: Prepare Image Files
1. Create a folder: `store/static/images/products/`
2. Add your product images in format: `{brand}-{model}-{storage}.jpg`

### Step 2: Run Upload Command
```bash
python manage.py upload_product_images
```

---

## Where Images Are Stored

- **Local Development**: `media/products/` folder
- **Production (Render)**: CloudFront CDN or Render's persistent storage

---

## Current Placeholder System

**Placeholder URL Format:**
```
https://via.placeholder.com/400x400?text=Apple+iPhone
```

**Features:**
- Generates placeholder images on-the-fly
- Shows brand name and model
- Works offline as backup
- Useful for testing layout

---

## How to Get Product Images

### Free Sources:
1. **Unsplash** (unsplash.com) - Free high-quality images
2. **Pexels** (pexels.com) - Free stock photos
3. **Brand Websites** - Official product images
4. **Phone Manufacturer Sites** - Samsung, Apple, Xiaomi stores

### Steps to Use:
1. Search for "iPhone 15 Pro Max product image"
2. Download the image
3. Rename it to match the product format
4. Upload via Django Admin

---

## Image Specifications

| Field | Spec |
|-------|------|
| Main Image | 400x400px (square recommended) |
| Thumbnails | 64x64px |
| Format | JPG, PNG |
| Max Size | 5MB per image |
| Product Card | 200x160px |

---

## After Setting Up Images

1. **Homepage** will show real product images in sliders
2. **Product List** will display product images with proper branding
3. **Product Detail** will show image gallery with zoom functionality
4. **Mobile** version will be optimized for smaller screens

---

## Testing Images

After uploading images:
1. Go to `http://127.0.0.1:8000/`
2. Verify flash sale products show your images
3. Click on a product to see the detail page
4. Check the image gallery functionality

---

## Troubleshooting

### Images Not Showing?
- Clear browser cache (Ctrl+Shift+Del)
- Verify image file exists in `media/products/`
- Check file permissions

### Image Quality Low?
- Use high-resolution source images (1000x1000px+)
- Avoid stretching images in HTML
- Use PNG for graphics, JPG for photos

### Storage Issues?
- Delete unused images from `media/` folder
- On Render, use external CDN or S3 storage
- See deployment guide for more info

---

## Production Setup

For Render deployment, configure:
1. **AWS S3** for image storage (recommended)
2. **Django Storages** package
3. Update `settings.py` with S3 credentials

See `DEPLOYMENT.md` for complete AWS S3 setup instructions.
