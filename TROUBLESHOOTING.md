# Troubleshooting Guide - Gutter Tracker

Quick reference for diagnosing and fixing common issues in production and development.

## Production App Info

**URL:** https://gutter-tracker-app.fly.dev  
**Password:** NAO$  
**Platform:** Fly.io (512MB RAM, 1 worker)  
**Database:** PostgreSQL (gutter-tracker-db)

---

## Quick Diagnostics

### Check if App is Running
```bash
curl -I https://gutter-tracker-app.fly.dev
# Expected: HTTP/2 200

flyctl status --app gutter-tracker-app
# Expected: Machine state = started
```

### Test All Routes
```bash
for route in /dashboard /customers /jobs /calendar /inventory /materials /reports /quick-estimate /help; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://gutter-tracker-app.fly.dev$route")
  echo "$route: $status"
done
# Expected: All routes return 200
```

### View Recent Logs
```bash
flyctl logs --app gutter-tracker-app --no-tail | tail -50
```

### Check Resource Usage
```bash
flyctl status --app gutter-tracker-app
# Shows memory usage, machine state
```

---

## Common Issues & Solutions

### 1. Login Page Freezes / Won't Redirect

**Symptoms:**
- Login form submits but nothing happens
- Stuck on login page after entering password
- Browser shows "loading" indefinitely

**Causes:**
1. Missing route that dashboard tries to redirect to
2. JavaScript error blocking redirect
3. Session not being created

**Diagnosis:**
```bash
# Check logs during login attempt
flyctl logs --app gutter-tracker-app

# Test login locally
make run
# Visit http://127.0.0.1:5001/login
# Use password: NAO$
```

**Solutions:**
1. **Check for missing routes:**
   ```bash
   # Find all href links in templates
   grep -r 'href="/' app/templates/*.html | grep -v static
   
   # Check routes.py has all these routes
   grep '@main.route' app/routes.py
   ```

2. **Verify SECRET_KEY is set:**
   ```bash
   flyctl secrets list --app gutter-tracker-app | grep SECRET_KEY
   ```

3. **Check browser console for JS errors:**
   - Open DevTools (F12)
   - Look for red errors in Console tab

**Fixed in:** Commits b3669f4, e339347 (added missing routes)

---

### 2. Out of Memory (OOM) Crashes

**Symptoms:**
- App suddenly stops responding
- 502 Bad Gateway errors
- Logs show: "Worker sent SIGKILL! Perhaps out of memory?"

**Diagnosis:**
```bash
# Check logs for OOM killer
flyctl logs --app gutter-tracker-app --no-tail | grep -i "out of memory"
flyctl logs --app gutter-tracker-app --no-tail | grep -i "SIGKILL"

# Check current memory allocation
flyctl status --app gutter-tracker-app
```

**Causes:**
- Too many Gunicorn workers for available RAM
- Memory leak in application code
- Large file uploads not streaming

**Solutions:**

1. **Increase memory:**
   ```bash
   # Edit fly.toml
   [[vm]]
     memory = "512mb"  # Was 256mb
   
   flyctl deploy --app gutter-tracker-app
   ```

2. **Reduce workers:**
   ```bash
   # Edit fly_start.sh
   exec gunicorn run:app --workers 1 --threads 2  # Was --workers 2
   
   git commit -am "Reduce workers to 1"
   flyctl deploy --app gutter-tracker-app
   ```

3. **Add worker recycling:**
   ```bash
   # In fly_start.sh, add:
   --max-requests 1000 --max-requests-jitter 50
   ```

**Fixed in:** Commit 742e870 (512MB RAM, 1 worker)

---

### 3. Tab Navigation Crashes (404 Errors)

**Symptoms:**
- Clicking nav links shows blank page or 404
- Browser URL changes but page doesn't load
- Some tabs work, others don't

**Diagnosis:**
```bash
# Test each route
for route in /dashboard /customers /jobs /calendar /inventory /materials /reports /quick-estimate /help; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://gutter-tracker-app.fly.dev$route")
  if [ "$status" != "200" ]; then
    echo "❌ $route: $status"
  else
    echo "✅ $route: $status"
  fi
done
```

**Causes:**
- Route referenced in template but not defined in routes.py
- Typo in route path
- Route not protected with @login_required

**Solutions:**

1. **Find missing routes:**
   ```bash
   # Extract all links from templates
   grep -rh 'href="/' app/templates/*.html | sed 's/.*href="//;s/".*//' | sort -u
   
   # Compare with actual routes
   grep '@main.route' app/routes.py | sed 's/.*route("//;s/".*//'
   ```

2. **Add missing route:**
   ```python
   # In app/routes.py
   @main.route("/materials")
   @login_required
   def materials():
       materials = Material.query.all()
       return render_template("materials.html", materials=materials)
   ```

3. **Update navigation in ALL templates:**
   ```bash
   # Add to each template's <nav> section
   <li><a href="/materials">Materials</a></li>
   ```

**Fixed in:** Commit e339347 (added /materials and /reports routes)

---

### 4. Database Connection Errors

**Symptoms:**
- 500 Internal Server Error on page load
- Logs show: "could not translate host name" or "connection refused"
- Database queries timeout

**Diagnosis:**
```bash
# Check database status
flyctl postgres db list -a gutter-tracker-db

# Check connection string
flyctl secrets list --app gutter-tracker-app | grep DATABASE_URL

# Test connection
flyctl postgres connect -a gutter-tracker-db
\dt  # List tables
\q
```

**Causes:**
- DATABASE_URL not set or incorrect
- PostgreSQL format issue (postgres:// vs postgresql://)
- Database not running
- Network connectivity

**Solutions:**

1. **Verify DATABASE_URL format:**
   ```python
   # app/config.py handles conversion
   if database_url.startswith("postgres://"):
       database_url = database_url.replace("postgres://", "postgresql://", 1)
   ```

2. **Restart database:**
   ```bash
   flyctl postgres restart -a gutter-tracker-db
   ```

3. **Check tables exist:**
   ```bash
   flyctl ssh console -a gutter-tracker-app
   python3
   >>> from app import create_app
   >>> app = create_app()
   >>> from app.extensions import db
   >>> with app.app_context():
   ...     db.create_all()
   ```

**Auto-fixed:** Tables created on startup by fly_start.sh

---

### 5. AI Features Not Working

**Symptoms:**
- Help chatbot returns generic responses
- Quick estimate doesn't generate AI output
- Inventory scanner doesn't analyze photos

**Diagnosis:**
```bash
# Check Gemini API key is set
flyctl secrets list --app gutter-tracker-app | grep GEMINI

# Check logs for API errors
flyctl logs --app gutter-tracker-app | grep -i gemini
flyctl logs --app gutter-tracker-app | grep -i "API error"

# Test locally
export GEMINI_API_KEY="your-key"
python3 -c "
from app.ai import gemini_model
response = gemini_model.generate_content('test')
print(response.text)
"
```

**Causes:**
- GEMINI_API_KEY not set or invalid
- API quota exceeded
- Network connectivity to Google AI
- Incorrect import in app/ai.py

**Solutions:**

1. **Set/Update API key:**
   ```bash
   flyctl secrets set GEMINI_API_KEY="your-gemini-key" --app gutter-tracker-app
   ```

2. **Check API quota:**
   - Visit https://makersuite.google.com/app/apikey
   - Check usage limits

3. **Verify error handling:**
   ```python
   # app/ai.py should have:
   try:
       response = gemini_model.generate_content(prompt)
       return response.text
   except Exception as e:
       current_app.logger.error(f"Gemini error: {e}")
       return "AI temporarily unavailable"
   ```

---

### 6. Static Files Not Loading (CSS/JS)

**Symptoms:**
- Page loads but has no styling
- Browser console shows 404 for /static/style.css
- Layout looks broken

**Diagnosis:**
```bash
# Check static files exist
ls -la app/static/

# Test static route
curl -I https://gutter-tracker-app.fly.dev/static/style.css
# Expected: HTTP/2 200

# Check template links
grep -r "href.*static" app/templates/
```

**Causes:**
- Static files not deployed
- Incorrect path in templates
- Flask not serving static files

**Solutions:**

1. **Verify files in deployment:**
   ```bash
   flyctl ssh console -a gutter-tracker-app
   ls -la /app/app/static/
   ```

2. **Check template paths:**
   ```html
   <!-- Correct -->
   <link href="/static/style.css" rel="stylesheet">
   
   <!-- Also correct -->
   <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
   ```

3. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Chrome/Firefox)
   - Or open in incognito/private mode

---

### 7. Session Lost / Logged Out Unexpectedly

**Symptoms:**
- Redirected to login after clicking links
- Session expires too quickly
- Can't stay logged in

**Diagnosis:**
```bash
# Check SECRET_KEY is set and consistent
flyctl secrets list --app gutter-tracker-app | grep SECRET_KEY

# Check session cookie in browser
# DevTools → Application → Cookies → Check "session" cookie
```

**Causes:**
- SECRET_KEY changed between deployments
- SECRET_KEY not set (using default)
- Cookie domain mismatch

**Solutions:**

1. **Set permanent SECRET_KEY:**
   ```bash
   # Generate secure key
   python3 -c "import secrets; print(secrets.token_hex(32))"
   
   # Set as Fly.io secret
   flyctl secrets set SECRET_KEY="generated-key-here" --app gutter-tracker-app
   ```

2. **Don't change SECRET_KEY:**
   - Once set, never change unless necessary
   - Changing invalidates all sessions

---

### 8. Deployment Fails

**Symptoms:**
- `flyctl deploy` hangs or errors
- Build succeeds but machine won't start
- Deployment timeout

**Diagnosis:**
```bash
# Check deployment status
flyctl status --app gutter-tracker-app

# View build logs
flyctl logs --app gutter-tracker-app

# Check for stuck deployments
flyctl releases --app gutter-tracker-app
```

**Causes:**
- Buildpack errors
- Out of disk space
- fly.toml misconfiguration
- Requirements.txt errors

**Solutions:**

1. **Check requirements.txt:**
   ```bash
   # Test locally
   python3 -m venv test_venv
   source test_venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Verify fly.toml syntax:**
   ```bash
   flyctl config validate
   ```

3. **Force rebuild:**
   ```bash
   flyctl deploy --app gutter-tracker-app --strategy immediate
   ```

4. **Check disk space:**
   ```bash
   flyctl ssh console -a gutter-tracker-app
   df -h
   ```

---

## Log Analysis

### Understanding Log Output

**Successful startup:**
```
Starting Gutter Tracker application...
Configuration loaded.
Database initialized.
Blueprint registered.
Database tables created.
Application creation finished.
[INFO] Booting worker with pid: 640
```

**Warning (safe to ignore):**
```
Could not create tables (may already exist)
FutureWarning: You are using a Python version...
```

**Critical errors:**
```
[ERROR] Worker (pid:XXX) was sent SIGKILL! Perhaps out of memory?
Out of memory: Killed process XXX
connection to server ... failed
```

### Useful Log Commands

```bash
# Live tail
flyctl logs --app gutter-tracker-app

# Last 100 lines
flyctl logs --app gutter-tracker-app --no-tail | tail -100

# Filter by level
flyctl logs --app gutter-tracker-app | grep -i error
flyctl logs --app gutter-tracker-app | grep -i warning

# Filter by time (look for timestamp)
flyctl logs --app gutter-tracker-app --no-tail | grep "2025-12-27"

# Filter by feature
flyctl logs --app gutter-tracker-app | grep -i "login"
flyctl logs --app gutter-tracker-app | grep -i "gemini"
flyctl logs --app gutter-tracker-app | grep -i "database"
```

---

## Emergency Procedures

### App is Completely Down

1. **Check Fly.io status:**
   ```bash
   flyctl status --app gutter-tracker-app
   ```

2. **Restart the machine:**
   ```bash
   flyctl machine restart -a gutter-tracker-app
   ```

3. **If still down, redeploy last known good version:**
   ```bash
   git log --oneline -10  # Find last working commit
   git checkout <commit-hash>
   flyctl deploy --app gutter-tracker-app
   git checkout main
   ```

### Database Corruption

1. **Backup current database:**
   ```bash
   flyctl postgres db backup -a gutter-tracker-db
   ```

2. **Reinitialize tables:**
   ```bash
   flyctl ssh console -a gutter-tracker-app
   python3 scripts/init_db.py
   ```

### Lost Secrets

```bash
# Re-set all required secrets
flyctl secrets set SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')" --app gutter-tracker-app
flyctl secrets set APP_PASSWORD="NAO$" --app gutter-tracker-app
flyctl secrets set GEMINI_API_KEY="your-key" --app gutter-tracker-app
flyctl secrets set DATABASE_URL="$(flyctl postgres db show gutter-tracker-db -a gutter-tracker-db --json | jq -r .uri)" --app gutter-tracker-app
```

---

## Getting Help

1. **Check this guide first**
2. **Review recent commits:** `git log --oneline -20`
3. **Check AGENTS.md** for code patterns
4. **Check CLAUDE.md / GEMINI.md** for AI-specific issues
5. **Search logs** for error messages
6. **Test locally** with `make run`

---

## Prevention Checklist

Before every deployment:
- [ ] Run `make test` - all tests pass
- [ ] Run `make lint` - no errors
- [ ] Test locally - app works at :5001
- [ ] Review changes - `git diff`
- [ ] Check logs after deploy - `flyctl logs`
- [ ] Test all routes - run verification script
- [ ] Verify AI features work (if changed)

**Last Updated:** Dec 27, 2025  
**Status:** All known issues resolved ✅
