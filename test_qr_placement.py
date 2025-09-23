#!/usr/bin/env python3
"""
Test script to generate a QR code and place it on the postcard
using the optimal coordinates we found
"""

import qrcode
from PIL import Image
import random

# Import our optimal placement values
from optimal_qr_placement import QR_SIZE, CENTER_X, CENTER_Y, TOP_LEFT_X, TOP_LEFT_Y

def generate_test_qr(url):
    """Generate a QR code for the given URL with #cefe05 background and minimal border"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,  # Reduced from 4 to 1 for larger QR code
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image with yellow-green background #cefe05
    qr_img = qr.make_image(fill_color="black", back_color="#cefe05")
    return qr_img

def place_qr_on_postcard(postcard_path, qr_image, output_path):
    """Place QR code on postcard at optimal position"""

    # Open the postcard
    postcard = Image.open(postcard_path)

    # Resize QR to optimal size
    qr_resized = qr_image.resize((QR_SIZE, QR_SIZE), Image.Resampling.LANCZOS)

    # Place QR at optimal position
    postcard.paste(qr_resized, (TOP_LEFT_X, TOP_LEFT_Y))

    # Save the result
    postcard.save(output_path)
    print(f"QR postcard saved as: {output_path}")

def main():
    # Use the specific test URL
    test_url = "http://ruralmetrofire.com/start/testingproperties?utm_source=testing&urm_medium=testing"
    print(f"Generating QR code for: {test_url}")

    # Generate QR code
    qr_image = generate_test_qr(test_url)
    print(f"QR code generated successfully")

    # Place on postcard
    postcard_path = "postcardSampleBlank.png"
    output_path = "test_qr_postcard.png"

    place_qr_on_postcard(postcard_path, qr_image, output_path)

    print("\nTest Results:")
    print(f"URL: {test_url}")
    print(f"QR Size: {QR_SIZE}x{QR_SIZE}px")
    print(f"QR Center: ({CENTER_X}, {CENTER_Y})")
    print(f"QR Top-left: ({TOP_LEFT_X}, {TOP_LEFT_Y})")
    print(f"Output file: {output_path}")
    print("\nScan the QR code with your phone to test!")

if __name__ == "__main__":
    main()