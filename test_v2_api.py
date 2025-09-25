#!/usr/bin/env python3
"""
Test script for QR Postcard Generator API v2.0
Tests percentage-based positioning and API key authentication
"""

import requests
import os
from PIL import Image

def test_api_v2():
    """Test the new API with API key and percentage-based positioning"""

    base_url = "http://localhost:8080"
    test_api_key = "your-secret-api-key-change-this"  # Default API key

    print("QR Postcard Generator API v2.0 Test")
    print("=" * 50)

    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Version: {health_data['version']}")
            print(f"   Features: {health_data['features']}")
        print()
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return

    # Test API documentation
    print("2. Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            api_data = response.json()
            print(f"   Version: {api_data['version']}")
            print(f"   Authentication required: {api_data['security']['api_key_required']}")
        print()
    except Exception as e:
        print(f"   ❌ Documentation check failed: {e}")

    # Test without API key (should fail)
    print("3. Testing without API key (should fail)...")
    try:
        with open("postcardSampleBlank.png", "rb") as f:
            files = {"image": f}
            data = {"url": "https://example.com/test"}

            response = requests.post(f"{base_url}/generate-qr-postcard", files=files, data=data)

        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly rejected without API key")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
        print()
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    # Test with API key (should work)
    print("4. Testing with API key (should work)...")
    try:
        with open("postcardSampleBlank.png", "rb") as f:
            files = {"image": f}
            data = {
                "url": "https://ruralmetrofire.com/start/testingproperties?utm_source=testing&utm_medium=postcard",
                "api_key": test_api_key
            }

            response = requests.post(f"{base_url}/generate-qr-postcard", files=files, data=data)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            # Save the result
            with open("api_v2_test_result.png", "wb") as f:
                f.write(response.content)

            # Print QR positioning info from headers
            print("   ✅ Success! QR positioning info:")
            print(f"      QR Size: {response.headers.get('X-QR-Size')}px")
            print(f"      QR Center: ({response.headers.get('X-QR-Center-X')}, {response.headers.get('X-QR-Center-Y')})")
            print(f"      Postcard Size: {response.headers.get('X-Postcard-Size')}")
            print("   📁 Result saved as: api_v2_test_result.png")
        else:
            print(f"   ❌ Error: {response.text}")
        print()
    except Exception as e:
        print(f"   ❌ Test failed: {e}")

    # Test with X-API-Key header instead of form field
    print("5. Testing with X-API-Key header...")
    try:
        headers = {"X-API-Key": test_api_key}

        with open("postcardSampleBlank.png", "rb") as f:
            files = {"image": f}
            data = {"url": "https://example.com/header-test"}

            response = requests.post(
                f"{base_url}/generate-qr-postcard",
                files=files,
                data=data,
                headers=headers
            )

        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Header authentication works!")
            with open("api_v2_header_test.png", "wb") as f:
                f.write(response.content)
        else:
            print(f"   ❌ Error: {response.text}")
        print()
    except Exception as e:
        print(f"   ❌ Header test failed: {e}")

def test_scaling():
    """Test percentage-based scaling with different image sizes"""

    print("6. Testing percentage-based scaling...")

    # Create a smaller version of the postcard to test scaling
    try:
        original = Image.open("postcardSampleBlank.png")
        original_width, original_height = original.size

        # Create 50% scaled version
        scaled_width = original_width // 2
        scaled_height = original_height // 2
        scaled_postcard = original.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        scaled_postcard.save("postcard_50percent.png")

        print(f"   Original size: {original_width}x{original_height}")
        print(f"   Scaled size: {scaled_width}x{scaled_height}")

        # Test with scaled postcard
        base_url = "http://localhost:8080"
        test_api_key = "your-secret-api-key-change-this"

        with open("postcard_50percent.png", "rb") as f:
            files = {"image": f}
            data = {
                "url": "https://example.com/scaling-test",
                "api_key": test_api_key
            }

            response = requests.post(f"{base_url}/generate-qr-postcard", files=files, data=data)

        if response.status_code == 200:
            with open("api_v2_scaled_test.png", "wb") as f:
                f.write(response.content)

            print("   ✅ Scaling test successful!")
            print(f"      Scaled QR Size: {response.headers.get('X-QR-Size')}px")
            print(f"      Scaled QR Center: ({response.headers.get('X-QR-Center-X')}, {response.headers.get('X-QR-Center-Y')})")
            print("   📁 Result saved as: api_v2_scaled_test.png")
        else:
            print(f"   ❌ Scaling test failed: {response.text}")

    except Exception as e:
        print(f"   ❌ Scaling test error: {e}")

if __name__ == "__main__":
    test_api_v2()
    test_scaling()