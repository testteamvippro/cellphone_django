"""
Custom managers for models to support complex queries.
Implements Manager Pattern for data access layer.
"""
from django.db.models import Manager, QuerySet, Q
from decimal import Decimal


class ProductQuerySet(QuerySet):
    """Custom QuerySet for Product model"""
    
    def available(self):
        """Filter only available products"""
        return self.filter(is_available=True)
    
    def flash_sale(self):
        """Filter only flash sale products"""
        return self.filter(is_flash_sale=True)
    
    def in_stock(self):
        """Filter products with stock > 0"""
        return self.filter(stock__gt=0)
    
    def by_category(self, slug):
        """Filter by category slug"""
        return self.filter(category__slug=slug)
    
    def by_brand(self, slug):
        """Filter by brand slug"""
        return self.filter(brand__slug=slug)
    
    def expensive(self, threshold=Decimal('10000000')):
        """Filter expensive products"""
        return self.filter(price__gte=threshold)
    
    def cheap(self, threshold=Decimal('5000000')):
        """Filter cheap products"""
        return self.filter(price__lte=threshold)
    
    def high_rated(self, rating=Decimal('4.0')):
        """Filter high-rated products"""
        return self.filter(rating__gte=rating)
    
    def popular(self):
        """Sort by views and reviews"""
        return self.order_by('-views_count', '-reviews_count')
    
    def search(self, query):
        """Search by name or description"""
        return self.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )


class ProductManager(Manager):
    """Custom manager for Product model"""
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def available(self):
        return self.get_queryset().available()
    
    def flash_sale(self):
        return self.get_queryset().flash_sale()
    
    def in_stock(self):
        return self.get_queryset().in_stock()
    
    def by_category(self, slug):
        return self.get_queryset().by_category(slug)
    
    def by_brand(self, slug):
        return self.get_queryset().by_brand(slug)
    
    def expensive(self, threshold=Decimal('10000000')):
        return self.get_queryset().expensive(threshold)
    
    def cheap(self, threshold=Decimal('5000000')):
        return self.get_queryset().cheap(threshold)
    
    def high_rated(self, rating=Decimal('4.0')):
        return self.get_queryset().high_rated(rating)
    
    def popular(self):
        return self.get_queryset().popular()
    
    def search(self, query):
        return self.get_queryset().search(query)


class OrderQuerySet(QuerySet):
    """Custom QuerySet for Order model"""
    
    def pending(self):
        """Filter pending orders"""
        return self.filter(status='pending')
    
    def processing(self):
        """Filter processing orders"""
        return self.filter(status='processing')
    
    def shipped(self):
        """Filter shipped orders"""
        return self.filter(status='shipped')
    
    def delivered(self):
        """Filter delivered orders"""
        return self.filter(status='delivered')
    
    def cancelled(self):
        """Filter cancelled orders"""
        return self.filter(status='cancelled')
    
    def recent(self, days=30):
        """Filter recent orders"""
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
    
    def high_value(self, threshold=Decimal('20000000')):
        """Filter high-value orders"""
        return self.filter(total_amount__gte=threshold)


class OrderManager(Manager):
    """Custom manager for Order model"""
    
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def processing(self):
        return self.get_queryset().processing()
    
    def shipped(self):
        return self.get_queryset().shipped()
    
    def delivered(self):
        return self.get_queryset().delivered()
    
    def cancelled(self):
        return self.get_queryset().cancelled()
    
    def recent(self, days=30):
        return self.get_queryset().recent(days)
    
    def high_value(self, threshold=Decimal('20000000')):
        return self.get_queryset().high_value(threshold)


class CartQuerySet(QuerySet):
    """Custom QuerySet for Cart model"""
    
    def with_items(self):
        """Filter carts with items"""
        return self.filter(items__isnull=False).distinct()
    
    def empty(self):
        """Filter empty carts"""
        return self.filter(items__isnull=True).distinct()
    
    def abandoned(self, days=7):
        """Filter abandoned carts"""
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(updated_at__lt=cutoff, items__isnull=False)
    
    def user_carts(self, user):
        """Filter carts for specific user"""
        return self.filter(user=user)


class CartManager(Manager):
    """Custom manager for Cart model"""
    
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)
    
    def with_items(self):
        return self.get_queryset().with_items()
    
    def empty(self):
        return self.get_queryset().empty()
    
    def abandoned(self, days=7):
        return self.get_queryset().abandoned(days)
    
    def user_carts(self, user):
        return self.get_queryset().user_carts(user)
