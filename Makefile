.PHONY: help lint format check test clean install dev-install lint-templates format-templates db-create db-drop db-truncate db-migrate db-reset db-reset-with-data db-status db-import

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install .
	@$(MAKE) install-dev

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

db-create: ## Create database tables
	python scripts/database.py create

db-import: ## Import data from CSV files
	python scripts/importer.py

db-drop: ## Drop all database tables
	python scripts/database.py drop

db-reset: ## Drop and recreate all tables
	python scripts/database.py reset

lint: ## Run ruff linter on Python code
	@echo "Running ruff linter..."
	ruff check .

lint-templates: ## Run djlint on HTML templates
	@echo "Linting HTML templates..."
	djlint app/templates/ --check

lint-fix: ## Format code with ruff and templates with djlint
	@echo "Formatting Python code with ruff..."
	ruff format .
	@echo "Fixing linting issues with ruff..."
	ruff check --fix .
	@echo "Formatting HTML templates..."
	djlint app/templates/ --reformat

lint-check: ## Run all checks (lint + format check)
	@echo "Running all checks..."
	@$(MAKE) lint
	@$(MAKE) lint-templates
	@echo "Checking if code is properly formatted..."
	ruff format --check .
	djlint app/templates/ --check
	@echo "All checks passed!"

test: ## Run tests
	pytest

coverage: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

ci: ## Run CI checks (format, lint, test)
	@echo "Running CI checks..."
	@$(MAKE) format
	@$(MAKE) format-templates
	@$(MAKE) check
	@$(MAKE) test
	@echo "All CI checks passed!"

server: ## Run the server locally
	@echo "Starting server in mode..."
	python scripts/server.py