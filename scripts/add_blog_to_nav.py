"""Add a 'Blog' link to the header + footer nav on every existing HTML page.

The blog nav link gets inserted between 'Results' and 'Our Team' in the desktop
header, and between 'Online Training' (or similar) and the tel: link in mobile.
Also adds 'Blog' to the footer 'Explore' section.

Idempotent: skips pages that already have the Blog link.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent / "src"

# Desktop nav: insert after 'Results' link, before 'Group Programs' dropdown
DESKTOP_RESULTS = re.compile(
    r'(<a href="(?:\.\./|)results" class="nav-link">Results</a>)\s*\n'
)

# Mobile nav: insert after 'Results' link
MOBILE_RESULTS = re.compile(
    r'(<a href="(?:\.\./|)results" class="block py-3 nav-link">Results</a>)\s*\n'
)

# Footer 'Explore' list: insert after the Online Training link
FOOTER_EXPLORE = re.compile(
    r'(<li><a href="(?:\.\./|)online"[^>]*>Online Training</a></li>)\s*\n'
)


def prefix_for(path: Path) -> str:
    """../ if in a subdirectory of src/, '' if at the root."""
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def process(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    if 'href="' in content and 'blog-page"' in content.lower():
        return False  # already has blog link
    if ">Blog</a>" in content:
        return False

    pref = prefix_for(path)
    blog_href = f"{pref}blog-page"

    original = content

    desktop_insert = (
        f'          <a href="{blog_href}" class="nav-link">Blog</a>\n'
    )
    content = DESKTOP_RESULTS.sub(
        lambda m: f'{m.group(1)}\n{desktop_insert}', content, count=1,
    )

    mobile_insert = (
        f'        <a href="{blog_href}" class="block py-3 nav-link">Blog</a>\n'
    )
    content = MOBILE_RESULTS.sub(
        lambda m: f'{m.group(1)}\n{mobile_insert}', content, count=1,
    )

    footer_insert = (
        f'            <li><a href="{blog_href}" class="text-gray-400 hover:text-white transition-colors">Blog</a></li>\n'
    )
    content = FOOTER_EXPLORE.sub(
        lambda m: f'{m.group(1)}\n{footer_insert}', content, count=1,
    )

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    files = sorted(
        p for p in ROOT.rglob("*.html")
        if "blog-page" not in p.relative_to(ROOT).parts
    )
    changed = 0
    for p in files:
        if process(p):
            changed += 1
            print(f"  + {p.relative_to(ROOT)}")
    print(f"\nUpdated {changed}/{len(files)} files")


if __name__ == "__main__":
    main()
