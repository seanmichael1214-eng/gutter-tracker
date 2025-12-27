.PHONY: install run test lint db-init

# ==============================================================================
# VIRTUAL ENVIRONMENT
# ==============================================================================

VENV_NAME ?= .venv
PYTHON ?= python3
VENV_ACTIVATE = . $(VENV_NAME)/bin/activate

# ==============================================================================
# COMMANDS
# ==============================================================================

install:
	@echo "Installing dependencies..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@$(VENV_ACTIVATE) && pip install --upgrade pip
	@$(VENV_ACTIVATE) && pip install -r requirements.txt

run:
	@echo "Starting the application..."
	@$(VENV_ACTIVATE) && python run.py

test:
	@echo "Running tests..."
	@$(VENV_ACTIVATE) && pytest

format:
	@echo "Formatting code..."
	@$(VENV_ACTIVATE) && black .

lint:
	@echo "Linting code..."
	@$(VENV_ACTIVATE) && flake8 .

db-init:
	@echo "Initializing the database..."
	@$(VENV_ACTIVATE) && python scripts/init_db.py

# These are placeholders, you might want to use a tool like Alembic for migrations
db-migrate:
	@echo "Creating database migration..."
	@echo "Not implemented yet. Consider using a tool like Alembic."

db-upgrade:
	@echo "Upgrading the database..."
	@echo "Not implemented yet. Consider using a tool like Alembic."

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_NAME)
	@rm -rf instance
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete

help:
	@echo "Available commands:"
	@echo "  install      : Create a virtual environment and install dependencies"
	@echo "  run          : Run the application"
	@echo "  test         : Run tests"
	@echo "  lint         : Lint the code"
	@echo "  db-init      : Initialize the database"
	@echo "  db-migrate   : (Placeholder) Create a database migration"
	@echo "  db-upgrade   : (Placeholder) Upgrade the database"
	@echo "  clean        : Remove virtual environment and other generated files"
	@echo "  help         : Show this help message"

