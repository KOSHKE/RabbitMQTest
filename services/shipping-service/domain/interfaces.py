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
    async def subscribe(self, queue_name: str, callback: Callable) -> None:
        """Subscribe to queue messages"""
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