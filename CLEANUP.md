# Project Cleanup & Maintenance Guide

This guide helps AI agents (Claude, Gemini, etc.) safely clean up old projects and manage disk space.

---

## Quick Cleanup Commands

### For This Project (Gutter Tracker)

```bash
cd /Users/Sean/code/gutter-tracker

# Clean generated/cached files (safe - regenerates automatically)
make clean
# OR manually:
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf app/__pycache__/
rm -rf tests/__pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove old virtual environment (if you have both venv and .venv)
rm -rf venv/  # Old one, we use .venv now

# Clean Vercel cache (not needed if using Fly.io)
rm -rf .vercel/

# Clean logs (if they get too large)
rm -f app.log app_run.log

# Result: Saves ~20-50MB
```

### For ANY Flask Project

```bash
cd /path/to/any-flask-project

# Remove virtual environment (can reinstall with: make install or pip install -r requirements.txt)
rm -rf venv/ .venv/ env/

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Remove test cache
rm -rf .pytest_cache/

# Remove build artifacts
rm -rf build/ dist/ *.egg-info/

# Remove local database (WARNING: Data loss!)
# Only do this if you don't need the data
rm -rf instance/

# Result: Project goes from 200-300MB to ~1-5MB (just source code)
```

### For Node.js/React Projects

```bash
cd /path/to/react-project

# Remove dependencies (can reinstall with: npm install)
rm -rf node_modules/

# Remove build artifacts
rm -rf build/ dist/ .next/

# Remove cache
rm -rf .cache/

# Result: Project goes from 500MB-1GB to ~1-10MB (just source code)
```

---

## Cleanup Script for All Projects

### Safe Cleanup (Keeps Dependencies)

```bash
#!/bin/bash
# cleanup-safe.sh - Removes only temporary/cache files

echo "🧹 Safe cleanup of all projects in ~/code..."
echo ""

for project in ~/code/*/; do
  echo "Cleaning: $project"
  cd "$project"
  
  # Python cache
  find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
  find . -type f -name "*.pyc" -delete 2>/dev/null
  rm -rf .pytest_cache/ 2>/dev/null
  
  # Build artifacts
  rm -rf build/ dist/ *.egg-info/ 2>/dev/null
  
  # Logs
  rm -f *.log 2>/dev/null
  
  # IDE caches
  rm -rf .idea/ .vscode/__pycache__/ 2>/dev/null
  
  echo "  ✓ Cleaned cache files"
  echo ""
done

echo "✅ Safe cleanup complete!"
```

### Aggressive Cleanup (Removes Dependencies)

```bash
#!/bin/bash
# cleanup-aggressive.sh - Removes dependencies too (can reinstall later)

echo "⚠️  AGGRESSIVE cleanup - will remove dependencies!"
echo "You can reinstall with 'pip install -r requirements.txt' or 'npm install'"
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 1
fi

echo ""
echo "🧹 Aggressive cleanup starting..."
echo ""

for project in ~/code/*/; do
  echo "Cleaning: $project"
  cd "$project"
  
  # Python
  rm -rf venv/ .venv/ env/ __pycache__/ .pytest_cache/ 2>/dev/null
  find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
  
  # Node.js
  rm -rf node_modules/ .next/ 2>/dev/null
  
  # Build artifacts
  rm -rf build/ dist/ *.egg-info/ 2>/dev/null
  
  # Logs
  rm -f *.log 2>/dev/null
  
  echo "  ✓ Cleaned"
  echo ""
done

echo "✅ Aggressive cleanup complete!"
echo "📦 To restore dependencies:"
echo "  Python: pip install -r requirements.txt"
echo "  Node.js: npm install"
```

---

## Claude Commands for Cleanup

### Command 1: Analyze Disk Usage

```
Claude, analyze disk usage in ~/code and show me:
1. Total size of each project
2. Size breakdown (venv, node_modules, source code, etc.)
3. Which projects can be cleaned up
4. Estimated space savings

Use these commands:
- du -sh ~/code/*
- For each project, show: du -sh * .venv .git node_modules
```

### Command 2: Safe Cleanup

```
Claude, perform a safe cleanup of all projects in ~/code:
1. Remove __pycache__ directories
2. Remove .pytest_cache
3. Remove *.pyc files
4. Remove build/dist folders
5. Remove log files
6. Show how much space was saved

Do NOT remove: venv, .venv, node_modules, instance, .git
```

### Command 3: Aggressive Cleanup (After Confirmation)

```
Claude, I want to aggressively clean old projects:
1. First, show me the list of projects in ~/code
2. Ask me which ones to clean
3. For confirmed projects:
   - Remove venv/.venv/node_modules
   - Remove all cache
   - Keep only source code
4. Show space saved
```

### Command 4: Archive Old Projects

```
Claude, help me archive old projects:
1. List all projects in ~/code with last modified date
2. For projects older than 3 months:
   - Remove dependencies (venv, node_modules)
   - Keep source code
   - Create a note with reinstall commands
3. Show final disk usage
```

---

## What's Safe to Delete

### ✅ Always Safe (Regenerates Automatically)

| File/Folder | What It Is | Regenerates With |
|-------------|------------|------------------|
| `__pycache__/` | Python bytecode cache | Running any Python file |
| `*.pyc` | Compiled Python files | Running Python |
| `.pytest_cache/` | Test cache | Running pytest |
| `build/` | Build artifacts | Running build command |
| `dist/` | Distribution files | Running build |
| `*.egg-info/` | Package metadata | pip install |
| `*.log` | Log files | Running app |
| `.DS_Store` | macOS metadata | Automatic |

### ⚠️ Safe But Need to Reinstall

| File/Folder | What It Is | Reinstall With |
|-------------|------------|----------------|
| `venv/` or `.venv/` | Python packages | `pip install -r requirements.txt` |
| `node_modules/` | Node.js packages | `npm install` or `yarn install` |
| `.next/` | Next.js build | `npm run build` |

### ❌ DO NOT Delete (Data Loss!)

| File/Folder | What It Is | Why Keep |
|-------------|------------|----------|
| `instance/` | Local database | Your data! |
| `.git/` | Git history | Version control |
| `.env` | Secrets/config | API keys, passwords |
| `src/` `app/` | Source code | Your actual code! |
| `requirements.txt` | Dependencies list | Needed to reinstall |
| `package.json` | Node dependencies | Needed to reinstall |

---

## Cleanup Frequency

### Daily
```bash
# Just clean cache (very quick)
find ~/code -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

### Weekly
```bash
# Clean cache and logs
cd ~/code/active-project
make clean  # or rm -rf __pycache__ *.log
```

### Monthly
```bash
# Review all projects
# Remove dependencies from unused projects
# Keep only source code for archived projects
```

### Before Low Disk Space
```bash
# Aggressive cleanup
# Remove ALL dependencies
# Keep only source code + requirements.txt/package.json
```

---

## Space Estimates

### Typical Project Sizes

**Before Cleanup:**
- Flask app: 200-300MB (210MB is .venv)
- React app: 500MB-1GB (400-800MB is node_modules)
- Full-stack: 1-2GB

**After Safe Cleanup:**
- Flask: 150-250MB (removed 20-50MB cache)
- React: 400-900MB (removed 100-200MB cache)

**After Aggressive Cleanup:**
- Flask: 1-10MB (just source code)
- React: 1-20MB (just source code)

**Reinstall Time:**
- Flask `pip install`: 1-3 minutes
- React `npm install`: 2-5 minutes

---

## Automation Ideas

### Create a Monthly Cron Job

```bash
# Edit crontab
crontab -e

# Add this line (runs 1st of every month at 2am)
0 2 1 * * /Users/Sean/cleanup-safe.sh >> /Users/Sean/cleanup.log 2>&1
```

### Create Cleanup Aliases

```bash
# Add to ~/.zshrc or ~/.bashrc
alias clean-cache='find ~/code -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null'
alias clean-project='make clean || (rm -rf __pycache__ .pytest_cache *.log)'
alias clean-all='cd ~/code && for d in */; do (cd "$d" && make clean 2>/dev/null); done'

# Then use:
# clean-cache    - Quick cache cleanup
# clean-project  - Clean current project
# clean-all      - Clean all projects
```

---

## Claude Workflow Example

**User Says:** "Claude, my disk is getting full, help me clean up old projects"

**Claude Should:**

1. **Analyze First**
```bash
du -sh ~/code/*
# Show results to user
```

2. **Ask for Confirmation**
```
I found:
- gutter-tracker: 230MB (active project)
- old-flask-app: 280MB (last modified 3 months ago)
- test-project: 150MB (last modified 6 months ago)

Should I:
A) Safe cleanup (remove cache only, saves ~50MB)
B) Aggressive cleanup of old projects (saves ~400MB)
C) Show me more details first
```

3. **Execute Based on Choice**

**If Choice A (Safe):**
```bash
cd ~/code
for project in */; do
  cd "$project"
  find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null
  rm -rf .pytest_cache *.log
  cd ..
done
```

**If Choice B (Aggressive):**
```bash
# For old projects only
cd ~/code/old-flask-app
rm -rf venv .venv __pycache__ .pytest_cache
echo "To reinstall: pip install -r requirements.txt" > REINSTALL.txt

cd ~/code/test-project
rm -rf venv .venv __pycache__ .pytest_cache
echo "To reinstall: pip install -r requirements.txt" > REINSTALL.txt
```

4. **Report Results**
```
✅ Cleanup complete!

Before: 660MB
After: 260MB
Saved: 400MB

Active projects (kept dependencies):
- gutter-tracker: 230MB ✓

Archived projects (source code only):
- old-flask-app: 15MB ✓
- test-project: 10MB ✓

To restore archived project:
cd ~/code/old-flask-app
pip install -r requirements.txt
```

---

## Emergency Cleanup (Disk Almost Full)

If you need space IMMEDIATELY:

```bash
# 1. Find largest projects
du -sh ~/code/* | sort -hr | head -10

# 2. For each large unused project:
cd ~/code/unused-project
rm -rf venv .venv node_modules

# 3. Clean system caches too
rm -rf ~/Library/Caches/pip
rm -rf ~/.npm
rm -rf ~/.cache

# Can save: 1-5GB+ quickly
```

---

## Checklist for Claude

When user requests cleanup, verify:

- [ ] Analyzed disk usage first
- [ ] Identified which projects are active vs old
- [ ] Asked user before deleting dependencies
- [ ] Created REINSTALL.txt notes for aggressive cleanups
- [ ] Did NOT delete .git or source code
- [ ] Did NOT delete instance/ (databases)
- [ ] Did NOT delete .env files
- [ ] Reported space saved
- [ ] Provided reinstall commands

---

## Notes for AI Agents

**Golden Rule:** When in doubt, ask the user first!

**Safe bets:**
- Always safe to delete `__pycache__`, `*.pyc`, logs
- Ask before deleting `venv`, `node_modules`
- NEVER delete `src/`, `app/`, `.git/`, `.env/`, `instance/`

**Best practice:**
1. Analyze and report
2. Suggest cleanup plan
3. Get user confirmation
4. Execute cleanup
5. Report results with reinstall instructions

---

**Last Updated:** Dec 27, 2025  
**For:** Claude, Gemini, and other AI coding assistants  
**Project:** Gutter Tracker (and future projects)
