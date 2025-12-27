# Agent Development Guide - Gutter Tracker

This guide is for AI coding agents working on the Gutter Tracker Flask application. The app is **production-ready** and deployed at https://gutter-tracker-app.fly.dev.

## Quick Reference

**Stack:** Flask 3.1.2, SQLAlchemy, PostgreSQL/SQLite, Google Gemini AI  
**Python Version:** 3.10+  
**Code Style:** Black (line length 88), Flake8  
**Production:** Fly.io (512MB RAM, 1 worker) | Database: PostgreSQL  
**Development:** SQLite (instance/gutter_tracker.db)

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

## Production Deployment

### Fly.io Commands
```bash
# Deploy to production
flyctl deploy --app gutter-tracker-app

# View logs (live tail)
flyctl logs --app gutter-tracker-app

# View recent logs
flyctl logs --app gutter-tracker-app --no-tail

# Check app status
flyctl status --app gutter-tracker-app

# SSH into machine
flyctl ssh console --app gutter-tracker-app

# Scale resources
flyctl scale memory 512 --app gutter-tracker-app
flyctl scale count 1 --app gutter-tracker-app
```

### Environment Variables (Fly.io Secrets)
```bash
# List secrets
flyctl secrets list --app gutter-tracker-app

# Set secret
flyctl secrets set SECRET_KEY="..." --app gutter-tracker-app
flyctl secrets set APP_PASSWORD="NAO$" --app gutter-tracker-app
flyctl secrets set GEMINI_API_KEY="..." --app gutter-tracker-app
```

---

## Project Structure

```
gutter-tracker/
├── app/
│   ├── __init__.py         # Flask app factory (CRITICAL: StreamHandler for serverless)
│   ├── routes.py           # All HTTP routes (main blueprint)
│   ├── models.py           # SQLAlchemy models
│   ├── extensions.py       # Shared extensions (db)
│   ├── config.py           # Configuration (handles postgres:// → postgresql://)
│   ├── ai.py               # Gemini AI integration
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS assets
│   └── tools/              # Expert review & upgrade tools
├── tests/                  # Pytest test files
├── scripts/                # Utility scripts (init_db.py)
├── instance/               # SQLite database (gitignored)
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── fly.toml               # Fly.io configuration
├── fly_start.sh           # Fly.io startup script
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
- **Routes:** kebab-case URLs (`/quick-estimate`, `/customers/add`)

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
- **CRITICAL:** When adding new routes, ensure templates that link to them exist
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
- **Production:** StreamHandler instead of FileHandler (read-only filesystem)
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

## Troubleshooting Guide

### Common Issues & Fixes

**1. Login Freeze / Page Won't Load**
- **Cause:** Missing route handlers that templates reference
- **Fix:** Check templates for `href` links, ensure all routes exist in `routes.py`
- **Example:** Added `/materials`, `/reports`, `/calendar` routes to fix tab crashes

**2. Out of Memory (OOM) on Fly.io**
- **Cause:** Insufficient RAM for Gunicorn workers
- **Fix:** Increase memory in `fly.toml` (`memory = "512mb"`)
- **Fix:** Reduce workers in `fly_start.sh` (`--workers 1`)
- **Symptoms:** `Worker sent SIGKILL! Perhaps out of memory?` in logs

**3. Database Connection Errors**
- **Cause:** PostgreSQL URL format issue (postgres:// vs postgresql://)
- **Fix:** `app/config.py` handles conversion automatically
- **Check:** Environment variable `DATABASE_URL` is set correctly

**4. 500 Error on Serverless (Vercel)**
- **Cause:** FileHandler trying to write to read-only filesystem
- **Fix:** Use `StreamHandler()` instead in `app/__init__.py`
- **Status:** Already fixed in production code

**5. AI Features Not Working**
- **Cause:** Missing or invalid `GEMINI_API_KEY`
- **Check:** `flyctl secrets list --app gutter-tracker-app`
- **Fix:** Set key with `flyctl secrets set GEMINI_API_KEY="..."`

### Viewing Logs

```bash
# Live tail logs
flyctl logs --app gutter-tracker-app

# Last 100 lines
flyctl logs --app gutter-tracker-app --no-tail | tail -100

# Filter by error level
flyctl logs --app gutter-tracker-app | grep -i error

# Check specific time range (use timestamps from logs)
flyctl logs --app gutter-tracker-app --no-tail | grep "2025-12-27"
```

### Debugging Steps

1. **Check if app is running:**
   ```bash
   curl -I https://gutter-tracker-app.fly.dev
   ```

2. **Verify all routes:**
   ```bash
   for route in /dashboard /customers /jobs /calendar /inventory /materials /reports /quick-estimate /help; do
     echo -n "$route: "
     curl -s -o /dev/null -w "%{http_code}" "https://gutter-tracker-app.fly.dev$route"
     echo ""
   done
   ```

3. **Test locally:**
   ```bash
   make run
   # Visit http://127.0.0.1:5001
   # Login password: NAO$
   ```

4. **Check database:**
   ```bash
   # Local
   sqlite3 instance/gutter_tracker.db ".tables"
   
   # Production (via Fly.io proxy)
   flyctl postgres connect -a gutter-tracker-db
   ```

---

## Key Features & Architecture

### Authentication
- Simple password-based auth via `APP_PASSWORD` env var
- Session-based with Flask sessions
- `@login_required` decorator protects routes

### Multi-User Inventory
- Each `InventoryItem` has `owner_id` FK to `Customer`
- Session stores `current_owner_id` for active user context
- Filter all inventory queries by `owner_id`

### Calendar View
- Month-based calendar showing scheduled jobs
- Color-coded by status (scheduled/in-progress/completed)
- Clickable dates navigate to jobs for that day
- Previous/Next month navigation

### Chat-Driven Commands
- `/api/chat` endpoint parses text commands
- Format: `inventory-add name=X, quantity=Y, owner_id=Z`
- Simple key=value parser in `routes.py`

### AI Integration
- `app/ai.py` wraps Google Gemini API
- Functions: `get_ai_estimate()`, `analyze_photo()`
- Always include error handling and fallbacks
- Requires `GEMINI_API_KEY` environment variable

---

## Common Tasks

### Add a New Route
1. Add function in `app/routes.py` with `@main.route()` decorator
2. Import required models from `app/models.py`
3. Add `@login_required` if authentication needed
4. **CRITICAL:** If templates link to this route, ensure route exists FIRST
5. Add navigation link to relevant templates
6. Write test in `tests/test_*.py`
7. Deploy: `flyctl deploy --app gutter-tracker-app`

### Add Navigation Link
Update these templates to add new nav items:
- `app/templates/dashboard.html`
- `app/templates/customers.html`
- `app/templates/jobs.html`
- `app/templates/calendar.html`
- `app/templates/inventory.html`
- `app/templates/materials.html`
- `app/templates/reports.html`
- `app/templates/quick_estimate.html`
- `app/templates/help.html`

### Add a New Model
1. Define class in `app/models.py` inheriting `db.Model`
2. Run `make db-init` to create tables locally (drops existing!)
3. Update relationships in related models if needed
4. For production, tables auto-created by `fly_start.sh` on deploy

### Handle Customer Feedback
1. **Bug Report:** Check logs first (`flyctl logs`)
2. **Feature Request:** Add to issues/notes, discuss scope
3. **UI Issue:** Test locally, check browser console for errors
4. **Performance:** Check Fly.io metrics, consider scaling

### Deploy Changes
```bash
# 1. Commit changes
git add .
git commit -m "Description of changes"

# 2. Deploy to Fly.io
flyctl deploy --app gutter-tracker-app

# 3. Verify deployment
curl -I https://gutter-tracker-app.fly.dev

# 4. Check logs for errors
flyctl logs --app gutter-tracker-app --no-tail | tail -20
```

---

## Production Status

**URL:** https://gutter-tracker-app.fly.dev  
**Password:** `NAO$`  
**Database:** PostgreSQL on Fly.io  
**Memory:** 512MB  
**Workers:** 1 Gunicorn worker  
**Status:** ✅ All features working, no known bugs

### All Routes (Tested & Working)
- `/` - Splash page
- `/login` - Authentication
- `/dashboard` - Main dashboard with stats
- `/customers` - Customer management
- `/jobs` - Job tracking
- `/calendar` - **NEW** Calendar view of scheduled jobs
- `/inventory` - Inventory with AI scanner
- `/materials` - Materials database
- `/reports` - Analytics & reports
- `/quick-estimate` - Photo-based estimates
- `/help` - AI chatbot support

### Recent Fixes (Dec 27, 2025)
1. ✅ Fixed login freeze - added missing `/quick-estimate` and `/help` routes
2. ✅ Fixed serverless deployment - switched to StreamHandler
3. ✅ Fixed OOM crashes - increased memory to 512MB, reduced to 1 worker
4. ✅ Fixed tab navigation - added missing `/materials` and `/reports` routes
5. ✅ Added calendar feature - monthly view of scheduled jobs

---

## Support & Resources

- **Production App:** https://gutter-tracker-app.fly.dev
- **Fly.io Dashboard:** https://fly.io/apps/gutter-tracker-app
- **Password:** NAO$ (stored in `APP_PASSWORD` secret)
- **This Guide:** `/AGENTS.md`
- **Git History:** Use `git log` for recent changes and fixes
