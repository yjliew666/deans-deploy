.PHONY: help install lint format test build clean

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black and isort"
	@echo "  make test        - Run all tests with coverage"
	@echo "  make build       - Build Docker images"
	@echo "  make clean       - Clean generated files"

install:
	cd deans-api && pip install -r requirements.txt

lint:
	cd deans-api && flake8 deans_api/ && pylint deans_api/

format:
	cd deans-api && black deans_api/ && isort deans_api/

test:
	cd deans-api && pytest --cov=deans_api --cov-report=html

build:
	docker-compose build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf deans-api/htmlcov/
	rm -rf deans-api/.coverage
