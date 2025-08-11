import asyncio
import time
import random
from infrastructure.messaging import RabbitMQEventBus
from infrastructure.metrics import PrometheusMetricsCollector
from infrastructure.repository import InMemoryOrderRepository
from application.service import OrderApplicationService

class OrderService:
    """Order Microservice"""
    
    def __init__(self):
        self.event_bus = None
        self.metrics = None
        self.repository = None
        self.service = None
    
    async def setup(self):
        """Setup infrastructure"""
        # Infrastructure
        self.event_bus = RabbitMQEventBus()
        await self.event_bus.connect()
        
        self.metrics = PrometheusMetricsCollector()
        self.metrics.start_server(8001)  # Order service on port 8001
        
        self.repository = InMemoryOrderRepository()
        
        # Application
        self.service = OrderApplicationService(
            self.event_bus, self.metrics, self.repository
        )
    
    async def order_generator(self):
        """Generate orders periodically - limited to 100 orders"""
        for i in range(100):
            self.service.place_order()
            print(f"Order Service: Generated {i+1}/100 orders")
            await asyncio.sleep(random.uniform(1, 4))
        
        print("Order Service: Order generation completed")
    
    async def run(self):
        """Start the order service"""
        print("Starting Order Service...")
        
        await self.setup()
        
        print("Order Service started on port 8001")
        
        # Start order generator
        asyncio.create_task(self.order_generator())
        
        # Keep service running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Order Service: Shutting down...")
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.event_bus:
            await self.event_bus.close()

async def main():
    """Order Service entry point"""
    service = OrderService()
    await service.run()

if __name__ == "__main__":
    asyncio.run(main())