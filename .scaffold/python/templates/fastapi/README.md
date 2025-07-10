# {{name}}

{{description}}

*Generated on {{date}} by {{author}}*

## Features

- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: Database ORM with async support
- **Structured Logging**: JSON structured logging with structlog
{{#if auth}}
- **Authentication**: JWT token-based authentication
{{/if}}
{{#if testing}}
- **Testing**: Comprehensive test suite with pytest
{{/if}}
{{#if docker}}
- **Docker**: Containerization support
{{/if}}
{{#if docs}}
- **API Documentation**: Interactive API docs with Swagger UI
{{/if}}

## Quick Start

### Local Development

1. **Install dependencies**:
```bash
pip install -e .
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

{{#if database}}
3. **Set up database**:
```bash
# For PostgreSQL
createdb {{name}}

# For MySQL
mysql -e "CREATE DATABASE {{name}};"
```
{{/if}}

4. **Run the application**:
```bash
python -m {{module}}.main
```

The API will be available at `http://localhost:8000`

{{#if docs}}
### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
{{/if}}

{{#if docker}}
### Docker Development

1. **Build and run with Docker Compose**:
```bash
docker-compose up --build
```

2. **Run in production mode**:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```
{{/if}}

## API Endpoints

### Health Checks
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check
- `GET /health/metrics` - Basic metrics

### Users
- `GET /api/v1/users` - List users (paginated)
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

{{#if auth}}
### Authentication
- `POST /api/v1/auth/login` - Login and get token
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Get current user
{{/if}}

## Configuration

Environment variables:

```bash
# Application
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["https://yourdomain.com"]

{{#if database}}
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME={{name}}
DB_USER=postgres
DB_PASSWORD=your_password
{{/if}}

{{#if auth}}
# Authentication
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
{{/if}}
```

{{#if testing}}
## Testing

Run tests:
```bash
# Install test dependencies
pip install -e .[test]

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Run specific test file
pytest tests/test_main.py
```
{{/if}}

## Development

### Code Quality

```bash
# Install development dependencies
pip install -e .[dev]

# Format code
black .
isort .

# Lint code
flake8 .
mypy .

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Database Migrations

{{#if database}}
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
{{/if}}

## Deployment

### Environment Setup

1. **Production environment variables**
2. **Database setup and migrations**
3. **SSL certificate configuration**
4. **Reverse proxy setup (nginx)**

### Docker Deployment

```bash
# Build production image
docker build -t {{name}}:latest .

# Run with environment file
docker run --env-file .env -p 8000:8000 {{name}}:latest
```

### Kubernetes Deployment

```yaml
# Example deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{name}}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{name}}
  template:
    metadata:
      labels:
        app: {{name}}
    spec:
      containers:
      - name: {{name}}
        image: {{name}}:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{name}}-secrets
              key: database-url
```

## Monitoring

### Health Checks

The application provides health check endpoints for monitoring:

- `/health` - Basic health status
- `/health/ready` - Kubernetes readiness probe
- `/health/live` - Kubernetes liveness probe
- `/health/metrics` - Basic metrics

### Logging

Structured JSON logging is configured with the following fields:

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "info",
  "logger": "{{module}}.main",
  "message": "Request completed",
  "request_id": "abc123",
  "method": "GET",
  "path": "/api/v1/users",
  "status_code": 200,
  "duration": 0.123
}
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Create an issue in the repository
- Check the FastAPI documentation: https://fastapi.tiangolo.com/