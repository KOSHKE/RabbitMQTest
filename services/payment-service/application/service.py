import json
import random
import os
from domain.interfaces import EventBus, MetricsCollector
from domain.events import PaymentProcessedEvent

class PaymentApplicationService:
    """Application Layer - Payment use cases"""
    
    def __init__(self, event_bus: EventBus, metrics: MetricsCollector):
        self.event_bus = event_bus
        self.metrics = metrics
        self.payment_success_rate = float(os.getenv('PAYMENT_SUCCESS_RATE', '0.9'))
        
    def process_order_payment(self, order_data: dict):
        """Process payment for an order"""
        try:
            # Extract order data
            order_id = order_data['order_id']
            amount = order_data['value']
            
            # Simulate payment processing time
            import time
            processing_time = random.uniform(0.5, 2.0)
            time.sleep(processing_time)
            
            # Simulate payment success/failure
            success = random.random() < self.payment_success_rate
            
            # Create payment event
            payment_event = PaymentProcessedEvent(
                order_id=order_id,
                amount=amount,
                success=success
            )
            
            # Publish payment result
            if success:
                self.event_bus.publish('payment.processed', payment_event.to_dict())
                self.metrics.increment_payments('success')
            else:
                self.event_bus.publish('payment.failed', payment_event.to_dict())
                self.metrics.increment_payments('failed')
            
            # Record processing time
            self.metrics.record_payment_processing_time(processing_time)
            
        except Exception as e:
            self.metrics.increment_payments('error')