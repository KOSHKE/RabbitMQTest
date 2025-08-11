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
        
    def increment_counter(self, name: str, labels: dict = None) -> None:
        """Increment counter metric"""
        if name == 'payments_total' and labels:
            self.payments_total.labels(**labels).inc()
        
    def record_histogram(self, name: str, value: float) -> None:
        """Record histogram value"""
        if name == 'payment_processing_time':
            self.payment_processing_time.observe(value)