import asyncio
import time
import random
import os
from infrastructure.messaging import RabbitMQEventBus
from infrastructure.metrics import PrometheusMetricsCollector
from infrastructure.redis_repository import RedisOrderRepository
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
        
        # Setup Redis repository
        self.repository = RedisOrderRepository()
        await self.repository.connect()
        
        # Application
        self.service = OrderApplicationService(
            self.event_bus, self.metrics, self.repository
        )
    
    async def order_generator(self):
        """Generate orders periodically - limited to 100 orders"""
        for i in range(100):
            await self.service.place_order()
            await asyncio.sleep(random.uniform(1, 4))
    
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
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.event_bus:
            await self.event_bus.close()
        if self.repository:
            await self.repository.close()

async def main():
    """Order Service entry point"""
    service = OrderService()
    await service.run()

if __name__ == "__main__":
    asyncio.run(main())