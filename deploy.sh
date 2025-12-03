#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
BUILD_TAG=${2:-latest}

echo -e "${YELLOW}Deploying to ${ENVIRONMENT} with tag ${BUILD_TAG}${NC}"

# Load environment variables
if [ -f ".env.${ENVIRONMENT}" ]; then
    export $(cat ".env.${ENVIRONMENT}" | grep -v '^#' | xargs)
else
    echo -e "${RED}Error: .env.${ENVIRONMENT} not found${NC}"
    exit 1
fi

# Pre-deployment checks
echo -e "${YELLOW}Running pre-deployment checks...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed${NC}"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-deployment checks passed${NC}"

# Build images
echo -e "${YELLOW}Building Docker images...${NC}"
export BUILD_TAG=${BUILD_TAG}
docker-compose build --no-cache

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose run --rm web python manage.py migrate

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
docker-compose run --rm web python manage.py collectstatic --noinput

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to become healthy...${NC}"
sleep 10

# Verify deployment
echo -e "${YELLOW}Verifying deployment...${NC}"
if docker-compose ps | grep -q "healthy"; then
    echo -e "${GREEN}✓ Deployment successful${NC}"
else
    echo -e "${RED}✗ Deployment verification failed${NC}"
    docker-compose logs
    exit 1
fi

echo -e "${GREEN}Deployment to ${ENVIRONMENT} completed successfully!${NC}"
