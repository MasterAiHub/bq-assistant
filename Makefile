.PHONY: install test run docker-build docker-run clean

install:
	pip install -r requirements.txt -r security-requirements.txt

test:
	pytest

run:
	uvicorn backend.app:app --reload

docker-build:
	docker build -t bq-assistant .

docker-run:
	docker run -p 8000:8000 bq-assistant

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf logs/*.log
