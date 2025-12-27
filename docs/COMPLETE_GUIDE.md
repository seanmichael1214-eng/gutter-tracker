# 🎯 MASTER SETUP & DEPLOYMENT GUIDE
# Complete instructions for Gutter Tracker app

## 📋 TABLE OF CONTENTS
1. My Recommendation (AI Provider)
2. Complete Setup Instructions
3. Deployment Guide
4. Troubleshooting Guide
5. Cost Breakdown & How to Avoid Them
6. Bug Fixing Reference

═══════════════════════════════════════════════════════════════

## 1️⃣ MY RECOMMENDATION: USE GEMINI (FREE)

### Why Gemini is Best for Your App:

✅ **COST**: $0/month (vs $9-30 for Claude)
✅ **FREE TIER**: 1,500 requests/day = 45,000/month
✅ **QUALITY**: Excellent for cost estimates & photo analysis
✅ **YOU HAVE IT**: Already have Gemini API key
✅ **RELIABLE**: Google infrastructure
✅ **VISION**: Photo analysis works perfectly

### Your App Usage:
- 30-50 AI estimates/day
- 10-20 photo analyses/day
- Total: ~60 requests/day
- **That's only 4% of free tier!**

### Decision: **Use Gemini (app_gemini.py)**

═══════════════════════════════════════════════════════════════

## 2️⃣ COMPLETE SETUP INSTRUCTIONS

### Prerequisites:
- Python 3.9 or higher
- pip (Python package manager)
- Git (for deployment)
- Your Gemini API key

### Step-by-Step Setup:

#### A. Get Your API Key (30 seconds):
```bash
# 1. Go to: https://aistudio.google.com/apikey
# 2. Click "Create API Key"
# 3. Copy the key (starts with "AIza...")
```

#### B. Run Automated Setup (Recommended):
```bash
cd /Users/Sean/code/gutter-tracker

# Run the setup wizard
python3 setup_gemini.py

# Follow prompts:
# - Paste your Gemini API key
# - Choose SQLite for local testing (y)
# - Setup will auto-install dependencies
```

#### C. Manual Setup (If wizard fails):
```bash
cd /Users/Sean/code/gutter-tracker

# 1. Create environment file
cp .env.example .env

# 2. Edit .env file (use nano or any text editor)
nano .env

# Add these lines:
GEMINI_API_KEY=your_actual_gemini_key_here
DATABASE_URL=sqlite:///gutter_tracker.db
SECRET_KEY=paste_random_key_here

# To generate secret key, run:
python3 -c "import secrets; print(secrets.token_hex(32))"

# 3. Install dependencies
pip3 install -r requirements_gemini.txt

# 4. Initialize database
python3 -c "from app_gemini import app, db; app.app_context().push(); db.create_all()"

# 5. Test locally
python3 app_gemini.py
# Open browser: http://localhost:5000
```

#### D. Verify Setup:
```bash
# App should show:
# 🚀 Gutter Tracker - Powered by Google Gemini (FREE)
# ✨ AI Features: 100% FREE with Gemini API
# 📍 Running on: http://localhost:5000

# Test in browser:
# 1. Go to http://localhost:5000
# 2. Click "Add Customer" (should work)
# 3. Try AI estimate feature (should generate response)
```

═══════════════════════════════════════════════════════════════

## 3️⃣ DEPLOYMENT GUIDE

### Option A: Vercel (Recommended - FREE Tier)

#### Initial Setup:
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel (creates account if needed)
vercel login
# Follow browser authentication

# 3. Deploy
cd /Users/Sean/code/gutter-tracker
vercel

# Answer prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? gutter-tracker
# - Directory? ./
# - Override settings? N
```

#### Set Environment Variables in Vercel:
```bash
# Method 1: Via CLI
vercel env add GEMINI_API_KEY
# Paste your Gemini API key when prompted

vercel env add SECRET_KEY
# Paste your secret key

vercel env add DATABASE_URL
# For production, use Vercel Postgres (see below)
# Or use: sqlite:///gutter_tracker.db for testing

# Method 2: Via Dashboard
# 1. Go to vercel.com/dashboard
# 2. Select your project
# 3. Settings → Environment Variables
# 4. Add each variable for Production
```

#### Setup Production Database (Vercel Postgres - FREE):
```bash
# 1. Go to vercel.com/dashboard
# 2. Select your project
# 3. Storage → Connect Database → Create New
# 4. Choose Postgres
# 5. Name it "gutter-tracker-db"
# 6. Create (free tier: 256MB)
# 7. Copy the DATABASE_URL shown
# 8. Add to environment variables

# Or use Vercel CLI:
vercel postgres create
```

#### Deploy to Production:
```bash
vercel --prod

# Your app URL will be:
# https://gutter-tracker-xxx.vercel.app
# Share this with your client!
```

#### Update After Changes:
```bash
# After editing code:
git add .
git commit -m "Updated feature X"
git push

# Then redeploy:
vercel --prod
```

### Option B: Alternative - Render.com (FREE Tier)

```bash
# 1. Go to render.com
# 2. Connect GitHub repo
# 3. New → Web Service
# 4. Select your repo
# 5. Settings:
#    - Name: gutter-tracker
#    - Environment: Python 3
#    - Build Command: pip install -r requirements_gemini.txt
#    - Start Command: gunicorn app_gemini:app
# 6. Add environment variables (same as Vercel)
# 7. Create Web Service (free tier)
```

### Option C: Railway.app (FREE $5/month credit)

```bash
# 1. Go to railway.app
# 2. New Project → Deploy from GitHub
# 3. Select your repo
# 4. Add variables:
#    - GEMINI_API_KEY
#    - SECRET_KEY
#    - DATABASE_URL (Railway provides Postgres free)
# 5. Deploy
```

═══════════════════════════════════════════════════════════════

## 4️⃣ TROUBLESHOOTING GUIDE

### Common Issues & Solutions:

#### Issue 1: "ModuleNotFoundError: No module named 'google.generativeai'"
**Solution:**
```bash
pip3 install -r requirements_gemini.txt
# or
pip3 install google-generativeai
```

#### Issue 2: "API key not valid"
**Solution:**
```bash
# Check .env file
cat .env
# Should show: GEMINI_API_KEY=AIza...

# Verify key at: https://aistudio.google.com/apikey
# Make sure it's not expired

# Test key:
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

#### Issue 3: "Database error" or "no such table"
**Solution:**
```bash
# Reinitialize database
python3 -c "from app_gemini import app, db; app.app_context().push(); db.drop_all(); db.create_all()"

# Or delete and recreate:
rm gutter_tracker.db
python3 -c "from app_gemini import app, db; app.app_context().push(); db.create_all()"
```

#### Issue 4: "Port 5000 already in use"
**Solution:**
```bash
# Find and kill process:
lsof -ti:5000 | xargs kill -9

# Or use different port:
python3 app_gemini.py
# Edit app_gemini.py, change last line to:
# app.run(debug=True, port=5001)
```

#### Issue 5: "AI features not working"
**Solution:**
```bash
# Test Gemini connection:
python3 << EOF
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content("Say hello")
print(response.text)
EOF

# Should print "Hello!" or similar
# If error, check API key
```

#### Issue 6: "Deployment fails on Vercel"
**Solution:**
```bash
# Check logs:
vercel logs

# Common fixes:
# 1. Make sure vercel.json exists:
cat vercel.json

# 2. Should contain:
{
  "version": 2,
  "builds": [{"src": "app_gemini.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "app_gemini.py"}]
}

# 3. Verify environment variables are set:
vercel env ls

# 4. Redeploy:
vercel --prod --force
```

#### Issue 7: "CSS/Static files not loading"
**Solution:**
```bash
# Check static folder structure:
ls -la static/

# Should have:
# static/style_mobile.css
# static/style.css

# In templates, verify:
# <link rel="stylesheet" href="{{ url_for('static', filename='style_mobile.css') }}">

# Clear browser cache and refresh
```

#### Issue 8: "Photos not uploading"
**Solution:**
```bash
# Check photo data size in HTML:
# Max base64 string length

# In app_gemini.py, add size limit:
# MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB

# Compress large images before upload
```

#### Issue 9: "Database connection timeout (Production)"
**Solution:**
```bash
# For Vercel Postgres:
# 1. Check connection string includes ?sslmode=require
# 2. Add connection pooling:

# In app_gemini.py, add after db initialization:
from sqlalchemy.pool import NullPool
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': NullPool,
    'connect_args': {'sslmode': 'require'}
}
```

#### Issue 10: "Rate limit exceeded"
**Solution:**
```bash
# Gemini free tier: 1,500 requests/day
# Check usage at: https://aistudio.google.com

# Add caching to reduce calls:
# In app_gemini.py, cache similar requests

# Or upgrade to paid tier (very cheap):
# $0.002 per request after free tier
```

### Debug Mode:

```bash
# Enable detailed logging:
# In app_gemini.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug:
python3 app_gemini.py

# Check logs for errors
```

### Getting Help:

```bash
# Check Python version:
python3 --version
# Should be 3.9+

# Check installed packages:
pip3 list | grep -E "flask|google|sqlalchemy"

# Test database:
python3 -c "from app_gemini import app, db, Customer; app.app_context().push(); print(Customer.query.count())"

# Test Gemini:
python3 -c "from app_gemini import get_ai_estimate; print(get_ai_estimate('test', 'test address'))"
```

═══════════════════════════════════════════════════════════════

## 5️⃣ COST BREAKDOWN & HOW TO AVOID THEM

### Free Tier Limits:

#### Gemini API (Recommended):
- **FREE**: 1,500 requests/day (45,000/month)
- **After free**: $0.002 per request (very cheap)
- **Your usage**: ~60 requests/day = $0/month ✅

#### Hosting (Vercel):
- **FREE tier includes**:
  - 100GB bandwidth/month
  - 100 hours build time/month
  - Unlimited deployments
- **Your usage**: Well within free tier ✅

#### Database (Vercel Postgres):
- **FREE tier**:
  - 256MB storage
  - 60 hours compute time/month
- **Your usage**: ~10MB for small business ✅
- **Alternative FREE**: SQLite (unlimited, local)

#### Total Monthly Cost: **$0** ✅

### When You Might Pay:

#### Scenario 1: Heavy Usage
```
If doing 2,000+ AI requests/day:
- First 1,500: FREE
- Next 500: $1.00/day
- Monthly: ~$30

Solution: Use caching, batch requests
```

#### Scenario 2: Large Database
```
If database > 256MB:
- Vercel: $20/month for 1GB
- Alternative: Supabase free tier (500MB)

Solution: Use Supabase instead
```

#### Scenario 3: High Traffic
```
If > 100GB bandwidth/month:
- Vercel: $20/month

Solution: Use Cloudflare CDN (free)
```

### How to Avoid ALL Costs:

#### Strategy 1: Stay Within Free Tiers
```bash
# Monitor usage:
# - Gemini: https://aistudio.google.com
# - Vercel: dashboard.vercel.com

# Set up alerts at 80% of limits
```

#### Strategy 2: Optimize AI Calls
```python
# Add caching in app_gemini.py:
from functools import lru_cache

@lru_cache(maxsize=100)
def get_ai_estimate(job_description, customer_address):
    # Caches last 100 estimates
    # Same request = no API call
```

#### Strategy 3: Use Free Alternatives
```bash
# Database: SQLite (unlimited, free)
DATABASE_URL=sqlite:///gutter_tracker.db

# Hosting alternatives:
# - Railway: $5/month credit (free)
# - Render: Free tier (500 hours/month)
# - Fly.io: Free tier (3GB storage)
```

#### Strategy 4: Self-Host (100% Free)
```bash
# Run on your own computer:
python3 app_gemini.py

# Access via:
# - Local: http://localhost:5000
# - Network: http://your-ip:5000

# Use ngrok for public access (free):
ngrok http 5000
# Gives public URL for testing
```

### Cost Comparison:

| Component | Free Option | Cost | Paid Alternative | Cost |
|-----------|-------------|------|------------------|------|
| AI | Gemini | $0 | Claude | $9-30/mo |
| Hosting | Vercel | $0 | Heroku | $7/mo |
| Database | SQLite | $0 | Heroku Postgres | $9/mo |
| **TOTAL** | **FREE** | **$0** | Paid | $25-46/mo |

### My Recommendation:
**Use 100% free tier setup:**
- Gemini AI (free 1,500/day)
- Vercel hosting (free tier)
- Vercel Postgres (free 256MB) or SQLite
- **Total: $0/month indefinitely** ✅

═══════════════════════════════════════════════════════════════

## 6️⃣ BUG FIXING REFERENCE

### For Your AI Coder:

#### Project Structure:
```
gutter-tracker/
├── app_gemini.py           ← Main app (USE THIS)
├── app_new.py              ← Claude version (backup)
├── requirements_gemini.txt ← Dependencies
├── .env                    ← Config (API keys)
├── .gitignore             ← Protect secrets
├── vercel.json            ← Deployment config
├── static/
│   ├── style_mobile.css   ← Mobile styles
│   └── style.css          ← Desktop styles
├── templates/
│   ├── dashboard.html     ← Home page
│   ├── customers.html     ← Customer list
│   ├── jobs.html          ← Jobs list
│   └── [other templates]
└── gutter_tracker.db      ← SQLite database
```

#### Key Files to Know:

**app_gemini.py** - Main application
```python
# Database models: Customer, Job, Material, etc.
# AI functions: get_ai_estimate(), analyze_photo()
# Routes: All @app.route decorators
# Database: SQLAlchemy with Flask
```

**requirements_gemini.txt** - Python dependencies
```
Flask==3.1.2              # Web framework
flask-sqlalchemy==3.1.1   # Database ORM
google-generativeai==0.8.3 # Gemini AI
python-dotenv==1.0.0      # Environment variables
pillow==10.4.0            # Image processing
```

**.env** - Configuration (NEVER commit to git!)
```bash
GEMINI_API_KEY=your_key
DATABASE_URL=sqlite:///gutter_tracker.db
SECRET_KEY=random_string
```

#### Common Bug Fixes:

**Bug: AI estimate returns error**
```python
# In app_gemini.py, line ~45
def get_ai_estimate(job_description, customer_address):
    try:
        # Add error handling
        if not job_description:
            return "Error: No job description provided"
        
        # Add retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(1)
    except Exception as e:
        return f"Error: {str(e)}"
```

**Bug: Photo upload fails**
```python
# In app_gemini.py, analyze_photo function
# Add size check:
def analyze_photo(photo_base64, context=""):
    try:
        # Check size
        if len(photo_base64) > 5 * 1024 * 1024:  # 5MB
            return "Error: Photo too large. Please compress."
        
        # Rest of function...
```

**Bug: Database connection lost**
```python
# In app_gemini.py, add after app config:
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
```

**Bug: Mobile layout broken**
```css
/* In static/style_mobile.css */
/* Check viewport meta tag in HTML: */
<meta name="viewport" content="width=device-width, initial-scale=1.0">

/* Check media queries are working: */
@media (max-width: 767px) {
    /* Mobile styles */
}
```

**Bug: Deployment fails**
```bash
# Check vercel.json:
{
  "version": 2,
  "builds": [
    {
      "src": "app_gemini.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app_gemini.py"
    }
  ]
}

# Make sure it points to app_gemini.py, not app.py
```

#### Testing Checklist:

```bash
# 1. Test locally
python3 app_gemini.py
# Visit http://localhost:5000

# 2. Test AI features
# - Create job with AI estimate
# - Upload photo with analysis
# - Check responses are reasonable

# 3. Test database
# - Add customer
# - Create job
# - Add materials
# - Refresh page (data should persist)

# 4. Test mobile
# - Open in phone browser
# - Test touch interactions
# - Test camera upload

# 5. Deploy and test production
vercel --prod
# Visit production URL
# Test all features again
```

#### Debug Commands:

```bash
# Check what's running:
ps aux | grep python

# Check database:
sqlite3 gutter_tracker.db ".tables"

# Check environment:
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Gemini key:', os.getenv('GEMINI_API_KEY')[:20])"

# Check Gemini connection:
python3 -c "from app_gemini import gemini_model; print(gemini_model.generate_content('test').text)"

# Check database connection:
python3 -c "from app_gemini import app, db, Customer; app.app_context().push(); print(f'Customers: {Customer.query.count()}')"
```

#### Performance Optimization:

```python
# Add to app_gemini.py:

# 1. Enable caching
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)  # Cache for 5 minutes
def get_ai_estimate(job_description, customer_address):
    # existing code

# 2. Add database indexes
with app.app_context():
    db.engine.execute('CREATE INDEX IF NOT EXISTS idx_customer_name ON customer(name)')
    db.engine.execute('CREATE INDEX IF NOT EXISTS idx_job_status ON job(status)')

# 3. Lazy load relationships
# Already done in models with lazy=True
```

═══════════════════════════════════════════════════════════════

## 📝 QUICK REFERENCE COMMANDS

### Daily Use:
```bash
# Start app locally:
python3 app_gemini.py

# Deploy updates:
git add . && git commit -m "update" && git push
vercel --prod

# Check logs:
vercel logs

# Restart app:
vercel --prod --force
```

### Maintenance:
```bash
# Backup database:
cp gutter_tracker.db gutter_tracker_backup_$(date +%Y%m%d).db

# Update dependencies:
pip3 install --upgrade -r requirements_gemini.txt

# Clear cache:
rm -rf __pycache__ *.pyc

# Reset database:
rm gutter_tracker.db
python3 -c "from app_gemini import app, db; app.app_context().push(); db.create_all()"
```

═══════════════════════════════════════════════════════════════

## ✅ FINAL CHECKLIST

Setup Complete When:
- [ ] Can run `python3 app_gemini.py` successfully
- [ ] Can access http://localhost:5000 in browser
- [ ] Can add a customer and see it persist
- [ ] AI estimate generates a response
- [ ] Photo upload works (optional test)
- [ ] Mobile view looks good (check on phone)
- [ ] Deployed to Vercel with public URL
- [ ] Client can access and use the app

Costs = $0 When:
- [ ] Using Gemini (not Claude)
- [ ] < 1,500 AI requests/day
- [ ] Using Vercel free tier
- [ ] Database < 256MB
- [ ] < 100GB bandwidth/month

═══════════════════════════════════════════════════════════════

## 🎯 SUMMARY

**Use:** app_gemini.py (Gemini AI - FREE)
**Cost:** $0/month (stay within free tiers)
**Setup:** Run `python3 setup_gemini.py`
**Deploy:** Run `vercel --prod`
**Troubleshoot:** Check this guide, Section 4

**Save this file! Give it to your AI coder when fixing bugs.**

═══════════════════════════════════════════════════════════════
