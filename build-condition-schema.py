"""Insert MedicalWebPage + Service + FAQPage JSON-LD schema into the 10
condition pages that are missing it. Reads the page's existing title,
description, canonical URL and FAQ <details> blocks, then inserts the
schema block immediately before </head>. Idempotent via marker comments."""
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent
CONDITIONS = ROOT / "src" / "conditions"

MARKER_START = "<!-- Generated Schema Start -->"
MARKER_END = "<!-- Generated Schema End -->"

# Per-condition medical metadata. Each entry provides the editorial info
# that can't be reliably inferred from the page markup.
CONDITIONS_META = {
    "scoliosis.html": {
        "condition": "Scoliosis",
        "alternate": ["Spinal Curvature", "Lateral Curvature of the Spine"],
        "anatomy": "Spine",
        "mentions": ["Kyphosis", "Lordosis", "Postural Dysfunction"],
        "service_name": "Scoliosis Treatment",
        "service_desc": "Non-surgical scoliosis correction through gait analysis, intra-abdominal pressure training, and corrective biomechanics. Documented Cobb angle reductions without bracing or surgery.",
        "service_type": "Scoliosis Correction",
        "breadcrumb_label": "Straighten Scoliosis",
    },
    "posture-correction.html": {
        "condition": "Poor Posture",
        "alternate": ["Postural Dysfunction", "Forward Head Posture", "Rounded Shoulders"],
        "anatomy": "Spine",
        "mentions": ["Kyphosis", "Forward Head Posture", "Rounded Shoulders"],
        "service_name": "Posture Correction",
        "service_desc": "Biomechanics-based posture correction that addresses the whole-body movement patterns driving postural dysfunction, rather than cueing static positions.",
        "service_type": "Posture Correction",
        "breadcrumb_label": "Transform Posture",
    },
    "joint-pain.html": {
        "condition": "Joint Pain",
        "alternate": ["Hip Pain", "Knee Pain", "Shoulder Pain"],
        "anatomy": "Joints",
        "mentions": ["Hip Osteoarthritis", "Runner's Knee", "Rotator Cuff Pain"],
        "service_name": "Joint Pain Treatment",
        "service_desc": "Gait-based treatment for hip, knee and shoulder pain that targets the movement dysfunctions loading the joint, rather than managing symptoms at the joint itself.",
        "service_type": "Musculoskeletal Treatment",
        "breadcrumb_label": "Fix Joint Pain",
    },
    "gait-running.html": {
        "condition": "Gait Dysfunction",
        "alternate": ["Abnormal Gait", "Running Injuries", "Gait Asymmetry"],
        "anatomy": "Lower Limbs",
        "mentions": ["Runner's Knee", "Plantar Fasciitis", "IT Band Syndrome"],
        "service_name": "Gait Analysis and Running Retraining",
        "service_desc": "Slow-motion 4-angle gait analysis combined with movement-based retraining to resolve running injuries and inefficiencies at the source.",
        "service_type": "Running Gait Analysis",
        "breadcrumb_label": "Improve Gait and Running",
    },
    "hunchback-posture.html": {
        "condition": "Kyphosis",
        "alternate": ["Hunchback Posture", "Dowager's Hump", "Thoracic Kyphosis"],
        "anatomy": "Thoracic Spine",
        "mentions": ["Forward Head Posture", "Rounded Shoulders", "Dowager's Hump"],
        "service_name": "Hunchback Posture Correction",
        "service_desc": "Corrective exercise and biomechanics coaching that restores thoracic spine extension and rib cage position rather than just stretching the upper back.",
        "service_type": "Kyphosis Correction",
        "breadcrumb_label": "Hunchback Posture",
    },
    "winged-scapulas.html": {
        "condition": "Scapular Winging",
        "alternate": ["Winged Scapula", "Scapular Dyskinesis", "Shoulder Blade Protrusion"],
        "anatomy": "Scapula",
        "mentions": ["Rotator Cuff Dysfunction", "Rounded Shoulders", "Thoracic Outlet Syndrome"],
        "service_name": "Scapular Winging Correction",
        "service_desc": "Whole-body biomechanics training that restores scapulothoracic mechanics and the serratus-lat-trap force couple that typical exercises fail to integrate.",
        "service_type": "Shoulder Biomechanics",
        "breadcrumb_label": "Correct Winged Scapulas",
    },
    "athletes.html": {
        "condition": "Athletic Performance Optimisation",
        "alternate": ["Sports Biomechanics", "Athletic Performance"],
        "anatomy": "Musculoskeletal System",
        "mentions": ["Running Injuries", "Explosive Power Development", "Movement Efficiency"],
        "service_name": "Biomechanics for Athletes",
        "service_desc": "Gait-based biomechanics training for athletes targeting injury prevention, force transfer efficiency and movement-based strength development.",
        "service_type": "Sports Performance Training",
        "breadcrumb_label": "Biomechanics for Athletes",
    },
    "fascia.html": {
        "condition": "Fascial Dysfunction and Chronic Fatigue",
        "alternate": ["Myofascial Pain", "Chronic Fatigue", "Fibromyalgia"],
        "anatomy": "Fascia",
        "mentions": ["Chronic Pain", "Ehlers-Danlos Syndrome", "Hypermobility"],
        "service_name": "Fascia and Chronic Conditions Treatment",
        "service_desc": "Movement-based treatment for fascial dysfunction, chronic fatigue and connective-tissue conditions via whole-body gait and posture retraining.",
        "service_type": "Fascial Therapy",
        "breadcrumb_label": "Fascia and Chronic Conditions",
    },
    "diastasis-recti.html": {
        "condition": "Diastasis Recti",
        "alternate": ["Abdominal Separation", "Ab Coning", "Postpartum Abdominal Separation"],
        "anatomy": "Rectus Abdominis",
        "mentions": ["Pelvic Floor Dysfunction", "Postpartum Recovery"],
        "service_name": "Diastasis Recti Treatment",
        "service_desc": "Pre and postnatal biomechanics training that restores transverse abdominis function and intra-abdominal pressure management to close and prevent abdominal coning.",
        "service_type": "Postpartum Biomechanics",
        "breadcrumb_label": "Diastasis Recti and Coning",
    },
    "kids-teens.html": {
        "condition": "Paediatric and Adolescent Biomechanics",
        "alternate": ["Childhood Posture Dysfunction", "Adolescent Scoliosis"],
        "anatomy": "Developing Musculoskeletal System",
        "mentions": ["Scoliosis", "Poor Posture", "Sports Injuries"],
        "service_name": "Kids and Teenagers Biomechanics Training",
        "service_desc": "Age-appropriate gait and posture assessment for children and teenagers to catch developing dysfunctions before they become entrenched adult problems.",
        "service_type": "Paediatric Movement Training",
        "breadcrumb_label": "Kids and Teenagers",
    },
}

BASE_URL = "https://www.functionalpatternsbrisbane.com"


def extract_text(pattern: str, html: str, flags: int = 0) -> str:
    m = re.search(pattern, html, flags)
    if not m:
        raise RuntimeError(f"Pattern not found: {pattern[:50]}")
    return unescape(m.group(1).strip())


def extract_faqs(html: str) -> list[tuple[str, str]]:
    details_blocks = re.findall(
        r'<details class="border[^"]*"[^>]*>(.*?)</details>',
        html,
        re.DOTALL,
    )
    faqs = []
    for block in details_blocks:
        q_match = re.search(
            r'<span class="font-semibold[^"]*"[^>]*>([^<]+)</span>',
            block,
        )
        a_match = re.search(
            r'<div class="details-content[^"]*"[^>]*>\s*<p[^>]*>([^<]+)</p>',
            block,
            re.DOTALL,
        )
        if not (q_match and a_match):
            continue
        faqs.append((unescape(q_match.group(1).strip()), unescape(a_match.group(1).strip())))
    return faqs


def build_schema(filename: str, html: str) -> str:
    meta = CONDITIONS_META[filename]
    slug = filename.removesuffix(".html")
    page_url = f"{BASE_URL}/conditions/{slug}"

    title = extract_text(r"<title>([^<]+)</title>", html)
    desc = extract_text(r'<meta name="description" content="([^"]+)"', html)
    faqs = extract_faqs(html)
    if len(faqs) < 3:
        raise RuntimeError(f"{filename}: expected 3 FAQs, got {len(faqs)}")

    doc = [
        {
            "@context": "https://schema.org",
            "@type": "MedicalWebPage",
            "@id": f"{page_url}#webpage",
            "url": page_url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{BASE_URL}/#website"},
            "about": {
                "@type": "MedicalCondition",
                "name": meta["condition"],
                "alternateName": meta["alternate"],
                "associatedAnatomy": {
                    "@type": "AnatomicalStructure",
                    "name": meta["anatomy"],
                },
            },
            "mentions": [
                {"@type": "MedicalCondition", "name": name}
                for name in meta["mentions"]
            ],
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "What We Treat",
                        "item": f"{BASE_URL}/what-we-treat",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": meta["breadcrumb_label"],
                        "item": page_url,
                    },
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": f"{page_url}#service",
            "name": meta["service_name"],
            "description": meta["service_desc"],
            "url": page_url,
            "provider": {"@id": f"{BASE_URL}/#business"},
            "serviceType": meta["service_type"],
            "category": "Biomechanics & Movement Therapy",
            "areaServed": {"@type": "City", "name": "Brisbane"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": f"{page_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs[:3]
            ],
        },
    ]

    body = json.dumps(doc, indent=2, ensure_ascii=False)
    return f'  {MARKER_START}\n  <script type="application/ld+json">\n{body}\n  </script>\n  {MARKER_END}\n'


def insert(page: Path, schema_block: str) -> None:
    html = page.read_text(encoding="utf-8")
    if MARKER_START in html:
        pattern = re.compile(
            rf"  {re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n",
            re.DOTALL,
        )
        new = pattern.sub(schema_block, html, count=1)
    else:
        if "</head>" not in html:
            raise RuntimeError(f"No </head> in {page.name}")
        new = html.replace("</head>", schema_block + "</head>", 1)
    page.write_text(new, encoding="utf-8")


def main() -> None:
    for filename in CONDITIONS_META:
        page = CONDITIONS / filename
        html = page.read_text(encoding="utf-8")
        block = build_schema(filename, html)
        insert(page, block)
        print(f"updated {filename}")


if __name__ == "__main__":
    main()
