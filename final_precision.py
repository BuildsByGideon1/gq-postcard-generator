from PIL import Image, ImageDraw
import os

def create_final_precision_test():
    """
    Final precision test around the almost-perfect position
    Base: (4600, 2950) moved 50px left = (4550, 2950)
    Size: 1000px * 0.9 = 900px
    """

    postcard_path = "postcardSampleBlank.png"

    # Target position: 4600 moved right 50-200px = 4650-4800
    base_x = 4700  # Middle of the 50-200px right shift range
    base_y = 2950

    # Test positions spanning the 50-200px right shift
    x_offsets = [-50, -25, 0, 25, 50, 75, 100]  # 4650, 4675, 4700, 4725, 4750, 4775, 4800
    y_offsets = [-20, -10, 0, 10, 20]  # 2930, 2940, 2950, 2960, 2970

    # Size variations around 900px (0.9 * 1000)
    qr_sizes = [880, 900, 920]  # Slightly smaller/larger than 0.9x

    # Clean up old final test files
    for file in os.listdir('.'):
        if file.startswith('final_qr_'):
            os.remove(file)
            print(f"Removed: {file}")

    test_count = 0
    for size in qr_sizes:
        for x_offset in x_offsets:
            for y_offset in y_offsets:
                x = base_x + x_offset
                y = base_y + y_offset

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

                    # Draw thick red outline
                    draw.rectangle([left, top, right, bottom],
                                 fill=None, outline='red', width=12)

                    # Draw center point
                    center_size = 25
                    draw.ellipse([x - center_size//2, y - center_size//2,
                                 x + center_size//2, y + center_size//2],
                                fill='red', outline='darkred', width=3)

                    # Add detailed labels
                    text_y = top - 80
                    draw.text((left, text_y), f"QR: {size}x{size}px", fill='red')
                    draw.text((left, text_y + 40), f"Center: ({x},{y})", fill='red')

                    # Calculate offset from base position for reference
                    x_diff = x_offset
                    y_diff = y_offset
                    offset_text = f"Offset: ({x_diff:+d},{y_diff:+d})"
                    draw.text((left, text_y - 40), offset_text, fill='blue')

                    # Save with precise naming
                    output_name = f"final_qr_size{size}_x{x}_y{y}_offset{x_offset:+d}{y_offset:+d}.png"
                    postcard.save(output_name)
                    print(f"Created: {output_name}")

    print(f"\nCreated {test_count} final precision test images")
    print("Files: final_qr_*.png")
    print(f"\nBase position: ({base_x}, {base_y})")
    print(f"Target size: ~900px (0.9x of 1000px)")
    print("\nLook for the perfect fit and note the exact coordinates!")

if __name__ == "__main__":
    create_final_precision_test()