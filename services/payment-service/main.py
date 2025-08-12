import asyncio
from infrastructure.messaging import RabbitMQEventBus
from infrastructure.metrics import PrometheusMetricsCollector
from application.service import PaymentApplicationService

class PaymentService:
    """Payment Microservice"""
    
    def __init__(self):
        self.event_bus = None
        self.metrics = None
        self.service = None
    
    async def setup(self):
        """Setup infrastructure"""
        # Infrastructure
        self.event_bus = RabbitMQEventBus()
        await self.event_bus.connect()
        
        self.metrics = PrometheusMetricsCollector()
        self.metrics.start_server(8002)  # Payment service on port 8002
        
        # Application
        self.service = PaymentApplicationService(
            self.event_bus, self.metrics
        )
    
    async def run(self):
        """Start the payment service"""
        print("Starting Payment Service...")
        await self.setup()
        print("Payment Service started on port 8002")
        
        # Start payment processing
        asyncio.create_task(
            self.event_bus.subscribe('orders', self.service.process_order_payment)
        )
        
        # Keep service running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.event_bus:
            await self.event_bus.close()

async def main():
    """Payment Service entry point"""
    service = PaymentService()
    await service.run()

if __name__ == "__main__":
    asyncio.run(main())