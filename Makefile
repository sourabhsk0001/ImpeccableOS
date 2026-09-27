.PHONY: help up down restart logs build test lint clean seed

help:
	@echo "ImpeccableOS - Developer Command Interface"
	@echo "--------------------------------------------------"
	@echo "make up        - Start all services (PostgreSQL 16, pgvector, API, Web)"
	@echo "make down      - Stop all container services"
	@echo "make restart   - Restart all services"
	@echo "make logs      - Tail logs across services"
	@echo "make test      - Run automated test suite (backend unit & integration)"
	@echo "make seed      - Seed DAG taxonomy and reference corpus into PostgreSQL"
	@echo "make lint      - Run linters across python and frontend codebases"
	@echo "make clean     - Remove caches, pycache, build artifacts"

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

build:
	docker compose build

test:
	cd apps/api && pytest -v --cov=src

seed:
	cd apps/api && python ../../scripts/seed_database.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
