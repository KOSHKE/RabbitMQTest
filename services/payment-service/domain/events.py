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

class PaymentProcessedEvent(DomainEvent):
    """Event fired when a payment is processed"""
    
    def __init__(self, order_id: str, amount: float, success: bool, timestamp=None):
        super().__init__(timestamp)
        self.order_id = order_id
        self.amount = amount
        self.success = success
    
    def get_event_type(self) -> str:
        return "PaymentProcessed"
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.get_event_type(),
            "order_id": self.order_id,
            "amount": self.amount,
            "success": self.success,
            "timestamp": self.timestamp.isoformat()
        }