"""
One-shot script: adds favicon links to every <head> and an
"Designed by arclightdigital.com.au" credit to every footer
across src/**/*.html. Idempotent — re-running won't duplicate.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "src"

FAVICON_BLOCK = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
  <link rel="icon" type="image/png" sizes="512x512" href="/icon-512.png">
"""

# Existing footer bottom row format we're replacing:
# <p>&copy; 2026 Functional Patterns Brisbane. All rights reserved.</p>
# <p>Mon–Fri 7am–8pm &bull; ...</p>
CREDIT_TAG = '<p>Designed by <a href="https://arclightdigital.com.au" target="_blank" rel="noopener" class="hover:text-white transition-colors">arclightdigital.com.au</a></p>'

VIEWPORT_RE = re.compile(r'(<meta\s+name="viewport"[^>]*>)', re.IGNORECASE)
FAVICON_MARKER = '/favicon.svg'

# Match the existing two-paragraph copyright line and append the credit before the closing div.
COPYRIGHT_HOURS_RE = re.compile(
    r'(<p>&copy; 2026 Functional Patterns Brisbane\. All rights reserved\.</p>\s*'
    r'<p>Mon[^<]*</p>)',
    re.IGNORECASE
)

stats = {"head_done": 0, "head_skip": 0, "foot_done": 0, "foot_skip": 0, "foot_miss": 0, "files": 0}

for html in ROOT.rglob("*.html"):
    text = html.read_text(encoding="utf-8")
    orig = text
    stats["files"] += 1

    # 1. Favicon block in head
    if FAVICON_MARKER in text:
        stats["head_skip"] += 1
    else:
        new = VIEWPORT_RE.sub(r'\1\n' + FAVICON_BLOCK.rstrip(), text, count=1)
        if new != text:
            text = new
            stats["head_done"] += 1
        else:
            stats["head_skip"] += 1  # no viewport, leave alone

    # 2. Arclight credit
    if "arclightdigital.com.au" in text:
        stats["foot_skip"] += 1
    else:
        new, count = COPYRIGHT_HOURS_RE.subn(r'\1\n        ' + CREDIT_TAG, text)
        if count:
            text = new
            stats["foot_done"] += 1
        else:
            stats["foot_miss"] += 1

    if text != orig:
        html.write_text(text, encoding="utf-8")

print(f"Files scanned:        {stats['files']}")
print(f"Favicon added:        {stats['head_done']}")
print(f"Favicon already set:  {stats['head_skip']}")
print(f"Credit added:         {stats['foot_done']}")
print(f"Credit already set:   {stats['foot_skip']}")
print(f"No matching footer:   {stats['foot_miss']}")
