# 🚀 Gutter Tracker - Quick Testing Guide

## Before You Start

**Important Information:**
- **URL:** https://gutter-tracker-app.fly.dev
- **Password:** NAO$
- **Your Testing Goal:** Verify the app is ready for customer delivery

---

## Option 1: Manual Testing (Recommended - 30 minutes)

### Quick Test Flow:

1. **Open the app** → https://gutter-tracker-app.fly.dev
2. **Login** with password: NAO$
3. **Create a customer:**
   - Name: John Test
   - Address: 123 Main St, Columbus, OH 43016
   - Phone: (614) 555-1234
4. **Create a job** for that customer:
   - Pick tomorrow's date
   - Job type: Gutter Cleaning
   - Status: Scheduled
5. **Check the calendar** - Does the job appear?
6. **Try on mobile** - Resize browser or use your phone
7. **Mark job as complete** - Change status to "Completed"

### ✅ If These Work - You're Good!
- [x] Login works
- [x] Can create customers
- [x] Can create jobs
- [x] Calendar shows jobs
- [x] Works on mobile
- [x] Can update job status

**Use the detailed checklist** (GUTTER_TRACKER_TESTING_CHECKLIST.md) if you want to be thorough.

---

## Option 2: Automated Testing (5 minutes)

Run the automated test script to check basic functionality:

```bash
# From your Mac terminal
cd ~/Downloads  # or wherever you saved automated_test.py
python3 automated_test.py
```

**What it tests:**
- ✅ Site is accessible
- ✅ Splash page loads
- ✅ Login endpoint exists
- ✅ Pages load in < 3 seconds
- ✅ Static assets (CSS) load
- ✅ Basic security headers

---

## 🐛 Common Issues to Watch For

### Critical (Stop & Fix):
- [ ] Can't login at all
- [ ] Can't create customers
- [ ] Can't create jobs
- [ ] Jobs don't appear on calendar
- [ ] Data disappears after logout

### Medium (Note & Consider Fixing):
- [ ] Slow page loads (>5 seconds)
- [ ] Mobile layout broken
- [ ] Error messages unclear
- [ ] Calendar navigation buggy

### Minor (Note for Future):
- [ ] UI could be prettier
- [ ] Small alignment issues
- [ ] Minor typos
- [ ] Missing features user might want

---

## Decision Matrix

### ✅ SHIP IT if:
- Core features work (login, customers, jobs, calendar)
- No data loss
- Works on mobile
- No critical bugs

### ⚠️ SHIP WITH NOTES if:
- Core features work
- Minor UI issues exist
- Document known issues for customer

### ❌ DON'T SHIP if:
- Login broken
- Data loss occurs
- Core features don't work
- Major bugs that affect usability

---

## Quick Test Scenarios

### Scenario 1: New Customer Flow (5 min)
```
1. Login
2. Go to Customers
3. Add new customer with full details
4. View customer page
5. Edit one field
6. Save
7. Verify change appears
```

### Scenario 2: Schedule Job Flow (5 min)
```
1. Go to Jobs (or Calendar)
2. Click "New Job"
3. Select existing customer
4. Pick date next week
5. Add job details
6. Save
7. Go to Calendar
8. Verify job appears on correct date
9. Click job on calendar
10. Verify details are correct
```

### Scenario 3: Complete Job Flow (5 min)
```
1. Find a scheduled job
2. Click on it
3. Change status to "Completed"
4. Add completion notes
5. Save
6. Verify status changed
7. Check if it still appears on calendar
```

---

## Testing Report Template

After testing, fill this out:

**Date:** ___________  
**Tester:** ___________

### Results:
- **Login:** ☐ Pass ☐ Fail  
- **Customers:** ☐ Pass ☐ Fail  
- **Jobs:** ☐ Pass ☐ Fail  
- **Calendar:** ☐ Pass ☐ Fail  
- **Mobile:** ☐ Pass ☐ Fail

### Bugs Found:
1. _____________________
2. _____________________
3. _____________________

### Ready for Customer?
☐ **YES** - Ship it  
☐ **YES with notes** - Ship but document issues  
☐ **NO** - Needs fixes first

### Reasoning:
_________________________________________
_________________________________________

---

## Next Steps After Testing

### If Ready:
1. ✅ Document any known minor issues
2. ✅ Prepare user guide for customer
3. ✅ Set up customer credentials
4. ✅ Send access information
5. ✅ Schedule training call if needed

### If Not Ready:
1. ❌ List all critical bugs
2. ❌ Prioritize fixes
3. ❌ Fix bugs
4. ❌ Re-test
5. ❌ Repeat until ready

---

## Support Resources

**If you find issues:**
- Save screenshots
- Note exact steps to reproduce
- Check browser console (F12) for errors
- Document expected vs actual behavior

**App Structure (for reference):**
```
/Users/Sean/code/gutter-tracker/
├── app/                    # Main application code
│   ├── routes.py          # URL endpoints
│   ├── models.py          # Database models
│   └── templates/         # HTML pages
├── instance/              # Database location
│   └── gutter_tracker.db
└── config/                # JSON data files
```

**Quick Troubleshooting:**
- Clear browser cache if pages look weird
- Check Fly.dev dashboard for app status
- View app logs: `fly logs` (if you have Fly CLI)

---

## Time Estimate

- **Quick test:** 15-20 minutes
- **Thorough test:** 30-45 minutes
- **Full test with documentation:** 60 minutes

**Recommendation:** Start with quick test, then do thorough test if you find any issues.

---

**Ready? Let's test! 🚀**

Open https://gutter-tracker-app.fly.dev and start with the quick test flow above!
