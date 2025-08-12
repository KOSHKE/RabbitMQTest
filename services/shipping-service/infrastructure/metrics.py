from prometheus_client import Counter, Histogram, start_http_server
from domain.interfaces import MetricsCollector

class PrometheusMetricsCollector(MetricsCollector):
    """Prometheus implementation of MetricsCollector interface"""
    
    def __init__(self):
        # Business metrics
        self.shipments_total = Counter('shipments_total', 'Total shipments', ['status'])
        self.shipping_processing_time = Histogram('shipping_processing_seconds', 'Shipping processing time')
        
    def start_server(self, port: int = 8000) -> None:
        """Start Prometheus metrics server"""
        start_http_server(port)
        
    def increment_shipments(self, status: str) -> None:
        """Increment shipments counter"""
        self.shipments_total.labels(status=status).inc()
        
    def record_shipping_processing_time(self, duration: float) -> None:
        """Record shipping processing time"""
        self.shipping_processing_time.observe(duration)