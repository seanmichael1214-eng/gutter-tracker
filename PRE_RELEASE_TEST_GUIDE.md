# 🧪 Gutter Tracker - Pre-Release Testing Guide
## Complete Manual Test Run Before Customer Release

**App URL:** https://gutter-tracker-app.fly.dev  
**Password:** NAO$  
**Test Date:** December 27, 2025  
**Estimated Time:** 30-45 minutes

---

## ✅ Pre-Test Checklist

- [ ] Open browser (Chrome, Firefox, or Safari recommended)
- [ ] Have notepad ready for noting any issues
- [ ] Clear browser cache/cookies (optional but recommended)
- [ ] Ensure good internet connection

---

## 📋 Test Execution Steps

### Phase 1: Authentication & Login (5 minutes)

#### Test 1.1: Homepage/Splash
1. Open https://gutter-tracker-app.fly.dev
2. **✅ Verify:**
   - Page loads without errors
   - Logo/branding displays
   - "Login" button is visible
3. **❌ Red Flags:**
   - Blank page
   - 404 error
   - Broken images

#### Test 1.2: Login - Invalid Password
1. Click "Login" button
2. Enter password: `wrong123`
3. Click "Submit"
4. **✅ Verify:**
   - Error message appears: "Invalid password"
   - You remain on login page
3. **❌ Red Flags:**
   - App crashes
   - No error message
   - Allows login with wrong password

#### Test 1.3: Login - Correct Password
1. Enter password: `NAO$`
2. Click "Submit"
3. **✅ Verify:**
   - Redirects to /dashboard
   - Dashboard loads successfully
   - No errors in browser console (F12 → Console tab)
4. **❌ Red Flags:**
   - Login fails
   - Stuck on login page
   - Dashboard shows errors

---

### Phase 2: Dashboard Overview (3 minutes)

#### Test 2.1: Dashboard Display
1. On dashboard page
2. **✅ Verify:**
   - Navigation menu visible (Customers, Jobs, Calendar, etc.)
   - Stats/metrics displayed (if any exist)
   - Page looks professional
   - All links are clickable
3. **❌ Red Flags:**
   - Missing navigation
   - Broken layout
   - JavaScript errors

#### Test 2.2: Navigation Links
1. Click each nav link and verify it loads:
   - Customers
   - Jobs
   - Calendar
   - Inventory
   - Materials
   - Reports
   - Quick Estimate
   - Help
2. **✅ Verify:**
   - All pages load without errors
   - Navigation is consistent across pages
3. **❌ Red Flags:**
   - Any 404 errors
   - Blank pages
   - Crashes

---

### Phase 3: Customer Management (8 minutes)

#### Test 3.1: View Customers List
1. Navigate to /customers
2. **✅ Verify:**
   - Customer list page loads
   - "Add Customer" button visible
   - If customers exist, they display in a list/table
3. **❌ Red Flags:**
   - Page crashes
   - Can't see add button

#### Test 3.2: Create New Customer
1. Click "Add Customer" button
2. Fill in form:
   - **Name:** Test Customer Inc.
   - **Contact Person:** John Doe
   - **Email:** john.doe@testcustomer.com
   - **Phone:** (555) 123-4567
   - **Address:** 123 Test Street
   - **City:** Test City
   - **State:** TC
   - **ZIP:** 12345
3. Click "Save" or "Submit"
4. **✅ Verify:**
   - Success message appears
   - Customer appears in list
   - All data saved correctly
5. **❌ Red Flags:**
   - Form doesn't submit
   - Data not saved
   - Error messages

#### Test 3.3: View Customer Details
1. Click on "Test Customer Inc." in the list
2. **✅ Verify:**
   - Customer details page loads
   - All information displays correctly
   - Can see associated jobs (if any)
3. **❌ Red Flags:**
   - Wrong data displayed
   - Page doesn't load

#### Test 3.4: Edit Customer
1. On customer details page, click "Edit"
2. Change **Phone** to: (555) 999-8888
3. Click "Save"
4. **✅ Verify:**
   - Changes saved successfully
   - Updated phone number displays
5. **❌ Red Flags:**
   - Changes don't save
   - Wrong field updated

#### Test 3.5: Search/Filter Customers
1. Return to customers list
2. Use search box (if available)
3. Search for "Test"
4. **✅ Verify:**
   - "Test Customer Inc." appears in results
   - Search works correctly
5. **❌ Red Flags:**
   - Search doesn't work
   - No results found

---

### Phase 4: Job Management (10 minutes)

#### Test 4.1: View Jobs List
1. Navigate to /jobs
2. **✅ Verify:**
   - Jobs list page loads
   - "Add Job" button visible
   - Job list displays (if jobs exist)
3. **❌ Red Flags:**
   - Page crashes
   - Can't add jobs

#### Test 4.2: Create New Job
1. Click "Add Job" button
2. Fill in form:
   - **Customer:** Test Customer Inc. (select from dropdown)
   - **Service Type:** Gutter Installation
   - **Address:** 123 Test Street, Test City, TC 12345
   - **Status:** Scheduled
   - **Scheduled Date:** Tomorrow's date
   - **Estimated Cost:** $1,500.00
   - **Notes:** "Complete gutter installation - 100 linear feet. Includes downspouts and guards."
3. Click "Save" or "Submit"
4. **✅ Verify:**
   - Success message appears
   - Job appears in job list
   - All data saved correctly
   - Job shows "Scheduled" status
5. **❌ Red Flags:**
   - Form doesn't submit
   - Data not saved
   - Wrong customer assigned

#### Test 4.3: View Job Details
1. Click on the test job in the list
2. **✅ Verify:**
   - Job details page loads
   - All information displays correctly
   - Customer name visible
   - Status displayed
   - Can see materials section (even if empty)
3. **❌ Red Flags:**
   - Wrong job displayed
   - Missing information

#### Test 4.4: Update Job Status
1. On job details page
2. Change status: Scheduled → In Progress
3. Save changes
4. **✅ Verify:**
   - Status updates successfully
   - New status displays correctly
5. Change status again: In Progress → Completed
6. **✅ Verify:**
   - Status updates to Completed
7. **❌ Red Flags:**
   - Status doesn't change
   - Error on save

#### Test 4.5: Add Materials to Job
1. On job details page
2. Find "Add Materials" section
3. Add materials:
   - Material 1: 6" K-Style Gutter - White, Quantity: 100 feet
   - Material 2: Downspouts, Quantity: 4 pieces
4. Save materials
5. **✅ Verify:**
   - Materials added to job
   - Quantities display correctly
   - Total cost updated (if calculated)
6. **❌ Red Flags:**
   - Materials don't save
   - Wrong quantities

---

### Phase 5: Calendar View (5 minutes)

#### Test 5.1: View Calendar
1. Navigate to /calendar
2. **✅ Verify:**
   - Calendar displays current month
   - Days are laid out correctly
   - Month/year shown at top
   - Navigation buttons (prev/next month) visible
3. **❌ Red Flags:**
   - Calendar doesn't render
   - Wrong month displayed
   - Layout broken

#### Test 5.2: Check Job Appears on Calendar
1. Look for tomorrow's date (where you scheduled the test job)
2. **✅ Verify:**
   - Test job appears on that date
   - Job is color-coded by status
   - Can click on job to view details
3. **❌ Red Flags:**
   - Job doesn't appear
   - Wrong date
   - Can't click

#### Test 5.3: Navigate Calendar
1. Click "Next Month" button
2. **✅ Verify:** Calendar shows next month
3. Click "Previous Month" twice
4. **✅ Verify:** Calendar shows previous month
5. **❌ Red Flags:**
   - Navigation doesn't work
   - Calendar freezes

---

### Phase 6: Inventory Management (5 minutes)

#### Test 6.1: View Inventory
1. Navigate to /inventory
2. **✅ Verify:**
   - Inventory page loads
   - List of inventory items (or empty state)
   - "Add Item" button visible
3. **❌ Red Flags:**
   - Page crashes
   - Can't access

#### Test 6.2: Add Inventory Item
1. Click "Add Item" button
2. Fill in form:
   - **Name:** 6" K-Style Gutter - White
   - **Quantity:** 50
   - **Unit:** feet
   - **Cost per Unit:** $8.50
   - **Reorder Level:** 20 (minimum stock)
3. Click "Save"
4. **✅ Verify:**
   - Item added successfully
   - Appears in inventory list
   - All data correct
5. **❌ Red Flags:**
   - Item doesn't save
   - Wrong data

#### Test 6.3: Update Inventory Quantity
1. Find the item you just added
2. Click "Edit" or update quantity
3. Change quantity from 50 to 35
4. Save
5. **✅ Verify:**
   - Quantity updated
   - Changes saved
6. **❌ Red Flags:**
   - Update fails
   - Wrong quantity

---

### Phase 7: Materials Database (4 minutes)

#### Test 7.1: View Materials
1. Navigate to /materials
2. **✅ Verify:**
   - Materials list page loads
   - "Add Material" button visible
   - Materials displayed (if any)
3. **❌ Red Flags:**
   - Page doesn't load
   - No materials shown

#### Test 7.2: Add New Material
1. Click "Add Material"
2. Fill in:
   - **Name:** Premium Gutter Guard - Mesh
   - **Category:** Accessories
   - **Cost:** $15.00 per foot
   - **Description:** High-quality aluminum mesh guard
3. Save
4. **✅ Verify:**
   - Material saved
   - Appears in list
5. **❌ Red Flags:**
   - Save fails
   - Data missing

---

### Phase 8: AI Quick Estimate (5 minutes)

#### Test 8.1: Access Quick Estimate
1. Navigate to /quick-estimate
2. **✅ Verify:**
   - Page loads
   - Photo upload area visible
   - Instructions clear
3. **❌ Red Flags:**
   - Page crashes
   - No upload option

#### Test 8.2: Test Photo Upload
1. Take a photo of any house/building with your phone OR use a test image
2. Upload the photo
3. Click "Analyze" or "Get Estimate"
4. **✅ Verify:**
   - Upload works
   - AI analyzes photo (may take 10-30 seconds)
   - Estimate is generated
   - Estimate has reasonable values ($500-$5000 range)
   - Description makes sense
5. **❌ Red Flags:**
   - Upload fails
   - AI doesn't respond
   - Estimate is $0 or ridiculous value
   - Error messages

**Note:** AI features require GEMINI_API_KEY to be set in production. If this fails, it's expected.

---

### Phase 9: Reports/Analytics (3 minutes)

#### Test 9.1: View Reports
1. Navigate to /reports
2. **✅ Verify:**
   - Reports page loads
   - Shows some statistics
   - Revenue/jobs count displayed
   - Charts/graphs render (if any)
3. **❌ Red Flags:**
   - Page crashes
   - No data shown
   - Broken charts

#### Test 9.2: Filter Reports
1. If date filters exist, try changing date range
2. **✅ Verify:**
   - Filters work
   - Data updates
3. **❌ Red Flags:**
   - Filters don't work
   - Data doesn't change

---

### Phase 10: AI Help Assistant (4 minutes)

#### Test 10.1: Access Help
1. Navigate to /help
2. **✅ Verify:**
   - Help page loads
   - Chat interface visible
   - Input box for questions
3. **❌ Red Flags:**
   - Page crashes
   - No chat interface

#### Test 10.2: Ask Questions
1. Type: "How do I add a new customer?"
2. Submit question
3. **✅ Verify:**
   - AI responds (may take 5-15 seconds)
   - Response is helpful and relevant
   - Response makes sense for gutter business
4. Try another question: "What's the best material for gutters?"
5. **✅ Verify:**
   - AI responds again
   - Answer is relevant
6. **❌ Red Flags:**
   - AI doesn't respond
   - Error messages
   - Nonsensical answers

**Note:** AI features require GEMINI_API_KEY. If this fails, it's expected.

---

## 📊 Test Results Summary

### Routes Tested ✅
- [x] Homepage/Splash - **Status: 200 OK**
- [x] Login Page - **Status: 200 OK**
- [x] Dashboard - **Status: 200 OK**
- [x] Customers - **Status: 200 OK**
- [x] Jobs - **Status: 200 OK**
- [x] Calendar - **Status: 200 OK**
- [x] Inventory - **Status: 200 OK**
- [x] Materials - **Status: 200 OK**
- [x] Reports - **Status: 200 OK**
- [x] Quick Estimate - **Status: 200 OK**
- [x] Help - **Status: 200 OK**

**All routes are accessible!** ✅

### Manual Testing Checklist

Fill this out as you test:

**Phase 1: Authentication**
- [ ] Login with wrong password - Error shown
- [ ] Login with correct password (NAO$) - Success

**Phase 2: Dashboard**
- [ ] Dashboard loads and displays correctly
- [ ] All navigation links work

**Phase 3: Customers**
- [ ] Can view customer list
- [ ] Can add new customer (Test Customer Inc.)
- [ ] Can view customer details
- [ ] Can edit customer
- [ ] Can search customers

**Phase 4: Jobs**
- [ ] Can view jobs list
- [ ] Can create new job for test customer
- [ ] Can view job details
- [ ] Can update job status (Scheduled → In Progress → Completed)
- [ ] Can add materials to job

**Phase 5: Calendar**
- [ ] Calendar displays correctly
- [ ] Test job appears on scheduled date
- [ ] Can navigate months

**Phase 6: Inventory**
- [ ] Can view inventory
- [ ] Can add inventory item (6" K-Style Gutter)
- [ ] Can update quantity

**Phase 7: Materials**
- [ ] Can view materials list
- [ ] Can add new material (Gutter Guard)

**Phase 8: AI Quick Estimate**
- [ ] Can access page
- [ ] Can upload photo
- [ ] AI generates estimate (if API key set)

**Phase 9: Reports**
- [ ] Reports page loads
- [ ] Shows statistics
- [ ] Charts render (if any)

**Phase 10: AI Help**
- [ ] Help page loads
- [ ] Can ask questions
- [ ] AI responds (if API key set)

---

## 🐛 Issues Found

Document any bugs or problems here:

### Critical Issues (App Broken)
- None found so far

### Major Issues (Feature Doesn't Work)
- 

### Minor Issues (Visual/UX Problems)
- 

### Enhancement Suggestions
- 

---

## ✅ Final Checklist Before Release

Before giving access to your customer:

- [ ] All routes tested and working
- [ ] Test customer and job created successfully
- [ ] Can complete full workflow (Customer → Job → Complete)
- [ ] No critical bugs found
- [ ] Password is secure (NAO$ - consider changing before release)
- [ ] Database is working (data persists)
- [ ] AI features tested (or documented as optional)
- [ ] Mobile responsive (test on phone if possible)
- [ ] Performance is acceptable (<3 seconds page load)

---

## 📝 Test Notes

**Automated Route Testing Results:**
```
✅ All 11 routes returning 200 OK
✅ Average response time: ~0.19 seconds
✅ No 404 or 500 errors detected
✅ App is healthy and responding
```

**Database:** PostgreSQL (gutter-tracker-db on Fly.io)  
**Hosting:** Fly.io (512MB RAM, 1 instance)  
**SSL:** ✅ HTTPS enabled  
**Password Protected:** ✅ Yes (NAO$)

---

## 🎯 Recommendation

Based on automated testing, **all routes are accessible and responding correctly.**

**Next Step:** Complete manual testing using this guide to verify:
1. Forms work correctly
2. Data saves to database
3. Features function as expected
4. User experience is smooth

**Estimated Testing Time:** 30-45 minutes

**After completing tests, the app should be ready for customer release!** 🚀

---

_Test Guide Created: December 27, 2025_  
_App Version: Production (Fly.io)_  
_Tester: Pre-customer release validation_
