"""
Order service handling order creation and management
"""
import uuid
from typing import Optional, List
from django.contrib.auth.models import User
from store.models import Order, OrderItem, Cart
from store.repositories.order import OrderRepository, OrderItemRepository
from store.exceptions import EmptyCartException, OrderException


class OrderService:
    """
    Service for order operations.
    Handles order creation, status updates, and order queries.
    Implements Service Layer Pattern.
    """

    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()

    def create_order(self, user: User, cart: Cart, order_data: dict) -> Order:
        """
        Create order from cart.
        Order data should contain: full_name, email, phone, address, city, postal_code
        Implements Factory Pattern for order creation.
        """
        if not cart.items.exists():
            raise EmptyCartException("Cannot create order from empty cart")

        # Calculate total
        total_amount = sum(item.subtotal for item in cart.items.all())

        # Create order
        order = self.order_repo.create(
            user=user,
            order_number=self._generate_order_number(),
            full_name=order_data.get('full_name'),
            email=order_data.get('email'),
            phone=order_data.get('phone'),
            address=order_data.get('address'),
            city=order_data.get('city'),
            postal_code=order_data.get('postal_code'),
            total_amount=total_amount,
        )

        # Create order items from cart items
        for cart_item in cart.items.all():
            self.order_item_repo.create_order_item(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        return order

    def get_order_details(self, order_id: int) -> Optional[Order]:
        """
        Get order with items.
        """
        return self.order_repo.get_by_id(order_id)

    def get_user_orders(self, user: User) -> List[Order]:
        """
        Get all orders for user.
        """
        return self.order_repo.get_user_orders(user)

    def get_order_by_number(self, order_number: str, user: Optional[User] = None) -> Optional[Order]:
        """
        Get order by order number.
        If user provided, verify ownership.
        """
        if user:
            return self.order_repo.get_user_order_by_number(user, order_number)
        return self.order_repo.get_by_order_number(order_number)

    def get_order_items(self, order: Order) -> List[OrderItem]:
        """
        Get all items in order.
        """
        return self.order_item_repo.get_order_items(order)

    def update_order_status(self, order_id: int, new_status: str) -> Optional[Order]:
        """
        Update order status.
        Valid statuses: pending, processing, shipped, delivered, cancelled
        """
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        if new_status not in valid_statuses:
            raise OrderException(f"Invalid status: {new_status}. Valid: {valid_statuses}")

        return self.order_repo.update_order_status(order_id, new_status)

    def get_pending_orders(self) -> List[Order]:
        """
        Get all pending orders (admin use).
        """
        return self.order_repo.get_pending_orders()

    def get_orders_by_status(self, status: str) -> List[Order]:
        """
        Get all orders with specific status (admin use).
        """
        return self.order_repo.get_orders_by_status(status)

    def calculate_order_total(self, order: Order) -> float:
        """
        Calculate order total from items.
        """
        items = self.get_order_items(order)
        return sum(item.subtotal for item in items)

    def _generate_order_number(self) -> str:
        """
        Generate unique order number.
        Format: ORD-XXXXXXXX
        """
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    def can_cancel_order(self, order: Order) -> bool:
        """
        Check if order can be cancelled.
        Only pending and processing orders can be cancelled.
        """
        return order.status in ['pending', 'processing']

    def cancel_order(self, order: Order) -> bool:
        """
        Cancel order if possible.
        """
        if not self.can_cancel_order(order):
            raise OrderException(f"Cannot cancel order with status: {order.status}")

        return self.update_order_status(order.id, 'cancelled') is not None
