# Django E-Commerce Refactoring - Architecture & Design Patterns

## Overview

This project has been refactored to follow **Object-Oriented Programming (OOP)** principles and implement industry-standard **design patterns**. The code is now organized into distinct layers with clear separation of concerns.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         Views (Request Handlers)        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Services (Business Logic)          │
│  - CartService                          │
│  - ProductService                       │
│  - OrderService                         │
│  - WishlistService                      │
│  - NewsService                          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│   Repositories (Data Access Layer)      │
│  - ProductRepository                    │
│  - CartRepository                       │
│  - OrderRepository                      │
│  - WishlistRepository                   │
│  - NewsRepository                       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Models & Managers (Database)       │
└─────────────────────────────────────────┘
```

## Design Patterns Implemented

### 1. **Service Layer Pattern**
- **Location**: `store/services/`
- **Purpose**: Encapsulates business logic separate from views
- **Classes**:
  - `CartService`: Cart operations with validation
  - `ProductService`: Product queries and filtering
  - `OrderService`: Order creation and management
  - `WishlistService`: Wishlist operations
  - `NewsService`: News article retrieval

**Benefits**:
- Easier to test
- Reusable business logic
- Clear responsibility separation
- Simplified views

### 2. **Repository Pattern**
- **Location**: `store/repositories/`
- **Purpose**: Abstract database access layer
- **Classes**:
  - `BaseRepository`: Generic CRUD operations
  - `ProductRepository`: Product-specific queries
  - `CartRepository`: Cart data access
  - `OrderRepository`: Order data access
  - `WishlistRepository`: Wishlist data access
  - `NewsArticleRepository`: News data access

**Benefits**:
- Database queries centralized
- Easy to swap database implementations
- Simpler view and service code
- Consistent query patterns

**Example Usage**:
```python
# In services
product_repo = ProductRepository()
available_products = product_repo.get_available_products()
flash_sales = product_repo.get_flash_sale_products(limit=8)
```

### 3. **Strategy Pattern**
- **Location**: `store/strategies/discount.py`
- **Purpose**: Different discount calculation strategies
- **Classes**:
  - `DiscountStrategy`: Abstract base class
  - `NoDiscountStrategy`: No discount
  - `PercentageDiscountStrategy`: Percentage-based discount
  - `BulkDiscountStrategy`: Quantity-based discount
  - `FlashSaleDiscountStrategy`: Flash sale discount
  - `TieredDiscountStrategy`: Tiered discount by quantity
  - `ChainedDiscountStrategy`: Multiple strategies combined

**Example Usage**:
```python
# Create different discount strategies
bulk_discount = BulkDiscountStrategy(min_quantity=10, percentage=15)
flash_discount = FlashSaleDiscountStrategy(percentage=20)

# Use strategy
price, reason = bulk_discount.calculate_discount(product, quantity=15)
```

### 4. **Factory Pattern**
- **Implementation**: In `OrderService.create_order()`
- **Purpose**: Complex object creation (Order with items)
- **Benefits**:
  - Encapsulates complex creation logic
  - Single place to manage order creation
  - Easy validation before creation

**Example**:
```python
# Factory method creates complete order with items
order = order_service.create_order(user, cart, order_data)
```

### 5. **Manager Pattern (Django)**
- **Location**: `store/managers.py`
- **Purpose**: Custom QuerySet methods for common queries
- **Classes**:
  - `ProductManager`: Product-specific queries
  - `OrderManager`: Order-specific queries
  - `CartManager`: Cart-specific queries

**Example Usage**:
```python
# Use in models
Product.objects.available()          # Available products
Product.objects.flash_sale()         # Flash sales
Product.objects.high_rated()         # High-rated products
Product.objects.search("iPhone")     # Search products

Order.objects.pending()              # Pending orders
Order.objects.recent(days=30)        # Recent orders
Order.objects.high_value()           # High-value orders
```

### 6. **Helper/Utility Classes**
- **Location**: `store/utils/helpers.py`
- **Purpose**: Reusable utility functions
- **Classes**:
  - `PriceCalculator`: Price-related calculations
  - `CartCalculator`: Cart calculations
  - `ProductHelper`: Product utilities
  - `SessionHelper`: Session management
  - `ValidationHelper`: Data validation

**Example Usage**:
```python
from store.utils.helpers import PriceCalculator, ValidationHelper

# Price calculations
discount = PriceCalculator.calculate_discount_percentage(100, 80)
total_with_tax = PriceCalculator.calculate_total_with_tax(price, tax_rate=0.1)

# Validation
is_valid, errors = ValidationHelper.validate_order_data(order_data)
```

### 7. **Custom Exception Handling**
- **Location**: `store/exceptions/__init__.py`
- **Purpose**: Domain-specific exceptions
- **Classes**:
  - `StoreException`: Base exception
  - `CartException`: Cart-related errors
  - `ProductException`: Product-related errors
  - `OrderException`: Order-related errors
  - `InsufficientStockException`: Stock issues
  - `InvalidQuantityException`: Quantity validation
  - `EmptyCartException`: Empty cart operations

**Example Usage**:
```python
try:
    cart_service.add_to_cart(cart, product, quantity)
except InsufficientStockException as e:
    return JsonResponse({'error': str(e)}, status=400)
except InvalidQuantityException as e:
    return JsonResponse({'error': str(e)}, status=400)
```

## Refactored Views Example

### Before (Procedural):
```python
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect('store:cart_view')
    
    if request.method == 'POST':
        # Mixed concerns - validation, creation, clearing
        order = Order.objects.create(...)
        for cart_item in cart.items.all():
            OrderItem.objects.create(...)
        cart.items.all().delete()
        return redirect(...)
```

### After (Service Layer):
```python
@login_required
def checkout(request):
    cart = cart_service.get_or_create_cart(user, session_key)
    is_valid, message = cart_service.validate_cart_for_checkout(cart)
    
    if not is_valid:
        messages.error(request, message)
        return redirect('store:cart_view')
    
    if request.method == 'POST':
        try:
            order_data = request.POST.dict()
            is_valid, errors = ValidationHelper.validate_order_data(order_data)
            
            if not is_valid:
                for error in errors:
                    messages.error(request, error)
                return render(...)
            
            order = order_service.create_order(request.user, cart, order_data)
            cart_service.clear_cart(cart)
            
            return redirect('store:order_success', order_number=order.order_number)
        except OrderException as e:
            messages.error(request, str(e))
            return redirect('store:cart_view')
```

## Key Benefits of This Refactoring

### 1. **Separation of Concerns**
- Views: Handle HTTP requests/responses
- Services: Business logic
- Repositories: Database access
- Models: Data structure

### 2. **Reusability**
- Services can be used in multiple views
- Repositories used by multiple services
- Helpers used across the application

### 3. **Testability**
- Each layer can be tested independently
- Mock repositories easily
- Test services in isolation

### 4. **Maintainability**
- Clear code organization
- Easy to locate functionality
- Reduced code duplication

### 5. **Scalability**
- Easy to add new features
- Database layer abstraction
- Strategy pattern allows new features without modifying existing code

### 6. **Error Handling**
- Custom exceptions for specific errors
- Better error messages
- Consistent error handling

## Dependency Injection Pattern (Optional but Recommended)

For even better code organization, services could be instantiated via dependency injection:

```python
# In views
class CheckoutView(View):
    def __init__(self, 
                 cart_service: CartService,
                 order_service: OrderService):
        self.cart_service = cart_service
        self.order_service = order_service
    
    def post(self, request):
        # Use injected services
        ...
```

## Best Practices

1. **Always use services in views**, not models directly
2. **Always use repositories in services**, not models directly
3. **Use custom managers** for complex queries
4. **Use validation helpers** before processing data
5. **Use exceptions** for error handling, not return values
6. **Keep views thin** - most logic should be in services
7. **Use strategy pattern** for different implementations

## File Structure

```
store/
├── models.py           # Data models
├── managers.py         # Custom QuerySet managers
├── views.py            # HTTP request handlers (refactored)
├── urls.py             # URL routing
├── admin.py            # Django admin
├── context_processors.py # Template context (refactored)
│
├── services/           # Business logic layer
│   ├── __init__.py
│   ├── cart.py         # Cart operations
│   ├── product.py      # Product operations
│   ├── order.py        # Order operations
│   ├── wishlist.py     # Wishlist operations
│   └── news.py         # News operations
│
├── repositories/       # Data access layer
│   ├── __init__.py
│   ├── base.py         # Base repository class
│   ├── product.py      # Product repository
│   ├── cart.py         # Cart repository
│   ├── order.py        # Order repository
│   ├── wishlist.py     # Wishlist repository
│   └── news.py         # News repository
│
├── strategies/         # Strategy pattern implementations
│   ├── __init__.py
│   └── discount.py     # Discount strategies
│
├── utils/              # Utility classes
│   ├── __init__.py
│   └── helpers.py      # Helper utilities
│
├── exceptions/         # Custom exceptions
│   └── __init__.py
│
└── migrations/         # Database migrations
```

## Next Steps / Future Improvements

1. **Add Caching Layer**: Implement caching for frequently accessed data
2. **Add Logging**: Implement comprehensive logging
3. **Add Notifications**: Order/payment notifications
4. **Add Payment Integration**: Payment gateway integration
5. **Add API Layer**: RESTful API using Django REST Framework
6. **Add Admin Dashboards**: Analytics and reporting
7. **Add Celery Tasks**: Async operations for email, notifications
8. **Add Unit Tests**: Comprehensive test coverage
9. **Add Integration Tests**: Test service interactions
10. **Add API Documentation**: API docs with Swagger/OpenAPI
