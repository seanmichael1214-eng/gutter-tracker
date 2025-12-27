# Claude AI Context - Gutter Tracker

This file contains context specifically for Claude AI coding sessions.

## App Overview

**Gutter Tracker** is a production Flask app for managing gutter installation/cleaning businesses.  
**Live URL:** https://gutter-tracker-app.fly.dev  
**Password:** NAO$  
**Status:** ✅ Production-ready, all features working

## Tech Stack

- **Backend:** Flask 3.1.2, SQLAlchemy
- **Database:** PostgreSQL (prod) / SQLite (dev)
- **AI:** Google Gemini API for estimates & photo analysis
- **Hosting:** Fly.io (512MB RAM, 1 Gunicorn worker)
- **Frontend:** Jinja2 templates, vanilla CSS/JS

## Quick Start

```bash
# Local development
make install    # Setup venv
make db-init    # Create database
make run        # Start server on :5001

# Testing
make test       # Run all tests
pytest tests/test_api_endpoints.py::test_specific  # Single test

# Deploy
flyctl deploy --app gutter-tracker-app
flyctl logs --app gutter-tracker-app
```

## Key Features

1. **Dashboard** - Job stats, revenue, quick actions
2. **Customers** - Add, edit, delete, search customers
3. **Jobs** - Create jobs, track status, add photos
4. **Calendar** - Monthly view of scheduled jobs (NEW!)
5. **Inventory** - AI-powered scanner, multi-user support
6. **Materials** - Materials database for jobs
7. **Reports** - Analytics and metrics
8. **Quick Estimate** - AI photo analysis for quotes
9. **Help** - AI chatbot support (Gemini)

## Critical Production Learnings

### Issues Encountered & Fixed

1. **Login Freeze Bug**
   - Templates referenced routes that didn't exist (`/quick-estimate`, `/help`)
   - **Lesson:** Always verify template links have corresponding routes

2. **Tab Navigation Crashes**
   - Missing `/materials` and `/reports` routes
   - **Fix:** Added routes in `app/routes.py`
   - **Lesson:** Grep templates for all `href` links when adding new pages

3. **Out of Memory (OOM)**
   - 256MB insufficient for 2 Gunicorn workers (~65MB each)
   - **Fix:** Increased to 512MB, reduced to 1 worker
   - **Config:** `fly.toml` + `fly_start.sh`

4. **Serverless Deployment Failures**
   - FileHandler incompatible with read-only filesystems
   - **Fix:** Use `StreamHandler()` in `app/__init__.py`

### Production Checklist

When adding new features:
- [ ] Add route to `app/routes.py`
- [ ] Create template if needed
- [ ] Update navigation in ALL templates
- [ ] Test locally with `make run`
- [ ] Write pytest test
- [ ] Deploy with `flyctl deploy`
- [ ] Verify all routes return 200 (not 404)
- [ ] Check logs for errors

## File Structure

**Key Files:**
- `app/routes.py` - All routes (440 lines, single blueprint)
- `app/models.py` - Database models (Customer, Job, InventoryItem, etc.)
- `app/__init__.py` - Flask factory, **uses StreamHandler for logs**
- `app/config.py` - Config, handles postgres:// → postgresql://
- `fly.toml` - Fly.io config (512MB memory, **uses Docker build**)
- `Dockerfile` - Docker build config (Python 3.11, Gunicorn on port 8080)
- `fly_start.sh` - Legacy startup script (replaced by Dockerfile CMD)

**Templates:**
All in `app/templates/`:
- dashboard.html, customers.html, jobs.html
- calendar.html (NEW - monthly job view)
- inventory.html, materials.html, reports.html
- quick_estimate.html, help.html

## Common Patterns

### Adding a Route
```python
@main.route("/new-feature")
@login_required
def new_feature():
    data = YourModel.query.all()
    return render_template("new_feature.html", data=data)
```

### Database Query with Relationships
```python
job = Job.query.get_or_404(job_id)
customer_name = job.customer.name  # Uses backref
```

### AI Integration
```python
from .ai import gemini_model

try:
    response = gemini_model.generate_content(prompt)
    return jsonify({"success": True, "data": response.text})
except Exception as e:
    current_app.logger.error(f"Gemini error: {e}")
    return jsonify({"success": False, "error": str(e)}), 500
```

## Troubleshooting

### Check if App is Running
```bash
curl -I https://gutter-tracker-app.fly.dev
# Should return: HTTP/2 200
```

### View Logs
```bash
flyctl logs --app gutter-tracker-app              # Live tail
flyctl logs --app gutter-tracker-app --no-tail    # Recent logs
```

### Test All Routes
```bash
for route in /dashboard /customers /jobs /calendar /inventory /materials /reports /quick-estimate /help; do
  echo "$route: $(curl -s -o /dev/null -w '%{http_code}' https://gutter-tracker-app.fly.dev$route)"
done
```

### Common Error Patterns
- **404 on route:** Route missing from `routes.py`
- **500 on page load:** Check logs, likely DB or template error
- **OOM crash:** Increase memory in `fly.toml`
- **Session lost:** `SECRET_KEY` changed or not set

## Environment Variables

**Development (.env):**
```bash
SECRET_KEY=dev-secret-key
APP_PASSWORD=NAO$
GEMINI_API_KEY=your-key-here
DATABASE_URL=sqlite:///../instance/gutter_tracker.db
```

**Production (Fly.io secrets):**
```bash
flyctl secrets list --app gutter-tracker-app
flyctl secrets set SECRET_KEY="..." --app gutter-tracker-app
```

## Code Style

- **Formatter:** Black (88 chars)
- **Linter:** Flake8
- **Imports:** stdlib, third-party, local (separated by blank lines)
- **Naming:** snake_case functions, PascalCase classes
- **Routes:** All in `main` blueprint, use `@login_required` for protected pages

## Customer Feedback Protocol

1. **Reproduce Issue:** Test locally or on production
2. **Check Logs:** `flyctl logs` for server errors
3. **Review Code:** Find relevant route/template
4. **Fix & Test:** Local first, then deploy
5. **Verify:** Test the specific user flow that failed
6. **Document:** Add to git commit message

## Recent Updates (Dec 27, 2025)

- ✅ **LATEST:** Switched from Paketo Buildpacks to Docker deployment (Google Container Registry deprecated)
- ✅ **LATEST:** Fixed deployment issues - app redeployed and verified working
- ✅ **LATEST:** Added calendar date filtering for jobs
- ✅ **LATEST:** Created comprehensive testing documentation (PRE_RELEASE_TEST_GUIDE.md, automated_test.py)
- ✅ Fixed chatbot context - Gemini now has comprehensive Gutter Tracker app context
- ✅ Fixed photo upload - Mobile users can now choose camera OR gallery
- ✅ Cleaned up duplicate AI agent files (removed .ai-team-master directory)
- ✅ Fixed all navigation crashes (added missing routes)
- ✅ Optimized memory (512MB, 1 worker)
- ✅ Added calendar view for scheduled jobs
- ✅ All routes tested and working
- ✅ Production stable, all tests passing (20/20)

## Working with Claude

**Best Practices:**
1. Always check existing files before creating new ones
2. Test routes locally before deploying
3. Verify template links match actual routes
4. Use `make test` before committing
5. Check Fly.io logs after deployment
6. Keep AGENTS.md and CLAUDE.md updated

**Remember:**
- This app is PRODUCTION - test thoroughly before deploying
- Customer password is NAO$ - don't change without coordination
- Database is PostgreSQL in production - SQLite in development
- Logs use StreamHandler (not FileHandler) for serverless compatibility
- **Deployment uses Docker (not Paketo Buildpacks)** - Dockerfile defines port 8080, 1 worker, 2 threads
- Always update navigation in ALL templates when adding routes

---

For detailed code guidelines, see `/AGENTS.md`  
For production deployment, use Fly.io commands in AGENTS.md
