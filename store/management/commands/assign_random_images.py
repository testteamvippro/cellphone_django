"""
Management command to download and assign random phone images to products
Uses urllib to download images from Unsplash (free, no auth needed)
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product
import urllib.request
import os
import random
from pathlib import Path

class Command(BaseCommand):
    help = 'Download phone images from online sources and assign them randomly to products'

    def handle(self, *args, **options):
        self.stdout.write('Starting image assignment process...')
        
        # Phone image URLs from multiple sources
        # Mixed Unsplash, Pexels, and other free sources
        phone_image_urls = [
            # High-quality phone images
            'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1574405174712-7a6e9ed0ae11?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1511454612769-005902c7fb22?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1592286927505-1def25115558?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1516321318423-f06f70674b6e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1514306688900-42dc01e7f839?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1513001900722-e8fb308b4c1d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1505228395891-9a51e7e86e81?w=400&h=400&fit=crop',
            # Alternative phone images
            'https://images.unsplash.com/photo-1537228500867-2edd0d929bbe?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1490291540258-08d61f1e9d56?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1491933382519-3acca184cd13?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1484788984921-03950022c9ef?w=400&h=400&fit=crop',
        ]
        
        products = Product.objects.all()
        total = products.count()
        updated = 0
        failed = 0
        
        self.stdout.write(f'Found {total} products to update')
        self.stdout.write(f'Downloading and assigning {len(phone_image_urls)} different phone images randomly...\n')
        
        for idx, product in enumerate(products, 1):
            try:
                # Randomly select 2-3 different images for each product
                num_images = random.randint(2, 3)
                selected_urls = random.sample(phone_image_urls, num_images)
                
                for img_idx, url in enumerate(selected_urls):
                    try:
                        # Download image
                        self.stdout.write(f'[{idx}/{total}] Downloading image {img_idx + 1}/{num_images} for {product.name}...', ending='')
                        
                        response = urllib.request.urlopen(url, timeout=10)
                        image_data = response.read()
                        
                        # Create filename
                        filename = f'{product.slug}-img{img_idx + 1}.jpg'
                        
                        # Assign to product
                        if img_idx == 0:
                            product.image.save(filename, ContentFile(image_data), save=False)
                        elif img_idx == 1:
                            product.image_2.save(filename, ContentFile(image_data), save=False)
                        elif img_idx == 2:
                            product.image_3.save(filename, ContentFile(image_data), save=False)
                        
                        self.stdout.write(self.style.SUCCESS(' ✓'))
                        
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f' ✗ ({str(e)[:30]}...)'))
                        failed += 1
                
                # Save product with all images
                product.save()
                updated += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {product.name}: {str(e)}'))
                failed += 1
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Completed!'))
        self.stdout.write(f'  Products updated: {updated}')
        self.stdout.write(f'  Failed: {failed}')
        self.stdout.write('='*60)
        self.stdout.write('\nImages are now assigned to products!')
        self.stdout.write('Visit http://127.0.0.1:8000/ to see updated photos')
