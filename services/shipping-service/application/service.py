import json
import random
import time
from domain.interfaces import EventBus, MetricsCollector
from domain.events import OrderShippedEvent

class ShippingApplicationService:
    """Application Layer - Shipping use cases"""
    
    def __init__(self, event_bus: EventBus, metrics: MetricsCollector):
        self.event_bus = event_bus
        self.metrics = metrics
        
    def ship_order(self, ch, method, properties, body):
        """Ship order after successful payment"""
        try:
            # Parse payment event
            payment_data = json.loads(body.decode())
            
            # Only ship if payment was successful
            if not payment_data.get('success', False):
                print(f"Shipping Service: Skipping failed payment for order {payment_data['order_id']}")
                return
            
            order_id = payment_data['order_id']
            
            # Simulate shipping processing time
            processing_time = random.uniform(1.0, 3.0)
            time.sleep(processing_time)
            
            # Generate tracking number
            tracking_number = f"TRACK-{random.randint(100000, 999999)}"
            
            # Create shipping event
            shipping_event = OrderShippedEvent(
                order_id=order_id,
                tracking_number=tracking_number
            )
            
            # Publish shipping event
            self.event_bus.publish('shipping.shipped', shipping_event.to_dict())
            
            # Update metrics
            self.metrics.increment_counter('shipments_total', {'status': 'shipped'})
            self.metrics.record_histogram('shipping_processing_time', processing_time)
            
            print(f"Shipping Service: Order {order_id} shipped with tracking {tracking_number}")
            
        except Exception as e:
            print(f"Shipping Service: Error shipping order: {e}")
            self.metrics.increment_counter('shipments_total', {'status': 'error'})