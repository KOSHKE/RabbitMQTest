import asyncio
import json
import os
from typing import Any, Callable
import aio_pika
from domain.interfaces import EventBus

class RabbitMQEventBus(EventBus):
    """Async RabbitMQ implementation of EventBus interface"""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        
    async def connect(self, max_retries: int = 10, retry_delay: int = 2):
        """Establish async connection to RabbitMQ"""
        rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://admin:admin@rabbitmq:5672/')
        
        for attempt in range(max_retries):
            try:
                self.connection = await aio_pika.connect_robust(rabbitmq_url)
                self.channel = await self.connection.channel()
                
                # Declare exchange and queues
                exchange = await self.channel.declare_exchange('ecommerce', aio_pika.ExchangeType.TOPIC)
                
                await self.channel.declare_queue('orders', durable=True)
                await self.channel.declare_queue('payments', durable=True)
                await self.channel.declare_queue('shipping', durable=True)
                
                # Bind queues to exchange
                orders_queue = await self.channel.get_queue('orders')
                payments_queue = await self.channel.get_queue('payments')
                shipping_queue = await self.channel.get_queue('shipping')
                
                await orders_queue.bind(exchange, 'order.*')
                await payments_queue.bind(exchange, 'payment.*')
                await shipping_queue.bind(exchange, 'shipping.*')
                
                print("Shipping Service: Connected to RabbitMQ")
                break
            except Exception:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)
        
    def publish(self, routing_key: str, event: Any) -> None:
        """Publish event to RabbitMQ (sync wrapper for async)"""
        asyncio.create_task(self._async_publish(routing_key, event))
        
    async def _async_publish(self, routing_key: str, event: Any):
        """Async publish event to RabbitMQ"""
        exchange = await self.channel.get_exchange('ecommerce')
        message = aio_pika.Message(
            json.dumps(event).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await exchange.publish(message, routing_key=routing_key)
        
    async def subscribe(self, queue_name: str, callback: Callable):
        """Subscribe to queue messages"""
        queue = await self.channel.get_queue(queue_name)
        
        async def message_handler(message: aio_pika.IncomingMessage):
            async with message.process():
                # Convert to sync callback format for compatibility
                class MockMethod:
                    def __init__(self, delivery_tag):
                        self.delivery_tag = delivery_tag
                        
                class MockChannel:
                    def basic_ack(self, delivery_tag):
                        pass  # Auto-ack handled by aio-pika
                
                mock_ch = MockChannel()
                mock_method = MockMethod(message.delivery_tag)
                mock_properties = None
                
                callback(mock_ch, mock_method, mock_properties, message.body)
        
        await queue.consume(message_handler)
        
    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.close()