# saml2aws-multi Makefile - Unit Testing Focus
# Provides targets for running unit tests locally

.PHONY: help test test-coverage clean install-test-deps yamllint build check-uv

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Variables
UV := uv
PYTHON := $(UV) run python
PIP := $(UV) run pip
PYTEST := $(UV) run pytest
BUILD := $(UV) run python -m build

# Check if uv is available, install if not
check-uv:
	@which uv > /dev/null || (echo "Installing uv..." && pip install uv)

# Installation targets
install-test-deps: check-uv ## Install test dependencies
	@echo "Installing test dependencies..."
	$(PIP) install -e ".[test]"
	@echo "Dependencies installed."

install-deps: check-uv ## Install project dependencies
	@echo "Installing project dependencies..."
	$(PIP) install -e .
	@echo "Dependencies installed."

# Build targets
build: check-uv ## Build the package
	@echo "Building package..."
	$(BUILD)
	@echo "Package built successfully."

# Run targets (removed - awslogin is an interactive CLI tool)


# Testing targets
test: install-test-deps ## Run unit tests without coverage
	@echo "Running unit tests..."
	$(PYTEST) saml2awsmulti/tests/ -v --junit-xml junit.xml

test-coverage: install-test-deps ## Run unit tests with coverage reporting
	@echo "Running unit tests with coverage..."
	$(PYTEST) saml2awsmulti/tests/ -v --cov=saml2awsmulti --cov-report=xml:coverage.xml --cov-report=term-missing --junit-xml junit.xml

# Linting targets
yamllint: ## Run yamllint on GitHub workflow files
	yamllint -c .github/linters/.yaml-lint.yaml .github/

# Cleanup targets
clean: ## Clean test artifacts, build artifacts and temporary files
	rm -rf .coverage*
	rm -rf coverage.xml
	rm -rf junit.xml
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Default target when no target is specified
.DEFAULT_GOAL := help
