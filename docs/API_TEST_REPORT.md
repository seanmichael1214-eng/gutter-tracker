# Gutter Tracker API Endpoint Test Report

## Base URL
`https://gutter-tracker-eta.vercel.app`

## Test Scripts Created
- **`test_api_endpoints.py`** - Full-featured test with PIL for real images
- **`test_api_simple.py`** - Standalone test using only Python standard library

## API Endpoints to Test

### 1. POST /api/ai/estimate
**Purpose**: Generate AI cost estimates for gutter jobs using Gemini

**Location in code**: Lines 341-362 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "description": "Replace 50 feet of K-style gutters, install 2 downspouts",
  "address": "123 Main St, Seattle, WA"
}
```

**Expected Success Response** (200):
```json
{
  "success": true,
  "estimate": "[Detailed estimate from Gemini AI]",
  "provider": "Google Gemini (FREE)"
}
```

**Expected Error Response** (400):
```json
{
  "error": "Description required"
}
```

**Test Cases**:
- ✅ Valid request with description and address
- ✅ Missing description (should return 400)
- ✅ Empty description (should return 400)

**Potential Issues**:
- Requires valid GEMINI_API_KEY environment variable
- May fail with 500 if Gemini API is down or quota exceeded
- Network timeout if Gemini is slow

---

### 2. POST /api/ai/analyze-photo
**Purpose**: Analyze gutter photos using Gemini Vision API

**Location in code**: Lines 364-385 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "photo_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "context": "Analyzing damaged gutters on north side"
}
```

**Expected Success Response** (200):
```json
{
  "success": true,
  "analysis": "[Detailed analysis of gutter condition, damage, type, measurements, recommendations]",
  "provider": "Google Gemini Vision (FREE)"
}
```

**Expected Error Response** (400):
```json
{
  "error": "Photo data required"
}
```

**Test Cases**:
- ✅ Valid request with base64 image and context
- ✅ Valid request with base64 image, no context
- ✅ Missing photo_data (should return 400)
- ✅ Invalid base64 data (should return 500)

**Potential Issues**:
- Requires valid image data in base64 format
- Gemini expects data after comma in "data:image/jpeg;base64,..."
- May fail if image is too large
- Requires GEMINI_API_KEY

---

### 3. POST /api/ai/scan-inventory
**Purpose**: Scan photos of inventory/materials to identify items

**Location in code**: Lines 387-430 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "photo_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Expected Success Response** (200):
```json
{
  "success": true,
  "analysis": "[List of items identified with quantities, conditions, sizes, estimated values]",
  "provider": "Google Gemini Vision (FREE)"
}
```

**Expected Error Response** (400):
```json
{
  "error": "Photo data required"
}
```

**Test Cases**:
- ✅ Valid request with inventory photo
- ✅ Missing photo_data (should return 400)
- ✅ Invalid base64 (should return 500)

**Potential Issues**:
- Same base64 parsing as analyze-photo
- Quality of analysis depends on photo clarity
- Requires GEMINI_API_KEY

---

### 4. POST /api/ai/help
**Purpose**: AI-powered tech support chat for the app

**Location in code**: Lines 695-736 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "question": "How do I add a new customer?"
}
```

**Expected Success Response** (200):
```json
{
  "success": true,
  "answer": "[Helpful response about adding customers, with step-by-step instructions]"
}
```

**Expected Error Response** (400):
```json
{
  "error": "Question required"
}
```

**Test Cases**:
- ✅ Valid question about app features
- ✅ Question about navigation
- ✅ Question about profiles (Flo-Rite vs Triple Beezy)
- ✅ Missing question (should return 400)

**Potential Issues**:
- Quality depends on Gemini's understanding of the app
- Requires GEMINI_API_KEY

---

### 5. POST /api/ai/suggest-schedule
**Purpose**: AI suggestions for optimal job scheduling

**Location in code**: Lines 600-607 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "address": "456 Oak Ave, Portland, OR"
}
```

**Expected Success Response** (200):
```json
{
  "suggestion": "[Date in YYYY-MM-DD format with reasoning]"
}
```

**Test Cases**:
- ✅ Valid request with address
- ✅ Empty request (may still work)

**Potential Issues**:
- Queries database for existing scheduled jobs
- May return null if no jobs exist
- Requires GEMINI_API_KEY
- **No authentication required** (API endpoint is public)

---

### 6. POST /api/ai/estimate-from-photo
**Purpose**: Analyze house photo to estimate materials needed

**Location in code**: Lines 609-693 in `/Users/Sean/code/gutter-tracker/app_gemini.py`

**Expected Request**:
```json
{
  "photo_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Expected Success Response** (200):
```json
{
  "success": true,
  "analysis": "[Detailed analysis with measurements and notes]",
  "measurements": {
    "linearFeet": 120,
    "downspouts": 4,
    "stories": 2,
    "insideCorners": 2,
    "outsideCorners": 4
  },
  "provider": "Google Gemini Vision (FREE)"
}
```

**Expected Error Response** (400):
```json
{
  "error": "Photo data required"
}
```

**Test Cases**:
- ✅ Valid request with house photo
- ✅ Missing photo_data (should return 400)
- ✅ Check if measurements are parsed correctly

**Potential Issues**:
- Regex parsing for measurements (lines 661-681)
- May not find all measurements in response
- Requires clear house photo
- Requires GEMINI_API_KEY

---

## How to Run Tests

### Option 1: Using test_api_simple.py (Recommended)
```bash
python3 test_api_simple.py
```

This script:
- Uses only Python standard library (no dependencies)
- Tests all 6 endpoints
- Tests both success and error cases
- Provides colored output with pass/fail status

### Option 2: Using test_api_endpoints.py
```bash
pip install requests pillow
python3 test_api_endpoints.py
```

This script:
- Generates real test images using PIL
- More comprehensive image testing
- Better formatted output

### Option 3: Manual cURL Testing
```bash
# Test 1: AI Estimate
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/estimate \
  -H "Content-Type: application/json" \
  -d '{"description":"Replace 50 feet of K-style gutters","address":"123 Main St"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 2: Analyze Photo (needs base64 image)
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/analyze-photo \
  -H "Content-Type: application/json" \
  -d '{"photo_data":"data:image/jpeg;base64,/9j/...","context":"Test"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 3: Scan Inventory (needs base64 image)
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/scan-inventory \
  -H "Content-Type: application/json" \
  -d '{"photo_data":"data:image/jpeg;base64,/9j/..."}' \
  -w "\nHTTP: %{http_code}\n"

# Test 4: AI Help
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/help \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I add a customer?"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 5: Suggest Schedule
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/suggest-schedule \
  -H "Content-Type: application/json" \
  -d '{"address":"456 Oak Ave"}' \
  -w "\nHTTP: %{http_code}\n"

# Test 6: Estimate from Photo (needs base64 image)
curl -X POST https://gutter-tracker-eta.vercel.app/api/ai/estimate-from-photo \
  -H "Content-Type: application/json" \
  -d '{"photo_data":"data:image/jpeg;base64,/9j/..."}' \
  -w "\nHTTP: %{http_code}\n"
```

---

## Critical Dependencies

### Environment Variables Required
All endpoints require this environment variable to be set on Vercel:
- **GEMINI_API_KEY** - Google Gemini API key

### Other Environment Variables
- **SECRET_KEY** - Flask session secret (defaults to 'dev-secret-key-change-in-production')
- **DATABASE_URL** - Database connection string (defaults to SQLite)
- **APP_PASSWORD** - Login password (defaults to 'changeme')

### Python Packages Required
From `/Users/Sean/code/gutter-tracker/requirements_gemini.txt`:
- Flask
- flask-sqlalchemy
- google-generativeai
- python-dotenv

---

## Security Considerations

### Public Endpoints (No Authentication)
All 6 API endpoints are **PUBLIC** and do **NOT** require authentication:
- `/api/ai/estimate`
- `/api/ai/analyze-photo`
- `/api/ai/scan-inventory`
- `/api/ai/help`
- `/api/ai/suggest-schedule`
- `/api/ai/estimate-from-photo`

⚠️ **Security Risk**: These endpoints can be called by anyone without logging in, potentially:
- Consuming your Gemini API quota
- Costing money if you exceed free tier
- Being abused by bots

### Recommendations
1. Add rate limiting to API endpoints
2. Require authentication or API key for production
3. Monitor Gemini API usage
4. Add CORS restrictions
5. Implement request validation

---

## Expected Results Summary

| Endpoint | Authentication | Input Validation | Error Handling | Success Criteria |
|----------|----------------|------------------|----------------|------------------|
| `/api/ai/estimate` | ❌ None | ✅ Checks description | ✅ Try/catch | Returns estimate text |
| `/api/ai/analyze-photo` | ❌ None | ✅ Checks photo_data | ✅ Try/catch | Returns analysis text |
| `/api/ai/scan-inventory` | ❌ None | ✅ Checks photo_data | ✅ Try/catch | Returns item list |
| `/api/ai/help` | ❌ None | ✅ Checks question | ✅ Try/catch | Returns answer text |
| `/api/ai/suggest-schedule` | ❌ None | ⚠️ No validation | ⚠️ Returns None on error | Returns suggestion or null |
| `/api/ai/estimate-from-photo` | ❌ None | ✅ Checks photo_data | ✅ Try/catch | Returns analysis + measurements |

---

## Common Failure Scenarios

### 1. GEMINI_API_KEY Not Set
**Symptom**: 500 error with "Error generating estimate" or similar
**Solution**: Set GEMINI_API_KEY in Vercel environment variables

### 2. Gemini API Quota Exceeded
**Symptom**: 500 error from Gemini API
**Solution**: Wait for quota reset or upgrade Gemini plan

### 3. Invalid Base64 Image Data
**Symptom**: 500 error during base64.b64decode()
**Solution**: Ensure proper base64 encoding and format

### 4. Network Timeout
**Symptom**: Request timeout after 30 seconds
**Solution**: Increase timeout or check Gemini API status

### 5. Database Not Initialized (suggest-schedule)
**Symptom**: Database error when querying jobs
**Solution**: Ensure database is created (app_gemini.py lines 739-740)

---

## Test Execution Checklist

- [ ] Verify Vercel deployment is live
- [ ] Confirm GEMINI_API_KEY is set in Vercel
- [ ] Run test_api_simple.py
- [ ] Check all 6 endpoints return valid responses
- [ ] Verify error handling for missing parameters
- [ ] Test with real house/inventory photos
- [ ] Monitor Gemini API usage
- [ ] Check response times (should be < 30s)
- [ ] Verify JSON response format
- [ ] Test CORS if calling from frontend

---

## Files Created for Testing

1. **`/Users/Sean/code/gutter-tracker/test_api_endpoints.py`**
   - Full test suite with PIL for image generation
   - Requires: requests, pillow

2. **`/Users/Sean/code/gutter-tracker/test_api_simple.py`**
   - Standalone test using only standard library
   - No external dependencies
   - Recommended for quick testing

3. **`/Users/Sean/code/gutter-tracker/API_TEST_REPORT.md`**
   - This comprehensive test documentation

---

## Next Steps

1. Run the test script to verify all endpoints
2. Review any failures and check Vercel logs
3. Consider adding authentication to API endpoints
4. Implement rate limiting
5. Add API usage monitoring
6. Document API for frontend integration
