from prometheus_client import Counter, Histogram, Gauge, start_http_server
from domain.interfaces import MetricsCollector

class PrometheusMetricsCollector(MetricsCollector):
    """Prometheus implementation of MetricsCollector interface"""
    
    def __init__(self):
        # Business metrics
        self.orders_total = Counter('orders_total', 'Total orders', ['status'])
        self.order_value = Histogram('order_value_dollars', 'Order value in dollars')
        self.active_orders = Gauge('active_orders_count', 'Active orders count')
        
    def start_server(self, port: int = 8000) -> None:
        """Start Prometheus metrics server"""
        start_http_server(port)
        
    def increment_counter(self, name: str, labels: dict = None) -> None:
        """Increment counter metric"""
        if name == 'orders_total' and labels:
            self.orders_total.labels(**labels).inc()
        
    def record_histogram(self, name: str, value: float) -> None:
        """Record histogram value"""
        if name == 'order_value':
            self.order_value.observe(value)
        
    # Specific business methods
    def increment_orders(self, status: str) -> None:
        """Increment orders counter"""
        self.orders_total.labels(status=status).inc()
        
    def record_order_value(self, value: float) -> None:
        """Record order value"""
        self.order_value.observe(value)
        
    def increment_active_orders(self) -> None:
        """Increment active orders gauge"""
        self.active_orders.inc()
        
    def decrement_active_orders(self) -> None:
        """Decrement active orders gauge"""
        self.active_orders.dec()