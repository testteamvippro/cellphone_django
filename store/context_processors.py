"""
Context processors for global template context.
Uses Service Layer for data retrieval.
"""
from store.services.cart import CartService
from store.utils.helpers import SessionHelper


def cart_context(request):
    """
    Add cart information to all templates.
    Uses CartService for cart operations.
    """
    cart_service = CartService()
    
    try:
        user, session_key = SessionHelper.get_user_identifier(request)
        cart = cart_service.get_or_create_cart(user, session_key)
        cart_totals = cart_service.get_cart_totals(cart)
        
        return {
            'cart_items_count': cart_totals['total_items'],
            'cart': cart,
        }
    except Exception:
        # If any error occurs, return default values
        return {
            'cart_items_count': 0,
            'cart': None,
        }
