"""Insert schema for remaining pages: 9 research articles, what-we-treat,
how-we-work, online. Idempotent via marker comments."""
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
BASE_URL = "https://www.functionalpatternsbrisbane.com"

MARKER_START = "<!-- Generated Schema Start -->"
MARKER_END = "<!-- Generated Schema End -->"

RESEARCH_PAGES = [
    "ankle-foot-mechanics.html",
    "arm-swing-running.html",
    "diaphragm-spinal-stability.html",
    "fascia-load-adaptation.html",
    "gait-hip-pelvis-mechanics.html",
    "gait-retraining-knee-pain.html",
    "hip-internal-rotation.html",
    "motor-control-vs-strengthening.html",
    "movement-vs-standard-exercise.html",
]

CONDITIONS_LIST = [
    ("chronic-pain", "Resolve Chronic Pain"),
    ("scoliosis", "Straighten Scoliosis"),
    ("posture-correction", "Transform Posture"),
    ("joint-pain", "Fix Joint Pain"),
    ("gait-running", "Improve Gait and Running"),
    ("hunchback-posture", "Hunchback Posture"),
    ("winged-scapulas", "Correct Winged Scapulas"),
    ("diastasis-recti", "Diastasis Recti and Coning"),
    ("kids-teens", "Kids and Teenagers"),
    ("athletes", "Biomechanics for Athletes"),
    ("fascia", "Fascia and Chronic Conditions"),
]


def extract(pattern: str, html: str) -> str:
    m = re.search(pattern, html)
    if not m:
        raise RuntimeError(f"No match: {pattern[:60]}")
    return unescape(m.group(1).strip())


def wrap(doc: list) -> str:
    body = json.dumps(doc, indent=2, ensure_ascii=False)
    return (
        f'  {MARKER_START}\n'
        f'  <script type="application/ld+json">\n{body}\n  </script>\n'
        f'  {MARKER_END}\n'
    )


def insert(page: Path, block: str) -> None:
    html = page.read_text(encoding="utf-8")
    if MARKER_START in html:
        html = re.sub(
            rf"  {re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n",
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html = html.replace("</head>", block + "</head>", 1)
    page.write_text(html, encoding="utf-8")


def research_schema(filename: str) -> list:
    page = SRC / "research" / filename
    html = page.read_text(encoding="utf-8")
    slug = filename.removesuffix(".html")
    url = f"{BASE_URL}/research/{slug}"
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    # Clean trailing brand suffix on title.
    for suffix in [" | Functional Patterns Brisbane", " — Functional Patterns Brisbane"]:
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
            break
    return [
        {
            "@context": "https://schema.org",
            "@type": "ScholarlyArticle",
            "@id": f"{url}#article",
            "url": url,
            "headline": title,
            "description": desc,
            "author": {
                "@type": "Person",
                "name": "Louis Ellery",
                "jobTitle": "Owner and Lead Biomechanics Specialist",
                "worksFor": {"@id": f"{BASE_URL}/#business"},
            },
            "publisher": {"@id": f"{BASE_URL}/#business"},
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "about": {
                "@type": "Thing",
                "name": "Biomechanics and Movement Science",
            },
            "mainEntityOfPage": url,
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Research", "item": f"{BASE_URL}/results"},
                {"@type": "ListItem", "position": 3, "name": title, "item": url},
            ],
        },
    ]


def what_we_treat_schema() -> list:
    page = SRC / "what-we-treat.html"
    html = page.read_text(encoding="utf-8")
    url = f"{BASE_URL}/what-we-treat"
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    return [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "What We Treat", "item": url},
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "@id": f"{url}#conditions-list",
            "name": "Conditions Treated at Functional Patterns Brisbane",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "url": f"{BASE_URL}/conditions/{slug}",
                    "name": label,
                }
                for i, (slug, label) in enumerate(CONDITIONS_LIST)
            ],
        },
    ]


def how_we_work_schema() -> list:
    page = SRC / "how-we-work.html"
    html = page.read_text(encoding="utf-8")
    url = f"{BASE_URL}/how-we-work"
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    return [
        {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "mainEntity": {"@id": f"{BASE_URL}/#business"},
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "How We Work", "item": url},
                ],
            },
        }
    ]


def online_schema() -> list:
    page = SRC / "online.html"
    html = page.read_text(encoding="utf-8")
    url = f"{BASE_URL}/online"
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    return [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Online Training", "item": url},
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": f"{url}#service",
            "name": "Online Functional Patterns Training",
            "description": "Remote biomechanics coaching via video. 90-minute initial assessment plus follow-up integration training for clients anywhere in the world.",
            "url": url,
            "provider": {"@id": f"{BASE_URL}/#business"},
            "serviceType": "Online Biomechanics Coaching",
            "category": "Biomechanics & Movement Therapy",
            "areaServed": {"@type": "Country", "name": "Worldwide"},
            "offers": [
                {
                    "@type": "Offer",
                    "name": "Initial Online Assessment",
                    "price": "180",
                    "priceCurrency": "USD",
                    "description": "90-minute initial biomechanics assessment delivered remotely via video.",
                },
                {
                    "@type": "Offer",
                    "name": "Integration Training 5-Pack",
                    "price": "500",
                    "priceCurrency": "USD",
                    "description": "Five 60-minute online follow-up integration training sessions.",
                },
            ],
        },
    ]


def main() -> None:
    for filename in RESEARCH_PAGES:
        insert(SRC / "research" / filename, wrap(research_schema(filename)))
        print(f"updated research/{filename}")
    insert(SRC / "what-we-treat.html", wrap(what_we_treat_schema()))
    print("updated what-we-treat.html")
    insert(SRC / "how-we-work.html", wrap(how_we_work_schema()))
    print("updated how-we-work.html")
    insert(SRC / "online.html", wrap(online_schema()))
    print("updated online.html")


if __name__ == "__main__":
    main()
