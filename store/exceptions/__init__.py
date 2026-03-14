"""
Custom exceptions for the store application
"""


class StoreException(Exception):
    """Base exception for all store-related errors"""
    pass


class CartException(StoreException):
    """Exception raised for cart operations"""
    pass


class ProductException(StoreException):
    """Exception raised for product operations"""
    pass


class OrderException(StoreException):
    """Exception raised for order operations"""
    pass


class InsufficientStockException(ProductException):
    """Exception raised when product stock is insufficient"""
    pass


class InvalidQuantityException(CartException):
    """Exception raised for invalid quantity"""
    pass


class EmptyCartException(CartException):
    """Exception raised when attempting checkout with empty cart"""
    pass


class ProductNotAvailableException(ProductException):
    """Exception raised when product is not available"""
    pass
