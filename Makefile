.PHONY: help init build up down restart logs logs-engine logs-bridge logs-rag logs-dashboard ps seed test test-rag test-engine demo clean

.DEFAULT_GOAL := help

help: ## Show this help menu
	@python -c "import re; print('\nLedgerGuard - Available Make Targets:\n'); [print(f'  {m.group(1):<16} {m.group(2)}') for line in open('Makefile') if (m := re.match(r'^([a-zA-Z0-9_-]+):.*?## (.*)$$', line))]; print()"

init: ## Initialize .env and credential templates if missing
	@python -c "import os, shutil; os.path.exists('.env') or shutil.copy('.env.example', '.env'); print('[ok] .env configured')"
	@python -c "import os, shutil; os.path.exists('integrations/audit/sheets-creds.json') or shutil.copy('integrations/audit/sheets-creds.json.example', 'integrations/audit/sheets-creds.json'); print('[ok] sheets-creds.json configured')"

build: ## Build all Docker containers
	docker compose build

up: init ## Start all infrastructure and microservices in background
	docker compose up -d

down: ## Stop all running services
	docker compose down

restart: down up ## Restart the full stack

ps: ## Check status of all containers
	docker compose ps

logs: ## Stream logs from all services
	docker compose logs -f

logs-engine: ## Stream logs from Go reconciliation engine
	docker compose logs -f reconciliation-engine

logs-bridge: ## Stream logs from Kafka-to-n8n event bridge
	docker compose logs -f kafka-http-bridge

logs-rag: ## Stream logs from Policy RAG service
	docker compose logs -f policy-rag-service

logs-dashboard: ## Stream logs from Streamlit dashboard
	docker compose logs -f dashboard

seed: ## Generate mock transactions for testing
	python data/fixtures/generate-transactions.py

test: test-rag test-engine ## Run all unit tests across services

test-rag: ## Run Policy RAG service unit tests
	python -c "import sys, pytest; sys.path.insert(0, 'services/policy-rag-service'); sys.exit(pytest.main(['-q', 'services/policy-rag-service/tests']))"

test-engine: ## Run Go reconciliation engine unit tests
	go test -C services/reconciliation-engine ./...

demo: ## Print the golden-path verification checklist
	@echo '[1/4] Services: docker compose up --build'
	@echo '[2/4] Event: reconciliation-engine publishes demo-evt-001'
	@echo '[3/4] Audit: inspect audit_data/audit.csv for demo-evt-001'
	@echo '[4/4] Dashboard: refresh http://localhost:8501 and confirm metrics changed'

clean: ## Stop containers and prune volumes/orphans
	docker compose down -v --remove-orphans
