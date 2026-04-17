"""Convert all JPG/PNG images in src/images/ to WebP alongside originals.

Idempotent: skips images that already have a .webp counterpart newer than
the source. Produces one WebP file per source image, same basename.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image

SRC = Path(__file__).parent / "src" / "images"
QUALITY = 82  # visually lossless for photographic content


def convert_one(path: Path) -> tuple[int, int] | None:
    webp = path.with_suffix(".webp")
    if webp.exists() and webp.stat().st_mtime >= path.stat().st_mtime:
        return None

    with Image.open(path) as img:
        if img.mode in ("RGBA", "LA"):
            img.save(webp, "WEBP", quality=QUALITY, method=6)
        else:
            img.convert("RGB").save(webp, "WEBP", quality=QUALITY, method=6)

    return path.stat().st_size, webp.stat().st_size


def main() -> None:
    sources = sorted(
        [p for p in SRC.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    )
    total_before = 0
    total_after = 0
    converted = 0
    skipped = 0

    for src in sources:
        result = convert_one(src)
        if result is None:
            skipped += 1
            continue
        before, after = result
        total_before += before
        total_after += after
        converted += 1
        saving = (1 - after / before) * 100
        print(f"  {src.name:<40} {before/1024:>7.1f}KB -> {after/1024:>7.1f}KB  ({saving:+.0f}%)")

    print()
    print(f"Converted: {converted}, skipped (up-to-date): {skipped}")
    if converted:
        total_saving = (1 - total_after / total_before) * 100
        print(f"Total: {total_before/1024:.1f}KB -> {total_after/1024:.1f}KB ({total_saving:+.1f}%)")


if __name__ == "__main__":
    main()
