#!/usr/bin/env python3
"""
Helper script to organize and review QR placement test results
"""
import os
import re

def organize_test_results():
    """Organize test files by size and position for easier review"""

    # Get all QR test files
    test_files = [f for f in os.listdir('.') if f.startswith('qr_test_')]

    if not test_files:
        print("No QR test files found. Run coordinate_finder.py first.")
        return

    # Group by size
    sizes = {}
    for file in test_files:
        match = re.search(r'size(\d+)', file)
        if match:
            size = int(match.group(1))
            if size not in sizes:
                sizes[size] = []
            sizes[size].append(file)

    print("QR Test Results Summary")
    print("=" * 50)
    print(f"Total test images: {len(test_files)}")
    print(f"QR sizes tested: {sorted(sizes.keys())}")
    print(f"Positions per size: {len(sizes[list(sizes.keys())[0]]) if sizes else 0}")
    print()

    # Show file organization
    for size in sorted(sizes.keys()):
        print(f"Size {size}px:")
        print(f"  Files: qr_test_size{size}_pos*.png")
        print(f"  Count: {len(sizes[size])}")
        print()

    print("Next Steps:")
    print("1. Open test images in your image viewer")
    print("2. Find the position that best fits the yellow box")
    print("3. Note the size and coordinates from the filename")
    print("4. Use those values in your API")
    print()
    print("Recommended review order:")
    print("- Start with size 250px (good balance)")
    print("- Look for QR boxes that fit nicely in yellow area")
    print("- Check that QR doesn't overlap important text/design")

def extract_optimal_coordinates():
    """
    Helper function to extract coordinates from a filename
    Usage: Call this after you've identified the best test image
    """
    print("\nCoordinate Extraction Helper:")
    print("Once you find the best image, use this pattern:")
    print("  Filename: qr_test_size250_pos15_x4750_y3150.png")
    print("  Extracted values:")
    print("    QR Size: 250px")
    print("    Center X: 4750")
    print("    Center Y: 3150")
    print()
    print("For your API, you'll need:")
    print("  - qr_size = 250")
    print("  - center_x = 4750")
    print("  - center_y = 3150")
    print("  - top_left_x = center_x - (qr_size // 2)")
    print("  - top_left_y = center_y - (qr_size // 2)")

if __name__ == "__main__":
    organize_test_results()
    extract_optimal_coordinates()