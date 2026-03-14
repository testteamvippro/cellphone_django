"""
Wishlist service handling wishlist operations
"""
from typing import List, Optional
from django.contrib.auth.models import User
from store.models import Wishlist, Product
from store.repositories.wishlist import WishlistRepository


class WishlistService:
    """
    Service for wishlist operations.
    Handles adding/removing items for authenticated and anonymous users.
    """

    def __init__(self):
        self.repo = WishlistRepository()

    def add_to_wishlist(self, product: Product, user: Optional[User] = None, 
                       session_key: Optional[str] = None) -> tuple[Wishlist, bool]:
        """
        Add product to wishlist.
        Returns (wishlist_item, was_added)
        """
        if user and user.is_authenticated:
            return self._add_to_user_wishlist(user, product)
        elif session_key:
            return self._add_to_session_wishlist(session_key, product)
        else:
            raise Exception("Either user or session_key must be provided")

    def remove_from_wishlist(self, product: Product, user: Optional[User] = None,
                           session_key: Optional[str] = None) -> bool:
        """
        Remove product from wishlist.
        Returns True if removed, False if not found.
        """
        if user and user.is_authenticated:
            return self.repo.remove_from_wishlist(user, product)
        elif session_key:
            return self.repo.remove_session_from_wishlist(session_key, product)
        else:
            raise Exception("Either user or session_key must be provided")

    def toggle_wishlist(self, product: Product, user: Optional[User] = None,
                       session_key: Optional[str] = None) -> dict:
        """
        Toggle product in wishlist (add if not present, remove if present).
        Returns {in_wishlist: bool, added: bool, message: str}
        """
        is_in_wishlist = self.is_in_wishlist(product, user, session_key)

        if is_in_wishlist:
            self.remove_from_wishlist(product, user, session_key)
            return {
                'in_wishlist': False,
                'added': False,
                'message': 'Removed from wishlist'
            }
        else:
            self.add_to_wishlist(product, user, session_key)
            return {
                'in_wishlist': True,
                'added': True,
                'message': 'Added to wishlist'
            }

    def is_in_wishlist(self, product: Product, user: Optional[User] = None,
                      session_key: Optional[str] = None) -> bool:
        """
        Check if product is in wishlist.
        """
        if user and user.is_authenticated:
            return self.repo.is_in_user_wishlist(user, product)
        elif session_key:
            return self.repo.is_in_session_wishlist(session_key, product)
        return False

    def get_user_wishlist(self, user: User) -> List[Wishlist]:
        """
        Get all wishlist items for user.
        """
        return self.repo.get_user_wishlist(user)

    def get_session_wishlist(self, session_key: str) -> List[Wishlist]:
        """
        Get all wishlist items for session.
        """
        return self.repo.get_session_wishlist(session_key)

    def get_wishlist_products(self, user: Optional[User] = None,
                             session_key: Optional[str] = None) -> List[Product]:
        """
        Get list of products in wishlist.
        """
        if user and user.is_authenticated:
            items = self.get_user_wishlist(user)
        elif session_key:
            items = self.get_session_wishlist(session_key)
        else:
            return []

        return [item.product for item in items]

    def _add_to_user_wishlist(self, user: User, product: Product) -> tuple[Wishlist, bool]:
        """
        Internal method to add to user wishlist.
        """
        item, created = Wishlist.objects.get_or_create(user=user, product=product)
        return item, created

    def _add_to_session_wishlist(self, session_key: str, product: Product) -> tuple[Wishlist, bool]:
        """
        Internal method to add to session wishlist.
        """
        item, created = Wishlist.objects.get_or_create(session_key=session_key, product=product)
        return item, created
