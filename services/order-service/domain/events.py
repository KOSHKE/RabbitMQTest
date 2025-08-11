from abc import ABC, abstractmethod
from datetime import datetime

class DomainEvent(ABC):
    """Abstract base class for all domain events"""
    
    def __init__(self, timestamp=None):
        self.timestamp = timestamp or datetime.now()
    
    @abstractmethod
    def get_event_type(self) -> str:
        """Get event type identifier"""
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization"""
        pass

class OrderPlacedEvent(DomainEvent):
    """Event fired when an order is placed"""
    
    def __init__(self, order_id: str, customer_id: str, value: float, timestamp=None):
        super().__init__(timestamp)
        self.order_id = order_id
        self.customer_id = customer_id
        self.value = value
    
    def get_event_type(self) -> str:
        return "OrderPlaced"
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.get_event_type(),
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "value": self.value,
            "timestamp": self.timestamp.isoformat()
        }