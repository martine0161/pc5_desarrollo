.PHONY: help test run

help:
	@echo "Comandos disponibles:"
	@echo "  make test    - Ejecutar tests"
	@echo "  make run     - Ejecutar API"

test:
	python -m pytest tests/ -v --cov=app --cov-report=term

run:
	python -m uvicorn app.main:app --reload
