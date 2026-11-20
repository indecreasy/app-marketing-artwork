#!/usr/bin/env python3
"""Create a side-by-side preview of an artwork and its intended crop."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def crop_box(size, rect):
    width, height = size
    if rect is None:
        side = min(size)
        rect = ((width - side) // 2, (height - side) // 2, side, side)
    x, y, crop_width, crop_height = rect
    if min(x, y) < 0 or min(crop_width, crop_height) <= 0:
        raise ValueError("Crop requires non-negative coordinates and positive dimensions.")
    right, bottom = x + crop_width, y + crop_height
    if right > width or bottom > height:
        raise ValueError(f"Crop falls outside the {width} × {height} input.")
    return x, y, right, bottom


def scaled_preview(image, width):
    height = max(1, round(image.height * width / image.width))
    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    opaque = Image.new("RGBA", resized.size, "#f5f1ee")
    return Image.alpha_composite(opaque, resized).convert("RGB")


def make_preview(source, output, rect, preview_width):
    if source.resolve() == output.resolve():
        raise ValueError("Use a separate path for the preview.")
    with Image.open(source) as image:
        full = ImageOps.exif_transpose(image).convert("RGBA")
    box = crop_box(full.size, rect)
    left = scaled_preview(full, preview_width)
    right = scaled_preview(full.crop(box), preview_width)

    scale_x = left.width / full.width
    scale_y = left.height / full.height
    x0, y0, x1, y1 = box
    guide = (
        round(x0 * scale_x),
        round(y0 * scale_y),
        max(round(x0 * scale_x), round(x1 * scale_x) - 1),
        max(round(y0 * scale_y), round(y1 * scale_y) - 1),
    )
    ImageDraw.Draw(left).rectangle(guide, outline="#072b17", width=3)
    if guide[2] - guide[0] > 4 and guide[3] - guide[1] > 4:
        inner_guide = (guide[0] + 1, guide[1] + 1, guide[2] - 1, guide[3] - 1)
        ImageDraw.Draw(left).rectangle(inner_guide, outline="#8dffc0", width=1)

    margin, gap, top = 12, 12, 34
    right_x = margin + left.width + gap
    sheet = Image.new(
        "RGB", (right_x + right.width + margin, top + max(left.height, right.height) + margin), "#f5f1ee"
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), "FULL WITH GUIDE", fill="#282728")
    draw.text((right_x, 12), "CROPPED VIEW", fill="#282728")
    sheet.paste(left, (margin, top))
    sheet.paste(right, (right_x, top))
    sheet.save(output, format="PNG")
    return sheet.size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, help="Destination PNG, separate from the source image")
    crop = parser.add_mutually_exclusive_group(required=True)
    crop.add_argument("--square", action="store_true", help="Use a centred square crop")
    crop.add_argument("--rect", type=int, nargs=4, metavar=("X", "Y", "WIDTH", "HEIGHT"))
    parser.add_argument("--preview-width", type=int, default=390, help="Width of each preview in pixels")
    args = parser.parse_args()
    if args.output.suffix.lower() != ".png" or args.preview_width < 120:
        parser.error("Use a .png output and a preview width of at least 120 px.")
    try:
        width, height = make_preview(args.source, args.output, args.rect, args.preview_width)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"{args.output} ({width} × {height})")


if __name__ == "__main__":
    main()
