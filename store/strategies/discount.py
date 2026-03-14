"""
Strategy pattern implementations for discount and promotion logic
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from store.models import Product


class DiscountStrategy(ABC):
    """
    Abstract base class for discount strategies.
    Implements Strategy Pattern for different discount types.
    """

    @abstractmethod
    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        """
        Calculate discount for product.
        Returns (discounted_price, discount_reason)
        """
        pass


class NoDiscountStrategy(DiscountStrategy):
    """No discount applied"""
    
    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        return product.price, "No discount"


class PercentageDiscountStrategy(DiscountStrategy):
    """Apply percentage discount"""
    
    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self.percentage = percentage

    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        discount_amount = product.price * Decimal(self.percentage) / Decimal(100)
        discounted_price = product.price - discount_amount
        return discounted_price, f"{self.percentage}% off"


class BulkDiscountStrategy(DiscountStrategy):
    """Apply discount based on quantity"""
    
    def __init__(self, min_quantity: int, percentage: float):
        self.min_quantity = min_quantity
        self.percentage = percentage

    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        if quantity >= self.min_quantity:
            discount_amount = product.price * Decimal(self.percentage) / Decimal(100)
            discounted_price = product.price - discount_amount
            return discounted_price, f"Bulk discount {self.percentage}% for {self.min_quantity}+"
        return product.price, "No bulk discount"


class FlashSaleDiscountStrategy(DiscountStrategy):
    """Apply flash sale discount"""
    
    def __init__(self, discount_percentage: float):
        self.discount_percentage = discount_percentage

    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        if product.is_flash_sale:
            discount_amount = product.price * Decimal(self.discount_percentage) / Decimal(100)
            discounted_price = product.price - discount_amount
            return discounted_price, "Flash sale"
        return product.price, "No sale"


class TieredDiscountStrategy(DiscountStrategy):
    """
    Apply tiered discount based on quantity ranges.
    Example: 1-5 units (0%), 6-10 units (10%), 11+ units (15%)
    """
    
    def __init__(self, tiers: list[tuple[int, float]]):
        """
        Tiers format: [(min_qty, discount_percentage), ...]
        Example: [(1, 0), (6, 10), (11, 15)]
        """
        self.tiers = sorted(tiers, key=lambda x: x[0])

    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        discount_percentage = 0
        
        for min_qty, percentage in reversed(self.tiers):
            if quantity >= min_qty:
                discount_percentage = percentage
                break

        if discount_percentage > 0:
            discount_amount = product.price * Decimal(discount_percentage) / Decimal(100)
            discounted_price = product.price - discount_amount
            return discounted_price, f"Tiered discount {discount_percentage}%"
        
        return product.price, "No tiered discount"


class ChainedDiscountStrategy(DiscountStrategy):
    """
    Apply multiple discount strategies in sequence.
    Implements Chain of Responsibility pattern combined with Strategy.
    """
    
    def __init__(self, strategies: list[DiscountStrategy]):
        self.strategies = strategies

    def calculate_discount(self, product: Product, quantity: int = 1) -> tuple[Decimal, str]:
        current_price = product.price
        applied_discounts = []

        for strategy in self.strategies:
            price, reason = strategy.calculate_discount(product, quantity)
            if price < current_price:
                current_price = price
                if reason != "No discount":
                    applied_discounts.append(reason)

        discount_reason = " + ".join(applied_discounts) if applied_discounts else "No discount"
        return current_price, discount_reason
