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
    def increment_shipments(self, status: str) -> None:
        """Increment shipments counter"""
        pass
    
    @abstractmethod
    def record_shipping_processing_time(self, duration: float) -> None:
        """Record shipping processing time"""
        pass