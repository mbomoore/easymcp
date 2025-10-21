.PHONY: help install install-dev test lint format clean demo verify

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=easymcp --cov-report=html --cov-report=term

lint:  ## Run linter
	ruff check .

lint-fix:  ## Run linter with auto-fix
	ruff check --fix .

format:  ## Format code
	ruff format .

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

demo:  ## Run demo script
	python demo.py

verify:  ## Run verification script
	python verify.py

init:  ## Initialize a new configuration
	python -m easymcp.cli init

build:  ## Build distribution packages
	python -m pip install --upgrade build
	python -m build

publish-test:  ## Publish to Test PyPI
	python -m pip install --upgrade twine
	python -m twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	python -m pip install --upgrade twine
	python -m twine upload dist/*

.DEFAULT_GOAL := help
