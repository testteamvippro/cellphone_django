"""
Management command to assign iPhone 17 PM image to all products
"""
from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product
import os


class Command(BaseCommand):
    help = 'Assign iPhone 17 PM image to all products'

    def handle(self, *args, **options):
        self.stdout.write('Assigning iPhone 17 PM image to all products...\n')
        
        # Path to the source image
        image_path = 'store/static/store/images/products/iphone_17_pm.png'
        
        # Check if file exists
        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'Image file not found: {image_path}'))
            return
        
        # Get all products
        products = Product.objects.all()
        total = products.count()
        assigned = 0
        
        self.stdout.write(f'Found {total} products to update')
        
        # Assign image to each product
        for idx, product in enumerate(products, 1):
            try:
                # Open the image file
                with open(image_path, 'rb') as img_file:
                    # Assign to main image field
                    product.image.save(
                        f'{product.slug}-iphone-17-pm.png',
                        File(img_file),
                        save=True
                    )
                assigned += 1
                
                # Progress indicator
                if idx % 10 == 0:
                    self.stdout.write(f'  ✓ Processed {idx}/{total}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ Failed for {product.name}: {str(e)}'))
        
        self.stdout.write(f'\n{self.style.SUCCESS("Done!")} Assigned iPhone 17 PM image to {assigned}/{total} products ({round(assigned/total*100, 1)}%)')
