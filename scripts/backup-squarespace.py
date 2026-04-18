"""
Full backup of the live Squarespace site before the Vercel cutover.

- Seeds from sitemap.xml, then BFS-crawls internal links.
- Saves raw HTML under backup-squarespace/<path>/index.html (URL structure preserved).
- Downloads referenced images from www.functionalpatternsbrisbane.com and
  images.squarespace-cdn.com into backup-squarespace/_assets/<host>/<path>.
- Resume-safe: skips files that already exist.
- Writes a manifest (JSON + plain-text URL list) used later for the 301 redirect map.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "backup-squarespace"
PAGES_DIR = OUT / "pages"
ASSETS_DIR = OUT / "_assets"
MANIFEST_JSON = OUT / "_manifest.json"
URL_LIST = OUT / "_urls.txt"
LOG = OUT / "_log.txt"

BASE = "https://www.functionalpatternsbrisbane.com"
HOST = urlparse(BASE).netloc
ASSET_HOSTS = {HOST, "images.squarespace-cdn.com", "static1.squarespace.com"}

UA = "Mozilla/5.0 (compatible; FPBrisbane-Backup/1.0; archival)"
DELAY = 0.25  # polite crawl delay
TIMEOUT = 30

LINK_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
IMG_RE = re.compile(r'(?:src|data-src|data-image)=["\']([^"\']+)["\']', re.I)
SRCSET_RE = re.compile(r'srcset=["\']([^"\']+)["\']', re.I)


def fetch(url: str, retries: int = 4) -> tuple[bytes, str]:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=TIMEOUT) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except Exception as e:  # ConnectionReset, IncompleteRead, socket timeout, URLError, etc.
            last_err = e
            # exponential backoff: 1s, 2s, 4s, 8s
            time.sleep(2 ** attempt)
    raise last_err if last_err else RuntimeError("fetch failed")


def log(msg: str) -> None:
    print(msg, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


def url_to_page_path(url: str) -> Path:
    p = urlparse(url)
    path = p.path.strip("/")
    if not path:
        return PAGES_DIR / "index.html"
    return PAGES_DIR / path / "index.html"


def url_to_asset_path(url: str) -> Path:
    p = urlparse(url)
    path = p.path.lstrip("/")
    if not path:
        path = "_root"
    # strip query from filename but preserve a hash so different variants don't collide
    if p.query:
        from hashlib import md5
        stem, dot, ext = path.rpartition(".")
        q = md5(p.query.encode()).hexdigest()[:8]
        path = f"{stem}__{q}.{ext}" if dot else f"{path}__{q}"
    return ASSETS_DIR / p.netloc / path


def save(pathobj: Path, data: bytes) -> None:
    pathobj.parent.mkdir(parents=True, exist_ok=True)
    pathobj.write_bytes(data)


def load_sitemap() -> list[str]:
    urls: list[str] = []
    try:
        body, _ = fetch(f"{BASE}/sitemap.xml")
    except Exception as e:
        log(f"[sitemap] fetch failed: {e}")
        return urls
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.fromstring(body)
    # handle sitemap index or urlset
    for loc in root.findall(".//s:loc", ns):
        u = (loc.text or "").strip()
        if u.endswith(".xml"):
            try:
                sub, _ = fetch(u)
                subroot = ET.fromstring(sub)
                for l2 in subroot.findall(".//s:loc", ns):
                    u2 = (l2.text or "").strip()
                    if u2:
                        urls.append(u2)
            except Exception as e:
                log(f"[sitemap] sub fetch {u} failed: {e}")
        elif u:
            urls.append(u)
    return urls


def same_site(url: str) -> bool:
    return urlparse(url).netloc in {"", HOST}


def extract_links_and_assets(html: str, base_url: str) -> tuple[set[str], set[str]]:
    links: set[str] = set()
    assets: set[str] = set()
    for m in LINK_RE.finditer(html):
        href = urljoin(base_url, m.group(1))
        href, _ = urldefrag(href)
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        scheme = urlparse(href).scheme
        if scheme not in ("http", "https"):
            continue
        if same_site(href):
            links.add(href)
    for m in IMG_RE.finditer(html):
        src = urljoin(base_url, m.group(1))
        if urlparse(src).netloc in ASSET_HOSTS:
            assets.add(src)
    for m in SRCSET_RE.finditer(html):
        for part in m.group(1).split(","):
            cand = part.strip().split()[0] if part.strip() else ""
            if not cand:
                continue
            src = urljoin(base_url, cand)
            if urlparse(src).netloc in ASSET_HOSTS:
                assets.add(src)
    return links, assets


def main() -> int:
    OUT.mkdir(exist_ok=True)
    PAGES_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)

    seen_pages: set[str] = set()
    seen_assets: set[str] = set()
    manifest = {"pages": [], "assets": [], "errors": []}

    queue: deque[str] = deque()
    seeds = load_sitemap()
    log(f"[seed] sitemap returned {len(seeds)} urls")
    for u in seeds:
        if same_site(u):
            queue.append(u)
    queue.append(BASE + "/")

    while queue:
        url = queue.popleft()
        url, _ = urldefrag(url)
        if url in seen_pages:
            continue
        seen_pages.add(url)

        out_path = url_to_page_path(url)
        if out_path.exists():
            log(f"[skip] {url}")
            # still parse existing for link discovery (only if manifest missing)
            try:
                html = out_path.read_text(encoding="utf-8", errors="ignore")
                links, assets = extract_links_and_assets(html, url)
                for l in links:
                    if l not in seen_pages:
                        queue.append(l)
                for a in assets:
                    seen_assets.add(a)
            except Exception:
                pass
            manifest["pages"].append({"url": url, "path": str(out_path.relative_to(OUT)), "cached": True})
            continue

        try:
            body, ctype = fetch(url)
        except Exception as e:
            log(f"[err ] {url} -> {e}")
            manifest["errors"].append({"url": url, "error": str(e)})
            continue

        save(out_path, body)
        log(f"[page] {url} -> {out_path.relative_to(OUT)}")
        manifest["pages"].append({"url": url, "path": str(out_path.relative_to(OUT)), "ctype": ctype})

        if "html" in ctype.lower():
            html = body.decode("utf-8", errors="ignore")
            links, assets = extract_links_and_assets(html, url)
            for l in links:
                if l not in seen_pages:
                    queue.append(l)
            for a in assets:
                seen_assets.add(a)
        time.sleep(DELAY)

    log(f"[done-pages] {len(seen_pages)} pages, {len(seen_assets)} assets to fetch")

    for i, a in enumerate(sorted(seen_assets), 1):
        asset_path = url_to_asset_path(a)
        if asset_path.exists():
            manifest["assets"].append({"url": a, "path": str(asset_path.relative_to(OUT)), "cached": True})
            continue
        try:
            body, ctype = fetch(a)
        except Exception as e:
            log(f"[asset-err] {a} -> {e}")
            manifest["errors"].append({"url": a, "error": str(e)})
            continue
        save(asset_path, body)
        if i % 25 == 0:
            log(f"[asset] {i}/{len(seen_assets)}")
        manifest["assets"].append({"url": a, "path": str(asset_path.relative_to(OUT)), "ctype": ctype})
        time.sleep(DELAY)

    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    URL_LIST.write_text("\n".join(sorted(seen_pages)) + "\n", encoding="utf-8")
    log(f"[complete] pages={len(manifest['pages'])} assets={len(manifest['assets'])} errors={len(manifest['errors'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
