"""Transform a scraped blog post JSON into a Vercel site HTML page.

Input: scripts/scraped/{slug}.json — Firecrawl markdown + metadata
Output: src/blog-page/{slug}.html — full HTML page matching site template
Side effects: downloads all images into src/images/blog/{slug}/ as JPG + WebP

Usage:
    python scripts/transform_blog_post.py <slug>
    python scripts/transform_blog_post.py --all  # process every scraped/*.json
"""
from __future__ import annotations

import json
import re
import sys
import hashlib
from pathlib import Path
from urllib.parse import urlparse, unquote
from typing import Any

import markdown as md
import requests
from PIL import Image

ROOT = Path(__file__).parent.parent
SCRAPED_DIR = ROOT / "scripts" / "scraped"
OUT_DIR = ROOT / "src" / "blog-page"
IMG_DIR = ROOT / "src" / "images" / "blog"
SITE_URL = "https://www.functionalpatternsbrisbane.com"

OUT_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 FPBrisbaneMigrator/1.0"
})


# ──────────────────────────────────────────────────────────────────────
# Image download + WebP conversion
# ──────────────────────────────────────────────────────────────────────
def download_and_convert(url: str, out_dir: Path) -> tuple[str, str] | None:
    """Download image, save as JPG, generate WebP alongside. Returns (jpg_filename, webp_filename) relative to images/blog/{slug}/."""
    if not url or not url.startswith("http"):
        return None

    try:
        r = SESSION.get(url, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"  ! download failed: {url}: {e}")
        return None

    # Derive filename from URL
    parsed = urlparse(url)
    original_name = Path(unquote(parsed.path)).stem
    # Clean filename
    safe = re.sub(r'[^a-zA-Z0-9_-]+', '-', original_name).strip('-').lower() or "image"
    # Cap the slug portion to keep full paths under Windows 260-char limit
    safe = safe[:50].rstrip('-') or "image"
    # Hash to avoid collisions
    h = hashlib.md5(url.encode()).hexdigest()[:6]
    basename = f"{safe}-{h}"

    out_dir.mkdir(parents=True, exist_ok=True)
    jpg_path = out_dir / f"{basename}.jpg"
    webp_path = out_dir / f"{basename}.webp"

    if jpg_path.exists() and webp_path.exists():
        return (jpg_path.name, webp_path.name)

    # Load and save as JPG + WebP
    try:
        from io import BytesIO
        img = Image.open(BytesIO(r.content))
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        # Limit max dimension to 1500px
        if max(img.size) > 1500:
            img.thumbnail((1500, 1500), Image.LANCZOS)
        img.save(jpg_path, "JPEG", quality=85, optimize=True)
        img.save(webp_path, "WEBP", quality=82, method=6)
    except Exception as e:
        print(f"  ! image processing failed: {url}: {e}")
        return None

    return (jpg_path.name, webp_path.name)


# ──────────────────────────────────────────────────────────────────────
# Markdown → clean HTML body
# ──────────────────────────────────────────────────────────────────────
def strip_article_cruft(text: str) -> str:
    """Remove Squarespace navigation, author block, form remnants, and footer cruft."""
    # Remove leading cart link
    text = re.sub(r'^\[\d+\]\([^)]*cart[^)]*\)\s*', '', text)

    # Cut at the author bio block (repeated "Louis Ellery" link after content)
    patterns_end = [
        r"\n\[Previous\\\\",           # Previous/Next nav
        r"\n\[Previous\n",
        r"\n\*\s*\*\s*\*\s*\n",         # horizontal rule
        r"\n\[Louis Ellery\]\(https://www\.functionalpatternsbrisbane\.com/blog-page\?author=",  # repeated author link
    ]
    cut_index = len(text)
    for pat in patterns_end:
        m = re.search(pat, text)
        if m and m.start() < cut_index:
            cut_index = m.start()
    text = text[:cut_index]

    # Strip any leading H1 (we render the title in the hero, not article body)
    text = re.sub(r'^#\s+[^\n]+\n+', '', text, count=1)

    # Strip author/date preamble — the Firecrawl markdown reliably has a
    # date line + "Written By [Louis Ellery](...)" + blanks at the top.
    # Keep stripping each matching leading line until no more match.
    leading_junk_patterns = [
        r'^\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s*\n',
        r'^\s*Written [Bb]y\s*\[?[^\n]+\]?\([^\n]*\)[^\n]*\n',
        r'^\s*Written [Bb]y[^\n]+\n',
    ]
    changed = True
    while changed:
        changed = False
        for pat in leading_junk_patterns:
            new_text = re.sub(pat, '', text, count=1)
            if new_text != text:
                text = new_text
                changed = True

    return text.strip()


def rewrite_internal_links(text: str) -> str:
    """Rewrite absolute functionalpatternsbrisbane.com links to relative site paths."""
    def _repl(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        # Keep external links as-is (not fp brisbane)
        if "functionalpatternsbrisbane.com" not in url:
            return m.group(0)
        # Parse path
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        if not path:
            return f"[{label}](../)"
        # Map Squarespace paths to new site paths
        mappings = {
            "/back-pain-brisbane": "../conditions/chronic-pain",
            "/correct-posture": "../conditions/posture-correction",
            "/scoliosisresults": "../results",
            "/scoliosisresults-1": "../results",
            "/training-with-us": "../book",
            "/functionalpatternsservices": "../how-we-work",
            "/our-facility": "../contact",
            "/our-gait-based-assessment": "../book",
            "/functionalpatternsmethod": "../how-we-work",
            "/privacy-policy": "../privacy",
            "/trainer-credentials": "../team",
            "/diastasis-recti-coning": "../conditions/diastasis-recti",
            "/fascia": "../conditions/fascia",
            "/functional-fundamentals": "../programs/functional-fundamentals",
            "/balance-symmetry-group-program": "../programs/balance-and-symmetry",
            "/boxing-for-balance": "../programs",
            "/fpfundamentalsclass": "../programs/functional-fundamentals",
            "/chronicpainexperts": "../conditions/chronic-pain",
            "/hunchback-posture": "../conditions/hunchback-posture",
            "/correct-winged-scapulas": "../conditions/winged-scapulas",
        }
        if path in mappings:
            return f"[{label}]({mappings[path]})"
        # Blog-page links stay relative to src/blog-page/
        if path.startswith("/blog-page/"):
            new_slug = path[len("/blog-page/"):]
            return f"[{label}]({new_slug})"
        # Unknown FP path — point to homepage
        return f"[{label}](../)"

    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', _repl, text)


def markdown_to_html(text: str, image_mapping: dict[str, tuple[str, str]], slug: str) -> str:
    """Render cleaned markdown to HTML. Also rewrites image URLs to local webp+jpg picture tags."""
    # First, replace image markdown with <picture> tags using local paths.
    # markdown library would otherwise produce plain <img>.
    def _image_repl(m: re.Match) -> str:
        alt = m.group(1)
        url = m.group(2)
        files = image_mapping.get(url)
        if not files:
            # No local file — fallback to external url as plain img
            return f'<img src="{url}" alt="{alt}" loading="lazy" class="w-full rounded-xl my-8">'
        jpg, webp = files
        base = f"../images/blog/{slug}"
        return (
            f'<picture>'
            f'<source type="image/webp" srcset="{base}/{webp}">'
            f'<img src="{base}/{jpg}" alt="{alt}" loading="lazy" class="w-full rounded-xl my-8">'
            f'</picture>'
        )

    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _image_repl, text)

    # Now render the rest of the markdown normally
    html = md.markdown(text, extensions=['extra', 'nl2br'], output_format='html5')

    # Add Tailwind classes to common tags in the rendered HTML
    html = re.sub(r'<h2\b', '<h2 class="text-dark-900 text-2xl sm:text-3xl font-bold mb-4 mt-12"', html)
    html = re.sub(r'<h3\b', '<h3 class="text-dark-900 text-xl font-bold mb-3 mt-8"', html)
    html = re.sub(r'<h4\b', '<h4 class="text-dark-900 text-lg font-semibold mb-2 mt-6"', html)
    html = re.sub(r'<p\b', '<p class="text-gray-700 text-base leading-relaxed mb-5"', html)
    html = re.sub(r'<ul\b', '<ul class="list-disc pl-6 space-y-2 mb-6 text-gray-700"', html)
    html = re.sub(r'<ol\b', '<ol class="list-decimal pl-6 space-y-2 mb-6 text-gray-700"', html)
    html = re.sub(r'<li\b', '<li class="leading-relaxed"', html)
    html = re.sub(r'<strong\b', '<strong class="text-dark-900 font-semibold"', html)
    html = re.sub(r'<a\b(?![^>]*class=)', '<a class="text-accent-500 hover:text-accent-400 underline underline-offset-2"', html)
    html = re.sub(r'<blockquote\b', '<blockquote class="border-l-4 border-accent-500 pl-5 italic text-gray-600 my-6"', html)

    return html


# ──────────────────────────────────────────────────────────────────────
# HTML template
# ──────────────────────────────────────────────────────────────────────
HEADER_HTML = '''  <!-- Header -->
  <header class="fixed top-0 left-0 right-0 z-50 bg-dark-950/90 backdrop-blur-md border-b border-white/5">
    <nav class="px-4 sm:px-6 lg:px-8">
      <div class="container-narrow flex items-center justify-between h-20 sm:h-28">
        <a href="../" class="text-white font-bold text-lg tracking-tight">
          <picture><source type="image/webp" srcset="../images/fp-logo-full.webp"><img src="../images/fp-logo-full.jpg" alt="Functional Patterns Brisbane" loading="eager" width="499" height="374" class="h-28 w-auto"></picture>
        </a>
        <div class="hidden lg:flex items-center gap-6">
          <a href="../" class="nav-link">Home</a>
          <div class="relative group"><a href="../how-we-work" class="nav-link">How We Work</a><div class="absolute top-full left-1/2 -translate-x-1/2 pt-2 hidden group-hover:block z-50"><div class="bg-dark-800 border border-white/10 rounded-lg shadow-xl py-2 w-56"><a href="../book" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">1-on-1 Assessment</a><a href="../online" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Train Online</a><div class="border-t border-white/10 mt-1 pt-1"><a href="../how-we-work" class="block px-4 py-2 text-sm text-accent-500 hover:text-accent-400">Our Approach</a></div></div></div></div>
          <div class="relative group"><a href="../what-we-treat" class="nav-link">What We Treat</a><div class="absolute top-full left-1/2 -translate-x-1/2 pt-2 hidden group-hover:block z-50"><div class="bg-dark-800 border border-white/10 rounded-lg shadow-xl py-2 w-56"><a href="../conditions/chronic-pain" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Chronic Pain</a><a href="../conditions/scoliosis" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Scoliosis</a><a href="../conditions/posture-correction" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Posture Correction</a><a href="../conditions/joint-pain" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Joint Pain</a><a href="../conditions/gait-running" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Gait &amp; Running</a><a href="../conditions/hunchback-posture" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Hunchback Posture</a><a href="../conditions/winged-scapulas" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Winged Scapulas</a><a href="../conditions/diastasis-recti" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Diastasis Recti</a><a href="../conditions/kids-teens" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Kids &amp; Teens</a><a href="../conditions/athletes" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Athletes</a><a href="../conditions/fascia" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Fascia &amp; Chronic Fatigue</a><div class="border-t border-white/10 mt-1 pt-1"><a href="../what-we-treat" class="block px-4 py-2 text-sm text-accent-500 hover:text-accent-400">View All Conditions</a></div></div></div></div>
          <a href="../results" class="nav-link">Results</a>
          <a href="." class="nav-link">Blog</a>
          <div class="relative group"><a href="../programs" class="nav-link">Group Programs</a><div class="absolute top-full left-1/2 -translate-x-1/2 pt-2 hidden group-hover:block z-50"><div class="bg-dark-800 border border-white/10 rounded-lg shadow-xl py-2 w-56"><a href="../programs/bells-and-bands" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Bells &amp; Bands (Ladies)</a><a href="../programs/rise-and-realign" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Rise &amp; Realign</a><a href="../programs/balance-and-symmetry" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Balance &amp; Symmetry</a><a href="../programs/functional-fundamentals" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Functional Fundamentals</a><a href="../programs/core-and-mobility" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Core &amp; Mobility</a><a href="../programs/human-foundations" class="block px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-white/5">Human Foundations Course</a><div class="border-t border-white/10 mt-1 pt-1"><a href="../programs" class="block px-4 py-2 text-sm text-accent-500 hover:text-accent-400">View All Programs</a></div></div></div></div>
          <a href="../team" class="nav-link">Our Team</a>
          <a href="../book" class="btn-primary py-2.5 px-5 text-xs">Book Assessment</a>
        </div>
        <div class="flex items-center gap-3 lg:hidden">
          <a href="../book" class="btn-primary py-2 px-4 text-xs">Book</a>
          <button id="mobile-menu-btn" class="p-2 text-white" aria-label="Open menu">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>
          </button>
        </div>
      </div>
    </nav>
    <div id="mobile-menu" class="hidden lg:hidden border-t border-white/5 bg-dark-950">
      <div class="px-4 py-4 space-y-1">
        <a href="../" class="block py-3 nav-link">Home</a>
        <a href="../how-we-work" class="block py-3 nav-link font-medium">How We Work</a><div class="pl-4 space-y-0"><a href="../book" class="block py-2 text-sm text-gray-400 hover:text-white">1-on-1 Assessment</a><a href="../online" class="block py-2 text-sm text-gray-400 hover:text-white">Train Online</a></div>
        <a href="../what-we-treat" class="block py-3 nav-link font-medium">What We Treat</a><div class="pl-4 space-y-0"><a href="../conditions/chronic-pain" class="block py-2 text-sm text-gray-400 hover:text-white">Chronic Pain</a><a href="../conditions/scoliosis" class="block py-2 text-sm text-gray-400 hover:text-white">Scoliosis</a><a href="../conditions/posture-correction" class="block py-2 text-sm text-gray-400 hover:text-white">Posture Correction</a><a href="../conditions/joint-pain" class="block py-2 text-sm text-gray-400 hover:text-white">Joint Pain</a><a href="../conditions/gait-running" class="block py-2 text-sm text-gray-400 hover:text-white">Gait &amp; Running</a><a href="../conditions/hunchback-posture" class="block py-2 text-sm text-gray-400 hover:text-white">Hunchback Posture</a><a href="../conditions/winged-scapulas" class="block py-2 text-sm text-gray-400 hover:text-white">Winged Scapulas</a><a href="../conditions/diastasis-recti" class="block py-2 text-sm text-gray-400 hover:text-white">Diastasis Recti</a><a href="../conditions/kids-teens" class="block py-2 text-sm text-gray-400 hover:text-white">Kids &amp; Teens</a><a href="../conditions/athletes" class="block py-2 text-sm text-gray-400 hover:text-white">Athletes</a><a href="../conditions/fascia" class="block py-2 text-sm text-gray-400 hover:text-white">Fascia &amp; Chronic Fatigue</a></div>
        <a href="../results" class="block py-3 nav-link">Results</a>
        <a href="." class="block py-3 nav-link">Blog</a>
        <a href="../programs" class="block py-3 nav-link font-medium">Group Programs</a><div class="pl-4 space-y-0"><a href="../programs/bells-and-bands" class="block py-2 text-sm text-gray-400 hover:text-white">Bells &amp; Bands (Ladies)</a><a href="../programs/rise-and-realign" class="block py-2 text-sm text-gray-400 hover:text-white">Rise &amp; Realign</a><a href="../programs/balance-and-symmetry" class="block py-2 text-sm text-gray-400 hover:text-white">Balance &amp; Symmetry</a><a href="../programs/functional-fundamentals" class="block py-2 text-sm text-gray-400 hover:text-white">Functional Fundamentals</a><a href="../programs/core-and-mobility" class="block py-2 text-sm text-gray-400 hover:text-white">Core &amp; Mobility</a><a href="../programs/human-foundations" class="block py-2 text-sm text-gray-400 hover:text-white">Human Foundations Course</a></div>
        <a href="../team" class="block py-3 nav-link">Our Team</a>
        <a href="../contact" class="block py-3 nav-link">Contact</a>
        <a href="../online" class="block py-3 nav-link">Online Training</a>
        <a href="tel:0433801181" class="block py-3 text-accent-500 font-semibold">0433 801 181</a>
      </div>
    </div>
  </header>
'''

FOOTER_HTML = '''  <!-- CTA -->
  <section class="bg-dark-900 px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
    <div class="container-narrow text-center">
      <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">Apply This to Your Body</p>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mb-4">Ready to Fix the Root Cause?</h2>
      <p class="text-gray-300 mb-8 max-w-xl mx-auto">Book a 90-minute posture and gait assessment. We identify the movement patterns driving your pain and build a correction plan specific to you.</p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a href="../book" class="btn-primary">Book an Assessment</a>
        <a href="../results" class="btn-outline">See Our Results</a>
      </div>
    </div>
  </section>

  <footer class="bg-dark-950 border-t border-white/5 pt-16 pb-8 px-4">
    <div class="container-narrow">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <div>
          <div class="text-white font-bold text-lg mb-4"><picture><source type="image/webp" srcset="../images/fp-logo-full.webp"><img src="../images/fp-logo-full.jpg" alt="Functional Patterns Brisbane" loading="eager" width="499" height="374" class="h-28 w-auto"></picture></div>
          <p class="text-gray-400 text-sm leading-relaxed mb-4">Brisbane's leading biomechanics facility. Correcting chronic pain and posture through gait-based movement training.</p>
        </div>
        <div>
          <h4 class="text-white font-semibold text-sm mb-4">Explore</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="../how-we-work" class="text-gray-400 hover:text-white transition-colors">How We Work</a></li>
            <li><a href="../what-we-treat" class="text-gray-400 hover:text-white transition-colors">What We Treat</a></li>
            <li><a href="../results" class="text-gray-400 hover:text-white transition-colors">Results</a></li>
            <li><a href="." class="text-gray-400 hover:text-white transition-colors">Blog</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold text-sm mb-4">About</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="../team" class="text-gray-400 hover:text-white transition-colors">Our Team</a></li>
            <li><a href="../book" class="text-gray-400 hover:text-white transition-colors">Book Assessment</a></li>
            <li><a href="../contact" class="text-gray-400 hover:text-white transition-colors">Contact</a></li>
            <li><a href="../privacy" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold text-sm mb-4">Contact</h4>
          <ul class="space-y-3 text-sm">
            <li><a href="tel:0433801181" class="text-gray-400 hover:text-white transition-colors">0433 801 181</a></li>
            <li><a href="mailto:brisbane@functionalpatterns.com" class="text-gray-400 hover:text-white transition-colors">brisbane@functionalpatterns.com</a></li>
            <li><span class="text-gray-400">45 Michael Street<br>Bulimba, QLD 4171</span></li>
          </ul>
        </div>
      </div>
      <p class="text-xs text-gray-600 mt-6 leading-relaxed max-w-2xl mx-auto text-center">Individual results vary. The content on this website is for educational purposes and does not constitute medical advice. Consult a qualified health professional before making changes to your health management.</p>
      <div class="border-t border-white/5 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-500">
        <p>&copy; 2026 Functional Patterns Brisbane. All rights reserved.</p>
        <p>Mon&ndash;Fri 7am&ndash;8pm &bull; Sat 7am&ndash;3pm &bull; Sun 7am&ndash;1pm</p>
      </div>
    </div>
  </footer>

  <script>
    document.getElementById('mobile-menu-btn').addEventListener('click', function() {
      document.getElementById('mobile-menu').classList.toggle('hidden');
    });
  </script>
</body>
</html>
'''


def render_page(meta: dict, body_html: str, hero_files: tuple[str, str] | None, slug: str) -> str:
    title = meta["title"]
    description = meta.get("description", "")
    meta_title = meta.get("meta_title") or f"{title} | Functional Patterns Brisbane"
    author = meta.get("author", "Louis Ellery")
    date_published = meta.get("date_published", "")
    date_modified = meta.get("date_modified", date_published)
    canonical = f"{SITE_URL}/blog-page/{slug}"

    # Hero image
    if hero_files:
        jpg, webp = hero_files
        hero_src = f"images/blog/{slug}/{jpg}"
        og_image_abs = f"{SITE_URL}/images/blog/{slug}/{jpg}"
        hero_picture = (
            f'<picture>'
            f'<source type="image/webp" srcset="../images/blog/{slug}/{webp}">'
            f'<img src="../images/blog/{slug}/{jpg}" alt="{title}" loading="eager" fetchpriority="high" class="w-full h-full object-cover opacity-40">'
            f'</picture>'
        )
    else:
        hero_src = "images/og/og-default.jpg"
        og_image_abs = f"{SITE_URL}/images/og/og-default.jpg"
        hero_picture = (
            f'<picture>'
            f'<source type="image/webp" srcset="../images/fp-brisbane-training.webp">'
            f'<img src="../images/fp-brisbane-training.jpg" alt="{title}" loading="eager" class="w-full h-full object-cover opacity-30">'
            f'</picture>'
        )

    # Publish date nice
    if date_published:
        try:
            from datetime import datetime
            dt = datetime.strptime(date_published, "%Y-%m-%d")
            date_display = dt.strftime("%B %Y")
        except Exception:
            date_display = date_published
    else:
        date_display = ""

    # Escape quotes in meta fields
    def esc(s: str) -> str:
        return (s or "").replace('"', '&quot;').replace('\n', ' ').strip()

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": og_image_abs,
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {
            "@type": "Person",
            "name": author,
            "url": f"{SITE_URL}/team"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Functional Patterns Brisbane",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/images/fp-logo-full.jpg"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical
        }
    }

    schema_json = json.dumps(article_schema, indent=2)

    date_line = ""
    if date_display:
        date_line = f'<span class="text-gray-400">&bull;</span><time class="text-gray-400">{date_display}</time>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(meta_title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{esc(meta_title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{og_image_abs}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="{date_published}">
  <meta property="article:modified_time" content="{date_modified}">
  <meta property="article:author" content="{author}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og_image_abs}">
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>

{HEADER_HTML}

  <!-- Hero -->
  <section class="relative min-h-[50vh] flex items-center bg-dark-950 overflow-hidden pt-20">
    <div class="absolute inset-0">
      {hero_picture}
      <div class="absolute inset-0 bg-gradient-to-r from-dark-950 via-dark-950/75 via-[40%] to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-dark-950 via-transparent to-dark-950/30"></div>
    </div>
    <div class="relative px-4 sm:px-6 lg:px-8 py-16 sm:py-20 w-full">
      <div class="container-narrow max-w-3xl">
        <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-4">Functional Patterns Brisbane Blog</p>
        <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white leading-tight mb-6">{title}</h1>
        <div class="flex items-center gap-3 text-sm">
          <span class="text-gray-300">Written by <a href="../team" class="text-accent-500 hover:text-accent-400">{author}</a></span>
          {date_line}
        </div>
      </div>
    </div>
  </section>

  <!-- Article Body -->
  <section class="bg-white px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
    <div class="container-narrow max-w-3xl">
      <article class="prose-article">
{body_html}
      </article>

      <div class="mt-16 pt-8 border-t border-gray-200">
        <p class="text-xs text-gray-500 leading-relaxed">This article is for educational purposes and does not constitute medical advice. Individual results vary. Consult a qualified health professional before making changes to your health management.</p>
      </div>
    </div>
  </section>

{FOOTER_HTML}'''


# ──────────────────────────────────────────────────────────────────────
# Main per-post transform
# ──────────────────────────────────────────────────────────────────────
def transform(slug: str) -> bool:
    scraped_path = SCRAPED_DIR / f"{slug}.json"
    if not scraped_path.exists():
        print(f"  ! no scrape for {slug}")
        return False

    meta = json.loads(scraped_path.read_text(encoding="utf-8"))

    markdown_text = meta.get("markdown", "")
    markdown_text = strip_article_cruft(markdown_text)
    markdown_text = rewrite_internal_links(markdown_text)

    # Download images (hero + inline)
    image_urls = set()
    if meta.get("hero_image"):
        image_urls.add(meta["hero_image"])
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', markdown_text):
        image_urls.add(m.group(1))

    post_img_dir = IMG_DIR / slug
    image_mapping: dict[str, tuple[str, str]] = {}
    hero_files: tuple[str, str] | None = None
    for url in sorted(image_urls):
        result = download_and_convert(url, post_img_dir)
        if result:
            image_mapping[url] = result
            if url == meta.get("hero_image"):
                hero_files = result

    # Render body markdown to HTML (with image URL rewriting)
    body_html = markdown_to_html(markdown_text, image_mapping, slug)

    page = render_page(meta, body_html, hero_files, slug)
    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(page, encoding="utf-8")
    print(f"  wrote {out_path.relative_to(ROOT)} ({len(page):,} bytes, {len(image_mapping)} images)")
    return True


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "--all":
        slugs = sorted([p.stem for p in SCRAPED_DIR.glob("*.json")])
    else:
        slugs = args

    ok = 0
    for slug in slugs:
        print(f"[{slug}]")
        if transform(slug):
            ok += 1

    print(f"\nProcessed {ok}/{len(slugs)} posts")


if __name__ == "__main__":
    main()
