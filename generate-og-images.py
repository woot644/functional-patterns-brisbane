"""Generate 1200x630 Open Graph social-share images for key pages.

Takes an existing hero photo, crops to 1200x630, overlays a dark gradient
and page-specific title + brand name. Outputs to src/images/og/.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).parent
IMAGES = ROOT / "src" / "images"
OUT_DIR = IMAGES / "og"
OUT_DIR.mkdir(exist_ok=True)

W, H = 1200, 630
ACCENT = "#4A9FD9"       # brand accent (matches tailwind config)
DARK = (5, 5, 5)         # dark-950
TEXT = "#FFFFFF"
MUTED = "#D4D4D4"

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"

# (output filename, source hero image, page title, eyebrow label)
PAGES = [
    ("og-home.jpg", "fp-brisbane-training.jpg",
     "Biomechanics & Posture Specialists", "FUNCTIONAL PATTERNS BRISBANE"),
    ("og-book.jpg", "book-hero.jpg",
     "Book a 90-Minute Posture & Gait Assessment", "BOOK ASSESSMENT"),
    ("og-results.jpg", "result-posture-louis.jpg",
     "Real Results from Real Clients", "RESULTS & CASE STUDIES"),
    ("og-contact.jpg", "fp-brisbane-training.jpg",
     "Speak with a Biomechanics Specialist", "GET IN TOUCH"),
    ("og-team.jpg", "gait-analysis.jpg",
     "Meet Our Team of Biomechanics Practitioners", "OUR TEAM"),
    ("og-what-we-treat.jpg", "training-posture.jpg",
     "Chronic Pain, Posture, Scoliosis & More", "WHAT WE TREAT"),
    ("og-chronic-pain.jpg", "training-posture.jpg",
     "Chronic Back Pain Treatment in Brisbane", "CHRONIC PAIN"),
    ("og-scoliosis.jpg", "scoliosis-specialist.jpg",
     "Scoliosis Treatment in Brisbane — Without Surgery", "SCOLIOSIS"),
    ("og-posture.jpg", "straighten-back.jpg",
     "Posture Correction Through Movement Retraining", "POSTURE CORRECTION"),
    ("og-programs.jpg", "programs-hero-wide.jpg",
     "Group Programs at Functional Patterns Brisbane", "GROUP PROGRAMS"),
    ("og-online.jpg", "online-hero.jpg",
     "Train Online with Functional Patterns", "ONLINE TRAINING"),
    ("og-how-we-work.jpg", "gait-analysis.jpg",
     "Our Assessment-First Approach", "HOW WE WORK"),
    ("og-default.jpg", "fp-brisbane-training.jpg",
     "Correct Pain & Posture at the Root Cause", "FUNCTIONAL PATTERNS BRISBANE"),
]


def load_crop_hero(source: Path) -> Image.Image:
    img = Image.open(source).convert("RGB")
    src_ratio = img.width / img.height
    target_ratio = W / H
    if src_ratio > target_ratio:
        # source wider — crop horizontally
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        # source taller — crop vertically
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((W, H), Image.LANCZOS)


def apply_gradient(img: Image.Image) -> Image.Image:
    # Dark gradient from left (opaque) to right (semi-transparent) + bottom.
    gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    # Horizontal gradient
    for x in range(W):
        t = x / W
        alpha = int(210 * (1 - t) + 60 * t)
        draw.line([(x, 0), (x, H)], fill=(*DARK, alpha))

    # Additional darken at bottom for brand footer
    for y in range(H - 180, H):
        t = (y - (H - 180)) / 180
        alpha = int(60 + 150 * t)
        draw.line([(0, y), (W, y)], fill=(*DARK, alpha))

    out = img.convert("RGBA")
    out.alpha_composite(gradient)
    return out.convert("RGB")


def draw_text_block(img: Image.Image, title: str, eyebrow: str) -> Image.Image:
    d = ImageDraw.Draw(img)

    # Fonts
    eyebrow_font = ImageFont.truetype(FONT_BOLD, 22)
    title_font = ImageFont.truetype(FONT_BOLD, 58)
    brand_font = ImageFont.truetype(FONT_BOLD, 20)
    meta_font = ImageFont.truetype(FONT_REG, 20)

    margin_x = 60
    title_max_w = 920

    # Eyebrow (accent coloured)
    d.text((margin_x, 130), eyebrow, font=eyebrow_font, fill=ACCENT)

    # Accent underline
    eyebrow_bbox = d.textbbox((margin_x, 130), eyebrow, font=eyebrow_font)
    d.rectangle(
        [(margin_x, eyebrow_bbox[3] + 8), (margin_x + 60, eyebrow_bbox[3] + 12)],
        fill=ACCENT,
    )

    # Title — wrap to fit
    words = title.split()
    lines: list[str] = []
    current = ""
    for w in words:
        candidate = f"{current} {w}".strip()
        if d.textlength(candidate, font=title_font) <= title_max_w:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    title_y = 200
    for i, line in enumerate(lines):
        d.text((margin_x, title_y + i * 72), line, font=title_font, fill=TEXT)

    # Brand footer
    footer_y = H - 80
    d.text((margin_x, footer_y), "functionalpatternsbrisbane.com", font=brand_font, fill=TEXT)
    d.text(
        (margin_x, footer_y + 28),
        "45 Michael Street, Bulimba QLD  ·  0433 801 181",
        font=meta_font,
        fill=MUTED,
    )

    # Accent dot
    d.ellipse([(W - 120, footer_y + 4), (W - 100, footer_y + 24)], fill=ACCENT)
    d.text(
        (W - 90, footer_y + 4),
        "FP",
        font=brand_font,
        fill=TEXT,
    )
    d.text(
        (W - 90, footer_y + 28),
        "Brisbane",
        font=meta_font,
        fill=MUTED,
    )
    return img


def render_one(out_name: str, source_name: str, title: str, eyebrow: str) -> Path:
    source_path = IMAGES / source_name
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    img = load_crop_hero(source_path)
    # Subtle blur so text reads cleanly
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    img = apply_gradient(img)
    img = draw_text_block(img, title, eyebrow)

    out_path = OUT_DIR / out_name
    img.save(out_path, "JPEG", quality=88, optimize=True)
    return out_path


def main() -> None:
    for out_name, source, title, eyebrow in PAGES:
        try:
            path = render_one(out_name, source, title, eyebrow)
            size_kb = path.stat().st_size / 1024
            print(f"  {path.name:<26} {size_kb:>6.1f}KB  from {source}")
        except FileNotFoundError as e:
            print(f"  ! missing source for {out_name}: {e}")


if __name__ == "__main__":
    main()
