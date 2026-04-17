"""Blog SEO pass: add condition-specific back-links, clean up doubled title
suffixes, audit missing alt text. Idempotent via marker comments."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BLOGS = ROOT / "src" / "blog-page"

MARKER_START = "<!-- Related Condition Start -->"
MARKER_END = "<!-- Related Condition End -->"

# Map each condition slug to display label and keyword patterns that match its
# topic in a blog slug. Priority matters — earlier entries win over later ones
# so a post like "scoliosis-physio-vs-scoliosis-physiotherapy" doesn't get
# bucketed as generic "chronic-pain" just because it mentions the word back.
CONDITIONS = [
    ("scoliosis", "Scoliosis", ["scoliosis"]),
    ("hunchback-posture", "Hunchback Posture and Kyphosis", [
        "hunchback", "kyphosis", "kyphotic", "dowagers", "neck-hump",
        "buffalo-hump",
    ]),
    ("winged-scapulas", "Winged Scapulas", [
        "scapular", "scapula", "winged", "shoulder-blade", "subscapularis",
    ]),
    ("diastasis-recti", "Diastasis Recti", [
        "diastasis", "coning", "pregnancy", "pre-pregnancy", "post-baby",
        "postpartum",
    ]),
    ("kids-teens", "Kids and Teenagers", ["kids", "teenager", "teen"]),
    ("athletes", "Biomechanics for Athletes", [
        "athlete", "explosive-power", "explosive-leg", "athletic",
    ]),
    ("fascia", "Fascia and Chronic Conditions", [
        "fascia", "fascial", "ehlers-danlos", "eds", "hypermobile",
        "hypermobility", "chronic-fatigue", "double-jointed",
    ]),
    ("gait-running", "Gait and Running", [
        "running", "runners", "run-", "runs-", "gait", "walking", "stride",
        "arm-swing", "foot-fascia",
    ]),
    ("joint-pain", "Joint Pain", [
        "hip", "knee", "shoulder", "joint", "glute", "gluteal", "piriformis",
        "tfl", "tensor-fascia-lata", "groin", "buttocks", "rotator-cuff",
        "hyperextended", "tos",
    ]),
    ("posture-correction", "Posture Correction", [
        "posture", "forward-head", "rounded-shoulders",
    ]),
    ("chronic-pain", "Chronic Pain", [
        "back", "sciatica", "neck", "chronic", "disc", "spine", "spinal",
        "lumbar", "thoracic", "lower-back", "upper-back",
    ]),
]

DEFAULT_CONDITION = ("chronic-pain", "Chronic Pain")


def classify(slug: str) -> tuple[str, str]:
    lowered = slug.lower()
    for cond_slug, label, keywords in CONDITIONS:
        for kw in keywords:
            if kw in lowered:
                return (cond_slug, label)
    return DEFAULT_CONDITION


def build_block(cond_slug: str, cond_label: str) -> str:
    return f'''  {MARKER_START}
  <section class="bg-dark-950 px-4 sm:px-6 lg:px-8 py-12 border-t border-white/5">
    <div class="container-narrow">
      <div class="max-w-2xl mx-auto text-center">
        <p class="text-accent-500 text-xs font-semibold uppercase tracking-[0.2em] mb-3">Need Help With This?</p>
        <a href="/conditions/{cond_slug}" class="inline-flex items-center gap-2 text-white hover:text-accent-500 transition-colors">
          <span class="text-lg font-semibold">Learn how we treat {cond_label} &rarr;</span>
        </a>
      </div>
    </div>
  </section>
  {MARKER_END}
'''


def clean_title(html: str) -> tuple[str, bool]:
    """Collapse repeated brand suffixes in <title> and <meta og:title>."""
    suffixes = [
        " — Functional Patterns Brisbane",
        " | Functional Patterns Brisbane",
        " - Functional Patterns Brisbane",
    ]

    def _strip(match: re.Match) -> str:
        text = match.group(1)
        changed = True
        while changed:
            changed = False
            for suf in suffixes:
                if text.endswith(suf):
                    text = text[: -len(suf)]
                    changed = True
        # Canonical: always end with exactly one em-dash suffix.
        return f'<title>{text.strip()} — Functional Patterns Brisbane</title>'

    new, n = re.subn(r"<title>([^<]+)</title>", _strip, html, count=1)
    if n == 0:
        return html, False

    def _strip_og(match: re.Match) -> str:
        text = match.group(1)
        changed = True
        while changed:
            changed = False
            for suf in suffixes:
                if text.endswith(suf):
                    text = text[: -len(suf)]
                    changed = True
        return f'<meta property="og:title" content="{text.strip()} — Functional Patterns Brisbane">'

    new = re.sub(
        r'<meta property="og:title" content="([^"]+)">',
        _strip_og,
        new,
    )
    return new, new != html


def insert_block(html: str, block: str) -> str:
    if MARKER_START in html:
        return re.sub(
            rf"  {re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n",
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    anchor = "  <!-- CTA -->"
    if anchor not in html:
        return html  # Skip non-standard posts rather than crashing.
    return html.replace(anchor, block + anchor, 1)


def audit_alt(html: str) -> list[str]:
    """Return list of img tags missing meaningful alt text."""
    problems = []
    for m in re.finditer(r"<img\b[^>]*>", html):
        tag = m.group(0)
        alt_match = re.search(r'\balt="([^"]*)"', tag)
        src_match = re.search(r'\bsrc="([^"]+)"', tag)
        src = src_match.group(1) if src_match else "<no src>"
        if not alt_match:
            problems.append(f"MISSING alt: {src}")
        elif alt_match.group(1).strip() == "":
            problems.append(f"EMPTY alt:   {src}")
    return problems


def main() -> None:
    posts = sorted(BLOGS.glob("*.html"))
    stats = {"inserted": 0, "already_had": 0, "no_anchor": 0}
    title_fixes = 0
    alt_report: list[tuple[str, list[str]]] = []
    mapping_report: list[tuple[str, str]] = []

    for post in posts:
        if post.name == "index.html":
            continue

        html = post.read_text(encoding="utf-8")
        slug = post.stem

        # 1. Cleanup doubled title / og:title.
        html, title_changed = clean_title(html)
        if title_changed:
            title_fixes += 1

        # 2. Insert condition-specific back-link block.
        cond_slug, cond_label = classify(slug)
        mapping_report.append((slug, cond_slug))
        had_block = MARKER_START in html
        if "<!-- CTA -->" in html:
            html = insert_block(html, build_block(cond_slug, cond_label))
            if had_block:
                stats["already_had"] += 1
            else:
                stats["inserted"] += 1
        else:
            stats["no_anchor"] += 1

        # 3. Alt text audit — report only.
        problems = audit_alt(html)
        if problems:
            alt_report.append((slug, problems))

        post.write_text(html, encoding="utf-8")

    print("=== Summary ===")
    print(f"Posts processed: {len(posts)-1}")
    print(f"Condition back-link blocks inserted: {stats['inserted']}")
    print(f"Blocks refreshed (already present): {stats['already_had']}")
    print(f"Posts with no CTA anchor — skipped: {stats['no_anchor']}")
    print(f"Titles cleaned: {title_fixes}")

    print()
    print("=== Condition classification counts ===")
    from collections import Counter
    counts = Counter(cond for _, cond in mapping_report)
    for cond, n in counts.most_common():
        print(f"  {cond}: {n}")

    print()
    print(f"=== Alt-text audit: {len(alt_report)} posts have issues ===")
    total_missing = sum(len(p) for _, p in alt_report)
    total_empty = sum(
        sum(1 for pr in p if pr.startswith("EMPTY")) for _, p in alt_report
    )
    print(f"  Total image alt problems: {total_missing}")
    print(f"  (of which EMPTY alt=\"\"): {total_empty}")
    # Write report to file for Zac to review.
    report_path = ROOT / "blog-alt-audit.md"
    with report_path.open("w", encoding="utf-8") as fh:
        fh.write("# Blog image alt-text audit\n\n")
        fh.write(f"{len(alt_report)} posts flagged, {total_missing} image issues total.\n\n")
        for slug, problems in alt_report:
            fh.write(f"## {slug}\n\n")
            for p in problems:
                fh.write(f"- {p}\n")
            fh.write("\n")
    print(f"  Full report written to {report_path.name}")


if __name__ == "__main__":
    main()
