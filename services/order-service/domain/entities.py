from enum import Enum
from datetime import datetime

class OrderStatus(Enum):
    PLACED = "placed"
    PAID = "paid" 
    SHIPPED = "shipped"
    PAYMENT_FAILED = "payment_failed"

class Order:
    """Aggregate Root - Order"""
    def __init__(self, customer_id, value):
        self.id = f"ORD-{int(datetime.now().timestamp())}"
        self.customer_id = customer_id
        self.value = Money(value)
        self.status = OrderStatus.PLACED
        self.created_at = datetime.now()
        
    def can_process_payment(self):
        return self.status == OrderStatus.PLACED
        
    def mark_as_paid(self):
        if not self.can_process_payment():
            raise InvalidOrderStateException(f"Cannot pay order in {self.status} status")
        self.status = OrderStatus.PAID
        
    def mark_payment_failed(self):
        if not self.can_process_payment():
            raise InvalidOrderStateException(f"Cannot fail payment for order in {self.status} status")
        self.status = OrderStatus.PAYMENT_FAILED
        
    def mark_as_shipped(self, tracking_number):
        if self.status != OrderStatus.PAID:
            raise InvalidOrderStateException(f"Cannot ship unpaid order")
        self.status = OrderStatus.SHIPPED
        self.tracking_number = tracking_number

class Money:
    """Value Object - Money"""
    def __init__(self, amount, currency="USD"):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = round(amount, 2)
        self.currency = currency
        
    def __str__(self):
        return f"${self.amount}"

class InvalidOrderStateException(Exception):
    pass