#!/usr/bin/env python3
"""
Generate PWA icons from a source image.
Requires: pillow
Install: pip install pillow

Usage:
  python generate_icons.py source.png

Generates icons in multiple sizes for PWA:
  16x16, 32x32, 72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install pillow")
    sys.exit(1)

ICON_SIZES = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]


def create_placeholder_icon(size: int, output_dir: Path):
    """Create a simple placeholder icon with '5D' text."""
    img = Image.new("RGB", (size, size), color="#16213e")
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fallback to default
    try:
        font_size = int(size * 0.4)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    # Draw '5D' text centered
    text = "5D"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2

    # Draw text with shadow for depth
    draw.text((x + 2, y + 2), text, fill="#0f3460", font=font)  # Shadow
    draw.text((x, y), text, fill="#e94560", font=font)  # Main text

    # Save
    output_path = output_dir / f"icon-{size}x{size}.png"
    img.save(output_path, "PNG")
    print(f"  ✓ Generated {output_path.name}")


def generate_from_source(source_path: str, output_dir: Path):
    """Generate icons from a source image."""
    try:
        source = Image.open(source_path)
    except Exception as e:
        print(f"Error: Could not open source image: {e}")
        return False

    print(f"Source image: {source_path} ({source.size[0]}x{source.size[1]})")

    for size in ICON_SIZES:
        # Resize with high-quality resampling
        resized = source.resize((size, size), Image.Resampling.LANCZOS)

        output_path = output_dir / f"icon-{size}x{size}.png"
        resized.save(output_path, "PNG", optimize=True)
        print(f"  ✓ Generated {output_path.name}")

    return True


def main():
    output_dir = Path(__file__).parent / "icons"
    output_dir.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        source_path = sys.argv[1]
        if not Path(source_path).exists():
            print(f"Error: Source image not found: {source_path}")
            sys.exit(1)

        print(f"Generating icons from {source_path}...")
        if generate_from_source(source_path, output_dir):
            print(f"\n✓ Generated {len(ICON_SIZES)} icons in {output_dir}/")
    else:
        print("No source image provided, creating placeholder icons...")
        for size in ICON_SIZES:
            create_placeholder_icon(size, output_dir)
        print(f"\n✓ Generated {len(ICON_SIZES)} placeholder icons in {output_dir}/")
        print("\nTo generate from your own image, run:")
        print("  python generate_icons.py your-logo.png")


if __name__ == "__main__":
    main()
