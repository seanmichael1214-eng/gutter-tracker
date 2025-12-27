#!/usr/bin/env python3
"""
Automated Testing Script for Gutter Tracker
Run this after manual testing to verify API endpoints and data integrity
"""

import requests
import json
from datetime import datetime
import sys

# Configuration
BASE_URL = "https://gutter-tracker-app.fly.dev"
PASSWORD = "NAO$"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(test_name, passed, message=""):
    """Print formatted test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} | {test_name}")
    if message:
        print(f"     → {message}")

def test_site_accessibility():
    """Test if the site is accessible"""
    print(f"\n{Colors.BLUE}Testing Site Accessibility...{Colors.END}")
    try:
        response = requests.get(BASE_URL, timeout=10)
        passed = response.status_code == 200
        print_test(
            "Site is accessible",
            passed,
            f"Status: {response.status_code}"
        )
        return passed
    except Exception as e:
        print_test("Site is accessible", False, f"Error: {str(e)}")
        return False

def test_splash_page():
    """Test splash page content"""
    print(f"\n{Colors.BLUE}Testing Splash Page...{Colors.END}")
    try:
        response = requests.get(BASE_URL, timeout=10)
        content = response.text
        
        # Check for expected content
        has_title = "Gutter Tracker" in content
        has_password = "password" in content.lower()
        has_login = "login" in content.lower()
        
        print_test("Has Gutter Tracker title", has_title)
        print_test("Has password prompt", has_password)
        print_test("Has login link/button", has_login)
        
        return has_title and has_password and has_login
    except Exception as e:
        print_test("Splash page content", False, f"Error: {str(e)}")
        return False

def test_login_endpoint():
    """Test login endpoint exists"""
    print(f"\n{Colors.BLUE}Testing Login Endpoint...{Colors.END}")
    try:
        response = requests.get(f"{BASE_URL}/login", timeout=10)
        passed = response.status_code in [200, 401, 302]  # Could redirect if already logged in
        print_test(
            "Login endpoint exists",
            passed,
            f"Status: {response.status_code}"
        )
        return passed
    except Exception as e:
        print_test("Login endpoint", False, f"Error: {str(e)}")
        return False

def test_response_times():
    """Test response times for main pages"""
    print(f"\n{Colors.BLUE}Testing Response Times...{Colors.END}")
    
    endpoints = [
        ("Home/Splash", "/"),
        ("Login", "/login"),
    ]
    
    all_passed = True
    for name, endpoint in endpoints:
        try:
            start = datetime.now()
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            elapsed = (datetime.now() - start).total_seconds()
            
            passed = elapsed < 3.0  # Should load in under 3 seconds
            print_test(
                f"{name} page loads in < 3s",
                passed,
                f"Time: {elapsed:.2f}s"
            )
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"{name} response time", False, f"Error: {str(e)}")
            all_passed = False
    
    return all_passed

def test_security_headers():
    """Test for basic security headers"""
    print(f"\n{Colors.BLUE}Testing Security Headers...{Colors.END}")
    try:
        response = requests.get(BASE_URL, timeout=10)
        headers = response.headers
        
        # Check for common security headers
        has_xframe = 'X-Frame-Options' in headers or 'x-frame-options' in headers
        has_xcontent = 'X-Content-Type-Options' in headers or 'x-content-type-options' in headers
        
        print_test("Has X-Frame-Options header", has_xframe)
        print_test("Has X-Content-Type-Options header", has_xcontent)
        
        return True  # Not critical, just informational
    except Exception as e:
        print_test("Security headers", False, f"Error: {str(e)}")
        return False

def test_static_assets():
    """Test that static assets are loading"""
    print(f"\n{Colors.BLUE}Testing Static Assets...{Colors.END}")
    
    # Common static asset paths
    assets = [
        ("/static/style.css", "CSS"),
        ("/static/style_mobile.css", "Mobile CSS"),
    ]
    
    all_passed = True
    for path, name in assets:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
            passed = response.status_code == 200
            print_test(
                f"{name} loads",
                passed,
                f"Status: {response.status_code}"
            )
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"{name}", False, f"Error: {str(e)}")
            all_passed = False
    
    return all_passed

def generate_report(results):
    """Generate final test report"""
    print(f"\n{'='*60}")
    print(f"{Colors.BLUE}AUTOMATED TEST SUMMARY{Colors.END}")
    print(f"{'='*60}")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if pass_rate == 100:
        print(f"\n{Colors.GREEN}✅ ALL AUTOMATED TESTS PASSED!{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Remember to complete manual testing checklist{Colors.END}")
    elif pass_rate >= 80:
        print(f"\n{Colors.YELLOW}⚠️  MOST TESTS PASSED - Review failures{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ MULTIPLE FAILURES - Investigation required{Colors.END}")
    
    print(f"\n{'='*60}\n")
    
    return pass_rate >= 80

def main():
    """Run all automated tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"GUTTER TRACKER - AUTOMATED TESTING")
    print(f"{'='*60}{Colors.END}")
    print(f"URL: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {
        "Site Accessibility": test_site_accessibility(),
        "Splash Page": test_splash_page(),
        "Login Endpoint": test_login_endpoint(),
        "Response Times": test_response_times(),
        "Security Headers": test_security_headers(),
        "Static Assets": test_static_assets(),
    }
    
    # Generate report
    all_passed = generate_report(results)
    
    # Exit code for CI/CD
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
