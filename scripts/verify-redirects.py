"""
Post-deploy verification for the Squarespace -> Vercel cutover.

For every URL in backup-squarespace/_urls.txt, hits the corresponding path on
the target Vercel deployment and asserts one of:
  - direct 200 (for paths that carry over unchanged: blog-page/*, /, /contact, etc.)
  - 301 or 308 redirect whose Location resolves to 200

Reports only failures + a summary. Known-dead Squarespace pages (already 404 on
the live site at scrape time) are excluded from the expected-200 pool.

Usage:
    python scripts/verify-redirects.py https://www.functionalpatternsbrisbane.com
    python scripts/verify-redirects.py https://www.functionalpatternsbrisbane.com   # post-DNS cutover

Exit code: 0 if all green, 1 if any failures (suitable for CI gating).
"""
from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Optional: Vercel Deployment Protection bypass. Set VERCEL_PROTECTION_BYPASS
# in the environment; the value is sent as the x-vercel-protection-bypass
# header on every request. Never commit the secret itself.
BYPASS_SECRET = os.environ.get("VERCEL_PROTECTION_BYPASS", "")

ROOT = Path(__file__).resolve().parent.parent
URL_LIST = ROOT / "backup-squarespace" / "_urls.txt"

# Pages that returned 404 on the live Squarespace site at scrape time — no
# redirect was written for these and none is expected.
KNOWN_DEAD = {
    "/small-group-class-programs",
    "/fpresults",
    "/back-pain-brisbane",
}

# Squarespace hosts assets + utility URLs we don't want to check as pages.
SKIP_PREFIXES = (
    "/s/",  # Squarespace-hosted PDFs and static files
    "/universal/",  # Squarespace internal assets
    "/cart",  # commerce, not migrated
)

UA = "Mozilla/5.0 (compatible; FPBrisbane-RedirectVerifier/1.0)"
TIMEOUT = 15
WORKERS = 8


def normalise(url: str, target_base: str) -> str | None:
    """Strip query string, swap host to target, filter out skip-list and dead pages."""
    p = urlparse(url)
    path = p.path.rstrip("/") or "/"
    if path in KNOWN_DEAD:
        return None
    if any(path.startswith(pre) for pre in SKIP_PREFIXES):
        return None
    tb = urlparse(target_base)
    return urlunparse((tb.scheme, tb.netloc, path, "", "", ""))


def headers() -> dict[str, str]:
    h = {"User-Agent": UA}
    if BYPASS_SECRET:
        h["x-vercel-protection-bypass"] = BYPASS_SECRET
        h["x-vercel-set-bypass-cookie"] = "true"
    return h


def check(url: str) -> tuple[str, str, int, str]:
    """Returns (url, outcome, final_status, detail). outcome in {ok, redirect-ok, fail}."""
    try:
        req = Request(url, headers=headers(), method="HEAD")
        with urlopen(req, timeout=TIMEOUT) as r:
            status = r.status
            if status == 200:
                return url, "ok", 200, ""
            return url, "fail", status, f"unexpected non-redirect status {status}"
    except HTTPError as e:
        status = e.code
        if status in (301, 308):
            loc = e.headers.get("Location", "")
            if not loc:
                return url, "fail", status, "redirect with empty Location"
            # resolve relative Location against request URL
            if loc.startswith("/"):
                p = urlparse(url)
                loc = urlunparse((p.scheme, p.netloc, loc, "", "", ""))
            # fetch target, expect 200
            try:
                req2 = Request(loc, headers=headers(), method="HEAD")
                with urlopen(req2, timeout=TIMEOUT) as r2:
                    if r2.status == 200:
                        return url, "redirect-ok", status, f"-> {loc} (200)"
                    return url, "fail", r2.status, f"redirect to {loc} returned {r2.status}"
            except HTTPError as e2:
                return url, "fail", e2.code, f"redirect to {loc} returned {e2.code}"
            except URLError as e2:
                return url, "fail", 0, f"redirect target unreachable: {e2}"
        if status == 404:
            return url, "fail", 404, "404 — missing page or missing redirect"
        return url, "fail", status, f"unexpected status {status}"
    except URLError as e:
        return url, "fail", 0, f"unreachable: {e}"
    except Exception as e:
        return url, "fail", 0, f"error: {e}"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/verify-redirects.py <target-base-url>", file=sys.stderr)
        return 2
    target_base = sys.argv[1].rstrip("/")

    if not URL_LIST.exists():
        print(f"url list not found: {URL_LIST}", file=sys.stderr)
        return 2

    raw = [line.strip() for line in URL_LIST.read_text(encoding="utf-8").splitlines() if line.strip()]
    # de-dup after normalising (strips query strings, known-dead, skip prefixes)
    urls = sorted({u for u in (normalise(r, target_base) for r in raw) if u})
    print(f"checking {len(urls)} URLs against {target_base}")

    ok = 0
    redirected = 0
    failures: list[tuple[str, int, str]] = []

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(check, u) for u in urls]
        done = 0
        for fut in as_completed(futures):
            url, outcome, status, detail = fut.result()
            done += 1
            if outcome == "ok":
                ok += 1
            elif outcome == "redirect-ok":
                redirected += 1
            else:
                failures.append((url, status, detail))
                print(f"FAIL [{status}] {url} :: {detail}", flush=True)
            if done % 25 == 0:
                print(f"  progress {done}/{len(urls)}", flush=True)

    print("\n=== SUMMARY ===")
    print(f"checked:    {len(urls)}")
    print(f"200 direct: {ok}")
    print(f"301/308 ok: {redirected}")
    print(f"failures:   {len(failures)}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
