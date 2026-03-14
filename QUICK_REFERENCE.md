# Quick Reference Guide - OOP & Design Patterns

## 🗺️ Quick Navigation Map

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP REQUEST                          │
└─────────────────┬───────────────────────────────────────┘
                  │
          ┌─────────────────┐
          │  views.py       │  ← Light, only HTTP concerns
          │ (Refactored)    │
          └────────┬────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌────────────┐  ┌──────────┐
│services/│  │ utils/     │  │strategies│
│         │  │ helpers    │  │/discount │
└────┬────┘  └────────────┘  └──────────┘
     │
     ▼
┌─────────────────┐
│repositories/    │  ← Data access abstraction
│ (all repo)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│models.py        │  ← Database models
│managers.py      │
└────────┬────────┘
         │
         ▼
    DATABASE
```

## 📂 File Quick Links

### Services (Business Logic)
| File | Purpose | Key Classes |
|------|---------|------------|
| `services/cart.py` | Shopping cart operations | `CartService` |
| `services/product.py` | Product queries | `ProductService` |
| `services/order.py` | Order management | `OrderService` |
| `services/wishlist.py` | Wishlist operations | `WishlistService` |
| `services/news.py` | News articles | `NewsService` |

### Repositories (Data Access)
| File | Purpose | Key Classes |
|------|---------|------------|
| `repositories/base.py` | Generic CRUD | `BaseRepository` |
| `repositories/product.py` | Product queries | `ProductRepository` |
| `repositories/cart.py` | Cart data | `CartRepository` |
| `repositories/order.py` | Order data | `OrderRepository` |
| `repositories/wishlist.py` | Wishlist data | `WishlistRepository` |
| `repositories/news.py` | News data | `NewsArticleRepository` |

### Utilities & Others
| File | Purpose | Key Classes |
|------|---------|------------|
| `utils/helpers.py` | Helper utilities | `PriceCalculator`, `ValidationHelper` |
| `strategies/discount.py` | Discount strategies | `DiscountStrategy`, `BulkDiscountStrategy` |
| `managers.py` | Custom QuerySets | `ProductManager`, `OrderManager` |
| `exceptions/__init__.py` | Custom exceptions | `CartException`, `InsufficientStockException` |

## 🎯 Common Tasks - Where to Look

### Task: Display products on homepage
1. **View** (`views.py`): `home()` function
2. **Service** (`services/product.py`): `ProductService.get_homepage_products()`
3. **Repository** (`repositories/product.py`): `get_flash_sale_products()`, `get_new_products()`
4. **Database** (`models.py`): `Product` model

### Task: Add item to cart
1. **View** (`views.py`): `add_to_cart()` function
2. **Service** (`services/cart.py`): `CartService.add_to_cart()`
   - Validates quantity
   - Checks stock
   - Handles duplicates
3. **Repository** (`repositories/cart.py`): `CartItemRepository.get_item_in_cart()`
4. **Exception** (`exceptions/`): `InsufficientStockException`

### Task: Complete checkout
1. **View** (`views.py`): `checkout()` function
2. **Services**:
   - `CartService.validate_cart_for_checkout()`
   - `OrderService.create_order()`
   - `CartService.clear_cart()`
3. **Helpers** (`utils/helpers.py`): `ValidationHelper.validate_order_data()`
4. **Repository** (`repositories/order.py`): Create order and items

### Task: Filter products by category
1. **View** (`views.py`): `product_list()` function
2. **Service** (`services/product.py`): `ProductService.get_products_by_category()`
3. **Repository** (`repositories/product.py`): `ProductRepository.get_by_category()`

### Task: Apply discount to price
1. **Strategy** (`strategies/discount.py`): Choose strategy
   - `PercentageDiscountStrategy`
   - `BulkDiscountStrategy`
   - `TieredDiscountStrategy`
2. **Helper** (`utils/helpers.py`): `PriceCalculator`

## 🔍 Code Examples

### Using Services in Views
```python
from store.services.cart import CartService
from store.services.product import ProductService

# Initialize services
cart_service = CartService()
product_service = ProductService()

# Use in view
def my_view(request):
    cart = cart_service.get_or_create_cart(user, session_key)
    products = product_service.get_homepage_products()
```

### Using Repositories in Services
```python
from store.repositories.product import ProductRepository

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
    
    def get_products(self):
        return self.repo.get_available_products()
```

### Using Managers in Models
```python
from store.models import Product

# In a service or view
available = Product.objects.available()
flash_sales = Product.objects.flash_sale()
popular = Product.objects.popular()
```

### Using Helpers
```python
from store.utils.helpers import ValidationHelper, PriceCalculator

# Validate order data
is_valid, errors = ValidationHelper.validate_order_data(order_data)

# Calculate prices
discount = PriceCalculator.apply_discount(price, 20)
total_with_tax = PriceCalculator.calculate_total_with_tax(price)
```

### Using Strategies
```python
from store.strategies.discount import PercentageDiscountStrategy

strategy = PercentageDiscountStrategy(percentage=20)
discounted_price, reason = strategy.calculate_discount(product)
```

### Handling Exceptions
```python
from store.exceptions import InsufficientStockException

try:
    cart_service.add_to_cart(cart, product, quantity)
except InsufficientStockException as e:
    return JsonResponse({'error': str(e)}, status=400)
```

## 📋 Pattern Checklist

When adding new features, follow this checklist:

- [ ] **New data entity?**
  - [ ] Create model in `models.py`
  - [ ] Create manager in that model or `managers.py`
  - [ ] Create repository in `repositories/`

- [ ] **New business logic?**
  - [ ] Create service in `services/`
  - [ ] Use repository for data access
  - [ ] Use helpers for utilities
  - [ ] Define custom exceptions if needed

- [ ] **New view?**
  - [ ] Use services, not models directly
  - [ ] Use helpers for validation
  - [ ] Handle service exceptions
  - [ ] Keep view thin

- [ ] **New discount type?**
  - [ ] Create strategy in `strategies/discount.py`
  - [ ] Implement `calculate_discount()` method
  - [ ] Use in service

- [ ] **New utility function?**
  - [ ] Add to appropriate helper class in `utils/helpers.py`
  - [ ] Document with docstring
  - [ ] Consider reusability

## 🚀 Usage Patterns

### Pattern 1: Service → Repository → Model
```
CartService → CartRepository → CartItem Model → Database
```

### Pattern 2: Service → Helper
```
OrderService → ValidationHelper → Data Validation
OrderService → PriceCalculator → Price Calculations
```

### Pattern 3: Strategy Pattern
```
OrderService → DiscountStrategy → Calculate Price
```

### Pattern 4: Manager Pattern
```
View → ProductService → Product.objects.available() → Database
```

### Pattern 5: Exception Handling
```
CartService → raise InsufficientStockException
View → catch InsufficientStockException → Error Response
```

## 📊 Service Call Graph

```
home() view
├─ ProductService.get_homepage_products()
│  ├─ ProductRepository.get_flash_sale_products()
│  ├─ ProductRepository.get_new_products()
│  └─ ProductRepository.get_available_products()
├─ CartService.get_or_create_cart()
│  └─ CartRepository.get_or_create_for_user()
└─ NewsService.get_homepage_news()
   └─ NewsArticleRepository.get_all_articles()

product_list() view
├─ ProductService.get_products_by_category()
│  └─ ProductRepository.get_by_category()
└─ CartService.get_or_create_cart()

add_to_cart() view
├─ ProductService.get_available_product()
│  └─ ProductRepository.get_available_by_id()
├─ CartService.get_or_create_cart()
│  └─ CartRepository.get_or_create_for_user()
├─ CartService.add_to_cart()
│  └─ CartItemRepository.get_item_in_cart()
└─ Exception handling: InsufficientStockException

checkout() view
├─ CartService.validate_cart_for_checkout()
├─ ValidationHelper.validate_order_data()
├─ OrderService.create_order()
│  ├─ OrderRepository.create()
│  └─ OrderItemRepository.create_order_item()
└─ CartService.clear_cart()
   └─ CartItemRepository.clear_cart()
```

## 🔧 Configuration Reference

### Initialize Services in View
```python
# At top of views.py
from store.services.cart import CartService
from store.services.product import ProductService
from store.services.order import OrderService
from store.services.wishlist import WishlistService
from store.services.news import NewsService

cart_service = CartService()
product_service = ProductService()
order_service = OrderService()
wishlist_service = WishlistService()
news_service = NewsService()
```

### Import Helpers
```python
from store.utils.helpers import (
    SessionHelper,
    ValidationHelper,
    PriceCalculator,
    CartCalculator,
    ProductHelper
)
```

### Import Exceptions
```python
from store.exceptions import (
    CartException,
    InvalidQuantityException,
    InsufficientStockException,
    EmptyCartException,
    OrderException
)
```

## 📚 Documentation Reference

- **Architecture Details** → `ARCHITECTURE.md`
- **Service Usage Examples** → `SERVICES_GUIDE.md`
- **Repository Patterns** → `REPOSITORY_GUIDE.md`
- **Refactoring Summary** → `REFACTORING_SUMMARY.md` (this file)
- **Quick Reference** → This file

## 💡 Pro Tips

1. **Always initialize services at the top of views.py** - Makes testing easier
2. **Use ValidationHelper before processing user input** - Centralized validation
3. **Catch specific exceptions** - Not just `Exception`
4. **Use helpers for calculations** - Reusable and testable
5. **Document your custom managers** - Why this query is needed
6. **Use strategies for variations** - Don't hardcode logic
7. **Keep services focused** - One service per domain entity
8. **Write tests for services** - Easier than testing views
9. **Use type hints** - Helps with code completion
10. **Document complex logic** - Future you will thank present you

## 🎓 Learning Path

1. **Start with** `REFACTORING_SUMMARY.md` - Get overview
2. **Then read** `ARCHITECTURE.md` - Understand design
3. **Learn by example** `SERVICES_GUIDE.md` - See usage
4. **Deep dive** `REPOSITORY_GUIDE.md` - Understand data layer
5. **Explore the code** - Navigate from views to services to repositories
6. **Start adding features** - Use patterns as guide
7. **Refer to quick ref** - When you forget something

## ✨ Key Takeaways

- ✅ Views are now **thin and clean**
- ✅ Business logic is in **services**
- ✅ Data access is in **repositories**
- ✅ Utilities are in **helpers**
- ✅ Variations are in **strategies**
- ✅ Errors are **custom exceptions**
- ✅ Queries are **managers**
- ✅ Code is **reusable**
- ✅ Code is **testable**
- ✅ Code is **maintainable**

---

**Last Updated**: March 2026
**Refactoring Status**: ✅ Complete
**Documentation**: ✅ Complete
**Ready for Production**: ✅ Yes
