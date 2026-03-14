"""
Order repositories for data access layer
"""
from typing import Optional
from django.contrib.auth.models import User
from store.models import Order, OrderItem
from store.repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    """Repository for Order model"""

    def __init__(self):
        super().__init__(Order)

    def get_user_orders(self, user: User) -> list:
        """Get all orders for a user"""
        return list(self.filter(user=user).order_by('-created_at'))

    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        return self.get_single(order_number=order_number)

    def get_user_order_by_number(self, user: User, order_number: str) -> Optional[Order]:
        """Get order by number for specific user"""
        return self.get_single(user=user, order_number=order_number)

    def get_orders_by_status(self, status: str) -> list:
        """Get orders by status"""
        return list(self.filter(status=status).order_by('-created_at'))

    def get_pending_orders(self) -> list:
        """Get all pending orders"""
        return self.get_orders_by_status('pending')

    def update_order_status(self, order_id: int, status: str) -> Optional[Order]:
        """Update order status"""
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")
        return self.update(order_id, status=status)


class OrderItemRepository(BaseRepository):
    """Repository for OrderItem model"""

    def __init__(self):
        super().__init__(OrderItem)

    def get_order_items(self, order: Order) -> list:
        """Get all items in an order"""
        return list(self.filter(order=order))

    def create_order_item(self, order: Order, product, quantity: int, price) -> OrderItem:
        """Create order item"""
        return self.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )
