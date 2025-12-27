# Gemini AI Context - Gutter Tracker

Context file for Google Gemini AI when working on this codebase.

## Project Summary

**App:** Gutter Tracker - Business management for gutter installation/cleaning  
**URL:** https://gutter-tracker-app.fly.dev  
**Status:** Production (deployed Dec 27, 2025)  
**Framework:** Flask 3.1.2 + SQLAlchemy + PostgreSQL  
**Hosting:** Fly.io

## Your Role in This App

This Flask app **uses Gemini API** for AI features:
- Photo analysis for job estimates (`app/ai.py`)
- Inventory scanning via camera
- Help chatbot in `/help` page
- Quick estimate generation

### Gemini Integration Points

**File:** `app/ai.py`

```python
import google.generativeai as genai

gemini_model = genai.GenerativeModel('gemini-pro')

def get_ai_estimate(description, address):
    """Generate cost estimate for gutter job"""
    
def analyze_photo(photo_data, context):
    """Analyze uploaded photo for materials/damage"""
```

**API Routes Using Gemini:**
- `POST /api/ai/help` - Chatbot
- `POST /api/ai/estimate` - Job cost estimation
- `POST /api/ai/scan-inventory` - Photo scanning
- `POST /api/chat` - General chat commands

## Quick Commands

```bash
# Run locally
make run              # http://127.0.0.1:5001
make test             # Run tests

# Deploy to production
flyctl deploy --app gutter-tracker-app

# Check logs
flyctl logs --app gutter-tracker-app
```

## Project Structure

```
app/
├── ai.py              # ← GEMINI INTEGRATION HERE
├── routes.py          # All HTTP endpoints
├── models.py          # Database models
├── __init__.py        # Flask factory
├── config.py          # Configuration
├── templates/         # HTML pages
│   ├── help.html      # Uses Gemini chatbot
│   ├── quick_estimate.html  # Uses Gemini for estimates
│   └── inventory.html # Uses Gemini for scanning
└── static/           # CSS/JS
```

## Database Models

```python
# app/models.py
Customer - Business/homeowner info
Job - Installation/cleaning jobs
  - scheduled_date (for calendar)
  - status (scheduled/in-progress/completed)
  - total_cost, ai_estimate
InventoryItem - Materials tracking
  - owner_id (multi-user support)
Material - Material types/costs
JobPhoto - Photos attached to jobs
  - ai_analysis (stores Gemini response)
```

## Environment Variables

**Gemini API Key:**
```bash
# Development (.env)
GEMINI_API_KEY=your-key-here

# Production (Fly.io)
flyctl secrets set GEMINI_API_KEY="..." --app gutter-tracker-app
```

**Other Required Vars:**
- `SECRET_KEY` - Flask session security
- `APP_PASSWORD` - Login password (NAO$)
- `DATABASE_URL` - PostgreSQL connection string

## AI Feature Usage

### 1. Help Chatbot (`/help`)
User asks questions → Gemini provides answers  
Route: `POST /api/ai/help`

### 2. Quick Estimate (`/quick-estimate`)
Upload photo → Gemini analyzes → Cost estimate  
Route: `POST /api/ai/estimate`

### 3. Inventory Scanner (`/inventory`)
Camera scan → Gemini identifies materials → Auto-add to inventory  
Route: `POST /api/ai/scan-inventory`

### 4. Job Photo Analysis
Attach photo to job → Gemini analyzes damage/needs  
Used in: `POST /jobs/<id>/add_photo`

## Code Patterns

### Error Handling (Always use try/except)
```python
try:
    response = gemini_model.generate_content(prompt)
    return jsonify({"success": True, "data": response.text})
except Exception as e:
    current_app.logger.error(f"Gemini API error: {e}")
    return jsonify({"success": False, "error": str(e)}), 500
```

### Standard Response Format
```python
{
    "success": True/False,
    "data": "...",         # On success
    "error": "...",        # On failure
    "provider": "LocalFallback"  # If Gemini unavailable
}
```

## Recent Production Issues (Lessons Learned)

### 1. Missing Routes Crash App
**Problem:** Templates had links to `/materials`, `/reports` but routes didn't exist  
**Solution:** Always verify template `href` links have matching routes

### 2. Memory Issues on Fly.io
**Problem:** App crashed with OOM errors  
**Solution:** Increased to 512MB RAM, reduced to 1 worker  
**Config:** `fly.toml` and `fly_start.sh`

### 3. Logging in Production
**Problem:** FileHandler failed on read-only filesystem  
**Solution:** Use StreamHandler in `app/__init__.py`

### 4. Calendar Feature Added
**New:** `/calendar` route shows monthly job schedule  
**Update:** Navigation links in all templates

## Testing

### Test Gemini Integration
```python
# tests/test_ai.py
def test_ai_estimate(mocker):
    mock_response = mocker.Mock()
    mock_response.text = "Estimated cost: $500"
    mocker.patch('app.ai.gemini_model.generate_content', return_value=mock_response)
    
    result = get_ai_estimate("Clean gutters", "123 Main St")
    assert "$500" in result
```

### Manual Testing
```bash
# Start dev server
make run

# Test help endpoint
curl -X POST http://127.0.0.1:5001/api/ai/help \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I add a customer?"}'
```

## Common Tasks

### Update AI Prompt
Edit `app/ai.py`:
```python
def get_ai_estimate(description, address):
    prompt = f"""
    You are a gutter expert. Analyze this job:
    Description: {description}
    Location: {address}
    
    Provide cost estimate with breakdown.
    """
    response = gemini_model.generate_content(prompt)
    return response.text
```

### Add New AI Feature
1. Add function to `app/ai.py`
2. Create route in `app/routes.py`
3. Add UI in relevant template
4. Test with `make test`
5. Deploy: `flyctl deploy --app gutter-tracker-app`

## Troubleshooting

### Gemini API Not Working
```bash
# Check if key is set
flyctl secrets list --app gutter-tracker-app | grep GEMINI

# Test locally
export GEMINI_API_KEY="your-key"
python3 -c "import google.generativeai as genai; print(genai.list_models())"

# Check logs
flyctl logs --app gutter-tracker-app | grep -i gemini
```

### Rate Limiting
Add retry logic:
```python
import time
from google.api_core import retry

@retry.Retry()
def call_gemini(prompt):
    return gemini_model.generate_content(prompt)
```

### Error: "Gemini API error"
- Check API key is valid
- Verify API quota not exceeded
- Ensure `google-generativeai` package installed
- Check internet connectivity

## Production Checklist

Before deploying AI features:
- [ ] Test Gemini API call locally
- [ ] Add error handling (try/except)
- [ ] Provide fallback response if API fails
- [ ] Log errors with `current_app.logger`
- [ ] Test with mock/real API key
- [ ] Verify Fly.io has GEMINI_API_KEY secret
- [ ] Deploy and check logs for errors

## All Routes (Reference)

Core Pages:
- `/` - Splash/landing
- `/login` - Auth (password: NAO$)
- `/dashboard` - Main dashboard
- `/customers` - Customer list
- `/jobs` - Job tracking
- `/calendar` - **NEW** Monthly job schedule
- `/inventory` - Inventory with AI scanner
- `/materials` - Materials database
- `/reports` - Analytics
- `/quick-estimate` - AI photo estimates
- `/help` - AI chatbot (uses Gemini)

API Endpoints (AI):
- `POST /api/ai/help` - Chatbot
- `POST /api/ai/estimate` - Cost estimation
- `POST /api/ai/scan-inventory` - Photo scanning
- `POST /api/chat` - General commands

## Current Status

**Deployment:** ✅ Production on Fly.io  
**Features:** ✅ All working, tested Dec 27, 2025  
**Issues:** ✅ None known  
**Recent:** ✅ Added calendar view  
**Gemini:** ✅ API integrated, key configured  

## Contact & Resources

- **Production App:** https://gutter-tracker-app.fly.dev
- **Password:** NAO$
- **Gemini Docs:** https://ai.google.dev/docs
- **This Guide:** `/GEMINI.md`
- **Agent Guide:** `/AGENTS.md`
- **Claude Guide:** `/CLAUDE.md`

---

**For AI Developers:** This app actively uses Gemini API for intelligent features. When debugging or extending, always check `app/ai.py` and ensure proper error handling for API calls.
