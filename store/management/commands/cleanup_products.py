"""
Management command to remove non-core products (TVs)
Keep only: Phones, Watches, Tablets, Laptops
"""
from django.core.management.base import BaseCommand
from store.models import Product, Category

class Command(BaseCommand):
    help = 'Remove TV products, keep only core products'

    def handle(self, *args, **options):
        self.stdout.write('Removing non-core products...\n')
        
        # Get TV category
        try:
            tv_category = Category.objects.get(slug='tv')
            tv_products = Product.objects.filter(category=tv_category)
            count = tv_products.count()
            
            self.stdout.write(f'Found {count} TV products')
            self.stdout.write('Deleting TV products...')
            
            tv_products.delete()
            
            self.stdout.write(self.style.SUCCESS(f'Deleted {count} TV products'))
            
        except Category.DoesNotExist:
            self.stdout.write(self.style.WARNING('TV category not found'))
        
        # Show remaining categories
        self.stdout.write('\nCore product categories:')
        for cat in Category.objects.all():
            count = Product.objects.filter(category=cat).count()
            if count > 0:
                self.stdout.write(f'  - {cat.name}: {count} products')
        
        self.stdout.write(self.style.SUCCESS('\nDone! Website now focuses on core products only.'))
