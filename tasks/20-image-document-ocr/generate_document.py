#!/usr/bin/env python3
"""Generate a business invoice PNG for the image-document-ocr task.

Uses PIL to render a clear, readable invoice image.
Ground truth: INV-2025-0847, Northstar Consulting Group, $9,450.00, 2025-11-03, 5 items.
"""
from pathlib import Path

def main():
    from PIL import Image, ImageDraw, ImageFont

    W, H = 800, 1000
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Use default font (always available)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except (OSError, IOError):
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Border
    draw.rectangle([20, 20, W - 20, H - 20], outline="#333333", width=2)

    # Company header
    y = 40
    draw.text((40, y), "NORTHSTAR CONSULTING GROUP", fill="#1a237e", font=title_font)
    y += 35
    draw.text((40, y), "123 Innovation Drive, Suite 400", fill="#555", font=small_font)
    y += 18
    draw.text((40, y), "San Francisco, CA 94105", fill="#555", font=small_font)
    y += 18
    draw.text((40, y), "Phone: (415) 555-0192 | Email: billing@northstarcg.com", fill="#555", font=small_font)

    # Invoice title
    y += 40
    draw.text((40, y), "INVOICE", fill="#1a237e", font=title_font)

    # Invoice details (right side)
    draw.text((480, 80), "Invoice Number:", fill="#333", font=body_font)
    draw.text((620, 80), "INV-2025-0847", fill="#000", font=header_font)
    draw.text((480, 105), "Invoice Date:", fill="#333", font=body_font)
    draw.text((620, 105), "2025-11-03", fill="#000", font=body_font)
    draw.text((480, 130), "Due Date:", fill="#333", font=body_font)
    draw.text((620, 130), "2025-12-03", fill="#000", font=body_font)

    # Separator
    y += 40
    draw.line([(40, y), (W - 40, y)], fill="#1a237e", width=2)

    # Bill To
    y += 15
    draw.text((40, y), "Bill To:", fill="#333", font=header_font)
    y += 22
    draw.text((40, y), "Meridian Technologies Inc.", fill="#000", font=body_font)
    y += 20
    draw.text((40, y), "456 Enterprise Blvd", fill="#555", font=small_font)
    y += 16
    draw.text((40, y), "Austin, TX 78701", fill="#555", font=small_font)

    # Table header
    y += 40
    draw.rectangle([40, y, W - 40, y + 30], fill="#1a237e")
    draw.text((50, y + 6), "#", fill="white", font=header_font)
    draw.text((80, y + 6), "Description", fill="white", font=header_font)
    draw.text((420, y + 6), "Qty", fill="white", font=header_font)
    draw.text((500, y + 6), "Unit Price", fill="white", font=header_font)
    draw.text((640, y + 6), "Amount", fill="white", font=header_font)

    # Line items (5 items)
    line_items = [
        ("1", "Strategic Planning Workshop (2 days)", "2", "$1,500.00", "$3,000.00"),
        ("2", "Market Analysis Report", "1", "$2,200.00", "$2,200.00"),
        ("3", "Technical Architecture Review", "1", "$1,800.00", "$1,800.00"),
        ("4", "Staff Training Session (half-day)", "3", "$450.00", "$1,350.00"),
        ("5", "Project Management (monthly)", "1", "$1,100.00", "$1,100.00"),
    ]

    y += 30
    for i, (num, desc, qty, unit, amount) in enumerate(line_items):
        row_y = y + i * 30
        bg = "#f5f5f5" if i % 2 == 0 else "white"
        draw.rectangle([40, row_y, W - 40, row_y + 30], fill=bg)
        draw.text((50, row_y + 7), num, fill="#333", font=body_font)
        draw.text((80, row_y + 7), desc, fill="#333", font=body_font)
        draw.text((430, row_y + 7), qty, fill="#333", font=body_font)
        draw.text((500, row_y + 7), unit, fill="#333", font=body_font)
        draw.text((640, row_y + 7), amount, fill="#333", font=body_font)

    # Separator after items
    y += len(line_items) * 30 + 10
    draw.line([(400, y), (W - 40, y)], fill="#ccc", width=1)

    # Totals
    y += 10
    draw.text((500, y), "Subtotal:", fill="#333", font=body_font)
    draw.text((640, y), "$9,450.00", fill="#333", font=body_font)
    y += 25
    draw.text((500, y), "Tax (0%):", fill="#333", font=body_font)
    draw.text((640, y), "$0.00", fill="#333", font=body_font)
    y += 25
    draw.line([(500, y), (W - 40, y)], fill="#1a237e", width=2)
    y += 8
    draw.text((500, y), "TOTAL:", fill="#1a237e", font=header_font)
    draw.text((640, y), "$9,450.00", fill="#1a237e", font=header_font)

    # Footer
    y += 60
    draw.line([(40, y), (W - 40, y)], fill="#ccc", width=1)
    y += 10
    draw.text((40, y), "Payment Terms: Net 30 | Please include invoice number with payment.", fill="#777", font=small_font)
    y += 18
    draw.text((40, y), "Thank you for your business!", fill="#777", font=small_font)

    out_path = Path(__file__).parent / "seed" / "document.png"
    out_path.parent.mkdir(exist_ok=True)
    img.save(out_path, "PNG")
    print(f"Generated {out_path}")


if __name__ == "__main__":
    main()
