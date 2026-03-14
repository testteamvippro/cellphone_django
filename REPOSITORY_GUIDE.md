# Repository Pattern Guide

## Overview

Repositories provide an abstraction layer for data access. They centralize all database queries and make it easy to change the data source without affecting the rest of the application.

## Base Repository

Located in `store/repositories/base.py`

All repositories inherit from `BaseRepository` which provides generic CRUD operations:

```python
from store.repositories.base import BaseRepository
from store.models import MyModel

# Create a custom repository
class MyRepository(BaseRepository):
    def __init__(self):
        super().__init__(MyModel)

# Usage
repo = MyRepository()

# Get by ID
obj = repo.get_by_id(1)

# Get all
all_objs = repo.get_all()

# Filter
results = repo.filter(name='John')

# Get single object
obj = repo.get_single(email='john@example.com')

# Create
obj = repo.create(name='John', email='john@example.com')

# Get or create
obj, created = repo.get_or_create(
    defaults={'email': 'john@example.com'},
    name='John'
)

# Update
obj = repo.update(obj_id=1, name='Jane', email='jane@example.com')

# Delete
deleted = repo.delete(obj_id=1)

# Check existence
exists = repo.exists(email='john@example.com')

# Count
count = repo.count(status='active')

# Bulk operations
objects = [obj1, obj2, obj3]
repo.bulk_create(objects)
repo.bulk_update(objects, fields=['name', 'email'])
```

## Product Repository

Located in `store/repositories/product.py`

Specialized queries for products:

```python
from store.repositories.product import ProductRepository

product_repo = ProductRepository()

# Get available products
available = product_repo.get_available_products()

# Get flash sale products
flash_sales = product_repo.get_flash_sale_products(limit=8)

# Get newest products
new_products = product_repo.get_new_products(limit=8)

# Filter by category
phone_products = product_repo.get_by_category('phones', limit=20)

# Filter by brand
samsung_products = product_repo.get_by_brand('samsung')

# By category object
category = Category.objects.get(slug='phones')
products = product_repo.get_by_category_object(category, limit=10)

# Search products
results = product_repo.search('Galaxy S24')

# Get related products (same category)
related = product_repo.get_related_products(product, limit=4)

# Increment views
product_repo.increment_views(product)

# Get category with brands
products, brands = product_repo.get_products_by_category_with_brands('phones')

# Sort products
sorted_products = product_repo.get_sorted_products(queryset, sort_by='-price')

# Get available by ID
product = product_repo.get_available_by_id(product_id=1)
```

## Cart Repository

Located in `store/repositories/cart.py`

### CartRepository

```python
from store.repositories.cart import CartRepository

cart_repo = CartRepository()

# Get or create for user
cart = cart_repo.get_or_create_for_user(user)

# Get or create for session
cart = cart_repo.get_or_create_for_session(session_key)

# Get user cart (returns None if not found)
cart = cart_repo.get_user_cart(user)

# Get session cart
cart = cart_repo.get_session_cart(session_key)
```

### CartItemRepository

```python
from store.repositories.cart import CartItemRepository

item_repo = CartItemRepository()

# Get specific cart item
item = item_repo.get_item_in_cart(cart, product_id)

# Get all items in cart
items = item_repo.get_cart_items(cart)

# Remove from cart
removed = item_repo.remove_from_cart(cart, product_id)

# Clear entire cart
count = item_repo.clear_cart(cart)  # Returns number deleted
```

## Order Repository

Located in `store/repositories/order.py`

### OrderRepository

```python
from store.repositories.order import OrderRepository

order_repo = OrderRepository()

# Get user's orders
orders = order_repo.get_user_orders(user)

# Get by order number
order = order_repo.get_by_order_number('ORD-ABC12345')

# Get user's order by number
order = order_repo.get_user_order_by_number(user, 'ORD-ABC12345')

# Get orders by status
pending = order_repo.get_orders_by_status('pending')
shipped = order_repo.get_orders_by_status('shipped')

# Get all pending orders
pending_orders = order_repo.get_pending_orders()

# Update order status
order = order_repo.update_order_status(order_id=1, status='shipped')
```

### OrderItemRepository

```python
from store.repositories.order import OrderItemRepository

item_repo = OrderItemRepository()

# Get all items in order
items = item_repo.get_order_items(order)

# Create order item
item = item_repo.create_order_item(
    order=order,
    product=product,
    quantity=2,
    price=product.price
)
```

## Wishlist Repository

Located in `store/repositories/wishlist.py`

```python
from store.repositories.wishlist import WishlistRepository

wishlist_repo = WishlistRepository()

# Get user's wishlist
items = wishlist_repo.get_user_wishlist(user)

# Get session wishlist
items = wishlist_repo.get_session_wishlist(session_key)

# Check if in user wishlist
in_wishlist = wishlist_repo.is_in_user_wishlist(user, product)

# Check if in session wishlist
in_wishlist = wishlist_repo.is_in_session_wishlist(session_key, product)

# Add to user wishlist
item = wishlist_repo.add_to_wishlist(user, product)

# Add to session wishlist
item = wishlist_repo.add_session_to_wishlist(session_key, product)

# Remove from user wishlist
removed = wishlist_repo.remove_from_wishlist(user, product)

# Remove from session wishlist
removed = wishlist_repo.remove_session_from_wishlist(session_key, product)
```

## News Article Repository

Located in `store/repositories/news.py`

```python
from store.repositories.news import NewsArticleRepository

news_repo = NewsArticleRepository()

# Get all articles
articles = news_repo.get_all_articles(limit=10)

# Get by slug
article = news_repo.get_by_slug('iphone-15-review')

# Get by category
tech_news = news_repo.get_by_category('technology')

# Get related articles (same category, exclude current)
related = news_repo.get_related_articles(article, limit=3)

# Increment views
news_repo.increment_views(article)

# Search articles
results = news_repo.search('battery life')
```

## Pattern: Using Repositories in Services

The proper way to use repositories is in your services layer:

```python
from store.repositories.product import ProductRepository
from store.repositories.cart import CartRepository

class MyService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.cart_repo = CartRepository()
    
    def get_cart_with_available_products(self, cart):
        """Example: Get cart items ensuring all products are available"""
        items = self.cart_repo.cart_item_repo.get_cart_items(cart)
        available_items = []
        
        for item in items:
            product = self.product_repo.get_available_by_id(item.product_id)
            if product:
                available_items.append(item)
        
        return available_items
```

## Best Practices

1. **Use repositories only in services**, not in views or models
2. **Create specialized repositories** for each data entity
3. **Add domain-specific methods** to repositories for common queries
4. **Keep repositories focused** on data access, not business logic
5. **Return domain objects**, not querysets (when possible)
6. **Test repositories independently** with mock data
7. **Use consistent naming** for repository methods
8. **Document complex queries** in repository methods

## Common Repository Patterns

### Pattern 1: Get or Create with Defaults
```python
item, created = repo.get_or_create(
    defaults={'status': 'active'},
    user=user,
    product=product
)

if created:
    print("New item created")
else:
    print("Item already existed")
```

### Pattern 2: Conditional Filtering
```python
# Start with base query
query = repo.filter(is_active=True)

# Add optional filters
if category:
    query = query.filter(category=category)

if brand:
    query = query.filter(brand=brand)

# Return filtered results
results = list(query)
```

### Pattern 3: Aggregation
```python
from django.db.models import Count, Sum

# Count by category
counts = Product.objects.values('category').annotate(
    count=Count('id')
)

# Sum total prices
totals = Order.objects.values('user').annotate(
    total=Sum('total_amount')
)
```

### Pattern 4: Pagination
```python
from django.core.paginator import Paginator

products = repo.get_available_products()
paginator = Paginator(products, 20)

page = paginator.get_page(request.GET.get('page', 1))
```

## Error Handling in Repositories

```python
from django.core.exceptions import ObjectDoesNotExist

class SafeRepository(BaseRepository):
    def get_by_id_safe(self, obj_id):
        """Returns None instead of raising exception"""
        try:
            return self.get_by_id(obj_id)
        except ObjectDoesNotExist:
            return None
    
    def create_if_not_exists(self, **kwargs):
        """Create only if doesn't exist"""
        existing = self.get_single(**kwargs)
        if existing:
            return existing, False
        return self.create(**kwargs), True
```

## Performance Considerations

1. **Use select_related()** for ForeignKey relationships
2. **Use prefetch_related()** for reverse relationships
3. **Use only()** to limit fields retrieved
4. **Use values()** for simple data needs
5. **Use exists()** instead of checking count
6. **Use bulk operations** for multiple inserts/updates

Example:
```python
class OptimizedProductRepository(ProductRepository):
    def get_with_relations(self):
        """Get products with all related data optimized"""
        return self.get_all().select_related(
            'category', 'brand'
        ).prefetch_related(
            'colors', 'specs'
        )
```
