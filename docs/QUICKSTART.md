# 🚀 QUICK START - Gutter Tracker AI App

## ⚡ 5-Minute Setup

### Step 1: Run Setup Wizard
```bash
cd /Users/Sean/code/gutter-tracker
python3 setup_wizard.py
```

This will:
- Guide you through API key setup
- Create your .env file
- Initialize the database
- Make everything ready to go

### Step 2: Get Your API Keys

**Anthropic API Key** (Required for AI features):
1. Go to https://console.anthropic.com
2. Sign up (they give free credits!)
3. Create API key
4. Copy it (starts with `sk-ant-...`)

**Database** (For production):
- **Easy**: Use SQLite for local testing (no setup needed!)
- **Production**: Get free PostgreSQL from:
  - Vercel Postgres: https://vercel.com/storage
  - Supabase: https://supabase.com (generous free tier)

### Step 3: Test Locally
```bash
python3 app_new.py
```
Open http://localhost:5000 🎉

### Step 4: Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Then add your environment variables in the Vercel dashboard.

---

## 🎯 For Your Client

### What They Get:
✅ Mobile-friendly interface  
✅ AI cost estimates (saves 30 min per quote!)  
✅ Photo analysis (identifies damage instantly)  
✅ Smart scheduling  
✅ Inventory tracking  
✅ Customer management  
✅ Financial reports  

### Training (5 minutes):
1. **Add a customer** - Click Customers → Add Customer
2. **Create a job** - Click Jobs → New Job → Check "Use AI Estimate"
3. **Take photos** - Open job → Add Photo → AI will analyze it
4. **Track materials** - Click Inventory → Add items as you buy them

### Mobile Usage:
- Works on any phone/tablet
- Take photos on-site with camera
- Get instant AI estimates
- Update job status in the field

---

## 🤖 AI Features Explained

### 1. Smart Estimates
Input: "Replace 80 feet of gutters, 3 downspouts"  
AI Output:
- Estimated hours: 6-8 hours
- Materials needed (with quantities)
- Cost breakdown
- Price range: $1,200-$1,800
- Notes about potential issues

### 2. Photo Analysis
Take photo of damaged gutters  
AI identifies:
- Damage type (rust, sagging, clogged)
- Gutter style (K-style, half-round)
- Urgency level
- Repair recommendations

### 3. Smart Scheduling
AI suggests best date based on:
- Nearby jobs (route optimization)
- Current workload
- Weather patterns

---

## 💰 Cost Savings

**Traditional Method:**
- 30-45 min per estimate
- Manual pricing calculations
- Missed opportunities
- Scheduling conflicts

**With Gutter Tracker AI:**
- 2-3 min per estimate ⚡
- AI-powered pricing 🤖
- Quick photo assessments 📸
- Optimized scheduling 📅

**ROI: Save 20+ hours/month!**

---

## 📞 Quick Help

**App won't start?**
```bash
pip3 install -r requirements.txt
python3 app_new.py
```

**AI not working?**
- Check ANTHROPIC_API_KEY in .env
- Verify you have API credits

**Need database?**
- Local: Use SQLite (already setup!)
- Production: Get free Postgres from Supabase

**Deploy failing?**
```bash
vercel --prod
# Then add env vars in Vercel dashboard
```

---

## 🎉 You're Ready!

Run `python3 setup_wizard.py` and follow the prompts.

Questions? Check the full README.md for detailed docs.

**Your client will love this! 💪**
