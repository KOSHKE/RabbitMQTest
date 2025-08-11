from typing import Optional
from domain.interfaces import OrderRepository
from domain.entities import Order

class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository"""
    
    def __init__(self):
        self._orders: dict[str, Order] = {}
    
    def save(self, order: Order) -> None:
        """Save order to memory"""
        self._orders[order.id] = order
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        return self._orders.get(order_id)
    
    def find_all(self) -> list[Order]:
        """Find all orders"""
        return list(self._orders.values())
    
    def find_by_customer_id(self, customer_id: str) -> list[Order]:
        """Find orders by customer ID"""
        return [order for order in self._orders.values() 
                if order.customer_id == customer_id]