.PHONY: install dev test lint format docker-up docker-down migrate seed clean

install:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt -r requirements-dev.txt

dev:
	. venv/bin/activate && uvicorn app.main:app --reload --port 8000

test:
	. venv/bin/activate && pytest tests/ --cov=app --cov-report=term-missing

lint:
	. venv/bin/activate && ruff check app tests && mypy app tests

format:
	. venv/bin/activate && ruff format app tests

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	@echo "Running SQL Migrations in order..."
	# Normally runs migrations via alembic/custom runner script

seed:
	. venv/bin/activate && python scripts/seed_schemes.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov coverage.xml
