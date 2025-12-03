# Dean's Crisis Management System

Automated CI/CD pipeline for building, testing, and deploying the Dean's Crisis Management platform.

## Project Structure

```
deans-deploy/
├── deans-api/              # Django REST API
├── deans-frontend/         # React Frontend
├── nginx/                  # Nginx reverse proxy
├── cron/                   # Cron jobs
├── docker-compose.yaml     # Docker Compose configuration
├── .github/workflows/      # GitHub Actions CI/CD
├── deploy.sh               # Deployment script
└── Makefile                # Development commands
```

## Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.9+ (for local development)
- Node.js 18+ (for frontend development)

## Quick Start

### Local Development

```bash
# Install dependencies
make install

# Run linting and formatting
make lint
make format

# Run tests
make test

# Build Docker images
make build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f web
```

### Environment Setup

```bash
# Copy example environment file
cp .env.example default.env

# Edit for your local setup
nano default.env

# For staging/production
cp .env.example .env.staging
nano .env.staging
```

## CI/CD Pipeline

### Automated Workflows

1. **Lint** - Code quality checks (flake8, pylint, black, isort)
2. **Test** - Unit and integration tests with coverage
3. **Build** - Docker image creation
4. **Security Scan** - Vulnerability scanning with Trivy
5. **Report** - Test reports and artifacts

### Triggering Workflows

- **Push to main**: Full pipeline (lint → test → build → scan)
- **Push to develop**: Full pipeline
- **Pull requests**: Lint and test only

## Deployment

### Staging

```bash
./deploy.sh staging v1.0.0
```

### Production

```bash
./deploy.sh production v1.0.0
```

## Services

### Django API (`web`)
- Port: 8000 (internal)
- Health check: `GET /health`
- Volume: `./deans-api/deans_api:/work/deans-api/deans_api`

### React Frontend (`frontend`)
- Port: 3000
- Health check: HTTP request to port 3000

### PostgreSQL (`db`)
- Port: 5432
- Default DB: `deans_db`
- Volume: `db_data`

### Redis (`redis`)
- Port: 6379
- Volume: `redis_data`

### Nginx (`nginx`)
- Port: 8000 (external)
- Health check: `GET /health`

## Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100
```

## Testing

```bash
# Run all tests
make test

# Run specific test
cd deans-api && pytest tests/test_models.py

# With coverage report
cd deans-api && pytest --cov=deans_api --cov-report=html
```

## Code Quality

```bash
# Lint
make lint

# Format code
make format

# Check formatting without changing
cd deans-api && black --check deans_api/
```

## Troubleshooting

### Database Connection Issues
```bash
docker-compose logs db
docker-compose exec db psql -U postgres
```

### Port Already in Use
```bash
lsof -i :8000
lsof -i :3000
lsof -i :5432
```

### Clear Everything
```bash
docker-compose down -v
make clean
```

## Contributing

1. Create a feature branch
2. Make changes and run tests
3. Submit pull request
4. CI/CD pipeline must pass

## License

Proprietary - Dean's Crisis Management System
