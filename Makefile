.PHONY: help install run-api run-ui docker-up docker-down test clean

# Variables
PYTHON = python
VENV_DIR = venv
VENV_BIN = $(VENV_DIR)/Scripts

help: ## Show this help message
	@echo "============================================="
	@echo "🏥 MedNLP-RAG Engine - Developer Commands 🏥"
	@echo "============================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies in a virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	$(VENV_BIN)/pip install pytest flake8 black httpx

run-api: ## Run the FastAPI Backend backend
	$(VENV_BIN)/uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

run-ui: ## Run the Streamlit Frontend UI
	$(VENV_BIN)/streamlit run frontend/app.py

docker-up: ## Boot up the entire stack via Docker Compose
	docker-compose up --build -d

docker-down: ## Tear down the Docker Compose stack
	docker-compose down

test: ## Run the test suite
	$(VENV_BIN)/pytest tests/ -v

clean: ## Clean up virtual environment and cache files
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
