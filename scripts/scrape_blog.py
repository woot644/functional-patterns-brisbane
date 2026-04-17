"""
Bulk scrape Squarespace blog posts via Firecrawl API.
Reads slugs from blog-urls.txt, saves each as JSON in scraped/.
Skips slugs that already exist. Records failures in failed_slugs.txt.
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_KEY = "fc-0921dbcab7934e44ae221fe3d31e3555"
API_URL = "https://api.firecrawl.dev/v2/scrape"
BASE_URL = "https://www.functionalpatternsbrisbane.com/blog-page/"

SCRIPT_DIR = Path(__file__).parent
URLS_FILE = SCRIPT_DIR / "blog-urls.txt"
OUT_DIR = SCRIPT_DIR / "scraped"
FAILED_FILE = SCRIPT_DIR / "failed_slugs.txt"
OUT_DIR.mkdir(exist_ok=True)

TITLE_SUFFIX = " \u2014 Functional Patterns Brisbane"  # em-dash
TITLE_SUFFIX_HYPHEN = " - Functional Patterns Brisbane"


def parse_date(raw):
    if not raw:
        return ""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(raw))
    return m.group(1) if m else ""


def strip_suffix(s):
    if not s:
        return ""
    for suf in (TITLE_SUFFIX, TITLE_SUFFIX_HYPHEN):
        if s.endswith(suf):
            return s[: -len(suf)]
    return s


def first_desc(raw):
    """metadata.description can be a long repeated string, comma-joined. Take first distinct part."""
    if not raw:
        return ""
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    s = str(raw)
    # Squarespace often duplicates desc separated by ", " - first ~250 chars of OG is the clean one
    return s


def call_firecrawl(url, retries=3):
    payload = json.dumps({
        "url": url,
        "formats": ["markdown", "links"],
        "onlyMainContent": True,
        "removeBase64Images": True,
    }).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    last_err = None
    for attempt in range(retries):
        try:
            req = Request(API_URL, data=payload, headers=headers, method="POST")
            with urlopen(req, timeout=120) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read()[:200].decode('utf-8', errors='replace')}"
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            if e.code >= 500:
                time.sleep(2 * (attempt + 1))
                continue
            return {"_error": last_err}
        except URLError as e:
            last_err = f"URLError: {e}"
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            last_err = f"Exception: {e}"
            time.sleep(2 * (attempt + 1))
    return {"_error": last_err or "unknown error"}


def process_slug(slug):
    slug = slug.strip()
    if not slug:
        return ("skip-empty", slug, None)
    out_path = OUT_DIR / f"{slug}.json"
    if out_path.exists():
        return ("skip-exists", slug, None)

    url = BASE_URL + slug
    resp = call_firecrawl(url)

    if "_error" in resp:
        return ("fail", slug, resp["_error"])

    # Firecrawl v2 returns {"success": true, "data": {...}} OR flat {"markdown": ..., "metadata": ...}
    data = resp.get("data", resp)
    markdown = data.get("markdown", "") or ""
    metadata = data.get("metadata", {}) or {}

    if len(markdown) < 500:
        return ("fail", slug, f"markdown too short ({len(markdown)} chars)")

    meta_title = metadata.get("og:title") or metadata.get("ogTitle") or metadata.get("title") or ""
    headline = metadata.get("headline")
    if headline:
        title = headline
    else:
        title = strip_suffix(meta_title)

    desc = metadata.get("og:description") or metadata.get("ogDescription") or ""
    if not desc:
        d = metadata.get("description")
        if isinstance(d, list):
            desc = d[0] if d else ""
        else:
            # Often dup'd with ", " between copies - take first
            desc_s = str(d or "")
            # If the exact same string is repeated, split and take first
            parts = desc_s.split(", ")
            if len(parts) >= 2 and parts[0] == ", ".join(parts[1:])[: len(parts[0])]:
                desc = parts[0]
            else:
                desc = desc_s
    desc = first_desc(desc)

    hero = metadata.get("og:image") or metadata.get("ogImage") or metadata.get("image") or ""

    date_pub = parse_date(metadata.get("datePublished"))
    date_mod = parse_date(metadata.get("dateModified")) or date_pub

    record = {
        "slug": slug,
        "url": url,
        "title": title,
        "meta_title": meta_title,
        "description": desc,
        "author": "Louis Ellery",
        "date_published": date_pub,
        "date_modified": date_mod,
        "hero_image": hero,
        "markdown": markdown,
    }

    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return ("ok", slug, None)


def main():
    slugs = [s.strip() for s in URLS_FILE.read_text(encoding="utf-8").splitlines() if s.strip()]
    total = len(slugs)
    print(f"Total slugs: {total}")

    ok_count = 0
    skip_count = 0
    fail_list = []

    # Concurrent scraping
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(process_slug, s): s for s in slugs}
        done = 0
        for fut in as_completed(futures):
            slug = futures[fut]
            done += 1
            try:
                status, slug_ret, err = fut.result()
            except Exception as e:
                status, err = "fail", f"executor exception: {e}"

            if status == "ok":
                ok_count += 1
            elif status == "skip-exists":
                skip_count += 1
            elif status == "fail":
                fail_list.append((slug, err))
                print(f"  FAIL [{slug}]: {err}", flush=True)

            if done % 20 == 0 or done == total:
                print(f"Progress: {done}/{total} done | ok={ok_count} skip={skip_count} fail={len(fail_list)}", flush=True)

    # Write failed_slugs.txt
    if fail_list:
        with FAILED_FILE.open("w", encoding="utf-8") as f:
            for slug, err in fail_list:
                f.write(f"{slug}\t{err}\n")

    print("\n=== FINAL ===")
    print(f"Scraped OK: {ok_count}")
    print(f"Skipped (already existed): {skip_count}")
    print(f"Failed: {len(fail_list)}")
    for s, e in fail_list:
        print(f"  - {s}: {e}")


if __name__ == "__main__":
    main()
