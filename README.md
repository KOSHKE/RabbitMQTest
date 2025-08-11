# E-commerce Microservices: RabbitMQ + Prometheus + Grafana

🚀 **Production-ready** e-commerce microservices with **Domain-Driven Design** architecture.

## 🏗️ Architecture

### Domain-Driven Design Layers
- **Domain Layer** - Pure business logic (entities, events, services)
- **Application Layer** - Use cases orchestration  
- **Infrastructure Layer** - External concerns (RabbitMQ, Prometheus)

### Bounded Contexts
- **Orders** - Order management
- **Payments** - Payment processing  
- **Shipping** - Order fulfillment

## 🔄 Event Flow

```
OrderPlaced → PaymentProcessed → OrderShipped
```

- **Asynchronous processing** via RabbitMQ
- **90% payment success rate** (configurable)
- **Real-time metrics** collection

## 🚀 Quick Start

```bash
# Clone repository
git clone <repository-url>
cd RabbitMQTest

# Copy environment variables
cp .env.example .env

# (Optional) Edit configuration
nano .env

# Start all microservices
docker-compose up --build

# View logs
docker-compose logs -f order-service
docker-compose logs -f payment-service
docker-compose logs -f shipping-service
```

## 📊 Services Access

| Service | URL | Credentials |
|---------|-----|-------------|
| **Order Service** | http://localhost:8001/metrics | - |
| **Payment Service** | http://localhost:8002/metrics | - |
| **Shipping Service** | http://localhost:8003/metrics | - |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin/admin |

## 📈 Monitoring

- **Order metrics** by status (placed, paid, shipped, failed)
- **Payment processing time** (95th/50th percentiles)
- **Average order value** tracking
- **Active orders** gauge
- **RabbitMQ queue** monitoring

## 🛠️ Development

```bash
# Start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f <service-name>

# Rebuild specific service
docker-compose build <service-name>
```

## 🏗️ Project Structure

```
├── services/
│   ├── order-service/     # Order microservice (Port 8001)
│   │   ├── domain/        # Domain layer
│   │   ├── application/   # Application layer
│   │   ├── infrastructure/# Infrastructure layer
│   │   └── main.py       # Service entry point
│   ├── payment-service/   # Payment microservice (Port 8002)
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── main.py
│   └── shipping-service/  # Shipping microservice (Port 8003)
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       └── main.py
├── config/               # Configuration
├── grafana/              # Grafana dashboards
└── docker-compose.yml    # Microservices orchestration
```

## ⚙️ Configuration

All configuration is handled via `.env` file with sensible defaults:

```bash
# Business Configuration
PAYMENT_SUCCESS_RATE=0.9
MIN_ORDER_VALUE=10.0
MAX_ORDER_VALUE=500.0

# Infrastructure
RABBITMQ_URL=amqp://admin:admin@rabbitmq:5672/
RABBITMQ_USER=admin
RABBITMQ_PASS=admin

# Monitoring
GRAFANA_ADMIN_PASSWORD=admin
```

### Customizing configuration:
```bash
# Edit .env file
nano .env

# Example changes:
PAYMENT_SUCCESS_RATE=0.8
MIN_ORDER_VALUE=50.0
MAX_ORDER_VALUE=1000.0

# Restart services
docker-compose up --build
```

## 🧪 Testing

```bash
# View service metrics
curl http://localhost:8001/metrics  # Order Service
curl http://localhost:8002/metrics  # Payment Service
curl http://localhost:8003/metrics  # Shipping Service

# Check service logs
docker-compose logs order-service
docker-compose logs payment-service
docker-compose logs shipping-service

# Verify message flow
docker-compose logs -f  # Watch real-time event processing
```

## 📋 Features

- ✅ **Domain-Driven Design** architecture
- ✅ **Event-driven** microservices
- ✅ **Dependency Inversion** principle
- ✅ **Repository Pattern** implementation
- ✅ **Real-time monitoring** and observability
- ✅ **Production-ready** monitoring stack
- ✅ **Docker containerization**
- ✅ **Health checks** and retry logic
- ✅ **Configurable business rules**

## 🛑 Stopping

```bash
docker-compose down
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.