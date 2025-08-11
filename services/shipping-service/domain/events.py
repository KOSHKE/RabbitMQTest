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

class OrderShippedEvent(DomainEvent):
    """Event fired when an order is shipped"""
    
    def __init__(self, order_id: str, tracking_number: str, timestamp=None):
        super().__init__(timestamp)
        self.order_id = order_id
        self.tracking_number = tracking_number
    
    def get_event_type(self) -> str:
        return "OrderShipped"
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.get_event_type(),
            "order_id": self.order_id,
            "tracking_number": self.tracking_number,
            "timestamp": self.timestamp.isoformat()
        }