# {{project_name}} Makefile
# Author: {{author}}
# Created: {{date}}
# Based on: https://zenn.dev/loglass/articles/0016-make-makefile

.DEFAULT_GOAL := help

# Project configuration
PROJECT_NAME := {{project_name}}
PROJECT_TYPE := {{type}}

# Colors for output formatting
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m
BOLD := \033[1m

# Docker configuration (if type=docker)
DOCKER_IMAGE_NAME := $(PROJECT_NAME)
DOCKER_TAG := latest

# Node.js configuration (if type=node)
NODE_VERSION := 20
NPM_REGISTRY := https://registry.npmjs.org/

# Go configuration (if type=go)
GO_VERSION := 1.23
GO_BINARY := $(PROJECT_NAME)

# Python configuration (if type=python)
PYTHON_VERSION := 3.12
VENV_NAME := venv

## Development Environment ##

.PHONY: init
init: ## Initialize development environment
	@echo "$(CYAN)Initializing $(PROJECT_NAME) development environment...$(RESET)"
ifeq ($(PROJECT_TYPE),docker)
	@$(MAKE) docker-build
	@$(MAKE) docker-up
endif
ifeq ($(PROJECT_TYPE),node)
	@$(MAKE) deps-install
	@$(MAKE) deps-audit
endif
ifeq ($(PROJECT_TYPE),go)
	@$(MAKE) go-mod-tidy
	@$(MAKE) go-deps
endif
ifeq ($(PROJECT_TYPE),python)
	@$(MAKE) python-venv
	@$(MAKE) python-deps
endif
	@echo "$(GREEN)✓ Development environment initialized$(RESET)"

.PHONY: clean
clean: ## Clean up generated files and dependencies
	@echo "$(YELLOW)Cleaning up $(PROJECT_NAME)...$(RESET)"
ifeq ($(PROJECT_TYPE),docker)
	@$(MAKE) docker-clean
endif
ifeq ($(PROJECT_TYPE),node)
	@rm -rf node_modules package-lock.json
	@rm -rf dist build coverage
endif
ifeq ($(PROJECT_TYPE),go)
	@go clean -cache -modcache -testcache
	@rm -f $(GO_BINARY)
endif
ifeq ($(PROJECT_TYPE),python)
	@rm -rf $(VENV_NAME) __pycache__ *.pyc .pytest_cache
	@find . -name "*.pyc" -delete
endif
	@rm -rf tmp logs *.log
	@echo "$(GREEN)✓ Cleanup completed$(RESET)"

## Docker Tasks ##

.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "$(CYAN)Building Docker image $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)...$(RESET)"
	@docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) .
	@echo "$(GREEN)✓ Docker image built successfully$(RESET)"

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "$(CYAN)Starting Docker containers...$(RESET)"
	@docker-compose up -d
	@echo "$(GREEN)✓ Docker containers started$(RESET)"

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "$(YELLOW)Stopping Docker containers...$(RESET)"
	@docker-compose down
	@echo "$(GREEN)✓ Docker containers stopped$(RESET)"

.PHONY: docker-logs
docker-logs: ## Show Docker container logs
	@docker-compose logs -f

.PHONY: docker-clean
docker-clean: ## Clean Docker images and containers
	@echo "$(YELLOW)Cleaning Docker resources...$(RESET)"
	@docker-compose down --rmi all --volumes --remove-orphans
	@docker system prune -f
	@echo "$(GREEN)✓ Docker cleanup completed$(RESET)"

## Node.js Tasks ##

.PHONY: deps-install
deps-install: ## Install Node.js dependencies
	@echo "$(CYAN)Installing Node.js dependencies...$(RESET)"
	@npm install
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

.PHONY: deps-update
deps-update: ## Update Node.js dependencies
	@echo "$(CYAN)Updating Node.js dependencies...$(RESET)"
	@npm update
	@npm audit fix
	@echo "$(GREEN)✓ Dependencies updated$(RESET)"

.PHONY: deps-audit
deps-audit: ## Audit Node.js dependencies for vulnerabilities
	@echo "$(CYAN)Auditing dependencies...$(RESET)"
	@npm audit
	@echo "$(GREEN)✓ Dependency audit completed$(RESET)"

## Go Tasks ##

.PHONY: go-build
go-build: ## Build Go binary
	@echo "$(CYAN)Building Go binary...$(RESET)"
	@go build -o $(GO_BINARY) .
	@echo "$(GREEN)✓ Go binary built: $(GO_BINARY)$(RESET)"

.PHONY: go-run
go-run: ## Run Go application
	@echo "$(CYAN)Running Go application...$(RESET)"
	@go run .

.PHONY: go-mod-tidy
go-mod-tidy: ## Tidy Go modules
	@echo "$(CYAN)Tidying Go modules...$(RESET)"
	@go mod tidy
	@echo "$(GREEN)✓ Go modules tidied$(RESET)"

.PHONY: go-deps
go-deps: ## Download Go dependencies
	@echo "$(CYAN)Downloading Go dependencies...$(RESET)"
	@go mod download
	@echo "$(GREEN)✓ Go dependencies downloaded$(RESET)"

## Python Tasks ##

.PHONY: python-venv
python-venv: ## Create Python virtual environment
	@echo "$(CYAN)Creating Python virtual environment...$(RESET)"
	@python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	@echo "$(GREEN)✓ Virtual environment created: $(VENV_NAME)$(RESET)"

.PHONY: python-deps
python-deps: ## Install Python dependencies
	@echo "$(CYAN)Installing Python dependencies...$(RESET)"
	@. $(VENV_NAME)/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN)✓ Python dependencies installed$(RESET)"

.PHONY: python-run
python-run: ## Run Python application
	@echo "$(CYAN)Running Python application...$(RESET)"
	@. $(VENV_NAME)/bin/activate && python main.py

## Testing ##

.PHONY: test
test: ## Run all tests
	@echo "$(CYAN)Running tests for $(PROJECT_NAME)...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm test
endif
ifeq ($(PROJECT_TYPE),go)
	@go test -v ./...
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && pytest
endif
	@echo "$(GREEN)✓ All tests passed$(RESET)"

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	@echo "$(CYAN)Running tests in watch mode...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run test:watch
endif
ifeq ($(PROJECT_TYPE),go)
	@find . -name "*.go" | entr -r go test ./...
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && pytest-watch
endif

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(CYAN)Running test coverage...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run test:coverage
endif
ifeq ($(PROJECT_TYPE),go)
	@go test -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && pytest --cov=. --cov-report=html
endif
	@echo "$(GREEN)✓ Coverage report generated$(RESET)"

## Code Quality ##

.PHONY: lint
lint: ## Run code linting
	@echo "$(CYAN)Running code linting...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run lint
endif
ifeq ($(PROJECT_TYPE),go)
	@golangci-lint run
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && flake8 .
	@. $(VENV_NAME)/bin/activate && black --check .
endif
	@echo "$(GREEN)✓ Code linting completed$(RESET)"

.PHONY: format
format: ## Format code
	@echo "$(CYAN)Formatting code...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run format
endif
ifeq ($(PROJECT_TYPE),go)
	@go fmt ./...
	@goimports -w .
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && black .
	@. $(VENV_NAME)/bin/activate && isort .
endif
	@echo "$(GREEN)✓ Code formatting completed$(RESET)"

.PHONY: check
check: lint test ## Run all code quality checks
	@echo "$(GREEN)✓ All quality checks passed$(RESET)"

## Build and Release ##

.PHONY: build
build: ## Build the project
	@echo "$(CYAN)Building $(PROJECT_NAME)...$(RESET)"
ifeq ($(PROJECT_TYPE),docker)
	@$(MAKE) docker-build
endif
ifeq ($(PROJECT_TYPE),node)
	@npm run build
endif
ifeq ($(PROJECT_TYPE),go)
	@$(MAKE) go-build
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && python setup.py build
endif
	@echo "$(GREEN)✓ Build completed$(RESET)"

.PHONY: release
release: check build ## Create a release (run checks, build, and tag)
	@echo "$(CYAN)Creating release for $(PROJECT_NAME)...$(RESET)"
	@echo "$(YELLOW)Warning: This will create a git tag. Continue? [y/N]$(RESET)"
	@read -r CONTINUE && [ "$$CONTINUE" = "y" ] || exit 1
	@VERSION=$$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.1.0") && \
	echo "Current version: $$VERSION" && \
	echo "Enter new version (e.g., v1.0.0):" && \
	read -r NEW_VERSION && \
	git tag -a "$$NEW_VERSION" -m "Release $$NEW_VERSION" && \
	git push origin "$$NEW_VERSION"
	@echo "$(GREEN)✓ Release created successfully$(RESET)"

## Database ##

.PHONY: db-up
db-up: ## Start database services
	@echo "$(CYAN)Starting database services...$(RESET)"
	@docker-compose up -d db redis
	@echo "$(GREEN)✓ Database services started$(RESET)"

.PHONY: db-migrate
db-migrate: ## Run database migrations
	@echo "$(CYAN)Running database migrations...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run migrate
endif
ifeq ($(PROJECT_TYPE),go)
	@migrate -path ./migrations -database "$$DATABASE_URL" up
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && alembic upgrade head
endif
	@echo "$(GREEN)✓ Database migrations completed$(RESET)"

.PHONY: db-seed
db-seed: ## Seed database with initial data
	@echo "$(CYAN)Seeding database...$(RESET)"
ifeq ($(PROJECT_TYPE),node)
	@npm run seed
endif
ifeq ($(PROJECT_TYPE),go)
	@go run cmd/seed/main.go
endif
ifeq ($(PROJECT_TYPE),python)
	@. $(VENV_NAME)/bin/activate && python seed.py
endif
	@echo "$(GREEN)✓ Database seeded successfully$(RESET)"

## Monitoring and Logs ##

.PHONY: logs
logs: ## Show application logs
	@echo "$(CYAN)Showing logs for $(PROJECT_NAME)...$(RESET)"
ifeq ($(PROJECT_TYPE),docker)
	@$(MAKE) docker-logs
else
	@tail -f logs/*.log 2>/dev/null || echo "No log files found"
endif

.PHONY: status
status: ## Show project status
	@echo "$(BOLD)$(PROJECT_NAME) Status Report$(RESET)"
	@echo "$(CYAN)Project Type:$(RESET) $(PROJECT_TYPE)"
	@echo "$(CYAN)Git Status:$(RESET)"
	@git status --porcelain || echo "Not a git repository"
ifeq ($(PROJECT_TYPE),docker)
	@echo "$(CYAN)Docker Status:$(RESET)"
	@docker-compose ps 2>/dev/null || echo "Docker Compose not available"
endif
ifeq ($(PROJECT_TYPE),node)
	@echo "$(CYAN)Node.js Version:$(RESET)"
	@node --version 2>/dev/null || echo "Node.js not installed"
endif
ifeq ($(PROJECT_TYPE),go)
	@echo "$(CYAN)Go Version:$(RESET)"
	@go version 2>/dev/null || echo "Go not installed"
endif
ifeq ($(PROJECT_TYPE),python)
	@echo "$(CYAN)Python Version:$(RESET)"
	@python$(PYTHON_VERSION) --version 2>/dev/null || echo "Python $(PYTHON_VERSION) not installed"
endif

## Help ##

.PHONY: help
help: ## Show this help message
	@echo "$(BOLD)$(CYAN)$(PROJECT_NAME) - Available Commands$(RESET)"
	@echo ""
	@awk -f help.awk $(MAKEFILE_LIST) | less -R

.PHONY: help-simple
help-simple: ## Show simple help without colors
	@echo "$(PROJECT_NAME) - Available Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'