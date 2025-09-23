from PIL import Image, ImageDraw
import os

def find_qr_placement(postcard_path, test_positions, qr_sizes=[200, 250, 300, 350]):
    """
    Create test images with QR code bounding boxes at different positions and sizes
    to help find the perfect QR placement in the yellow box area
    """

    for size in qr_sizes:
        for i, (x, y) in enumerate(test_positions):
            # Open the postcard
            postcard = Image.open(postcard_path)
            draw = ImageDraw.Draw(postcard)

            # Draw QR bounding box (centered on x,y)
            half_size = size // 2
            left = x - half_size
            top = y - half_size
            right = x + half_size
            bottom = y + half_size

            # Draw the QR bounding box
            draw.rectangle([left, top, right, bottom],
                         fill=None, outline='red', width=8)

            # Draw center point
            center_size = 20
            draw.ellipse([x - center_size//2, y - center_size//2,
                         x + center_size//2, y + center_size//2],
                        fill='red', outline='darkred', width=2)

            # Add info text
            text_y = top - 60
            draw.text((left, text_y), f"QR: {size}x{size}px", fill='red')
            draw.text((left, text_y + 30), f"Center: ({x},{y})", fill='red')

            # Save test image
            output_name = f"qr_test_size{size}_pos{i+1}_x{x}_y{y}.png"
            postcard.save(output_name)
            print(f"Created: {output_name}")

def create_refined_positions():
    """
    Generate refined test positions focusing on the bottom-right yellow area
    Based on postcard dimensions: 5541 × 3741 pixels
    """

    # Fine-tuned positions around the yellow box area
    # Focusing on bottom-right quadrant with more precision
    positions = []

    # Create a denser grid in the promising area
    # X range: 4400-5300 (900px range)
    # Y range: 2800-3600 (800px range)

    x_coords = [4450, 4600, 4750, 4900, 5050, 5200, 5350]
    y_coords = [2850, 3000, 3150, 3300, 3450, 3600]

    for x in x_coords:
        for y in y_coords:
            # Make sure we don't go outside postcard bounds
            if x <= 5541 - 200 and y <= 3741 - 200:  # Leave margin for QR size
                positions.append((x, y))

    return positions

if __name__ == "__main__":
    # Path to your postcard
    postcard_path = "postcardSampleBlank.png"

    # Generate refined test positions
    test_positions = create_refined_positions()

    # Test different QR sizes (in pixels)
    qr_sizes = [200, 250, 300]  # Start with common sizes

    print(f"Testing {len(test_positions)} positions with {len(qr_sizes)} QR sizes...")
    print(f"Total test images to create: {len(test_positions) * len(qr_sizes)}")

    # Clean up old test files first
    for file in os.listdir('.'):
        if file.startswith('qr_test_'):
            os.remove(file)
            print(f"Removed old test file: {file}")

    find_qr_placement(postcard_path, test_positions, qr_sizes)
    print("Done! Check the qr_test_*.png images to find the best QR placement.")