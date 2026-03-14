"""
Wishlist repository for data access layer
"""
from typing import Optional
from django.contrib.auth.models import User
from store.models import Wishlist, Product
from store.repositories.base import BaseRepository


class WishlistRepository(BaseRepository):
    """Repository for Wishlist model"""

    def __init__(self):
        super().__init__(Wishlist)

    def get_user_wishlist(self, user: User) -> list:
        """Get all wishlist items for user"""
        return list(self.filter(user=user).order_by('-added_at'))

    def get_session_wishlist(self, session_key: str) -> list:
        """Get all wishlist items for session"""
        return list(self.filter(session_key=session_key).order_by('-added_at'))

    def is_in_user_wishlist(self, user: User, product: Product) -> bool:
        """Check if product is in user wishlist"""
        return self.exists(user=user, product=product)

    def is_in_session_wishlist(self, session_key: str, product: Product) -> bool:
        """Check if product is in session wishlist"""
        return self.exists(session_key=session_key, product=product)

    def add_to_wishlist(self, user: User, product: Product) -> Wishlist:
        """Add product to user wishlist"""
        item, created = self.get_or_create(user=user, product=product)
        return item

    def add_session_to_wishlist(self, session_key: str, product: Product) -> Wishlist:
        """Add product to session wishlist"""
        item, created = self.get_or_create(session_key=session_key, product=product)
        return item

    def remove_from_wishlist(self, user: User, product: Product) -> bool:
        """Remove product from user wishlist"""
        item = self.get_single(user=user, product=product)
        if item:
            item.delete()
            return True
        return False

    def remove_session_from_wishlist(self, session_key: str, product: Product) -> bool:
        """Remove product from session wishlist"""
        item = self.get_single(session_key=session_key, product=product)
        if item:
            item.delete()
            return True
        return False
