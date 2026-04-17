"""Insert 'Further Reading' section into condition pages linking to top-3 relevant blogs."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
BLOGS = SRC / "blog-page"
CONDITIONS = SRC / "conditions"

MAPPING = {
    "chronic-pain.html": {
        "title": "Chronic Pain",
        "slugs": [
            "what-is-chronic-pain-syndrome",
            "chronic-neck-pain-solutions-that-actually-work",
            "why-your-pain-keeps-coming-back-and-what-to-do-instead",
        ],
    },
    "scoliosis.html": {
        "title": "Scoliosis",
        "slugs": [
            "can-you-naturally-straighten-scoliosis",
            "scoliosis-correction-brisbane-why-intra-abdominal-pressure-changes-everything",
            "unlocking-balanced-movement-a-holistic-approach-to-understanding-and-addressing-scoliosis",
        ],
    },
    "joint-pain.html": {
        "title": "Joint Pain",
        "slugs": [
            "why-your-knees-always-hurt-hip-rotation-gait-cycle-and-knee-pain",
            "why-your-glute-pain-keeps-coming-back-its-not-just-a-pulled-muscle",
            "clicking-snapping-or-dislocated-why-your-hip-stability-isnt-found-in-a-brace",
        ],
    },
    "gait-running.html": {
        "title": "Gait and Running",
        "slugs": [
            "running-gait-analysis-in-brisbane-get-to-the-root-of-your-injuries-and-inefficiencies",
            "why-your-hip-hurts-after-running-7-real-reasons-most-people-miss",
            "running-with-knee-pain-why-your-recovery-is-stalling",
        ],
    },
    "posture-correction.html": {
        "title": "Posture Correction",
        "slugs": [
            "how-to-correct-your-posture-permanently-and-why-most-fixes-dont-last",
            "why-most-posture-exercises-dont-work-amp-what-actually-does",
            "workouts-to-fix-posture-in-brisbane-why-most-dont-work-and-what-actually-does",
        ],
    },
    "winged-scapulas.html": {
        "title": "Winged Scapulas",
        "slugs": [
            "how-to-fix-scapular-winging-typical-exercises-dont-work",
            "why-your-scapulars-stick-out-winged-scapulars-the-thoracic-spine",
            "10-effective-remedies-for-your-aching-scapula-why-your-shoulder-blade-pain-isnt-a-shoulder-problem",
        ],
    },
    "athletes.html": {
        "title": "Athletic Biomechanics",
        "slugs": [
            "explosive-power-is-built-on-mechanics-not-just-intensity",
            "movement-based-strength-training-how-it-differs-from-traditional-strength-programs",
            "mobility-training-that-actually-transfers-to-real-life",
        ],
    },
    "fascia.html": {
        "title": "Fascia and Chronic Conditions",
        "slugs": [
            "the-role-of-fascia-in-chronic-pain-pathways-mechanisms-and-functional-patterns",
            "why-i-stopped-fascia-blasting-amp-fascia-stretching",
            "fascia-amp-chronic-pain-the-cause-amp-the-cure",
        ],
    },
    "hunchback-posture.html": {
        "title": "Hunchback Posture",
        "slugs": [
            "how-to-remove-a-hunchback-and-why-most-advice-gets-it-wrong",
            "beyond-the-hunch-why-most-posture-exercises-fail-to-fix-kyphosis",
            "everything-you-need-to-know-about-kyphosis-and-how-to-fix-it",
        ],
    },
    "diastasis-recti.html": {
        "title": "Diastasis Recti",
        "slugs": [
            "transverse-abdominis-vs-six-pack-abs-why-most-core-training-misses-the-point",
            "the-transverse-abdominis-tva-vs-the-superficial-abs-6-pack-why-its-crucial-to-know-the-difference",
            "preparing-your-body-for-pregnancy-and-life-after-birth-why-the-right-fitness-class-matters",
        ],
    },
    "kids-teens.html": {
        "title": "Kids and Teenagers",
        "slugs": [
            "why-kids-amp-teenagers-should-get-a-gaitrunning-analysis",
            "is-scoliosis-hereditary-what-genetics-can-and-cant-explain",
            "exercises-for-hyperextended-knees-a-guide-to-strength",
        ],
    },
}

MARKER_START = "<!-- Further Reading -->"
MARKER_END = "<!-- /Further Reading -->"


def extract_title(slug: str) -> str:
    path = BLOGS / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        raise RuntimeError(f"No title in {path}")
    title = m.group(1).strip()
    suffixes = [
        " — Functional Patterns Brisbane",
        " | Functional Patterns Brisbane",
        " - Functional Patterns Brisbane",
    ]
    # Strip repeatedly — some titles have the brand suffix twice.
    changed = True
    while changed:
        changed = False
        for suffix in suffixes:
            if title.endswith(suffix):
                title = title[: -len(suffix)].strip()
                changed = True
    return title.rstrip(".")


def build_section(condition_label: str, slugs: list[str]) -> str:
    cards = []
    for slug in slugs:
        title = extract_title(slug)
        cards.append(
            f'''        <a href="/blog-page/{slug}" class="group block p-6 border border-white/10 rounded-lg hover:border-accent-500/40 hover:bg-white/5 transition-all">
          <h3 class="font-semibold text-white text-base mb-3 leading-snug group-hover:text-accent-500 transition-colors">{title}</h3>
          <p class="text-sm text-accent-500 font-semibold">Read article &rarr;</p>
        </a>'''
        )
    cards_html = "\n".join(cards)
    return f'''  {MARKER_START}
  <section class="section-charcoal">
    <div class="container-narrow">
      <div class="max-w-5xl mx-auto">
        <p class="section-label">Further Reading</p>
        <h2 class="text-2xl sm:text-3xl font-bold mb-8">More on {condition_label}</h2>
        <div class="grid md:grid-cols-3 gap-5">
{cards_html}
        </div>
      </div>
    </div>
  </section>
  {MARKER_END}
'''


def insert_into(page: Path, section_html: str) -> None:
    html = page.read_text(encoding="utf-8")
    if MARKER_START in html:
        # Replace existing block so we can safely re-run.
        pattern = re.compile(
            rf"  {re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n",
            re.DOTALL,
        )
        new = pattern.sub(section_html, html, count=1)
    else:
        # Insert just before the CTA section.
        anchor = "  <!-- CTA -->"
        if anchor not in html:
            raise RuntimeError(f"CTA anchor not found in {page.name}")
        new = html.replace(anchor, section_html + anchor, 1)
    page.write_text(new, encoding="utf-8")


def main() -> None:
    for filename, cfg in MAPPING.items():
        section = build_section(cfg["title"], cfg["slugs"])
        insert_into(CONDITIONS / filename, section)
        print(f"updated {filename} with 3 related articles")


if __name__ == "__main__":
    main()
