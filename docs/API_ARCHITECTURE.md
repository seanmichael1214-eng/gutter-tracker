# Gutter Tracker API Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Gutter Tracker Web App                        │
│              https://gutter-tracker-eta.vercel.app              │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │
                    ┌────────────┴────────────┐
                    │                         │
              ┌─────▼──────┐           ┌─────▼──────┐
              │  Web Pages │           │ API Routes │
              │ (Protected)│           │  (PUBLIC)  │
              └────────────┘           └─────┬──────┘
              Login Required                 │
              Dashboard, Jobs,               │
              Customers, etc.                │
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
              │         ALL PUBLIC (NO AUTHENTICATION)                      │
              │                              │                              │
┌─────────────▼──────────┐   ┌──────────────▼──────────┐   ┌──────────────▼──────────┐
│  /api/ai/estimate      │   │ /api/ai/analyze-photo   │   │ /api/ai/scan-inventory  │
│                        │   │                         │   │                         │
│  Input: description,   │   │  Input: photo_data,     │   │  Input: photo_data      │
│         address        │   │         context         │   │                         │
│                        │   │                         │   │  Output: Material list  │
│  Output: Cost estimate │   │  Output: Damage analysis│   │          with details   │
└────────────┬───────────┘   └────────────┬────────────┘   └────────────┬────────────┘
             │                            │                             │
┌────────────▼───────────┐   ┌────────────▼────────────┐   ┌───────────▼─────────────┐
│  /api/ai/help          │   │ /api/ai/suggest-schedule│   │/api/ai/estimate-from-   │
│                        │   │                         │   │      photo              │
│  Input: question       │   │  Input: address         │   │                         │
│                        │   │                         │   │  Input: photo_data      │
│  Output: Help answer   │   │  Output: Suggested date │   │                         │
│                        │   │          & reason       │   │  Output: Measurements   │
│                        │   │                         │   │          (linear feet,  │
│                        │   │  Uses: Database queries │   │          downspouts,    │
│                        │   │        to existing jobs │   │          corners, etc.) │
└────────────┬───────────┘   └────────────┬────────────┘   └───────────┬─────────────┘
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          │
                                          │
                                 ┌────────▼────────┐
                                 │  Gemini AI API  │
                                 │                 │
                                 │  Model:         │
                                 │  gemini-2.0-    │
                                 │  flash-exp      │
                                 │                 │
                                 │  Features:      │
                                 │  - Text gen     │
                                 │  - Vision       │
                                 │  - FREE tier    │
                                 └─────────────────┘
```

## Request Flow

### Text-Based Endpoints (No Photos)

```
User Request
    │
    ├─ POST /api/ai/estimate
    │   └─> get_ai_estimate(description, address)
    │       └─> Gemini API (text generation)
    │           └─> Returns detailed cost estimate
    │
    ├─ POST /api/ai/help
    │   └─> Gemini API with help prompt
    │       └─> Returns user-friendly answer
    │
    └─ POST /api/ai/suggest-schedule
        └─> Query database for existing jobs
            └─> suggest_schedule(jobs_data, address)
                └─> Gemini API (schedule optimization)
                    └─> Returns suggested date + reason
```

### Photo-Based Endpoints (Vision API)

```
User Request with Base64 Image
    │
    ├─ POST /api/ai/analyze-photo
    │   └─> analyze_photo(photo_data, context)
    │       └─> Parse base64 -> bytes
    │           └─> Gemini Vision API
    │               └─> Returns condition analysis
    │
    ├─ POST /api/ai/scan-inventory
    │   └─> Parse base64 -> bytes
    │       └─> Gemini Vision API (inventory prompt)
    │           └─> Returns material list
    │
    └─ POST /api/ai/estimate-from-photo
        └─> Parse base64 -> bytes
            └─> Gemini Vision API (measurement prompt)
                └─> Returns analysis text
                    └─> Regex parsing for measurements
                        └─> Returns {analysis, measurements}
```

## Data Flow Architecture

```
┌──────────────┐
│   Frontend   │ (Browser/Mobile)
└──────┬───────┘
       │ HTTP POST (JSON)
       ▼
┌──────────────────────────────────┐
│     Flask Application            │
│  (app_gemini.py on Vercel)       │
├──────────────────────────────────┤
│  Route Handlers                  │
│  - Input validation              │
│  - Error handling                │
│  - Response formatting           │
└──────┬───────────────────────────┘
       │
       ├─────────────┬──────────────┐
       │             │              │
       ▼             ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│  Gemini  │  │ Database │  │ Helper Funcs │
│   API    │  │ (SQLite) │  │ - get_ai_*   │
│          │  │          │  │ - analyze_*  │
│  Vision  │  │ Jobs     │  │ - suggest_*  │
│  & Text  │  │ Customers│  │              │
└──────────┘  └──────────┘  └──────────────┘
```

## Security Architecture (CURRENT STATE)

```
┌─────────────────────────────────────────┐
│          PUBLIC INTERNET                │
│     Anyone can call API endpoints       │
└─────────────┬───────────────────────────┘
              │
              │ NO AUTHENTICATION
              │ NO RATE LIMITING
              │ NO API KEYS
              │
              ▼
┌─────────────────────────────────────────┐
│       Flask API Endpoints               │
│  ❌ No auth middleware                   │
│  ❌ No rate limiting                     │
│  ❌ No request validation (size)         │
│  ❌ No CORS configuration                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Gemini API (via API key)           │
│  ✅ Protected by GEMINI_API_KEY          │
│  ⚠️  Quota limits apply                  │
│  ⚠️  Can be exhausted by abuse           │
└─────────────────────────────────────────┘
```

## Recommended Security Architecture

```
┌─────────────────────────────────────────┐
│          PUBLIC INTERNET                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│       API Gateway / Cloudflare          │
│  ✅ Rate limiting                        │
│  ✅ DDoS protection                      │
│  ✅ Request logging                      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│     Authentication Middleware           │
│  ✅ API key validation                   │
│  ✅ Session tokens                       │
│  ✅ Request signing                      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│       Flask API Endpoints               │
│  ✅ Input validation                     │
│  ✅ Request size limits                  │
│  ✅ Error handling                       │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Gemini API (via API key)           │
│  ✅ Protected by GEMINI_API_KEY          │
│  ✅ Monitored usage                      │
└─────────────────────────────────────────┘
```

## Error Handling Flow

```
API Request
    │
    ▼
┌──────────────────┐
│ Input Validation │
└────┬─────────────┘
     │
     ├─ Valid ──────────────────────┐
     │                              │
     └─ Invalid ─> 400 Error        │
         └─> {"error": "msg"}       │
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Try/Catch Block │
                          └────┬────────────┘
                               │
                               ├─ Success ───────────────┐
                               │                         │
                               └─ Exception ─> 500 Error │
                                   └─> {"success": false,│
                                        "error": "msg"}  │
                                                         │
                                                         ▼
                                              ┌──────────────────┐
                                              │ JSON Response    │
                                              │ - Status code    │
                                              │ - Data payload   │
                                              │ - Error details  │
                                              └──────────────────┘
```

## Database Interaction

```
API Endpoint: /api/ai/suggest-schedule
    │
    ├─ Receives: {"address": "123 Main St"}
    │
    ▼
Job.query.filter_by(status='scheduled').all()
    │
    ├─> Fetches scheduled jobs from SQLite
    │
    └─> jobs_data = [
            {
                'address': job.customer.address,
                'date': str(job.scheduled_date)
            },
            ...
        ]
    │
    ▼
suggest_schedule(jobs_data, new_address)
    │
    └─> Gemini API analyzes:
        - Existing job locations
        - Route optimization
        - Workload distribution
        - Weather considerations
    │
    ▼
Returns: {"suggestion": "2025-01-15 - Groups with nearby job on Oak St"}
```

## Technology Stack

```
┌──────────────────────────────────────────┐
│           Deployment (Vercel)            │
├──────────────────────────────────────────┤
│  Runtime: Python 3.9+                    │
│  Framework: Flask                        │
│  Database: SQLite (SQLAlchemy ORM)       │
│  AI: Google Gemini API                   │
│  Session: Flask sessions (cookie-based)  │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│         Python Dependencies              │
├──────────────────────────────────────────┤
│  • Flask - Web framework                 │
│  • flask-sqlalchemy - ORM                │
│  • google-generativeai - Gemini SDK      │
│  • python-dotenv - Env var management    │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│       Environment Variables              │
├──────────────────────────────────────────┤
│  • GEMINI_API_KEY (required)             │
│  • SECRET_KEY (recommended)              │
│  • DATABASE_URL (optional)               │
│  • APP_PASSWORD (optional)               │
└──────────────────────────────────────────┘
```

## API Response Formats

### Success Response (Text Generation)
```json
{
  "success": true,
  "estimate": "Based on your job...",  // or "analysis", "answer"
  "provider": "Google Gemini (FREE)"
}
```

### Success Response (Vision with Measurements)
```json
{
  "success": true,
  "analysis": "This house appears to be...",
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

### Error Response (400 - Bad Request)
```json
{
  "error": "Description required"
}
```

### Error Response (500 - Server Error)
```json
{
  "success": false,
  "error": "Error generating estimate: API quota exceeded"
}
```

## Performance Characteristics

```
Endpoint                    | Avg Response Time | Rate Limit | Cache?
─────────────────────────────────────────────────────────────────────
/api/ai/estimate            | 5-15 seconds      | None       | No
/api/ai/analyze-photo       | 10-20 seconds     | None       | No
/api/ai/scan-inventory      | 10-20 seconds     | None       | No
/api/ai/help                | 3-8 seconds       | None       | No
/api/ai/suggest-schedule    | 5-15 seconds      | None       | No
/api/ai/estimate-from-photo | 10-25 seconds     | None       | No
```

Note: Response times depend on:
- Gemini API load
- Network latency
- Image size (for vision endpoints)
- Prompt complexity

## Monitoring Recommendations

```
┌──────────────────────────────────────────┐
│        What to Monitor                   │
├──────────────────────────────────────────┤
│  ✅ API request count per endpoint        │
│  ✅ Response times (P50, P95, P99)        │
│  ✅ Error rates (400, 500)                │
│  ✅ Gemini API quota usage                │
│  ✅ Database query performance            │
│  ✅ Concurrent request count              │
│  ✅ Failed authentication attempts        │
│  ✅ Unusual traffic patterns              │
└──────────────────────────────────────────┘
```

## Scaling Considerations

### Current Limitations
- Single Gemini API key (quota shared)
- No connection pooling
- No caching layer
- No load balancing
- Synchronous request handling

### Future Improvements
1. Add Redis caching for repeated requests
2. Implement async request handling
3. Add multiple Gemini API keys with rotation
4. Implement request queuing for high load
5. Add CDN for static assets
6. Database connection pooling
7. Horizontal scaling with load balancer

## Testing Checklist

- [ ] All 6 endpoints return 200 for valid requests
- [ ] Error handling returns appropriate status codes
- [ ] Response format matches documentation
- [ ] Gemini API integration works
- [ ] Photo upload/processing works
- [ ] Database queries complete successfully
- [ ] Response times are acceptable
- [ ] No sensitive data in responses
- [ ] CORS headers set appropriately
- [ ] Rate limiting works (when implemented)
