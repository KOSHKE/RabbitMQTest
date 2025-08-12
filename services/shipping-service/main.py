import asyncio
from infrastructure.messaging import RabbitMQEventBus
from infrastructure.metrics import PrometheusMetricsCollector
from application.service import ShippingApplicationService

class ShippingService:
    """Shipping Microservice"""
    
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
        self.metrics.start_server(8003)  # Shipping service on port 8003
        
        # Application
        self.service = ShippingApplicationService(
            self.event_bus, self.metrics
        )
    
    async def run(self):
        """Start the shipping service"""
        print("Starting Shipping Service...")
        await self.setup()
        print("Shipping Service started on port 8003")
        
        # Start shipping processing
        asyncio.create_task(
            self.event_bus.subscribe('payments', self.service.ship_order)
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
    """Shipping Service entry point"""
    service = ShippingService()
    await service.run()

if __name__ == "__main__":
    asyncio.run(main())