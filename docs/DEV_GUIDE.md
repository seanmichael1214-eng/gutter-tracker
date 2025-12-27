# Developer Guide - Gutter Tracker

Quick reference for developers working on this project.

## Table of Contents
- [Quick Start](#quick-start)
- [Daily Commands](#daily-commands)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)
- [Database](#database)
- [AI Integration](#ai-integration)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### First Time Setup
```bash
# Clone and setup
git clone <repo-url>
cd gutter-tracker

# Run the automated setup
bash scripts/START_HERE_GEMINI.sh

# Or manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy and configure environment
cp config/.env.example .env
# Edit .env and add your keys
```

### Environment Variables Required
```bash
# .env file
DATABASE_URL=postgresql://...           # Neon Postgres URL
GEMINI_API_KEY=your-key-here           # FREE Google Gemini API
APP_PASSWORD=your-password             # Login password
SECRET_KEY=random-secret-key           # Flask session secret
```

---

## Daily Commands

### Development Server
```bash
# Start local development server
python3 app_gemini.py
# Runs on http://localhost:5000

# Or use the run script
bash scripts/run.sh
```

### Quick Deploy
```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel
```

### Database Operations
```bash
# Reset database (drop all tables)
python3 -c "from app_gemini import db; db.drop_all(); db.create_all()"

# Check database connection
python3 -c "from app_gemini import db; print(db.engine.url)"

# Backup database (export to JSON)
python3 -c "from app_gemini import Customer, db; import json; customers = [{'name': c.name, 'phone': c.phone, 'address': c.address} for c in Customer.query.all()]; print(json.dumps(customers))" > backup.json
```

### Testing
```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 tests/test_api_simple.py

# Run API endpoint tests
bash scripts/TEST_COMMANDS.sh

# Test with coverage
python3 -m pytest --cov=. tests/
```

### Git Workflow
```bash
# Daily workflow
git status
git add .
git commit -m "descriptive message"
git push

# Create feature branch
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

---

## Development Workflow

### 1. Making Changes to UI
```bash
# Edit templates
nano templates/dashboard.html

# Edit styles
nano static/style.css

# Changes reflect immediately with Flask debug mode
# Just refresh browser
```

### 2. Adding New Features
```bash
# 1. Edit app_gemini.py to add route/function
# 2. Create/edit template in templates/
# 3. Update CSS if needed in static/
# 4. Test locally
# 5. Deploy with: vercel --prod
```

### 3. Adding New Database Models
```python
# In app_gemini.py, add new model class
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Then reset database
db.drop_all()
db.create_all()
```

---

## Testing

### Test API Endpoints
```bash
# Simple automated test
python3 tests/test_api_simple.py

# Full test with image generation
python3 tests/test_api_endpoints.py

# Manual curl tests
bash scripts/TEST_COMMANDS.sh
```

### Test Frontend
```bash
# Start server
python3 app_gemini.py

# Open browser
open http://localhost:5000

# Test pages:
# / - Splash screen
# /login - Login page
# /dashboard - Main dashboard
# /customers - Customer management
# /jobs - Job tracking
# /inventory - Inventory with AI scanner
# /materials - Materials pricing
# /reports - Reports
# /help - AI tech support
```

### Test AI Features
```bash
# Test Gemini API connection
python3 -c "import google.generativeai as genai; import os; genai.configure(api_key=os.getenv('GEMINI_API_KEY')); model = genai.GenerativeModel('gemini-2.0-flash-exp'); print(model.generate_content('Hello').text)"

# Test AI estimate endpoint
curl -X POST http://localhost:5000/api/ai/estimate \
  -H "Content-Type: application/json" \
  -d '{"house_type":"2-story","linear_feet":"150"}'
```

---

## Deployment

### Vercel Production
```bash
# First time - link project
vercel link

# Deploy to production
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs <deployment-url>
```

### Environment Variables on Vercel
```bash
# Set via CLI
vercel env add DATABASE_URL
vercel env add GEMINI_API_KEY
vercel env add APP_PASSWORD
vercel env add SECRET_KEY

# Or set in Vercel dashboard:
# Settings → Environment Variables
```

### Rollback Deployment
```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote <previous-deployment-url>
```

---

## Database

### Models Overview
- **Customer** - Customer information
- **Job** - Jobs/projects for customers
- **Material** - Material catalog with pricing
- **InventoryItem** - Physical inventory tracking
- **JobMaterial** - Materials used in jobs
- **JobPhoto** - Photos attached to jobs

### Common Database Queries
```python
# In Python shell or app_gemini.py

# Get all customers
from app_gemini import Customer, db
customers = Customer.query.all()

# Search customers
customers = Customer.query.filter(
    Customer.name.ilike('%john%')
).all()

# Get customer with jobs
customer = Customer.query.get(1)
jobs = customer.jobs

# Create new customer
new_customer = Customer(
    name="John Doe",
    phone="555-1234",
    address="123 Main St",
    email="john@example.com"
)
db.session.add(new_customer)
db.session.commit()

# Update customer
customer = Customer.query.get(1)
customer.phone = "555-9999"
db.session.commit()

# Delete customer
customer = Customer.query.get(1)
db.session.delete(customer)
db.session.commit()
```

---

## AI Integration

### Gemini API Usage
```python
# In app_gemini.py

# Initialize Gemini
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Text generation
response = model.generate_content("Your prompt here")
print(response.text)

# Vision (with image)
import base64
image_data = base64.b64decode(photo_data.split(',')[1])
image_part = {"mime_type": "image/jpeg", "data": image_data}
response = model.generate_content(["Describe this image", image_part])
```

### AI Endpoints
- `POST /api/ai/estimate` - Generate job estimate
- `POST /api/ai/analyze-photo` - Analyze gutter photo
- `POST /api/ai/scan-inventory` - Identify materials in photo
- `POST /api/ai/help` - AI tech support chat
- `POST /api/ai/suggest-schedule` - Schedule optimization
- `POST /api/ai/estimate-from-photo` - Estimate from house photo

### AI Prompt Engineering Tips
```python
# Good prompt structure
prompt = f"""
You are a gutter installation expert.

CONTEXT:
- House type: {house_type}
- Linear feet: {linear_feet}

TASK:
Provide an accurate estimate.

FORMAT:
- Material costs
- Labor costs
- Total price

Be specific and professional.
"""
```

---

## Troubleshooting

### Server Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000
kill -9 <PID>

# Check Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Connection Issues
```bash
# Test database connection
python3 -c "from app_gemini import db; print(db.engine.url)"

# Check DATABASE_URL format
# Should be: postgresql://user:pass@host/dbname

# Reset database
python3 -c "from app_gemini import db; db.drop_all(); db.create_all()"
```

### Gemini API Errors
```bash
# Verify API key
echo $GEMINI_API_KEY

# Test API directly
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$GEMINI_API_KEY \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# Common issues:
# - Invalid API key → Get new key from ai.google.dev
# - Rate limit → Wait or upgrade plan (free tier: 15 req/min)
# - Model not found → Update model name in app_gemini.py
```

### Vercel Deployment Issues
```bash
# Check build logs
vercel logs <deployment-url>

# Verify environment variables
vercel env ls

# Test build locally
vercel dev

# Common issues:
# - Missing env vars → Add with: vercel env add
# - Build timeout → Optimize dependencies
# - Runtime error → Check logs with: vercel logs
```

### Login Issues
```bash
# Check APP_PASSWORD in .env
cat .env | grep APP_PASSWORD

# Session issues - clear browser cookies/cache

# Reset session secret
# Generate new SECRET_KEY and update .env
```

---

## Code Style

### Python
```python
# Follow PEP 8
# Use 4 spaces for indentation
# Max line length: 100 characters

# Good function naming
def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)

# Use type hints where helpful
def calculate_total(items: list[dict]) -> float:
    return sum(item['price'] for item in items)
```

### HTML/CSS
```html
<!-- Use semantic HTML -->
<nav class="navbar">
    <ul>
        <li><a href="/">Home</a></li>
    </ul>
</nav>

<!-- Use CSS custom properties -->
<style>
:root {
    --accent: #00d4aa;
    --touch-min: 54px;
}

.btn {
    background: var(--accent);
    min-height: var(--touch-min);
}
</style>
```

---

## Useful Resources

### Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Gemini API: https://ai.google.dev/docs
- Vercel: https://vercel.com/docs

### Project Docs
- [COMPLETE_GUIDE.md](docs/COMPLETE_GUIDE.md) - Full system documentation
- [API_TESTING_README.md](docs/API_TESTING_README.md) - API testing guide
- [BROTHER_GUIDE.md](docs/BROTHER_GUIDE.md) - User guide for end users
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and fixes

### Getting Help
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check app logs: `vercel logs`
3. Test AI endpoint: `/help` page has AI assistant
4. Check GitHub issues (if repo public)

---

## Quick Command Reference

```bash
# Development
python3 app_gemini.py              # Start dev server
vercel dev                         # Start Vercel dev server
vercel --prod                      # Deploy to production

# Testing
python3 tests/test_api_simple.py   # Run API tests
python3 -m pytest tests/           # Run all tests
bash scripts/TEST_COMMANDS.sh      # Manual API tests

# Database
python3 -c "from app_gemini import db; db.create_all()"    # Create tables
python3 -c "from app_gemini import db; db.drop_all()"      # Drop tables

# Git
git status                         # Check changes
git add .                          # Stage all changes
git commit -m "message"            # Commit changes
git push                           # Push to remote

# Utilities
vercel logs                        # View deployment logs
vercel env ls                      # List environment variables
vercel ls                          # List deployments
```

---

Made with ❤️ for the gutter business. Questions? Check `/help` page for AI assistant.
