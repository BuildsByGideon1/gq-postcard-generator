#!/usr/bin/env python3
"""
Calculate percentage-based positioning from our optimal coordinates
"""

# Original postcard dimensions
ORIGINAL_WIDTH = 5541
ORIGINAL_HEIGHT = 3741

# Optimal coordinates we found
QR_SIZE = 880
CENTER_X = 4695
CENTER_Y = 2940

# Calculate percentages
center_x_percent = (CENTER_X / ORIGINAL_WIDTH) * 100
center_y_percent = (CENTER_Y / ORIGINAL_HEIGHT) * 100
qr_size_percent = (QR_SIZE / ORIGINAL_WIDTH) * 100  # Use width as reference

print("Percentage-based QR Configuration:")
print("=" * 40)
print(f"Original dimensions: {ORIGINAL_WIDTH} × {ORIGINAL_HEIGHT}px")
print(f"Original QR center: ({CENTER_X}, {CENTER_Y})")
print(f"Original QR size: {QR_SIZE}px")
print()
print(f"QR Center X: {center_x_percent:.2f}% of width")
print(f"QR Center Y: {center_y_percent:.2f}% of height")
print(f"QR Size: {qr_size_percent:.2f}% of width")
print()
print("For use in code:")
print(f"QR_CENTER_X_PERCENT = {center_x_percent:.2f}")
print(f"QR_CENTER_Y_PERCENT = {center_y_percent:.2f}")
print(f"QR_SIZE_PERCENT = {qr_size_percent:.2f}")