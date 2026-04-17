"""Insert schema into the programs hub, 6 program subpages, and the team page.
Idempotent via marker comments."""
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
BASE_URL = "https://functional-patterns-brisbane.vercel.app"

MARKER_START = "<!-- Generated Schema Start -->"
MARKER_END = "<!-- Generated Schema End -->"

PROGRAMS = {
    "bells-and-bands.html": {
        "name": "Bells & Bands — Women's Strength Class",
        "desc": "Ladies-only group class at Functional Patterns Brisbane. Core strength and glute activation using dumbbells and resistance bands. Thursdays 10am, Bulimba.",
        "service_type": "Group Fitness Class",
    },
    "rise-and-realign.html": {
        "name": "Rise & Realign",
        "desc": "Morning group program focused on gait mechanics, posture realignment and chronic pain resolution through functional patterns training.",
        "service_type": "Group Biomechanics Program",
    },
    "balance-and-symmetry.html": {
        "name": "Balance & Symmetry 6-Week Program",
        "desc": "Six-week group program correcting left-right asymmetries and movement imbalances through gait-based biomechanics training.",
        "service_type": "Group Biomechanics Program",
    },
    "functional-fundamentals.html": {
        "name": "Functional Fundamentals",
        "desc": "Foundational biomechanics group class teaching the core movement patterns that underpin the Functional Patterns methodology.",
        "service_type": "Group Biomechanics Program",
    },
    "core-and-mobility.html": {
        "name": "Core & Mobility",
        "desc": "Group class targeting functional core activation and whole-body mobility through Functional Patterns movement sequences.",
        "service_type": "Group Biomechanics Program",
    },
    "human-foundations.html": {
        "name": "Human Foundations Course",
        "desc": "Three-day intensive course (9am–3pm) teaching the foundational movements and principles of the Functional Patterns methodology. $1,850 USD.",
        "service_type": "Biomechanics Intensive Course",
    },
}

TEAM = [
    ("Louis Ellery", "Owner, HBS — Functional Patterns Brisbane"),
    ("Skye Ashton", "HBS, HBS1 Certified Biomechanics Specialist"),
    ("Sam Marsh", "HBS, HBS1 Certified Biomechanics Specialist"),
    ("Keriann Zipperer", "HBS, HBS1 Certified. Bachelor of Health Science (Clinical Nutrition)"),
    ("Emmanuel Searty", "Chronic Pain Specialist"),
    ("Harj Sethi", "Practitioner"),
    ("Emma Kopcikas", "Doctorate in Osteopathy. Practitioner"),
    ("Kaan Akkaya", "Practitioner"),
    ("Aman Jagpal", "Practitioner"),
    ("Max Emett", "Practitioner"),
    ("Trent Hill", "Practitioner"),
    ("Pietro Cucinotta", "Online Services Practitioner"),
    ("Gavin O'Neill", "Online Practitioner — Functional Patterns Dublin"),
    ("Steve Zekic", "Online Practitioner — Functional Patterns Sydney"),
]


def extract(pattern: str, html: str) -> str:
    m = re.search(pattern, html)
    if not m:
        raise RuntimeError(f"No match: {pattern[:60]}")
    return unescape(m.group(1).strip())


def wrap_script(doc: list) -> str:
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


def program_schema(filename: str) -> list:
    page = SRC / "programs" / filename
    html = page.read_text(encoding="utf-8")
    meta = PROGRAMS[filename]
    slug = filename.removesuffix(".html")
    url = f"{BASE_URL}/programs/{slug}"
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
                    {"@type": "ListItem", "position": 2, "name": "Group Programs", "item": f"{BASE_URL}/programs"},
                    {"@type": "ListItem", "position": 3, "name": meta["name"], "item": url},
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": f"{url}#service",
            "name": meta["name"],
            "description": meta["desc"],
            "url": url,
            "provider": {"@id": f"{BASE_URL}/#business"},
            "serviceType": meta["service_type"],
            "category": "Biomechanics & Movement Therapy",
            "areaServed": {"@type": "City", "name": "Brisbane"},
        },
    ]


def programs_hub_schema() -> list:
    html = (SRC / "programs.html").read_text(encoding="utf-8")
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    url = f"{BASE_URL}/programs"
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{BASE_URL}/programs/{slug.removesuffix('.html')}",
            "name": meta["name"],
        }
        for i, (slug, meta) in enumerate(PROGRAMS.items())
    ]
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
                    {"@type": "ListItem", "position": 2, "name": "Group Programs", "item": url},
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "@id": f"{url}#program-list",
            "name": "Functional Patterns Brisbane Group Programs",
            "itemListElement": items,
        },
    ]


def team_schema() -> list:
    html = (SRC / "team.html").read_text(encoding="utf-8")
    title = extract(r"<title>([^<]+)</title>", html)
    desc = extract(r'<meta name="description" content="([^"]+)"', html)
    url = f"{BASE_URL}/team"
    people = [
        {
            "@type": "Person",
            "name": name,
            "jobTitle": role,
            "worksFor": {"@id": f"{BASE_URL}/#business"},
        }
        for name, role in TEAM
    ]
    return [
        {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Our Team", "item": url},
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "@id": f"{url}#team-list",
            "name": "Functional Patterns Brisbane Practitioners",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "item": person}
                for i, person in enumerate(people)
            ],
        },
    ]


def main() -> None:
    insert(SRC / "programs.html", wrap_script(programs_hub_schema()))
    print("updated programs.html")
    for filename in PROGRAMS:
        insert(SRC / "programs" / filename, wrap_script(program_schema(filename)))
        print(f"updated programs/{filename}")
    insert(SRC / "team.html", wrap_script(team_schema()))
    print("updated team.html")


if __name__ == "__main__":
    main()
