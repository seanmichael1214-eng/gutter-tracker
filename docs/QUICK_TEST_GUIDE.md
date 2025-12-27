# Quick API Test Guide - Gutter Tracker

## Run All Tests
```bash
python3 test_api_simple.py
```

## Individual Endpoint Tests (cURL)

### 1. Test AI Estimate (No Photo Required)
```bash
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Replace 50 feet of K-style gutters, install 2 downspouts",
    "address": "123 Main St, Seattle, WA"
  }' | python3 -m json.tool
```

### 2. Test AI Help (No Photo Required)
```bash
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/help \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I add a new customer to the app?"
  }' | python3 -m json.tool
```

### 3. Test Schedule Suggestion (No Photo Required)
```bash
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/suggest-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "address": "456 Oak Ave, Portland, OR"
  }' | python3 -m json.tool
```

### 4. Test Photo Analysis (Requires Photo)
First, create a test base64 image:
```bash
# Convert a local image to base64
BASE64_IMAGE=$(base64 -i test_house.jpg | tr -d '\n')
echo "data:image/jpeg;base64,$BASE64_IMAGE" > photo_data.txt

# Use it in the request
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/analyze-photo \
  -H "Content-Type: application/json" \
  -d "{
    \"photo_data\": \"$(cat photo_data.txt)\",
    \"context\": \"Analyzing damaged gutters\"
  }" | python3 -m json.tool
```

### 5. Test Inventory Scanner (Requires Photo)
```bash
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/scan-inventory \
  -H "Content-Type: application/json" \
  -d "{
    \"photo_data\": \"$(cat photo_data.txt)\"
  }" | python3 -m json.tool
```

### 6. Test Estimate from Photo (Requires Photo)
```bash
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/estimate-from-photo \
  -H "Content-Type: application/json" \
  -d "{
    \"photo_data\": \"$(cat photo_data.txt)\"
  }" | python3 -m json.tool
```

## Expected Results Quick Reference

✅ **Success Response** (Status 200):
```json
{
  "success": true,
  "estimate": "...",  // or "analysis", "answer", etc.
  "provider": "Google Gemini (FREE)"
}
```

❌ **Error Response** (Status 400):
```json
{
  "error": "Description required"
}
```

❌ **Server Error** (Status 500):
```json
{
  "success": false,
  "error": "Error message"
}
```

## What to Look For

### Signs of Success:
- HTTP status 200
- "success": true in response
- Meaningful AI-generated content
- Response time < 30 seconds
- Provider: "Google Gemini (FREE)"

### Signs of Problems:
- HTTP status 400 (bad request - check your data)
- HTTP status 500 (server error - check Vercel logs)
- Timeout (Gemini API slow or down)
- "Error generating estimate" (GEMINI_API_KEY issue)
- Empty responses

## Debugging Steps

1. **Check Vercel is live:**
   ```bash
   curl -I https://gutter-tracker-eta.vercel.app
   ```

2. **Check environment variables in Vercel dashboard:**
   - GEMINI_API_KEY must be set
   - SECRET_KEY should be set
   - DATABASE_URL (optional)

3. **Check Vercel logs:**
   ```bash
   vercel logs gutter-tracker-eta.vercel.app
   ```

4. **Test with minimal request:**
   ```bash
   curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/help \
     -H "Content-Type: application/json" \
     -d '{"question":"test"}' -v
   ```

## Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| 500 error | Missing GEMINI_API_KEY | Set in Vercel env vars |
| Timeout | Gemini API slow | Increase timeout or retry |
| 400 error | Missing required field | Check request payload |
| Empty response | API key quota exceeded | Check Gemini dashboard |
| CORS error | Cross-origin request | Add CORS headers (if testing from browser) |

## Quick Health Check
```bash
# Test the simplest endpoint
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/help \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}' \
  -w "\nStatus: %{http_code}\n"
```

If this works, all endpoints should work (they all use the same Gemini setup).
