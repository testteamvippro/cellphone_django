"""
Product service handling product-related business logic
"""
from typing import List, Optional
from store.models import Product, Category
from store.repositories.product import ProductRepository


class ProductService:
    """
    Service for product operations.
    Handles product queries, filtering, and display logic.
    """

    def __init__(self):
        self.repo = ProductRepository()

    def get_product_detail(self, slug: str) -> Optional[Product]:
        """
        Get product by slug with full details.
        Increments view count.
        """
        try:
            product = Product.objects.get(slug=slug)
            self.repo.increment_views(product)
            return product
        except Product.DoesNotExist:
            return None

    def get_available_product(self, product_id: int) -> Optional[Product]:
        """
        Get available product by ID.
        """
        return self.repo.get_available_by_id(product_id)

    def get_homepage_products(self) -> dict:
        """
        Get all products needed for homepage display.
        Returns dict with different product categories.
        """
        return {
            'flash_sale': self.repo.get_flash_sale_products(limit=8),
            'new': self.repo.get_new_products(limit=8),
            'featured': self.repo.get_available_products()[:12],
        }

    def get_products_by_category(self, category_slug: str, brand_slug: Optional[str] = None,
                                 search_query: Optional[str] = None, sort_by: str = '-created_at') -> tuple:
        """
        Get filtered products with metadata.
        Returns (products, category, brands)
        """
        if search_query:
            products = self.repo.search(search_query)
        else:
            products = self.repo.get_by_category(category_slug)

        if brand_slug:
            products = products.filter(brand__slug=brand_slug)

        products = self.repo.get_sorted_products(products, sort_by)

        try:
            category = Category.objects.get(slug=category_slug) if category_slug else None
        except Category.DoesNotExist:
            category = None

        return products, category

    def get_related_products(self, product: Product, limit: int = 4) -> List[Product]:
        """
        Get products related to given product.
        """
        return list(self.repo.get_related_products(product, limit))

    def get_product_with_details(self, product_id: int) -> Optional[dict]:
        """
        Get product with all related information.
        Returns dict with product, related products, colors, specs.
        """
        product = self.get_product_detail(product_id) if isinstance(product_id, int) else \
                  self.get_product_detail(str(product_id))
        
        if not product:
            return None

        return {
            'product': product,
            'related_products': self.get_related_products(product),
            'colors': list(product.colors.all()),
            'specs': list(product.specs.all()),
            'discount_percentage': product.discount_percentage,
        }

    def search_products(self, query: str, sort_by: str = '-created_at') -> List[Product]:
        """
        Search products and return sorted results.
        """
        results = self.repo.search(query)
        return list(self.repo.get_sorted_products(results, sort_by))

    def get_products_by_brand(self, brand_slug: str) -> List[Product]:
        """
        Get all products from a brand.
        """
        return list(self.repo.get_by_brand(brand_slug))
