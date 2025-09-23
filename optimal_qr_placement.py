"""
OPTIMAL QR CODE PLACEMENT FOR POSTCARD API
==========================================

Based on testing with final_qr_size880_x4675_y2940_offset-25-10.png

FINAL COORDINATES:
- QR Size: 880px x 880px
- Center Position: (4675, 2940)
- Top-left Position: (4235, 2500)  # center_x - size/2, center_y - size/2
- Bottom-right Position: (5115, 3380)  # center_x + size/2, center_y + size/2

POSTCARD DIMENSIONS:
- Total size: 5541 × 3741 pixels
- QR fits within bounds: ✓

API IMPLEMENTATION VALUES:
"""

# Constants for your QR postcard generator API
QR_SIZE = 880
CENTER_X = 4675 + 20  # Shifted 20 pixels right = 4695
CENTER_Y = 2940

# Calculated positions
TOP_LEFT_X = CENTER_X - (QR_SIZE // 2)  # 4255
TOP_LEFT_Y = CENTER_Y - (QR_SIZE // 2)  # 2500

def get_qr_placement():
    """
    Returns the optimal QR code placement coordinates
    """
    return {
        'qr_size': QR_SIZE,
        'center_x': CENTER_X,
        'center_y': CENTER_Y,
        'top_left_x': TOP_LEFT_X,
        'top_left_y': TOP_LEFT_Y,
        'width': QR_SIZE,
        'height': QR_SIZE
    }

def place_qr_on_postcard(postcard_image, qr_image):
    """
    Example function to place QR code at optimal position
    """
    # Resize QR to optimal size
    qr_resized = qr_image.resize((QR_SIZE, QR_SIZE))

    # Paste at optimal position
    postcard_image.paste(qr_resized, (TOP_LEFT_X, TOP_LEFT_Y))

    return postcard_image

if __name__ == "__main__":
    placement = get_qr_placement()
    print("OPTIMAL QR PLACEMENT COORDINATES:")
    print("=" * 40)
    for key, value in placement.items():
        print(f"{key}: {value}")

    print("\nBounding Box:")
    print(f"Top-left: ({TOP_LEFT_X}, {TOP_LEFT_Y})")
    print(f"Bottom-right: ({TOP_LEFT_X + QR_SIZE}, {TOP_LEFT_Y + QR_SIZE})")