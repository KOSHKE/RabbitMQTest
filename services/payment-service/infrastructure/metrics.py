from prometheus_client import Counter, Histogram, start_http_server
from domain.interfaces import MetricsCollector

class PrometheusMetricsCollector(MetricsCollector):
    """Prometheus implementation of MetricsCollector interface"""
    
    def __init__(self):
        # Business metrics
        self.payments_total = Counter('payments_total', 'Total payments', ['status'])
        self.payment_processing_time = Histogram('payment_processing_seconds', 'Payment processing time')
        
    def start_server(self, port: int = 8000) -> None:
        """Start Prometheus metrics server"""
        start_http_server(port)
        
    def increment_payments(self, status: str) -> None:
        """Increment payments counter"""
        self.payments_total.labels(status=status).inc()
        
    def record_payment_processing_time(self, duration: float) -> None:
        """Record payment processing time"""
        self.payment_processing_time.observe(duration)