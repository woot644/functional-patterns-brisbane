"""Append all blog-page URLs to src/sitemap.xml.

Reads the scraped JSON files to get the slug list + date_modified per post.
Idempotent: removes any existing blog-page entries before re-adding.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRAPED = ROOT / "scripts" / "scraped"
SITEMAP = ROOT / "src" / "sitemap.xml"
SITE_URL = "https://functional-patterns-brisbane.vercel.app"
TODAY = "2026-04-17"


def load_posts() -> list[dict]:
    out = []
    for p in SCRAPED.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("title"):
            out.append(data)
    return out


def main() -> None:
    content = SITEMAP.read_text(encoding="utf-8")

    # Remove any existing /blog-page/ entries (idempotent re-run)
    content = re.sub(
        r'\s*<url>\s*<loc>[^<]*?/blog-page(?:/[^<]*)?</loc>.*?</url>',
        '',
        content,
        flags=re.DOTALL,
    )

    posts = load_posts()

    # Build blog entries
    blog_entries = [
        f"  <url>\n    <loc>{SITE_URL}/blog-page</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>"
    ]
    for p in sorted(posts, key=lambda x: x.get("date_modified") or x.get("date_published") or "", reverse=True):
        slug = p["slug"]
        lastmod = p.get("date_modified") or p.get("date_published") or TODAY
        blog_entries.append(
            f"  <url>\n    <loc>{SITE_URL}/blog-page/{slug}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>"
        )

    blog_block = "\n".join(blog_entries)

    # Insert before closing </urlset>
    content = content.replace(
        "</urlset>",
        f"{blog_block}\n</urlset>",
    )

    SITEMAP.write_text(content, encoding="utf-8")
    print(f"Added {len(posts) + 1} blog URL entries to sitemap.xml")


if __name__ == "__main__":
    main()
