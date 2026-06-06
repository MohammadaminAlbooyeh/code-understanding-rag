.PHONY: install run-backend run-frontend test lint clean docker-build docker-up

install:
	pip install -r requirements.txt
	cd frontend && npm install

run-backend:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	cd frontend && npm start

test:
	pytest tests/

lint:
	ruff check backend/
	cd frontend && npm run lint

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf frontend/node_modules

docker-build:
	docker-compose build

docker-up:
	docker-compose up

seed:
	python scripts/seed_data.py

index:
	python scripts/index_codebase.py

benchmark:
	python scripts/benchmark.py
