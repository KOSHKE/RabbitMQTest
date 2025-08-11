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
    def increment_counter(self, name: str, labels: dict = None) -> None:
        """Increment counter metric"""
        pass
    
    @abstractmethod
    def record_histogram(self, name: str, value: float) -> None:
        """Record histogram value"""
        pass

class OrderRepository(ABC):
    """Domain interface for order persistence"""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save order"""
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> list[Order]:
        """Find all orders"""
        pass