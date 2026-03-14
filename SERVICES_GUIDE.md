# Service Layer Usage Guide

## Quick Start

### 1. Cart Service

Located in `store/services/cart.py`

```python
from store.services.cart import CartService

cart_service = CartService()

# Get or create cart
cart = cart_service.get_or_create_cart(user=request.user)  # For authenticated user
cart = cart_service.get_or_create_cart(session_key=session_key)  # For guest

# Add to cart with validation
try:
    cart_item = cart_service.add_to_cart(cart, product, quantity=2)
except InsufficientStockException as e:
    # Handle insufficient stock
    pass
except InvalidQuantityException as e:
    # Handle invalid quantity
    pass

# Get cart totals
totals = cart_service.get_cart_totals(cart)
# Returns: {
#     'total_items': 5,
#     'total_price': Decimal('500000'),
#     'item_count': 3,
#     'items': [CartItem, ...]
# }

# Update item quantity
cart_item = cart_service.update_cart_item(cart, item_id=1, quantity=3)

# Increase/Decrease quantity
cart_service.increase_quantity(cart, item_id=1)
cart_service.decrease_quantity(cart, item_id=1)

# Remove from cart
cart_service.remove_from_cart(cart, item_id=1)

# Clear entire cart
count = cart_service.clear_cart(cart)

# Validate cart before checkout
is_valid, message = cart_service.validate_cart_for_checkout(cart)
```

### 2. Product Service

Located in `store/services/product.py`

```python
from store.services.product import ProductService

product_service = ProductService()

# Get product for detail page (increments views)
product = product_service.get_product_detail(slug='iphone-15')

# Get available product by ID
product = product_service.get_available_product(product_id=1)

# Get homepage products
homepage = product_service.get_homepage_products()
# Returns: {
#     'flash_sale': [Product, ...],
#     'new': [Product, ...],
#     'featured': [Product, ...]
# }

# Get products by category with filtering
products, category = product_service.get_products_by_category(
    category_slug='phones',
    brand_slug='samsung',
    search_query='Galaxy',
    sort_by='-price'
)

# Get related products
related = product_service.get_related_products(product, limit=4)

# Search products
results = product_service.search_products(query='iPhone', sort_by='-rating')

# Get products by brand
products = product_service.get_products_by_brand(brand_slug='apple')

# Get product with full details
details = product_service.get_product_with_details(product_id=1)
# Returns: {
#     'product': Product,
#     'related_products': [Product, ...],
#     'colors': [ProductColor, ...],
#     'specs': [ProductSpec, ...],
#     'discount_percentage': 20
# }
```

### 3. Order Service

Located in `store/services/order.py`

```python
from store.services.order import OrderService

order_service = OrderService()

# Create order from cart
order_data = {
    'full_name': 'John Doe',
    'email': 'john@example.com',
    'phone': '0123456789',
    'address': '123 Main St',
    'city': 'Ho Chi Minh',
    'postal_code': '70000'
}

try:
    order = order_service.create_order(user, cart, order_data)
except EmptyCartException:
    # Handle empty cart
    pass

# Get order details
order = order_service.get_order_details(order_id=1)

# Get user's orders
orders = order_service.get_user_orders(user)

# Get order by number
order = order_service.get_order_by_number('ORD-ABC12345', user=user)

# Get order items
items = order_service.get_order_items(order)

# Update order status
order = order_service.update_order_status(order_id=1, new_status='shipped')

# Check if order can be cancelled
can_cancel = order_service.can_cancel_order(order)

# Cancel order
order_service.cancel_order(order)

# Get all pending orders (admin)
pending = order_service.get_pending_orders()

# Get orders by status
shipped = order_service.get_orders_by_status('shipped')

# Calculate order total
total = order_service.calculate_order_total(order)
```

### 4. Wishlist Service

Located in `store/services/wishlist.py`

```python
from store.services.wishlist import WishlistService

wishlist_service = WishlistService()

# Add to wishlist
item, created = wishlist_service.add_to_wishlist(
    product,
    user=request.user  # For authenticated user
    # OR
    # session_key=session_key  # For guest
)

# Remove from wishlist
removed = wishlist_service.remove_from_wishlist(product, user=user)

# Toggle wishlist (add if not present, remove if present)
result = wishlist_service.toggle_wishlist(product, user=user)
# Returns: {
#     'in_wishlist': True,
#     'added': True,
#     'message': 'Added to wishlist'
# }

# Check if in wishlist
in_wishlist = wishlist_service.is_in_wishlist(product, user=user)

# Get user's wishlist
wishlist_items = wishlist_service.get_user_wishlist(user)

# Get session wishlist
session_items = wishlist_service.get_session_wishlist(session_key)

# Get wishlist products
products = wishlist_service.get_wishlist_products(user=user)
```

### 5. News Service

Located in `store/services/news.py`

```python
from store.services.news import NewsService

news_service = NewsService()

# Get article by slug (increments views)
article = news_service.get_article(slug='iphone-15-review')

# Get all articles
articles = news_service.get_all_articles(limit=10)

# Get articles by category
category_articles = news_service.get_articles_by_category('reviews')

# Get related articles
related = news_service.get_related_articles(article, limit=3)

# Search articles
results = news_service.search_articles(query='battery')

# Get homepage news
homepage_news = news_service.get_homepage_news(limit=3)

# Get popular articles (by views)
popular = news_service.get_popular_articles(limit=5)
```

## Error Handling

### Cart Service Exceptions:

```python
from store.exceptions import (
    CartException,
    InvalidQuantityException,
    InsufficientStockException,
    EmptyCartException
)

try:
    cart_service.add_to_cart(cart, product, quantity=-1)
except InvalidQuantityException as e:
    print(f"Error: {e}")  # "Quantity must be greater than 0"

try:
    cart_service.add_to_cart(cart, product, quantity=1000)
except InsufficientStockException as e:
    print(f"Error: {e}")  # "Insufficient stock for 'Product Name'"

try:
    order_service.create_order(user, empty_cart, data)
except EmptyCartException as e:
    print(f"Error: {e}")  # "Cannot create order from empty cart"
```

## Using Helpers

Located in `store/utils/helpers.py`

### Price Calculator:

```python
from store.utils.helpers import PriceCalculator

# Calculate discount percentage
discount = PriceCalculator.calculate_discount_percentage(
    original_price=Decimal('100000'),
    current_price=Decimal('80000')
)  # Returns: 20

# Calculate discount amount
amount = PriceCalculator.calculate_discount_amount(
    Decimal('100000'),
    Decimal('80000')
)  # Returns: Decimal('20000')

# Apply discount
price = PriceCalculator.apply_discount(Decimal('100000'), 20)
# Returns: Decimal('80000')

# Calculate tax
tax = PriceCalculator.calculate_tax(Decimal('100000'), tax_rate=0.1)
# Returns: Decimal('10000')

# Format price
formatted = PriceCalculator.format_price(Decimal('1000000'), currency='₫')
# Returns: "1,000,000₫"
```

### Cart Calculator:

```python
from store.utils.helpers import CartCalculator

# Calculate subtotal
subtotal = CartCalculator.calculate_subtotal(cart_items)

# Calculate total items (sum of quantities)
count = CartCalculator.calculate_item_count(cart_items)

# Calculate unique products
unique = CartCalculator.calculate_unique_products(cart_items)

# Calculate total discount
discount = CartCalculator.calculate_discount_total(cart_items)

# Calculate average item price
avg = CartCalculator.calculate_average_item_price(cart_items)
```

### Product Helper:

```python
from store.utils.helpers import ProductHelper

# Check stock
in_stock = ProductHelper.is_in_stock(product, quantity=5)

# Get stock status
status = ProductHelper.get_stock_status(product)
# Returns: "In Stock", "Limited Stock", "Out of Stock", etc.

# Get discount badge
badge = ProductHelper.get_discount_badge(product)
# Returns: "Flash Sale", "-20%", or None

# Get all images
images = ProductHelper.get_all_images(product)

# Get primary image
image = ProductHelper.get_primary_image(product)
```

### Session Helper:

```python
from store.utils.helpers import SessionHelper

# Ensure session key exists
key = SessionHelper.ensure_session_key(request)

# Get user or session identifier
user, session_key = SessionHelper.get_user_identifier(request)
# If authenticated: returns (user, None)
# If not: returns (None, session_key)
```

### Validation Helper:

```python
from store.utils.helpers import ValidationHelper

# Validate quantity
valid = ValidationHelper.validate_quantity(5)  # True

# Validate email
valid = ValidationHelper.validate_email('user@example.com')  # True

# Validate phone
valid = ValidationHelper.validate_phone('0123456789')  # True

# Validate complete order data
is_valid, errors = ValidationHelper.validate_order_data({
    'full_name': 'John Doe',
    'email': 'john@example.com',
    'phone': '0123456789',
    'address': '123 Main St',
    'city': 'Ho Chi Minh',
    'postal_code': '70000'
})
```

## Using Custom Managers

In templates or views, you can use custom managers:

```python
from store.models import Product, Order

# Product queries
Product.objects.available()              # Available products
Product.objects.flash_sale()             # Flash sale products
Product.objects.in_stock()               # Products with stock
Product.objects.by_category('phones')    # By category
Product.objects.by_brand('samsung')      # By brand
Product.objects.expensive(threshold=Decimal('20000000'))
Product.objects.high_rated()             # Rating >= 4.0
Product.objects.popular()                # Sort by popularity
Product.objects.search('iPhone')         # Search

# Order queries
Order.objects.pending()                  # Pending orders
Order.objects.processing()               # Processing orders
Order.objects.shipped()                  # Shipped orders
Order.objects.delivered()                # Delivered orders
Order.objects.recent(days=30)            # Orders from last 30 days
Order.objects.high_value()               # Orders > threshold
```

## Using Discount Strategies

Located in `store/strategies/discount.py`

```python
from store.strategies.discount import (
    PercentageDiscountStrategy,
    BulkDiscountStrategy,
    FlashSaleDiscountStrategy,
    TieredDiscountStrategy,
    ChainedDiscountStrategy
)

# Simple percentage discount
strategy = PercentageDiscountStrategy(percentage=20)
price, reason = strategy.calculate_discount(product)

# Bulk discount (10% off if quantity >= 5)
strategy = BulkDiscountStrategy(min_quantity=5, percentage=10)
price, reason = strategy.calculate_discount(product, quantity=10)

# Tiered discount
strategy = TieredDiscountStrategy(tiers=[
    (1, 0),      # 0% discount for 1-5 items
    (6, 10),     # 10% discount for 6-10 items
    (11, 20),    # 20% discount for 11+ items
])
price, reason = strategy.calculate_discount(product, quantity=15)

# Chained discounts (apply multiple)
strategies = [
    PercentageDiscountStrategy(percentage=10),
    BulkDiscountStrategy(min_quantity=5, percentage=5),
]
combined = ChainedDiscountStrategy(strategies)
price, reason = combined.calculate_discount(product, quantity=6)
```

## Best Practices

1. **Always use services** in views, never directly access models
2. **Handle exceptions** appropriately with try-except blocks
3. **Validate data** using ValidationHelper before processing
4. **Use managers** for complex queries in services
5. **Cache expensive operations** when appropriate
6. **Log important operations** for debugging
7. **Write tests** for services and repositories
8. **Document** any custom exceptions in your code
