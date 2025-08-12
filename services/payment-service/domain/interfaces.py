from abc import ABC, abstractmethod
from typing import Any, Callable

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
    async def subscribe(self, queue_name: str, callback: Callable[[dict], None]) -> None:
        """Subscribe to queue messages"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close connection"""
        pass

class MetricsCollector(ABC):
    """Domain interface for metrics collection"""
    
    @abstractmethod
    def increment_payments(self, status: str) -> None:
        """Increment payments counter"""
        pass
    
    @abstractmethod
    def record_payment_processing_time(self, duration: float) -> None:
        """Record payment processing time"""
        pass