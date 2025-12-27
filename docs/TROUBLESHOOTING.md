# Troubleshooting Guide - Gutter Tracker

Common issues and solutions for the Gutter Tracker app.

## Table of Contents
- [Server Issues](#server-issues)
- [Database Issues](#database-issues)
- [AI/Gemini Issues](#aigemini-issues)
- [Deployment Issues](#deployment-issues)
- [Authentication Issues](#authentication-issues)
- [Frontend Issues](#frontend-issues)
- [Performance Issues](#performance-issues)

---

## Server Issues

### Server Won't Start

**Symptom:** `python3 app_gemini.py` fails or hangs

**Solutions:**

1. **Port already in use**
```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=8000
python3 app_gemini.py
```

2. **Missing dependencies**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Or create fresh virtual environment
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Python version issues**
```bash
# Check Python version (need 3.8+)
python3 --version

# If too old, install newer Python
# macOS:
brew install python@3.11
python3.11 -m venv .venv
```

4. **Environment variables not loaded**
```bash
# Make sure .env file exists
ls -la .env

# Check contents
cat .env

# Manually export if needed
export DATABASE_URL="your-database-url"
export GEMINI_API_KEY="your-api-key"
```

---

### Module Not Found Errors

**Symptom:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Install missing package
pip install flask

# Or reinstall everything
pip install -r requirements.txt

# Verify installation
pip list | grep flask
```

---

### Flask Debug Mode Issues

**Symptom:** Changes not reflecting, or "already running" errors

**Solutions:**

```bash
# Kill all Python processes
pkill -f python

# Disable debug mode temporarily
export FLASK_DEBUG=0
python3 app_gemini.py

# Or use production WSGI server
pip install gunicorn
gunicorn app_gemini:app
```

---

## Database Issues

### Database Connection Failed

**Symptom:** `sqlalchemy.exc.OperationalError` or can't connect to database

**Solutions:**

1. **Check DATABASE_URL**
```bash
# Verify DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host/dbname

# Test connection
python3 -c "from app_gemini import db; print(db.engine.url)"
```

2. **Neon database sleeping (free tier)**
```bash
# Neon free tier databases sleep after inactivity
# Solution: Wait 10-15 seconds for wake up, or upgrade to paid tier

# Test connection
python3 -c "from app_gemini import db; db.session.execute('SELECT 1')"
```

3. **Database doesn't exist**
```bash
# Create database manually in Neon dashboard
# Or create tables
python3 -c "from app_gemini import db; db.create_all()"
```

---

### Table/Column Not Found

**Symptom:** `ProgrammingError: relation "customer" does not exist`

**Solutions:**

```bash
# Drop and recreate all tables
python3 << EOF
from app_gemini import db
db.drop_all()
db.create_all()
print("Tables created successfully")
EOF

# Verify tables exist
python3 << EOF
from app_gemini import db
print(db.engine.table_names())
EOF
```

---

### Data Not Saving

**Symptom:** Form submission succeeds but data not in database

**Solutions:**

1. **Missing commit**
```python
# Make sure you have db.session.commit()
customer = Customer(name=name, phone=phone)
db.session.add(customer)
db.session.commit()  # ← Don't forget this!
```

2. **Transaction rollback**
```python
# Check for errors and rollback
try:
    db.session.add(customer)
    db.session.commit()
except Exception as e:
    print(f"Error: {e}")
    db.session.rollback()
```

3. **Validation errors**
```bash
# Check Flask logs for validation errors
# Enable debug mode to see details
export FLASK_DEBUG=1
python3 app_gemini.py
```

---

## AI/Gemini Issues

### Invalid API Key

**Symptom:** `google.api_core.exceptions.PermissionDenied` or 403 errors

**Solutions:**

```bash
# 1. Verify API key is set
echo $GEMINI_API_KEY

# 2. Check if key is valid (test directly)
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# 3. Get new API key from https://ai.google.dev
# 4. Update .env file
nano .env
# Add: GEMINI_API_KEY=your-new-key

# 5. Restart server
pkill -f python
python3 app_gemini.py
```

---

### Rate Limit Exceeded

**Symptom:** `429 Resource Exhausted` or "rate limit" errors

**Solutions:**

```bash
# Free tier limits: 15 requests/minute, 1500/day

# 1. Wait 60 seconds and retry

# 2. Implement rate limiting in code
from time import sleep
sleep(5)  # Wait between requests

# 3. Cache AI responses
# Store frequently used estimates in database

# 4. Upgrade to paid tier
# https://ai.google.dev/pricing
```

---

### Empty AI Response

**Symptom:** AI returns blank or `None`

**Solutions:**

```python
# 1. Check response object
response = model.generate_content(prompt)
print(f"Response: {response}")
print(f"Text: {response.text}")

# 2. Check safety filters
if response.prompt_feedback.block_reason:
    print(f"Blocked: {response.prompt_feedback.block_reason}")

# 3. Improve prompt
# Be more specific, add context, use examples

# 4. Try different model
model = genai.GenerativeModel('gemini-pro')
```

---

### Image Analysis Fails

**Symptom:** Vision API errors with photos

**Solutions:**

```python
# 1. Verify image format
# Must be JPEG, PNG, WebP, HEIC, HEIF
# Max size: 20MB

# 2. Check base64 encoding
photo_data = request.json.get('photo_data')
if ',' in photo_data:
    photo_data = photo_data.split(',')[1]  # Remove data:image/jpeg;base64,

# 3. Verify image data
import base64
try:
    image_bytes = base64.b64decode(photo_data)
    print(f"Image size: {len(image_bytes)} bytes")
except Exception as e:
    print(f"Decode error: {e}")

# 4. Test with simple image
image_part = {
    "mime_type": "image/jpeg",
    "data": image_bytes
}
response = model.generate_content(["What's in this image?", image_part])
```

---

## Deployment Issues

### Vercel Build Failed

**Symptom:** Deployment fails during build

**Solutions:**

1. **Check build logs**
```bash
vercel logs <deployment-url>
```

2. **Missing environment variables**
```bash
# Add env vars to Vercel
vercel env add DATABASE_URL
vercel env add GEMINI_API_KEY
vercel env add APP_PASSWORD
vercel env add SECRET_KEY

# Or set in dashboard:
# Settings → Environment Variables
```

3. **Python version mismatch**
```bash
# Create runtime.txt
echo "python-3.11" > runtime.txt
git add runtime.txt
git commit -m "Add runtime.txt"
vercel --prod
```

4. **Dependencies too large**
```bash
# Optimize requirements.txt
# Remove unused packages

# Use minimal Gemini requirements
cp config/requirements_gemini_minimal.txt requirements.txt
```

---

### Deployment Succeeds But Site Broken

**Symptom:** Build succeeds but 500 errors on site

**Solutions:**

```bash
# 1. Check runtime logs
vercel logs <deployment-url> --follow

# 2. Verify environment variables
vercel env ls

# 3. Test locally with production settings
vercel dev

# 4. Check database connection from Vercel
# Ensure DATABASE_URL is accessible from Vercel's servers
# (Neon databases are globally accessible)

# 5. Verify static files
vercel deploy --debug
```

---

### Domain/SSL Issues

**Symptom:** Custom domain not working or SSL errors

**Solutions:**

```bash
# 1. Check domain settings in Vercel dashboard
# Domains → Add Domain

# 2. Update DNS records
# Add CNAME: www → cname.vercel-dns.com

# 3. Wait for SSL certificate (up to 24 hours)

# 4. Force HTTPS
# Add to vercel.json:
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000"
        }
      ]
    }
  ]
}
```

---

## Authentication Issues

### Can't Login

**Symptom:** Correct password rejected

**Solutions:**

```bash
# 1. Verify APP_PASSWORD
cat .env | grep APP_PASSWORD

# 2. Check for whitespace
echo "$APP_PASSWORD" | od -c

# 3. Reset password
nano .env
# Update APP_PASSWORD=newpassword

# 4. Clear browser cookies
# Or use incognito mode

# 5. Check session secret
# Make sure SECRET_KEY is set
echo $SECRET_KEY
```

---

### Session Expires Immediately

**Symptom:** Logged out right after login

**Solutions:**

```python
# 1. Set session to permanent
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# 2. Set session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Only for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 3. Check SECRET_KEY
# Must be consistent between restarts
# Set in environment, not hardcoded random
```

---

### Password Required on Every Page

**Symptom:** Login page appears on every click

**Solutions:**

```python
# 1. Make sure session is set
@app.route('/login', methods=['POST'])
def login():
    if password == os.getenv('APP_PASSWORD'):
        session['logged_in'] = True  # ← Must be set
        session.permanent = True
        return redirect(url_for('dashboard'))

# 2. Check login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:  # ← Check this
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 3. Verify SECRET_KEY is set
print(app.config['SECRET_KEY'])
```

---

## Frontend Issues

### Styles Not Loading

**Symptom:** Page shows but no CSS

**Solutions:**

```bash
# 1. Check static folder exists
ls -la static/style.css

# 2. Verify template link
# Should be:
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

# Not:
<link rel="stylesheet" href="/static/style.css">

# 3. Clear browser cache
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# 4. Check Flask static folder config
app.static_folder = 'static'
```

---

### JavaScript Not Working

**Symptom:** Buttons don't work, no camera, etc.

**Solutions:**

```javascript
// 1. Open browser console (F12)
// Check for JavaScript errors

// 2. Verify function names match
<button onclick="startCamera()">  // ← Must match function below
<script>
function startCamera() { ... }  // ← Same name
</script>

// 3. Check for missing dependencies
// e.g., if using jQuery:
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

// 4. Wrap code in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Your code here
});
```

---

### Camera Not Working

**Symptom:** Camera button does nothing or permission denied

**Solutions:**

```javascript
// 1. Check browser permissions
// Settings → Privacy → Camera → Allow

// 2. HTTPS required for camera
// Use https://localhost or deploy to Vercel

// 3. Test getUserMedia support
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => console.log('Camera works!'))
    .catch(err => console.error('Camera error:', err));

// 4. Use correct facing mode
navigator.mediaDevices.getUserMedia({
    video: {
        facingMode: 'environment'  // Back camera on mobile
    }
})
```

---

## Performance Issues

### Slow Page Loads

**Symptom:** Pages take >5 seconds to load

**Solutions:**

1. **Database query optimization**
```python
# Bad: N+1 query problem
for customer in Customer.query.all():
    print(customer.jobs)  # Separate query for each customer

# Good: Use joinedload
from sqlalchemy.orm import joinedload
customers = Customer.query.options(joinedload(Customer.jobs)).all()
```

2. **Add pagination**
```python
page = request.args.get('page', 1, type=int)
customers = Customer.query.paginate(page=page, per_page=20)
```

3. **Cache AI responses**
```python
# Store common estimates in database
# Check cache before calling AI
```

4. **Minimize AI calls**
```python
# Don't call AI on every page load
# Only when user explicitly requests
```

---

### AI Requests Timeout

**Symptom:** AI requests take >30 seconds

**Solutions:**

```python
# 1. Use faster model
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Faster

# 2. Reduce prompt size
# Be concise, remove unnecessary context

# 3. Implement timeout
import socket
socket.setdefaulttimeout(30)

# 4. Show loading indicator
# Let user know request is processing
```

---

### High Memory Usage

**Symptom:** Server crashes or becomes unresponsive

**Solutions:**

```bash
# 1. Check memory usage
top -pid $(pgrep -f app_gemini)

# 2. Limit image sizes
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

# 3. Use streaming for large responses
@app.route('/large-data', methods=['GET'])
def stream_data():
    def generate():
        for item in large_dataset:
            yield f"{item}\n"
    return Response(generate(), mimetype='text/plain')

# 4. Add garbage collection
import gc
gc.collect()
```

---

## Getting More Help

### Check Logs

```bash
# Local development
python3 app_gemini.py
# Watch terminal output

# Vercel production
vercel logs <deployment-url> --follow

# Check specific deployment
vercel logs gutter-tracker-eta.vercel.app
```

### Enable Debug Mode

```bash
# In .env
export FLASK_DEBUG=1

# Or in app_gemini.py
app.run(debug=True)
```

### Use AI Tech Support

1. Go to https://gutter-tracker-eta.vercel.app/help
2. Ask the AI assistant about your issue
3. It has knowledge of the entire codebase

### Still Stuck?

1. Check [DEV_GUIDE.md](DEV_GUIDE.md) for development tips
2. Check [docs/COMPLETE_GUIDE.md](docs/COMPLETE_GUIDE.md) for full documentation
3. Review error logs carefully
4. Google the exact error message
5. Check Flask/SQLAlchemy/Gemini API documentation

---

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `Address already in use` | Port 5000 taken | `lsof -i :5000`, kill process |
| `ModuleNotFoundError` | Missing package | `pip install <package>` |
| `relation does not exist` | Missing database table | `db.create_all()` |
| `PermissionDenied` (Gemini) | Invalid API key | Check GEMINI_API_KEY |
| `429 Resource Exhausted` | Rate limit hit | Wait or upgrade plan |
| `Unauthorized` | Not logged in | Check session/cookies |
| `CSRF token missing` | Session issue | Clear cookies, restart |
| `Internal Server Error` | Generic server error | Check logs for details |

---

**Last updated:** 2025-12-27
**Questions?** Use the `/help` page with AI assistant!
