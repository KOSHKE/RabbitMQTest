from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from .entities import Order

class EventBus(ABC):
    """Domain interface for event publishing"""
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to message broker"""
        pass
    
    @abstractmethod
    def publish(self, routing_key: str, event: Any) -> None:
        """Publish domain event"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close connection"""
        pass

class MetricsCollector(ABC):
    """Domain interface for metrics collection"""
    
    @abstractmethod
    def increment_orders(self, status: str) -> None:
        """Increment orders counter"""
        pass
    
    @abstractmethod
    def record_order_value(self, value: float) -> None:
        """Record order value"""
        pass
    
    @abstractmethod
    def increment_active_orders(self) -> None:
        """Increment active orders gauge"""
        pass
    
    @abstractmethod
    def decrement_active_orders(self) -> None:
        """Decrement active orders gauge"""
        pass

class OrderRepository(ABC):
    """Domain interface for order persistence"""
    
    @abstractmethod
    async def save(self, order: Order) -> None:
        """Save order"""
        pass
    
    @abstractmethod
    async def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        pass
    
    @abstractmethod
    async def find_all(self) -> list[Order]:
        """Find all orders"""
        pass
    
    @abstractmethod
    async def find_by_customer_id(self, customer_id: str) -> list[Order]:
        """Find orders by customer ID"""
        pass