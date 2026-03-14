"""
Cart service implementing business logic for cart operations
Uses: Repository Pattern, Strategy Pattern
"""
from decimal import Decimal
from typing import Optional, List, Tuple
from django.contrib.auth.models import User
from store.models import Cart, CartItem, Product
from store.repositories.cart import CartRepository, CartItemRepository
from store.repositories.product import ProductRepository
from store.exceptions import (
    CartException, InvalidQuantityException, 
    InsufficientStockException, EmptyCartException
)


class CartService:
    """
    Service class for cart operations.
    Handles business logic separate from views.
    Implements Service Layer Pattern.
    """

    def __init__(self):
        self.cart_repo = CartRepository()
        self.cart_item_repo = CartItemRepository()
        self.product_repo = ProductRepository()

    def get_or_create_cart(self, user: Optional[User] = None, session_key: Optional[str] = None) -> Cart:
        """
        Get or create cart for user or session.
        Factory pattern: creates cart if not exists
        """
        if user and user.is_authenticated:
            return self.cart_repo.get_or_create_for_user(user)
        elif session_key:
            return self.cart_repo.get_or_create_for_session(session_key)
        else:
            raise CartException("Either user or session_key must be provided")

    def add_to_cart(self, cart: Cart, product: Product, quantity: int = 1) -> CartItem:
        """
        Add product to cart with quantity check.
        Validates stock availability.
        """
        if quantity <= 0:
            raise InvalidQuantityException(f"Quantity must be greater than 0, got {quantity}")

        if not product.is_available:
            raise CartException(f"Product '{product.name}' is not available")

        if product.stock < quantity:
            raise InsufficientStockException(
                f"Insufficient stock for '{product.name}'. Available: {product.stock}, Requested: {quantity}"
            )

        cart_item = self.cart_item_repo.get_item_in_cart(cart, product.id)
        
        if cart_item:
            # Check if total quantity exceeds stock
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                raise InsufficientStockException(
                    f"Insufficient stock. Total requested: {new_quantity}, Available: {product.stock}"
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item, _ = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

        return cart_item

    def update_cart_item(self, cart: Cart, item_id: int, quantity: int) -> Optional[CartItem]:
        """
        Update cart item quantity with validation.
        """
        if quantity < 0:
            raise InvalidQuantityException(f"Quantity cannot be negative, got {quantity}")

        cart_item = CartItem.objects.get_or_none(id=item_id, cart=cart) if hasattr(CartItem.objects, 'get_or_none') else None
        if not cart_item:
            try:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)
            except CartItem.DoesNotExist:
                return None

        if quantity == 0:
            cart_item.delete()
            return None

        if cart_item.product.stock < quantity:
            raise InsufficientStockException(
                f"Insufficient stock. Requested: {quantity}, Available: {cart_item.product.stock}"
            )

        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def remove_from_cart(self, cart: Cart, item_id: int) -> bool:
        """
        Remove item from cart.
        """
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False

    def get_cart_items(self, cart: Cart) -> List[CartItem]:
        """
        Get all items in cart.
        """
        return self.cart_item_repo.get_cart_items(cart)

    def get_cart_totals(self, cart: Cart) -> dict:
        """
        Calculate cart totals.
        Returns: {total_items, total_price, item_count}
        """
        items = self.get_cart_items(cart)
        total_items = sum(item.quantity for item in items)
        total_price = sum(item.subtotal for item in items)
        
        return {
            'total_items': total_items,
            'total_price': total_price,
            'item_count': len(items),
            'items': items
        }

    def clear_cart(self, cart: Cart) -> int:
        """
        Clear all items from cart.
        Returns number of items cleared.
        """
        return self.cart_item_repo.clear_cart(cart)

    def validate_cart_for_checkout(self, cart: Cart) -> Tuple[bool, str]:
        """
        Validate cart is ready for checkout.
        Returns (is_valid, message)
        """
        items = self.get_cart_items(cart)
        
        if not items:
            return False, "Cart is empty"

        # Verify stock for all items
        for item in items:
            if not item.product.is_available:
                return False, f"Product '{item.product.name}' is no longer available"
            
            if item.product.stock < item.quantity:
                return False, f"Insufficient stock for '{item.product.name}'"

        return True, "Cart is valid"

    def increase_quantity(self, cart: Cart, item_id: int) -> Optional[CartItem]:
        """
        Increase item quantity by 1.
        """
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            if cart_item.product.stock <= cart_item.quantity:
                raise InsufficientStockException("Cannot increase quantity, max stock reached")
            cart_item.quantity += 1
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            return None

    def decrease_quantity(self, cart: Cart, item_id: int) -> Optional[CartItem]:
        """
        Decrease item quantity by 1, or remove if quantity is 1.
        """
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            if cart_item.quantity <= 1:
                cart_item.delete()
                return None
            cart_item.quantity -= 1
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            return None
