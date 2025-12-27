#!/bin/bash
# AI Agent Documentation Initializer
# Usage: ./init-ai-docs.sh [project-name] [tech-stack]

PROJECT_NAME="${1:-my-project}"
TECH_STACK="${2:-Python/Flask}"

echo "🤖 Initializing AI agent documentation for: $PROJECT_NAME"

# Create AGENTS.md
cat > AGENTS.md << 'EOF'
# AGENTS.md - Development Guide
> Main reference for all AI agents working on this project

## Project Overview
**Name:** PROJECT_NAME_PLACEHOLDER
**Tech Stack:** TECH_STACK_PLACEHOLDER
**Created:** $(date +%Y-%m-%d)
**Purpose:** [Describe what this project does]

## Quick Start
```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Development
make run          # Start dev server
make test         # Run tests
make format       # Format code
make lint         # Lint code

# Deployment
make deploy       # Deploy to production
```

## Project Structure
```
project/
├── app/              # Main application code
├── tests/            # Test files
├── docs/             # Documentation
├── .venv/            # Virtual environment (gitignored)
├── requirements.txt  # Dependencies
└── Makefile         # Common commands
```

## Key Commands
| Command | Purpose |
|---------|---------|
| `make run` | Start development server |
| `make test` | Run all tests |
| `make deploy` | Deploy to production |

## Important Files
- `app/__init__.py` - Application factory
- `app/routes.py` - Route definitions
- `app/models.py` - Database models
- `config.py` - Configuration

## Development Workflow
1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test: `make test`
3. Format code: `make format`
4. Commit with clear message
5. Deploy: `make deploy`

## Environment Variables
```bash
# Development
DATABASE_URL=sqlite:///dev.db
SECRET_KEY=dev-secret-key
DEBUG=True

# Production
DATABASE_URL=postgresql://...
SECRET_KEY=<secure-key>
DEBUG=False
```

## Testing
```bash
# All tests
pytest

# Specific test file
pytest tests/test_routes.py

# Specific test
pytest tests/test_routes.py::test_homepage

# With coverage
pytest --cov=app tests/
```

## Code Style
- **Python:** Black formatter, Flake8 linter
- **Max line length:** 100 characters
- **Import order:** stdlib, third-party, local
- **Docstrings:** Google style

## Git Workflow
```bash
# Feature development
git checkout -b feature/feature-name
git add .
git commit -m "Add feature: description"
git push origin feature/feature-name

# After merge
git checkout main
git pull origin main
```

## Production Details
- **URL:** https://your-app.example.com
- **Platform:** [Fly.io / Heroku / AWS / etc]
- **Database:** [PostgreSQL / MySQL / etc]
- **Monitoring:** [Where to check logs/metrics]

## Common Issues
See TROUBLESHOOTING.md for detailed solutions.

## Last Updated
- Date: $(date +%Y-%m-%d)
- By: [Your name or AI agent]
- Changes: Initial setup

---
**For AI Agents:** This is your primary reference. Read this first in every session.
EOF

# Create CLAUDE.md
cat > CLAUDE.md << 'EOF'
# CLAUDE.md - Claude CLI Context
> Quick reference for Claude Code CLI sessions

## Quick Commands
```bash
# Start here every session
cd /path/to/PROJECT_NAME_PLACEHOLDER
source .venv/bin/activate

# Test everything works
make test

# Check git status
git status
git log --oneline -5
```

## What Claude Should Know

### Project Context
- **This is:** [Brief 1-line description]
- **User wants:** [What user is building/solving]
- **Current status:** [Development / Staging / Production]

### Critical Files
1. **AGENTS.md** - Read this first for full context
2. **TROUBLESHOOTING.md** - Check when user reports issues
3. **app/routes.py** - Main application logic
4. **requirements.txt** - Dependencies

### Common Patterns in This Project

#### Adding a New Route
```python
# In app/routes.py
@main.route("/new-route")
@login_required
def new_route():
    return render_template("new_route.html")
```

#### Adding a New Model
```python
# In app/models.py
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

#### Adding a Test
```python
# In tests/test_routes.py
def test_new_route(client):
    response = client.get("/new-route")
    assert response.status_code == 200
```

### User Preferences
- **Communication style:** Concise, technical
- **No emojis** unless requested
- **Always test** before saying "done"
- **Explain changes** with file:line references

### Session Workflow
1. Check `git status` and recent commits
2. Read user request carefully
3. Use TodoWrite to plan if complex (3+ steps)
4. Make changes incrementally
5. Test after each change
6. Commit with clear messages
7. Summarize what was done

### What NOT to Do
- ❌ Don't create files unnecessarily
- ❌ Don't use emojis unless asked
- ❌ Don't skip testing
- ❌ Don't make up values - ask user if unclear
- ❌ Don't commit without testing

### Production Safety
- ✅ Always run tests before deploying
- ✅ Check logs after deployment
- ✅ Verify all routes work
- ✅ Never commit secrets/passwords

### Emergency Contacts
If something breaks:
1. Check TROUBLESHOOTING.md
2. View logs: `make logs`
3. Rollback: `git revert HEAD`
4. Notify user immediately

---
**Claude:** Start every session by checking git status and reading recent commits.
EOF

# Create GEMINI.md
cat > GEMINI.md << 'EOF'
# GEMINI.md - Gemini AI Context
> Context for Gemini CLI and Gemini Code Assist

## Gemini-Specific Features

### AI Integration Points
[Document if your project uses Gemini API]

```python
# Example Gemini API usage in this project
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Usage example
response = model.generate_content("Prompt here")
```

### Environment Setup
```bash
# Required for Gemini features
export GEMINI_API_KEY=your-key-here

# Test Gemini connection
python -c "import google.generativeai as genai; print('Gemini OK')"
```

### Quick Start for Gemini
```bash
cd /path/to/PROJECT_NAME_PLACEHOLDER
source .venv/bin/activate
make test
```

### Key Context
- Read **AGENTS.md** first for complete project context
- This project uses Gemini for: [list features if applicable]
- Gemini API limits: [document rate limits if known]

### Common Gemini Tasks
1. **Code generation** - Follow project patterns in AGENTS.md
2. **Bug fixing** - Check TROUBLESHOOTING.md first
3. **Testing** - Always run `make test` after changes
4. **Documentation** - Update relevant .md files

### Gemini Best Practices
- Use multimodal features for image analysis
- Implement proper error handling for API calls
- Cache responses when possible
- Monitor token usage

---
**Gemini:** You're great at creative solutions and multimodal tasks. Use AGENTS.md for project structure.
EOF

# Create TROUBLESHOOTING.md
cat > TROUBLESHOOTING.md << 'EOF'
# TROUBLESHOOTING.md
> Common Issues & Solutions

## 🔍 Quick Diagnostics

### 1. App Won't Start
**Symptoms:** Server fails to start, import errors

**Solutions:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check for missing environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Try with debug mode
export DEBUG=True
make run
```

### 2. Tests Failing
**Symptoms:** `pytest` returns errors

**Solutions:**
```bash
# Run specific failing test with verbose output
pytest -v tests/test_file.py::test_name

# Check test database
rm -f test.db  # Remove old test DB
pytest

# Update test dependencies
pip install -U pytest pytest-cov
```

### 3. Database Issues
**Symptoms:** Migration errors, data not saving

**Solutions:**
```bash
# Reset local database
rm -f app.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Check migrations
flask db current
flask db upgrade head

# Verify connection
python -c "from app import create_app; app = create_app(); print(app.config['DATABASE_URL'])"
```

### 4. Import Errors
**Symptoms:** `ModuleNotFoundError`

**Solutions:**
```bash
# Verify virtual environment is activated
which python  # Should point to .venv/bin/python

# Reinstall package
pip uninstall package-name
pip install package-name

# Check PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### 5. Git Conflicts
**Symptoms:** Merge conflicts, can't push

**Solutions:**
```bash
# Save current work
git stash

# Update from main
git pull origin main

# Apply stashed changes
git stash pop

# If conflicts, resolve then:
git add .
git commit -m "Resolve conflicts"
```

### 6. Production Deployment Fails
**Symptoms:** Deploy succeeds but app crashes

**Solutions:**
```bash
# Check production logs
make logs

# Verify environment variables
# [Platform-specific command]

# Check requirements.txt includes all dependencies
pip freeze > requirements.txt
git diff requirements.txt

# Test build locally
# [Platform-specific build command]
```

### 7. Memory Issues
**Symptoms:** Out of memory errors, slow performance

**Solutions:**
```bash
# Check memory usage
# [Platform-specific memory check]

# Reduce workers/threads
# Edit configuration to use fewer workers

# Check for memory leaks
python -m memory_profiler script.py
```

### 8. API Integration Errors
**Symptoms:** External API calls failing

**Solutions:**
```bash
# Verify API key
echo $API_KEY_NAME

# Test API endpoint
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/test

# Check rate limits
# Review API documentation

# Add retry logic
# Implement exponential backoff
```

## 📊 Log Analysis

### Finding Errors
```bash
# Search for errors in logs
grep -i "error" logs/app.log

# Last 50 lines
tail -50 logs/app.log

# Follow live logs
tail -f logs/app.log
```

### Common Error Patterns
- `ImportError` → Missing dependency
- `OperationalError` → Database issue
- `KeyError` → Missing config/environment variable
- `ConnectionError` → External service down
- `404` → Missing route
- `500` → Server-side error (check logs)

## 🚨 Emergency Procedures

### Production is Down
1. Check status page/logs
2. Rollback to last working version:
   ```bash
   git revert HEAD
   make deploy
   ```
3. Notify stakeholders
4. Investigate root cause
5. Fix and redeploy

### Data Loss Prevention
1. Backup database immediately
2. Don't run destructive operations
3. Test in staging first
4. Have rollback plan ready

## ✅ Prevention Checklist

Before every deployment:
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Dependencies updated
- [ ] Environment variables set
- [ ] Database migrations tested
- [ ] Rollback plan ready
- [ ] Logs/monitoring configured

---
**For AI Agents:** When user reports an issue, check this file first before investigating.
EOF

# Create CLEANUP.md
cat > CLEANUP.md << 'EOF'
# CLEANUP.md - Disk Space & Maintenance
> Guide for managing project files and dependencies

## 🧹 Quick Cleanup Commands

### Safe Cleanup (Run Anytime)
```bash
# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Remove test artifacts
rm -rf .pytest_cache
rm -f .coverage
rm -rf htmlcov/

# Remove build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Remove temporary files
find . -type f -name "*.tmp" -delete
find . -type f -name "*.log" -delete
find . -type f -name "*~" -delete
```

### Aggressive Cleanup (Will Require Reinstall)
```bash
# Remove virtual environment (will need to recreate)
rm -rf .venv/

# Remove node_modules if using JavaScript
rm -rf node_modules/

# Remove all untracked files (CAREFUL!)
git clean -fdx  # Preview with -n first
```

### Rebuild After Cleanup
```bash
# Recreate virtual environment
python -m venv .venv
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify everything works
make test
```

## 📊 Check Disk Usage

### Project Size
```bash
# Total project size
du -sh .

# Size by directory
du -h --max-depth=1 | sort -hr

# Largest files
find . -type f -exec du -h {} + | sort -rh | head -20
```

### What Takes Up Space
```
.venv/           # 100-300MB typically (Python packages)
node_modules/    # 200-500MB typically (if using JS)
__pycache__/     # 1-50MB (Python cache)
.pytest_cache/   # 1-10MB (test cache)
logs/            # Varies (application logs)
.git/            # Varies (git history)
```

## 🔄 Regular Maintenance

### Weekly Tasks
```bash
# Update dependencies
pip list --outdated
pip install -U package-name

# Clean cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Check git status
git status
git log --oneline -10
```

### Monthly Tasks
```bash
# Review and remove old branches
git branch -a
git branch -d old-branch-name

# Prune git objects
git gc --aggressive --prune=now

# Update all dependencies
pip install -U -r requirements.txt
make test  # Verify nothing broke
```

## 💾 Backup Before Cleanup

### What to Backup
```bash
# Backup database
cp app.db app.db.backup

# Backup important config
tar -czf config-backup.tar.gz .env fly.toml

# Export virtual environment
pip freeze > requirements.backup.txt
```

## 🚀 Optimize Virtual Environment

### Remove Unused Packages
```bash
# See what's installed
pip list

# Uninstall unused packages
pip uninstall package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Fresh Virtual Environment
```bash
# Save current requirements
pip freeze > requirements.old.txt

# Remove old venv
rm -rf .venv

# Create new venv
python -m venv .venv
source .venv/bin/activate

# Install only what's needed
pip install -r requirements.txt

# Test everything works
make test
```

## 📋 Cleanup Checklist

Before archiving/sharing project:
- [ ] Remove `.venv/`
- [ ] Remove `__pycache__/`
- [ ] Remove `.pytest_cache/`
- [ ] Remove `*.pyc` files
- [ ] Remove test databases (`test.db`)
- [ ] Remove log files
- [ ] Remove `.env` (contains secrets)
- [ ] Update `requirements.txt`
- [ ] Verify `.gitignore` is complete
- [ ] Test fresh clone works

## 🎯 Keep These Files

**Never delete:**
- `requirements.txt`
- Source code (`app/`, `tests/`)
- Documentation (`.md` files)
- Configuration (`fly.toml`, `Makefile`)
- `.git/` (unless intentionally removing version control)

**Safe to delete:**
- `.venv/` (can recreate)
- `__pycache__/` (auto-generated)
- `.pytest_cache/` (auto-generated)
- `*.pyc` (auto-generated)
- Log files (unless needed for debugging)

## 💡 Tips for AI Agents

When user asks about disk space:
1. Run `du -sh .` to show total size
2. Run `du -h --max-depth=1 | sort -hr` to show breakdown
3. Recommend safe cleanup commands first
4. Only suggest aggressive cleanup if necessary
5. Always remind to backup before cleanup

---
**Current Project Size:** [Run `du -sh .` to check]
EOF

# Replace placeholders
sed -i.bak "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" AGENTS.md CLAUDE.md GEMINI.md
sed -i.bak "s/TECH_STACK_PLACEHOLDER/$TECH_STACK/g" AGENTS.md
rm -f *.bak

echo ""
echo "✅ Created documentation files:"
echo "   - AGENTS.md"
echo "   - CLAUDE.md"
echo "   - GEMINI.md"
echo "   - TROUBLESHOOTING.md"
echo "   - CLEANUP.md"
echo ""
echo "📝 Next steps:"
echo "   1. Customize each file with project-specific details"
echo "   2. Add to git: git add *.md"
echo "   3. Commit: git commit -m 'Add AI agent documentation'"
echo ""
echo "🤖 Your project is now ready for multi-agent collaboration!"
