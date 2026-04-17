"""Build src/blog-page/index.html — a blog landing page listing all posts.

Reads every JSON file in scripts/scraped/ and renders a grid of cards, sorted
by date_published descending. Each card shows: hero image, title, excerpt,
date, read-more link.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
SCRAPED = ROOT / "scripts" / "scraped"
OUT = ROOT / "src" / "blog-page" / "index.html"
IMG_DIR = ROOT / "src" / "images" / "blog"
SITE_URL = "https://functional-patterns-brisbane.vercel.app"


def load_posts() -> list[dict]:
    posts = []
    for p in SCRAPED.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not data.get("title"):
            continue
        posts.append(data)
    # sort by date desc; undated posts go last
    posts.sort(key=lambda d: d.get("date_published") or "0000", reverse=True)
    return posts


def hero_relative_paths(slug: str) -> tuple[str, str] | None:
    """Find the hero image files for a given slug's post (if already downloaded)."""
    post_dir = IMG_DIR / slug
    if not post_dir.exists():
        return None
    # Just grab the first jpg/webp pair
    jpgs = sorted(post_dir.glob("*.jpg"))
    if not jpgs:
        return None
    jpg = jpgs[0]
    webp = jpg.with_suffix(".webp")
    if not webp.exists():
        return None
    return (jpg.name, webp.name)


def format_date(iso: str) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%d %B %Y")
    except Exception:
        return iso


def shorten(text: str, n: int = 160) -> str:
    text = (text or "").strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0] + "…"


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_card(post: dict) -> str:
    slug = post["slug"]
    title = esc(post["title"])
    description = esc(shorten(post.get("description", ""), 180))
    date_display = format_date(post.get("date_published", ""))

    hero_files = hero_relative_paths(slug)
    if hero_files:
        jpg, webp = hero_files
        img_html = (
            f'<picture>'
            f'<source type="image/webp" srcset="../images/blog/{slug}/{webp}">'
            f'<img src="../images/blog/{slug}/{jpg}" alt="{title}" loading="lazy" class="w-full h-48 object-cover">'
            f'</picture>'
        )
    else:
        img_html = (
            '<picture>'
            '<source type="image/webp" srcset="../images/fp-brisbane-training.webp">'
            '<img src="../images/fp-brisbane-training.jpg" alt="Functional Patterns Brisbane" loading="lazy" class="w-full h-48 object-cover opacity-80">'
            '</picture>'
        )

    date_html = (
        f'<time class="text-xs text-gray-400 uppercase tracking-wider">{date_display}</time>'
        if date_display else ""
    )

    return f'''    <a href="{slug}" class="group card-dark overflow-hidden hover:border-accent-500/40 transition-all">
      <div class="relative overflow-hidden">
        {img_html}
      </div>
      <div class="p-6">
        {date_html}
        <h3 class="text-white font-bold text-lg leading-tight mt-2 mb-3 group-hover:text-accent-500 transition-colors">{title}</h3>
        <p class="text-gray-400 text-sm leading-relaxed mb-4">{description}</p>
        <span class="text-accent-500 text-sm font-semibold inline-flex items-center gap-2">
          Read article
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>
        </span>
      </div>
    </a>'''


def build() -> str:
    posts = load_posts()
    cards = "\n".join(render_card(p) for p in posts)

    # Schema: Blog + BlogPosting itemList
    blog_items = []
    for i, p in enumerate(posts, 1):
        blog_items.append({
            "@type": "ListItem",
            "position": i,
            "url": f"{SITE_URL}/blog-page/{p['slug']}",
            "name": p["title"],
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{SITE_URL}/blog-page",
        "name": "Functional Patterns Brisbane Blog",
        "description": "Articles on gait, posture, biomechanics and chronic pain — written by Louis Ellery at Functional Patterns Brisbane.",
        "publisher": {
            "@type": "Organization",
            "name": "Functional Patterns Brisbane",
            "url": SITE_URL,
        },
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": blog_items,
        },
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog &mdash; Gait, Posture &amp; Movement Insights | Functional Patterns Brisbane</title>
  <meta name="description" content="Articles on gait, posture, biomechanics, and chronic pain from Functional Patterns Brisbane. Written by Louis Ellery.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
  <link rel="canonical" href="{SITE_URL}/blog-page">
  <meta property="og:title" content="Blog — Functional Patterns Brisbane">
  <meta property="og:description" content="Articles on gait, posture, biomechanics, and chronic pain from Functional Patterns Brisbane.">
  <meta property="og:image" content="{SITE_URL}/images/og/og-default.jpg">
  <meta property="og:url" content="{SITE_URL}/blog-page">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE_URL}/images/og/og-default.jpg">
  <script type="application/ld+json">
{json.dumps(schema, indent=2)}
  </script>
</head>
<body>

  <!-- Header -->
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
          <a href="." class="nav-link text-accent-500">Blog</a>
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
        <a href="." class="block py-3 nav-link text-accent-500">Blog</a>
        <a href="../programs" class="block py-3 nav-link font-medium">Group Programs</a><div class="pl-4 space-y-0"><a href="../programs/bells-and-bands" class="block py-2 text-sm text-gray-400 hover:text-white">Bells &amp; Bands (Ladies)</a><a href="../programs/rise-and-realign" class="block py-2 text-sm text-gray-400 hover:text-white">Rise &amp; Realign</a><a href="../programs/balance-and-symmetry" class="block py-2 text-sm text-gray-400 hover:text-white">Balance &amp; Symmetry</a><a href="../programs/functional-fundamentals" class="block py-2 text-sm text-gray-400 hover:text-white">Functional Fundamentals</a><a href="../programs/core-and-mobility" class="block py-2 text-sm text-gray-400 hover:text-white">Core &amp; Mobility</a><a href="../programs/human-foundations" class="block py-2 text-sm text-gray-400 hover:text-white">Human Foundations Course</a></div>
        <a href="../team" class="block py-3 nav-link">Our Team</a>
        <a href="../contact" class="block py-3 nav-link">Contact</a>
        <a href="../online" class="block py-3 nav-link">Online Training</a>
        <a href="tel:0433801181" class="block py-3 text-accent-500 font-semibold">0433 801 181</a>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <section class="relative bg-dark-950 pt-20">
    <div class="px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
      <div class="container-narrow max-w-3xl">
        <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">The FP Brisbane Blog</p>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white leading-tight mb-6">Gait, Posture &amp; Movement Insights</h1>
        <p class="text-gray-300 text-lg leading-relaxed">Articles from Louis Ellery on biomechanics, chronic pain, posture correction, and why most exercise advice misses the root cause. {len(posts)} articles and growing.</p>
      </div>
    </div>
  </section>

  <!-- Cards Grid -->
  <section class="section-charcoal">
    <div class="container-narrow">
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="bg-dark-950 border-t border-white/5 px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
    <div class="container-narrow text-center">
      <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">Ready to Apply This?</p>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mb-4">Book a Posture &amp; Gait Assessment</h2>
      <p class="text-gray-300 mb-8 max-w-xl mx-auto">The articles explain the principles. A 90-minute assessment shows you exactly how they apply to your body — and gives you a plan to fix it.</p>
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
            <li><a href="../programs" class="text-gray-400 hover:text-white transition-colors">Group Programs</a></li>
            <li><a href="../online" class="text-gray-400 hover:text-white transition-colors">Online Training</a></li>
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
    document.getElementById('mobile-menu-btn').addEventListener('click', function() {{
      document.getElementById('mobile-menu').classList.toggle('hidden');
    }});
  </script>
</body>
</html>
'''


def main() -> None:
    html = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
