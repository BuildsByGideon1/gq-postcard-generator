#!/usr/bin/env python3
"""
Test script for the QR Postcard Generator API
"""

import requests
import os

def test_local_api():
    """Test the API running locally"""

    base_url = "http://localhost:8080"

    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test main endpoint
    print("\nTesting QR generation endpoint...")

    if not os.path.exists("postcardSampleBlank.png"):
        print("Error: postcardSampleBlank.png not found!")
        return

    try:
        with open("postcardSampleBlank.png", "rb") as f:
            files = {"image": f}
            data = {"url": "https://example.com/test"}

            response = requests.post(
                f"{base_url}/generate-qr-postcard",
                files=files,
                data=data
            )

        print(f"QR generation: {response.status_code}")

        if response.status_code == 200:
            # Save the result
            with open("api_test_result.png", "wb") as f:
                f.write(response.content)
            print("✅ Success! Result saved as api_test_result.png")
        else:
            print(f"❌ Error: {response.text}")

    except Exception as e:
        print(f"❌ QR generation failed: {e}")

def test_railway_api(railway_url):
    """Test the API deployed on Railway"""

    print(f"Testing Railway API at: {railway_url}")

    # Test health endpoint
    try:
        response = requests.get(f"{railway_url}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Railway deployment is healthy!")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Failed to connect to Railway: {e}")

if __name__ == "__main__":
    print("QR Postcard Generator API Test")
    print("=" * 40)

    # Test local API
    test_local_api()

    # Uncomment to test Railway deployment
    # test_railway_api("https://your-app.railway.app")