"""
Product repository for data access layer
"""
from django.db.models import Q, QuerySet
from store.models import Product, Category, Brand
from store.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    """Repository for Product model with specialized queries"""

    def __init__(self):
        super().__init__(Product)

    def get_available_products(self) -> QuerySet:
        """Get all available products"""
        return self.filter(is_available=True)

    def get_flash_sale_products(self, limit: int = 8) -> QuerySet:
        """Get flash sale products"""
        return self.filter(is_flash_sale=True, is_available=True)[:limit]

    def get_new_products(self, limit: int = 8) -> QuerySet:
        """Get newest products"""
        return self.filter(is_available=True).order_by('-created_at')[:limit]

    def get_by_category(self, category_slug: str, limit: int = None) -> QuerySet:
        """Get products by category slug"""
        query = self.filter(category__slug=category_slug, is_available=True)
        if limit:
            query = query[:limit]
        return query

    def get_by_brand(self, brand_slug: str) -> QuerySet:
        """Get products by brand slug"""
        return self.filter(brand__slug=brand_slug, is_available=True)

    def get_by_category_object(self, category: Category, limit: int = None) -> QuerySet:
        """Get products by category object"""
        query = self.filter(category=category, is_available=True)
        if limit:
            query = query[:limit]
        return query

    def search(self, query: str) -> QuerySet:
        """Search products by name or description"""
        return self.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            is_available=True
        )

    def get_related_products(self, product: Product, limit: int = 4) -> QuerySet:
        """Get related products from same category"""
        return self.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product.id)[:limit]

    def increment_views(self, product: Product) -> None:
        """Increment product views count"""
        product.views_count += 1
        product.save(update_fields=['views_count'])

    def get_products_by_category_with_brands(self, category_slug: str) -> tuple:
        """Get products with available brands for category"""
        category = self.get_single(slug=category_slug)
        if not category:
            return None, None

        products = self.get_by_category(category_slug)
        brands = Brand.objects.filter(products__category=category).distinct()
        return products, brands

    def get_sorted_products(self, queryset: QuerySet, sort_by: str = '-created_at') -> QuerySet:
        """Sort products by field"""
        valid_sorts = [
            'created_at', '-created_at',
            'price', '-price',
            'rating', '-rating',
            'views_count', '-views_count'
        ]
        if sort_by in valid_sorts:
            return queryset.order_by(sort_by)
        return queryset.order_by('-created_at')

    def get_available_by_id(self, product_id: int) -> Product:
        """Get available product by ID"""
        return self.get_single(id=product_id, is_available=True)
