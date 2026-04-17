"""Replace empty alt="" on blog body images with descriptive text derived
from filename + the blog post's H1. Skips already-filled alts."""
import re
from html import unescape
from pathlib import Path

BLOGS = Path(__file__).parent / "src" / "blog-page"

# Filename patterns that are not human-readable and should fall back to H1
GENERIC_PATTERNS = [
    re.compile(r"^img[_-]?\d+"),
    re.compile(r"^mfr[-_]?\d*$"),
    re.compile(r"^screenshot"),
    re.compile(r"^images?$"),
    re.compile(r"^\d{4}-\d{2}-\d{2}"),
    re.compile(r"^[a-f0-9]{10,}$"),  # Pure hash
]


def humanize_filename(src: str) -> str | None:
    """Extract a meaningful phrase from an image filename, or None if generic."""
    stem = Path(src).stem  # strip extension
    # Strip trailing content hash like "-b5b4e8" or "-1f331e" (6-8 hex chars).
    stem = re.sub(r"-[a-f0-9]{6,8}$", "", stem)
    if not stem or any(p.match(stem) for p in GENERIC_PATTERNS):
        return None
    phrase = re.sub(r"[-_]+", " ", stem).strip()
    if not phrase or len(phrase) < 4:
        return None
    return phrase[0].upper() + phrase[1:]


def extract_h1(html: str) -> str | None:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if not m:
        return None
    inner = re.sub(r"<[^>]+>", "", m.group(1))
    return unescape(" ".join(inner.split()))


def fix_alt_attributes(html: str, h1: str | None) -> tuple[str, int]:
    fixed = 0

    def _replace(match: re.Match) -> str:
        nonlocal fixed
        tag = match.group(0)
        # Only touch blog body images — skip header/footer logo references.
        src_match = re.search(r'\bsrc="([^"]+)"', tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        if "fp-logo" in src:
            return tag
        alt_match = re.search(r'\balt="([^"]*)"', tag)
        if alt_match and alt_match.group(1).strip():
            return tag  # Already has meaningful alt

        filename_phrase = humanize_filename(src)
        if filename_phrase and h1:
            new_alt = f"{filename_phrase} — {h1}"
        elif filename_phrase:
            new_alt = filename_phrase
        elif h1:
            new_alt = h1
        else:
            return tag

        # Trim to reasonable length for screen readers.
        new_alt = new_alt[:200].rstrip(" —")

        if alt_match:
            tag = tag.replace(alt_match.group(0), f'alt="{new_alt}"')
        else:
            tag = tag[:-1] + f' alt="{new_alt}">'
        fixed += 1
        return tag

    return re.sub(r"<img\b[^>]*>", _replace, html), fixed


def main() -> None:
    total_fixed = 0
    posts_touched = 0
    for post in sorted(BLOGS.glob("*.html")):
        if post.name == "index.html":
            continue
        html = post.read_text(encoding="utf-8")
        h1 = extract_h1(html)
        new, n = fix_alt_attributes(html, h1)
        if n:
            posts_touched += 1
            total_fixed += n
            post.write_text(new, encoding="utf-8")
    print(f"Filled alt text on {total_fixed} images across {posts_touched} posts")


if __name__ == "__main__":
    main()
