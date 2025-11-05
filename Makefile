# Makefile for AI Agent

.PHONY: help install init run-api run-cli test clean lint format docs

help:
	@echo "AI Agent - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make init       - Initialize database"
	@echo "  make run-api    - Start API server"
	@echo "  make run-cli    - Run CLI in interactive mode"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make docs       - Generate documentation"
	@echo "  make clean      - Clean generated files"
	@echo ""

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "✓ Dependencies installed"

init:
	@echo "Initializing AI Agent..."
	@python cli.py init
	@echo "✓ Initialization complete"

run-api:
	@echo "Starting API server..."
	@python -m api.main

run-cli:
	@echo "Starting CLI in interactive mode..."
	@python cli.py chat

test:
	@echo "Running tests..."
	@pytest -v

test-cov:
	@echo "Running tests with coverage..."
	@pytest --cov=. --cov-report=html --cov-report=term

lint:
	@echo "Running linter..."
	@pylint core/ api/ database/

format:
	@echo "Formatting code..."
	@black .
	@echo "✓ Code formatted"

docs:
	@echo "Generating documentation..."
	@mkdocs build
	@echo "✓ Documentation generated in site/"

clean:
	@echo "Cleaning generated files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf build/ dist/ site/ htmlcov/ .coverage
	@echo "✓ Cleaned"

.DEFAULT_GOAL := help






