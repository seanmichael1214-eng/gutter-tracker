# Agent Development Guide - Gutter Tracker

This guide is for AI coding agents working on the Gutter Tracker Flask application.

## Quick Reference

**Stack:** Flask 3.1.2, SQLAlchemy, PostgreSQL/SQLite, Google Gemini AI  
**Python Version:** 3.10+  
**Code Style:** Black (line length 88), Flake8  
**Deployment:** Fly.io (production), local SQLite (development)

---

## Build Commands

### Setup & Installation
```bash
make install          # Create venv and install all dependencies
make db-init          # Initialize database with tables
```

### Development
```bash
make run              # Start local dev server (http://127.0.0.1:5001)
make test             # Run all tests with pytest
make lint             # Run flake8 linter
make format           # Format code with black
```

### Single Test Execution
```bash
# Run specific test file
source .venv/bin/activate && pytest tests/test_api_endpoints.py

# Run specific test function
source .venv/bin/activate && pytest tests/test_api_endpoints.py::test_chat_inventory_add

# Run with verbose output
source .venv/bin/activate && pytest -v tests/test_flask.py

# Run tests matching pattern
source .venv/bin/activate && pytest -k "inventory"
```

### Database
```bash
make db-init          # Initialize tables (uses scripts/init_db.py)
make clean            # Remove venv, instance/, and cached files
```

---

## Project Structure

```
gutter-tracker/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # All HTTP routes (main blueprint)
│   ├── models.py           # SQLAlchemy models
│   ├── extensions.py       # Shared extensions (db)
│   ├── config.py           # Configuration
│   ├── ai.py               # Gemini AI integration
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS assets
│   └── tools/              # Expert review & upgrade tools
├── tests/                  # Pytest test files
├── scripts/                # Utility scripts (init_db.py)
├── instance/               # SQLite database (gitignored)
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── Makefile               # Build commands
```

---

## Code Style Guidelines

### Imports
- **Standard library first**, then third-party, then local imports
- Group Flask imports together at the top
- Use relative imports within `app/` package (e.g., `from .models import Customer`)
- Example:
```python
from datetime import datetime
from functools import wraps

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from .extensions import db
from .models import Customer, Job
```

### Formatting
- **Black formatter** with 88 character line length (run `make format`)
- **4 spaces** for indentation (no tabs)
- **Double quotes** for strings (Black standard)
- **Trailing commas** in multi-line structures

### Naming Conventions
- **Classes:** PascalCase (`Customer`, `InventoryItem`)
- **Functions/methods:** snake_case (`get_ai_estimate`, `login_required`)
- **Variables:** snake_case (`current_id`, `owner_id`)
- **Constants:** UPPER_SNAKE_CASE (`BASE_URL`, `APP_PASSWORD`)
- **Private methods:** prefix with `_` (`_parse_kv`)
- **Blueprint names:** lowercase (`main`)

### Database Models
- Use `db.Model` base class
- Primary keys: `id = db.Column(db.Integer, primary_key=True)`
- Foreign keys: descriptive names (`customer_id`, `owner_id`)
- Relationships: use `backref` for bidirectional access
- Timestamps: use `default=datetime.utcnow` (no parentheses)
- Example:
```python
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
```

### Flask Routes
- Use `@main.route()` decorator (main blueprint)
- Add `@login_required` for protected routes
- Return early for error cases
- Use `jsonify()` for JSON responses
- Use `redirect(url_for())` for redirects
- Example:
```python
@main.route("/inventory/add", methods=["POST"])
@login_required
def add_inventory():
    if not request.form.get("name"):
        return jsonify({"error": "Name required"}), 400
    
    item = InventoryItem(
        name=request.form["name"],
        owner_id=session.get("current_owner_id")
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("main.inventory"))
```

### Error Handling
- Use try/except for external API calls (Gemini)
- Return JSON errors with appropriate status codes
- Log errors using `current_app.logger`
- Provide fallback behavior when possible
- Example:
```python
try:
    response = gemini_model.generate_content(prompt)
    return jsonify({"success": True, "data": response.text})
except Exception as e:
    current_app.logger.error(f"Gemini API error: {e}")
    return jsonify({"success": False, "error": str(e)}), 500
```

---

## Testing Guidelines

- **Test file naming:** `test_*.py` in `tests/` directory
- **Use pytest fixtures** for app and database setup
- **Test all API endpoints** with valid and invalid inputs
- **Mock external APIs** (Gemini) to avoid rate limits
- Keep tests **fast and isolated** (use SQLite in-memory for tests)
- Example:
```python
def test_add_inventory(client):
    response = client.post('/inventory/add', data={
        'name': 'Test Item',
        'quantity': 10,
        'owner_id': 1
    })
    assert response.status_code == 302  # Redirect
```

---

## Environment Variables

Required in `.env` (development) and Fly.io secrets (production):
- `GEMINI_API_KEY` - Google Gemini API key
- `SECRET_KEY` - Flask session secret (generate with `secrets.token_hex(32)`)
- `APP_PASSWORD` - Login password (default: `nao$`)
- `DATABASE_URL` - PostgreSQL URL (production) or SQLite path (dev)

---

## Key Features & Architecture

### Multi-User Inventory
- Each `InventoryItem` has `owner_id` FK to `Customer`
- Session stores `current_owner_id` for active user context
- Filter all inventory queries by `owner_id`

### Chat-Driven Commands
- `/api/chat` endpoint parses text commands
- Format: `inventory-add name=X, quantity=Y, owner_id=Z`
- Simple key=value parser in `routes.py`

### AI Integration
- `app/ai.py` wraps Google Gemini API
- Functions: `get_ai_estimate()`, `analyze_photo()`
- Always include error handling and fallbacks

### Expert Review System
- `app/tools/experts.py` - 5 internal expert personas
- `app/tools/upgrade_engine.py` - Generate upgrade plans
- Not exposed in UI, used for development guidance

---

## Common Tasks

**Add a new route:**
1. Add function in `app/routes.py` with `@main.route()` decorator
2. Import required models from `app/models.py`
3. Add `@login_required` if authentication needed
4. Write test in `tests/test_*.py`

**Add a new model:**
1. Define class in `app/models.py` inheriting `db.Model`
2. Run `make db-init` to create tables (drops existing!)
3. Update relationships in related models if needed

**Debug locally:**
1. `make run` starts dev server with auto-reload
2. Check logs in terminal
3. SQLite database at `instance/gutter_tracker.db`
4. Use `make db-init` to reset database

---

## Deployment

**Fly.io (Production):**
- App: `gutter-tracker-app.fly.dev`
- Database: PostgreSQL (gutter-tracker-db)
- Deploy: `flyctl deploy --app gutter-tracker-app`
- Logs: `flyctl logs --app gutter-tracker-app`
- Scale: `flyctl scale count 1 --app gutter-tracker-app`

**Local (Development):**
- Run: `make run`
- Test: `make test`
- DB: SQLite in `instance/` directory
