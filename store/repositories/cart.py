"""
Cart and CartItem repositories for data access layer
"""
from typing import Optional
from django.contrib.auth.models import User
from store.models import Cart, CartItem
from store.repositories.base import BaseRepository


class CartRepository(BaseRepository):
    """Repository for Cart model"""

    def __init__(self):
        super().__init__(Cart)

    def get_or_create_for_user(self, user: User) -> Cart:
        """Get or create cart for authenticated user"""
        cart, created = self.get_or_create(user=user)
        return cart

    def get_or_create_for_session(self, session_key: str) -> Cart:
        """Get or create cart for session/anonymous user"""
        cart, created = self.get_or_create(session_key=session_key)
        return cart

    def get_user_cart(self, user: User) -> Optional[Cart]:
        """Get cart for authenticated user"""
        return self.get_single(user=user)

    def get_session_cart(self, session_key: str) -> Optional[Cart]:
        """Get cart for session"""
        return self.get_single(session_key=session_key)


class CartItemRepository(BaseRepository):
    """Repository for CartItem model"""

    def __init__(self):
        super().__init__(CartItem)

    def get_item_in_cart(self, cart: Cart, product_id: int) -> Optional[CartItem]:
        """Get specific cart item"""
        return self.get_single(cart=cart, product_id=product_id)

    def get_cart_items(self, cart: Cart) -> list:
        """Get all items in cart"""
        return list(self.filter(cart=cart))

    def remove_from_cart(self, cart: Cart, product_id: int) -> bool:
        """Remove item from cart"""
        item = self.get_item_in_cart(cart, product_id)
        if item:
            item.delete()
            return True
        return False

    def clear_cart(self, cart: Cart) -> int:
        """Clear all items from cart"""
        count = self.filter(cart=cart).count()
        self.filter(cart=cart).delete()
        return count
