#!/usr/bin/env python3
"""
Test script for Gutter Tracker API endpoints
Tests all API endpoints at https://gutter-tracker-eta.vercel.app
"""

import requests
import json
import base64
import sys


# Base URL for the deployed app
BASE_URL = "https://gutter-tracker-eta.vercel.app"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def create_sample_image_base64():
    """Return a hardcoded base64 encoded 1x1 red pixel GIF"""
    return "data:image/gif;base64,R0lGODlhAQABAIABAP8AAP///yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="


def print_test_header(test_name):
    """Print formatted test header"""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}Testing: {test_name}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}")


def print_result(success, message, details=None):
    """Print formatted test result"""
    status = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
    print(f"\n{status}: {message}")
    if details:
        print(f"{YELLOW}Details:{RESET}")
        print(json.dumps(details, indent=2))


def test_ai_estimate():
    """Test POST /api/ai/estimate"""
    print_test_header("POST /api/ai/estimate - AI cost estimation")

    endpoint = f"{BASE_URL}/api/ai/estimate"

    # Test 1: Valid request
    print(f"\n{YELLOW}Test 1: Valid request with description and address{RESET}")
    payload = {
        "description": "Replace 50 feet of K-style gutters, install 2 downspouts",
        "address": "123 Main St, Seattle, WA",
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and "estimate" in data
            and "provider" in data
        )

        print_result(
            success,
            f"Status: {response.status_code}",
            {
                "success": data.get("success"),
                "has_estimate": "estimate" in data,
                "provider": data.get("provider"),
                "estimate_preview": (
                    data.get("estimate", "")[:200] + "..."
                    if data.get("estimate")
                    else None
                ),
            },
        )
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Missing description
    print(f"\n{YELLOW}Test 2: Missing description (should return 400){RESET}")
    payload = {"address": "123 Main St"}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()

        success = response.status_code == 400 and "error" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def test_analyze_photo():
    """Test POST /api/ai/analyze-photo"""
    print_test_header("POST /api/ai/analyze-photo - Photo analysis with Gemini Vision")

    endpoint = f"{BASE_URL}/api/ai/analyze-photo"

    # Test 1: Valid request with photo
    print(f"\n{YELLOW}Test 1: Valid request with sample photo{RESET}")
    photo_data = create_sample_image_base64()
    payload = {"photo_data": photo_data, "context": "Testing gutter condition analysis"}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and "analysis" in data
            and "provider" in data
        )

        print_result(
            success,
            f"Status: {response.status_code}",
            {
                "success": data.get("success"),
                "has_analysis": "analysis" in data,
                "provider": data.get("provider"),
                "analysis_preview": (
                    data.get("analysis", "")[:200] + "..."
                    if data.get("analysis")
                    else None
                ),
            },
        )
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Missing photo data
    print(f"\n{YELLOW}Test 2: Missing photo data (should return 400){RESET}")
    payload = {"context": "Test"}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()

        success = response.status_code == 400 and "error" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def test_scan_inventory():
    """Test POST /api/ai/scan-inventory"""
    print_test_header("POST /api/ai/scan-inventory - Inventory photo scanning")

    endpoint = f"{BASE_URL}/api/ai/scan-inventory"

    # Test 1: Valid request
    print(f"\n{YELLOW}Test 1: Valid request with sample inventory photo{RESET}")
    photo_data = create_sample_image_base64()
    payload = {"photo_data": photo_data}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and "analysis" in data
            and "provider" in data
        )

        print_result(
            success,
            f"Status: {response.status_code}",
            {
                "success": data.get("success"),
                "has_analysis": "analysis" in data,
                "provider": data.get("provider"),
                "analysis_preview": (
                    data.get("analysis", "")[:200] + "..."
                    if data.get("analysis")
                    else None
                ),
            },
        )
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Missing photo data
    print(f"\n{YELLOW}Test 2: Missing photo data (should return 400){RESET}")
    payload = {}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()

        success = response.status_code == 400 and "error" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def test_ai_help():
    """Test POST /api/ai/help"""
    print_test_header("POST /api/ai/help - AI tech support chat")

    endpoint = f"{BASE_URL}/api/ai/help"

    # Test 1: Valid question
    print(f"\n{YELLOW}Test 1: Valid help question{RESET}")
    payload = {"question": "How do I add a new customer?"}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and "answer" in data
        )

        print_result(
            success,
            f"Status: {response.status_code}",
            {
                "success": data.get("success"),
                "has_answer": "answer" in data,
                "answer_preview": (
                    data.get("answer", "")[:200] + "..." if data.get("answer") else None
                ),
            },
        )
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Missing question
    print(f"\n{YELLOW}Test 2: Missing question (should return 400){RESET}")
    payload = {}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()

        success = response.status_code == 400 and "error" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def test_suggest_schedule():
    """Test POST /api/ai/suggest-schedule"""
    print_test_header("POST /api/ai/suggest-schedule - AI scheduling suggestions")

    endpoint = f"{BASE_URL}/api/ai/suggest-schedule"

    # Test 1: Valid request
    print(f"\n{YELLOW}Test 1: Valid request with address{RESET}")
    payload = {"address": "456 Oak Ave, Portland, OR"}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = response.status_code == 200 and "suggestion" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Empty request
    print(f"\n{YELLOW}Test 2: Empty request (may still work){RESET}")
    payload = {}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        print_result(True, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def test_estimate_from_photo():
    """Test POST /api/ai/estimate-from-photo"""
    print_test_header(
        "POST /api/ai/estimate-from-photo - House photo to materials estimate"
    )

    endpoint = f"{BASE_URL}/api/ai/estimate-from-photo"

    # Test 1: Valid request
    print(f"\n{YELLOW}Test 1: Valid request with house photo{RESET}")
    photo_data = create_sample_image_base64()
    payload = {"photo_data": photo_data}

    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        data = response.json()

        success = (
            response.status_code == 200
            and data.get("success") is True
            and "analysis" in data
            and "measurements" in data
            and "provider" in data
        )

        print_result(
            success,
            f"Status: {response.status_code}",
            {
                "success": data.get("success"),
                "has_analysis": "analysis" in data,
                "has_measurements": "measurements" in data,
                "provider": data.get("provider"),
                "measurements": data.get("measurements"),
                "analysis_preview": (
                    data.get("analysis", "")[:200] + "..."
                    if data.get("analysis")
                    else None
                ),
            },
        )
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")

    # Test 2: Missing photo data
    print(f"\n{YELLOW}Test 2: Missing photo data (should return 400){RESET}")
    payload = {}

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json()

        success = response.status_code == 400 and "error" in data

        print_result(success, f"Status: {response.status_code}", data)
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")


def main():
    """Run all API endpoint tests"""
    print(f"\n{GREEN}{'=' * 70}{RESET}")
    print(f"{GREEN}Gutter Tracker API Endpoint Testing{RESET}")
    print(f"{GREEN}Testing deployed app at: {BASE_URL}{RESET}")
    print(f"{GREEN}{'=' * 70}{RESET}")

    # Run all tests
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
        print(f"\n\n{YELLOW}Testing interrupted by user{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{RED}Fatal error: {str(e)}{RESET}\n")
        sys.exit(1)
