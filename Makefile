.PHONY: help install dev test lint format clean docker-build docker-up docker-down deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest tests/ --cov=app --cov-report=term-missing

test-verbose: ## Run tests with verbose output
	pytest tests/ -v --cov=app --cov-report=html

lint: ## Run linting
	flake8 app tests
	mypy app --ignore-missing-imports

format: ## Format code
	black app tests

format-check: ## Check code formatting
	black --check app tests

clean: ## Clean up temporary files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache

docker-build: ## Build Docker image
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-clean: ## Clean Docker resources
	docker-compose down -v

deploy: ## Deploy application
	./scripts/deploy.sh

health: ## Check application health
	curl http://localhost:8000/health

setup: ## Initial setup
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
