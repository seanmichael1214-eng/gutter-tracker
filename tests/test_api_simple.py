#!/usr/bin/env python3
"""
Test script for Gutter Tracker API endpoints (using only standard library)
Tests all API endpoints at https://gutter-tracker-eta.vercel.app
"""

import urllib.request
import urllib.error
import json
import base64
import sys

# Base URL for the deployed app
BASE_URL = "https://gutter-tracker-eta.vercel.app"

# Simple color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def create_simple_base64_image():
    """Return a hardcoded base64 encoded 1x1 red pixel GIF"""
    return "data:image/gif;base64,R0lGODlhAQABAIABAP8AAP///yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="


def make_request(endpoint, payload):
    """Make a POST request to the API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "GutterTracker-API-Test/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            status_code = response.getcode()
            response_data = json.loads(response.read().decode("utf-8"))
            return status_code, response_data, None
    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            response_data = json.loads(e.read().decode("utf-8"))
        except Exception:
            response_data = {"error": "Could not parse error response"}
        return status_code, response_data, None
    except Exception as e:
        return None, None, str(e)


def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}")


def print_test(test_name):
    """Print test name"""
    print(f"\n{YELLOW}{test_name}{RESET}")


def print_pass(message):
    """Print pass message"""
    print(f"{GREEN}✓ PASS: {message}{RESET}")


def print_fail(message):
    """Print fail message"""
    print(f"{RED}✗ FAIL: {message}{RESET}")


def test_ai_estimate():
    """Test POST /api/ai/estimate"""
    print_header("Test 1: POST /api/ai/estimate - AI cost estimation")

    # Test 1a: Valid request
    print_test("Test 1a: Valid request with description and address")
    status, data, error = make_request(
        "/api/ai/estimate",
        {
            "description": "Replace 50 feet of K-style gutters, install 2 downspouts",
            "address": "123 Main St, Seattle, WA",
        },
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data and data.get("success"):
        print_pass(f"Status: {status}")
        print(f"  Provider: {data.get('provider')}")
        print(f"  Estimate preview: {data.get('estimate', '')[:150]}...")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 1b: Missing description
    print_test("Test 1b: Missing description (should return 400)")
    status, data, error = make_request("/api/ai/estimate", {"address": "123 Main St"})

    if status == 400 and data and "error" in data:
        print_pass(f"Status: {status}, Error: {data.get('error')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def test_analyze_photo():
    """Test POST /api/ai/analyze-photo"""
    print_header("Test 2: POST /api/ai/analyze-photo - Photo analysis")

    # Test 2a: Valid request
    print_test("Test 2a: Valid request with photo")
    photo_data = create_simple_base64_image()
    status, data, error = make_request(
        "/api/ai/analyze-photo",
        {"photo_data": photo_data, "context": "Testing gutter condition"},
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data and data.get("success"):
        print_pass(f"Status: {status}")
        print(f"  Provider: {data.get('provider')}")
        print(f"  Analysis preview: {data.get('analysis', '')[:150]}...")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 2b: Missing photo
    print_test("Test 2b: Missing photo data (should return 400)")
    status, data, error = make_request("/api/ai/analyze-photo", {"context": "Test"})

    if status == 400 and data and "error" in data:
        print_pass(f"Status: {status}, Error: {data.get('error')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def test_scan_inventory():
    """Test POST /api/ai/scan-inventory"""
    print_header("Test 3: POST /api/ai/scan-inventory - Inventory scanning")

    # Test 3a: Valid request
    print_test("Test 3a: Valid request with inventory photo")
    photo_data = create_simple_base64_image()
    status, data, error = make_request(
        "/api/ai/scan-inventory", {"photo_data": photo_data}
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data and data.get("success"):
        print_pass(f"Status: {status}")
        print(f"  Provider: {data.get('provider')}")
        print(f"  Analysis preview: {data.get('analysis', '')[:150]}...")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 3b: Missing photo
    print_test("Test 3b: Missing photo data (should return 400)")
    status, data, error = make_request("/api/ai/scan-inventory", {})

    if status == 400 and data and "error" in data:
        print_pass(f"Status: {status}, Error: {data.get('error')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def test_ai_help():
    """Test POST /api/ai/help"""
    print_header("Test 4: POST /api/ai/help - AI tech support")

    # Test 4a: Valid request
    print_test("Test 4a: Valid help question")
    status, data, error = make_request(
        "/api/ai/help", {"question": "How do I add a new customer?"}
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data and data.get("success"):
        print_pass(f"Status: {status}")
        print(f"  Answer preview: {data.get('answer', '')[:150]}...")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 4b: Missing question
    print_test("Test 4b: Missing question (should return 400)")
    status, data, error = make_request("/api/ai/help", {})

    if status == 400 and data and "error" in data:
        print_pass(f"Status: {status}, Error: {data.get('error')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def test_suggest_schedule():
    """Test POST /api/ai/suggest-schedule"""
    print_header("Test 5: POST /api/ai/suggest-schedule - Scheduling suggestions")

    # Test 5a: Valid request
    print_test("Test 5a: Valid request with address")
    status, data, error = make_request(
        "/api/ai/suggest-schedule", {"address": "456 Oak Ave, Portland, OR"}
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data:
        print_pass(f"Status: {status}")
        print(f"  Suggestion: {data.get('suggestion')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 5b: Empty request
    print_test("Test 5b: Empty request")
    status, data, error = make_request("/api/ai/suggest-schedule", {})

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200:
        print_pass(f"Status: {status}, Response: {data}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def test_estimate_from_photo():
    """Test POST /api/ai/estimate-from-photo"""
    print_header("Test 6: POST /api/ai/estimate-from-photo - House photo estimates")

    # Test 6a: Valid request
    print_test("Test 6a: Valid request with house photo")
    photo_data = create_simple_base64_image()
    status, data, error = make_request(
        "/api/ai/estimate-from-photo", {"photo_data": photo_data}
    )

    if error:
        print_fail(f"Request failed: {error}")
    elif status == 200 and data and data.get("success"):
        print_pass(f"Status: {status}")
        print(f"  Provider: {data.get('provider')}")
        print(f"  Measurements: {data.get('measurements')}")
        print(f"  Analysis preview: {data.get('analysis', '')[:150]}...")
    else:
        print_fail(f"Status: {status}, Response: {data}")

    # Test 6b: Missing photo
    print_test("Test 6b: Missing photo data (should return 400)")
    status, data, error = make_request("/api/ai/estimate-from-photo", {})

    if status == 400 and data and "error" in data:
        print_pass(f"Status: {status}, Error: {data.get('error')}")
    else:
        print_fail(f"Status: {status}, Response: {data}")


def main():
    """Run all tests"""
    print(f"\n{GREEN}{'=' * 70}{RESET}")
    print(f"{GREEN}Gutter Tracker API Endpoint Testing{RESET}")
    print(f"{GREEN}Testing: {BASE_URL}{RESET}")
    print(f"{GREEN}{'=' * 70}{RESET}")

    test_ai_estimate()
    test_analyze_photo()
    test_scan_inventory()
    test_ai_help()
    test_suggest_schedule()
    test_estimate_from_photo()

    print(f"\n{GREEN}{'=' * 70}{RESET}")
    print(f"{GREEN}All tests completed!{RESET}")
    print(f"{GREEN}{'=' * 70}{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Testing interrupted{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{RED}Fatal error: {e}{RESET}\n")
        import traceback

        traceback.print_exc()
        sys.exit(1)
