# 🚀 Deploy Gutter Tracker to Render (5 Minutes)

## Step 1: Push to GitHub

```bash
cd /Users/Sean/code/gutter-tracker
git push origin main
```

Wait for the push to complete (may take 1-2 minutes).

---

## Step 2: Sign Up/Login to Render

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign in with GitHub"** (easiest)
4. Authorize Render to access your repositories

---

## Step 3: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account if prompted
4. Find **"gutter-tracker"** in the repository list
5. Click **"Connect"**

---

## Step 4: Configure the Service

Render will auto-detect everything from `render.yaml`, but verify:

**Basic Settings:**
- **Name**: `gutter-tracker` (auto-filled)
- **Runtime**: `Python` (auto-detected)
- **Build Command**: `pip install -r requirements.txt` (auto-filled)
- **Start Command**: `./start.sh` (auto-filled)

**Environment Variables** (will be created automatically from render.yaml):
- `PYTHON_VERSION` = 3.11.0 ✅
- `SECRET_KEY` = (auto-generated) ✅
- `DATABASE_URL` = (from database) ✅
- `GEMINI_API_KEY` = **YOU NEED TO ADD THIS**
- `APP_PASSWORD` = **YOU NEED TO ADD THIS**

---

## Step 5: Add Your Environment Variables

In the Render dashboard:

1. Scroll to **"Environment Variables"** section
2. Click **"Add Environment Variable"**

**Add these two:**

```
Key: GEMINI_API_KEY
Value: AIzaSyBzL5HtpnpebjBb6IXsduYilv6PWzbx70g
```

```
Key: APP_PASSWORD  
Value: NAO$
```

---

## Step 6: Create Database (Optional - may auto-create)

If database isn't auto-created:

1. Click **"New +"** → **"PostgreSQL"**
2. Name: `gutter-tracker-db`
3. Plan: **Free**
4. Click **"Create Database"**

Then link it:
1. Go back to your web service
2. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: Internal Database URL from the database you just created

---

## Step 7: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will:
   - ✅ Clone your GitHub repo
   - ✅ Install dependencies
   - ✅ Create PostgreSQL database
   - ✅ Initialize database tables (via start.sh)
   - ✅ Start your app

**This takes ~3-5 minutes**

---

## Step 8: Get Your URL

Once deployed, you'll see:

```
Your service is live at https://gutter-tracker-xxxx.onrender.com
```

**Test it:**
- Visit the URL
- Should see the splash screen
- Login with password: `NAO$`
- All features work!

---

## 📋 Post-Deployment Checklist

- [ ] App loads at the Render URL
- [ ] Can login with APP_PASSWORD
- [ ] Dashboard shows (even if empty)
- [ ] Can create a customer
- [ ] Can view /home with customer tabs
- [ ] AI features work (test quick estimate)

---

## 🔧 Troubleshooting

### If deployment fails:

**Check Build Logs:**
1. In Render dashboard, click your service
2. Go to **"Logs"** tab
3. Look for red error messages

**Common Issues:**

❌ **"Module not found"**
→ Check `requirements.txt` has all packages

❌ **"Database connection failed"**  
→ Verify `DATABASE_URL` is linked to your Postgres database

❌ **"Application failed to start"**
→ Check `start.sh` has correct Python path

---

## 🎉 Success!

Your app is now live at:
**https://gutter-tracker-xxxx.onrender.com**

- ✅ Free PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Auto-deploys on git push
- ✅ Free 750 hours/month

**Note:** Free tier apps sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## 🚀 Share With Client

Send them:
- **URL**: https://gutter-tracker-xxxx.onrender.com
- **Password**: NAO$
- **Features**: See CLIENT_PRODUCT_SUMMARY.md

---

**Need help?** The app works perfectly locally, so any issues are hosting-specific. Check Render logs or try redeploying.
