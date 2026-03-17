"""
Management command to assign a single static image to all products.
Uses the bundled iphone_17_pm.png from static files — no downloads needed.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Product
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Assign the bundled product image to all products'

    def handle(self, *args, **options):
        self.stdout.write('Starting image assignment...')

        # Source: static file bundled in repo
        src = Path(settings.BASE_DIR) / 'store' / 'static' / 'store' / 'images' / 'products' / 'iphone_17_pm.png'

        if not src.exists():
            self.stdout.write(self.style.ERROR(f'Source image not found: {src}'))
            return

        # Destination inside MEDIA_ROOT
        dest_dir = Path(settings.MEDIA_ROOT) / 'products'
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / 'iphone_17_pm.png'
        shutil.copy2(src, dest)
        self.stdout.write(self.style.SUCCESS(f'Copied image to {dest}'))

        # Set every product to use this one image
        image_path = 'products/iphone_17_pm.png'
        updated = Product.objects.update(image=image_path, image_2='', image_3='')

        self.stdout.write(self.style.SUCCESS(f'Updated {updated} products with single image.'))
