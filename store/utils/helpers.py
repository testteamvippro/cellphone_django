"""
Utility classes for common operations
"""
from decimal import Decimal
from typing import Optional
from store.models import Product


class PriceCalculator:
    """
    Utility class for price-related calculations.
    Centralizes pricing logic.
    """

    @staticmethod
    def calculate_discount_percentage(original_price: Decimal, current_price: Decimal) -> int:
        """Calculate discount percentage"""
        if original_price and original_price > current_price:
            return int(((original_price - current_price) / original_price) * 100)
        return 0

    @staticmethod
    def calculate_discount_amount(original_price: Decimal, current_price: Decimal) -> Decimal:
        """Calculate discount amount"""
        return original_price - current_price if original_price > current_price else Decimal(0)

    @staticmethod
    def apply_discount(price: Decimal, discount_percentage: float) -> Decimal:
        """Apply percentage discount to price"""
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount percentage must be between 0-100")
        discount = price * Decimal(discount_percentage) / Decimal(100)
        return price - discount

    @staticmethod
    def calculate_tax(price: Decimal, tax_rate: float = 0.1) -> Decimal:
        """Calculate tax amount"""
        return price * Decimal(tax_rate)

    @staticmethod
    def calculate_total_with_tax(price: Decimal, tax_rate: float = 0.1) -> Decimal:
        """Calculate total price including tax"""
        tax = PriceCalculator.calculate_tax(price, tax_rate)
        return price + tax

    @staticmethod
    def format_price(price: Decimal, currency: str = "₫") -> str:
        """Format price for display"""
        return f"{int(price):,}{currency}"


class CartCalculator:
    """
    Utility class for cart-related calculations.
    """

    @staticmethod
    def calculate_subtotal(cart_items: list) -> Decimal:
        """Calculate cart subtotal"""
        return sum(item.subtotal for item in cart_items)

    @staticmethod
    def calculate_item_count(cart_items: list) -> int:
        """Calculate total number of items in cart"""
        return sum(item.quantity for item in cart_items)

    @staticmethod
    def calculate_unique_products(cart_items: list) -> int:
        """Calculate number of unique products in cart"""
        return len(cart_items)

    @staticmethod
    def calculate_discount_total(cart_items: list, original_items: Optional[list] = None) -> Decimal:
        """Calculate total discount amount for cart"""
        total_discount = Decimal(0)
        
        for item in cart_items:
            if item.product.original_price and item.product.original_price > item.product.price:
                discount_per_item = item.product.original_price - item.product.price
                total_discount += discount_per_item * item.quantity
        
        return total_discount

    @staticmethod
    def calculate_average_item_price(cart_items: list) -> Decimal:
        """Calculate average price per item"""
        if not cart_items:
            return Decimal(0)
        
        subtotal = CartCalculator.calculate_subtotal(cart_items)
        item_count = CartCalculator.calculate_item_count(cart_items)
        
        return subtotal / item_count if item_count > 0 else Decimal(0)


class ProductHelper:
    """
    Helper class for product-related utilities.
    """

    @staticmethod
    def is_in_stock(product: Product, quantity: int = 1) -> bool:
        """Check if product has sufficient stock"""
        return product.stock >= quantity and product.is_available

    @staticmethod
    def get_stock_status(product: Product) -> str:
        """Get human-readable stock status"""
        if not product.is_available:
            return "Out of Stock"
        elif product.stock == 0:
            return "Out of Stock"
        elif product.stock < 5:
            return "Only a few left!"
        elif product.stock < 20:
            return "Limited Stock"
        else:
            return "In Stock"

    @staticmethod
    def get_discount_badge(product: Product) -> Optional[str]:
        """Get discount badge text if applicable"""
        if product.is_flash_sale:
            return "Flash Sale"
        
        if product.discount_percentage > 0:
            return f"-{product.discount_percentage}%"
        
        if product.promotion_text:
            return product.promotion_text
        
        return None

    @staticmethod
    def get_images(product: Product) -> list:
        """Get all product images"""
        images = [product.image]
        if product.image_2:
            images.append(product.image_2)
        if product.image_3:
            images.append(product.image_3)
        return images

    @staticmethod
    def get_primary_image(product: Product):
        """Get primary product image"""
        return product.image

    @staticmethod
    def get_all_images(product: Product) -> list:
        """Get all product images as list"""
        return ProductHelper.get_images(product)


class SessionHelper:
    """
    Helper class for session management.
    """

    @staticmethod
    def ensure_session_key(request) -> str:
        """Ensure session has a key, create if needed"""
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key

    @staticmethod
    def get_user_identifier(request) -> tuple[Optional[object], Optional[str]]:
        """
        Get user or session identifier.
        Returns (user, session_key) - one will be None, other populated
        """
        if request.user.is_authenticated:
            return request.user, None
        
        session_key = SessionHelper.ensure_session_key(request)
        return None, session_key


class ValidationHelper:
    """
    Helper class for common validations.
    """

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        """Validate product quantity"""
        return isinstance(quantity, int) and quantity > 0

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        import re
        # Vietnam phone format or general international format
        pattern = r'^[\d\s\-\+\(\)\.]+$'
        return len(phone) >= 8 and re.match(pattern, phone) is not None

    @staticmethod
    def validate_order_data(data: dict) -> tuple[bool, list]:
        """
        Validate order form data.
        Returns (is_valid, errors)
        """
        errors = []
        
        if not data.get('full_name', '').strip():
            errors.append('Full name is required')
        
        if not data.get('email', '').strip() or not ValidationHelper.validate_email(data['email']):
            errors.append('Valid email is required')
        
        if not data.get('phone', '').strip() or not ValidationHelper.validate_phone(data['phone']):
            errors.append('Valid phone number is required')
        
        if not data.get('address', '').strip():
            errors.append('Address is required')
        
        if not data.get('city', '').strip():
            errors.append('City is required')
        
        if not data.get('postal_code', '').strip():
            errors.append('Postal code is required')
        
        return len(errors) == 0, errors
