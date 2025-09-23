from PIL import Image, ImageDraw
import os

def create_focused_test():
    """
    Create focused test around the promising position (4750, 3000)
    Shifted 100-300px left with much larger QR codes (4-5x larger)
    """

    postcard_path = "postcardSampleBlank.png"

    # Base position was (4750, 3000) - shift left 100-300px
    # Original sizes were 200-300px, so 4-5x larger = 800-1500px

    # Fine-tuned positions around the target area (shifted left)
    x_positions = [
        4750 - 100,  # 4650
        4750 - 150,  # 4600
        4750 - 200,  # 4550
        4750 - 250,  # 4500
        4750 - 300,  # 4450
    ]

    # Keep Y around 3000, maybe test slight variations
    y_positions = [
        3000 - 50,   # 2950
        3000,        # 3000 (original)
        3000 + 50,   # 3050
    ]

    # Much larger QR sizes (4-5x the original 250px)
    qr_sizes = [
        1000,  # 4x larger than 250px
        1200,  # ~5x larger
        1400,  # ~5.6x larger
    ]

    # Clean up old focused test files
    for file in os.listdir('.'):
        if file.startswith('focused_qr_'):
            os.remove(file)
            print(f"Removed: {file}")

    test_count = 0
    for size in qr_sizes:
        for x in x_positions:
            for y in y_positions:
                # Make sure QR fits within postcard bounds
                half_size = size // 2
                if (x - half_size >= 0 and x + half_size <= 5541 and
                    y - half_size >= 0 and y + half_size <= 3741):

                    test_count += 1

                    # Open postcard
                    postcard = Image.open(postcard_path)
                    draw = ImageDraw.Draw(postcard)

                    # Draw QR bounding box
                    left = x - half_size
                    top = y - half_size
                    right = x + half_size
                    bottom = y + half_size

                    # Draw thick red outline for large QR
                    draw.rectangle([left, top, right, bottom],
                                 fill=None, outline='red', width=12)

                    # Draw center point
                    center_size = 30
                    draw.ellipse([x - center_size//2, y - center_size//2,
                                 x + center_size//2, y + center_size//2],
                                fill='red', outline='darkred', width=3)

                    # Add large text labels
                    text_y = top - 80
                    draw.text((left, text_y), f"QR: {size}x{size}px", fill='red')
                    draw.text((left, text_y + 40), f"Center: ({x},{y})", fill='red')

                    # Save with descriptive name
                    output_name = f"focused_qr_size{size}_x{x}_y{y}.png"
                    postcard.save(output_name)
                    print(f"Created: {output_name}")

    print(f"\nCreated {test_count} focused test images")
    print("Files: focused_qr_*.png")
    print("\nThese QR codes are 4-5x larger and positioned 100-300px left of your target.")

if __name__ == "__main__":
    create_focused_test()