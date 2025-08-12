import json
import os
from typing import Optional
import redis.asyncio as redis
from domain.interfaces import OrderRepository
from domain.entities import Order, OrderStatus, Money

class RedisOrderRepository(OrderRepository):
    """Redis implementation of OrderRepository"""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        self.redis_client = None
        self.key_prefix = "order:"
    
    async def connect(self):
        """Connect to Redis"""
        self.redis_client = redis.from_url(self.redis_url)
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
    
    async def save(self, order: Order) -> None:
        """Save order to Redis"""
        order_data = {
            'id': order.id,
            'customer_id': order.customer_id,
            'value': order.value.amount,
            'currency': order.value.currency,
            'status': order.status.value,
            'created_at': order.created_at.isoformat()
        }
        
        key = f"{self.key_prefix}{order.id}"
        await self.redis_client.set(key, json.dumps(order_data))
        
        # Add to customer index
        customer_key = f"customer:{order.customer_id}:orders"
        await self.redis_client.sadd(customer_key, order.id)
    
    async def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find order by ID"""
        key = f"{self.key_prefix}{order_id}"
        data = await self.redis_client.get(key)
        
        if not data:
            return None
        
        order_data = json.loads(data)
        return self._deserialize_order(order_data)
    
    async def find_all(self) -> list[Order]:
        """Find all orders"""
        keys = await self.redis_client.keys(f"{self.key_prefix}*")
        orders = []
        
        for key in keys:
            data = await self.redis_client.get(key)
            if data:
                order_data = json.loads(data)
                orders.append(self._deserialize_order(order_data))
        
        return orders
    
    async def find_by_customer_id(self, customer_id: str) -> list[Order]:
        """Find orders by customer ID"""
        customer_key = f"customer:{customer_id}:orders"
        order_ids = await self.redis_client.smembers(customer_key)
        
        orders = []
        for order_id in order_ids:
            order = await self.find_by_id(order_id.decode())
            if order:
                orders.append(order)
        
        return orders
    
    def _deserialize_order(self, order_data: dict) -> Order:
        """Convert dict back to Order object"""
        from datetime import datetime
        
        order = Order.__new__(Order)  # Create without calling __init__
        order.id = order_data['id']
        order.customer_id = order_data['customer_id']
        order.value = Money(order_data['value'], order_data['currency'])
        order.status = OrderStatus(order_data['status'])
        order.created_at = datetime.fromisoformat(order_data['created_at'])
        
        return order