import random
from domain.entities import Order
from domain.interfaces import OrderRepository, EventBus, MetricsCollector
from domain.events import OrderPlacedEvent

class OrderApplicationService:
    """Application Layer - Order use cases"""
    
    def __init__(self, event_bus: EventBus, metrics: MetricsCollector, order_repository: OrderRepository):
        self.event_bus = event_bus
        self.metrics = metrics
        self.order_repository = order_repository
        
    def place_order(self):
        # Create domain object
        customer_id = f"CUST-{random.randint(1, 1000)}"
        order_value = round(random.uniform(10, 500), 2)
        order = Order(customer_id, order_value)
        
        # Create domain event
        event = OrderPlacedEvent(
            order_id=order.id,
            customer_id=order.customer_id,
            value=order.value.amount
        )
        
        # Save order to repository
        self.order_repository.save(order)
        
        # Publish domain event
        self.event_bus.publish('order.placed', event.to_dict())
        
        # Update metrics
        self.metrics.increment_orders('placed')
        self.metrics.record_order_value(order.value.amount)
        self.metrics.increment_active_orders()
        
        print(f"Order placed: {order.id} (${order.value.amount})")