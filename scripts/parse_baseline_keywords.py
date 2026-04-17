"""Parse DataForSEO ranked_keywords response and produce a CSV + markdown summary."""
import csv
import json
import sys
from pathlib import Path

INPUT = Path(
    r"C:\Users\zacen\.claude\projects\C--Users-zacen-Python-vibe-coding-functional-patterns-brisbane\e636930d-2f44-40ed-a26f-c385926aeb0a\tool-results\mcp-dataforseo-dataforseo_labs_google_ranked_keywords-1776399453646.txt"
)
OUT_CSV = Path(
    r"C:\Users\zacen\Python\vibe_coding\functional-patterns-brisbane\baseline-keywords-apr2026.csv"
)
OUT_SUMMARY_JSON = Path(
    r"C:\Users\zacen\Python\vibe_coding\functional-patterns-brisbane\scripts\_baseline_summary.json"
)


def main() -> None:
    raw = INPUT.read_text(encoding="utf-8")
    data = json.loads(raw)
    items = data.get("items", [])

    rows = []
    for it in items:
        kd = it.get("keyword_data", {}) or {}
        ki = kd.get("keyword_info", {}) or {}
        rse = it.get("ranked_serp_element", {}) or {}
        si = rse.get("serp_item", {}) or {}
        rc = si.get("rank_changes", {}) or {}

        prev = rc.get("previous_rank_absolute")
        is_new = rc.get("is_new", False)
        is_up = rc.get("is_up", False)
        is_down = rc.get("is_down", False)

        rank_group = si.get("rank_group")
        rank_absolute = si.get("rank_absolute")  # used for change delta vs previous_rank_absolute
        current_for_delta = rank_absolute if rank_absolute is not None else rank_group

        change = ""
        if is_new:
            change = "NEW"
        elif prev is not None and current_for_delta is not None:
            delta = prev - current_for_delta  # positive => improved (lower rank number is better)
            if delta > 0:
                change = f"+{delta}"
            elif delta < 0:
                change = f"{delta}"  # already has minus sign
            else:
                change = "0"
        elif is_up:
            change = "UP"
        elif is_down:
            change = "DOWN"

        rows.append(
            {
                "keyword": kd.get("keyword", ""),
                "rank": rank_group if rank_group is not None else "",
                "search_volume": ki.get("search_volume") or 0,
                "cpc_aud": ki.get("cpc") if ki.get("cpc") is not None else "",
                "competition": ki.get("competition") if ki.get("competition") is not None else "",
                "etv": si.get("etv") if si.get("etv") is not None else 0,
                "landing_url": si.get("relative_url") or si.get("url") or "",
                "previous_rank": prev if prev is not None else "",
                "change": change,
            }
        )

    # Sort by ETV desc
    rows.sort(key=lambda r: (r["etv"] or 0), reverse=True)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "keyword",
                "rank",
                "search_volume",
                "cpc_aud",
                "competition",
                "etv",
                "landing_url",
                "previous_rank",
                "change",
            ],
        )
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # Summary computations
    total = len(rows)
    buckets = {"1": 0, "2-3": 0, "4-10": 0, "11-20": 0, "21-50": 0, "51-100": 0}
    for r in rows:
        rk = r["rank"] if isinstance(r["rank"], int) else None
        if rk is None:
            continue
        if rk == 1:
            buckets["1"] += 1
        elif 2 <= rk <= 3:
            buckets["2-3"] += 1
        elif 4 <= rk <= 10:
            buckets["4-10"] += 1
        elif 11 <= rk <= 20:
            buckets["11-20"] += 1
        elif 21 <= rk <= 50:
            buckets["21-50"] += 1
        elif 51 <= rk <= 100:
            buckets["51-100"] += 1

    total_etv = sum((r["etv"] or 0) for r in rows)

    def path_of(url: str) -> str:
        if not url:
            return ""
        # If it's relative already, keep it; else strip scheme+host
        if url.startswith("/"):
            return url
        idx = url.find("//")
        if idx != -1:
            tail = url[idx + 2 :]
            slash = tail.find("/")
            if slash == -1:
                return "/"
            return tail[slash:]
        return url

    top20 = rows[:20]
    brisbane = [r for r in rows if "brisbane" in (r["keyword"] or "").lower()][:10]
    blog_page_rows = [
        r
        for r in rows
        if path_of(r["landing_url"]).startswith("/blog-page/")
    ]
    blog_page_rows.sort(key=lambda r: (r["etv"] or 0), reverse=True)

    branded_terms = ("fp brisbane", "functional patterns brisbane", "functionalpatternsbrisbane")
    branded = [
        r
        for r in rows
        if any(t in (r["keyword"] or "").lower() for t in branded_terms)
    ]
    branded.sort(key=lambda r: (r["etv"] or 0), reverse=True)

    summary = {
        "total": total,
        "buckets": buckets,
        "total_etv": total_etv,
        "top20": [
            {
                "keyword": r["keyword"],
                "rank": r["rank"],
                "sv": r["search_volume"],
                "etv": r["etv"],
                "path": path_of(r["landing_url"]),
            }
            for r in top20
        ],
        "brisbane": [
            {
                "keyword": r["keyword"],
                "rank": r["rank"],
                "sv": r["search_volume"],
                "etv": r["etv"],
                "path": path_of(r["landing_url"]),
            }
            for r in brisbane
        ],
        "blog_page_count": len(blog_page_rows),
        "blog_page_top5": [
            {
                "keyword": r["keyword"],
                "rank": r["rank"],
                "sv": r["search_volume"],
                "etv": r["etv"],
                "path": path_of(r["landing_url"]),
            }
            for r in blog_page_rows[:5]
        ],
        "branded": [
            {
                "keyword": r["keyword"],
                "rank": r["rank"],
                "sv": r["search_volume"],
                "etv": r["etv"],
                "path": path_of(r["landing_url"]),
            }
            for r in branded
        ],
    }

    OUT_SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote CSV: {OUT_CSV} ({total} rows)")
    print(f"Wrote summary JSON: {OUT_SUMMARY_JSON}")


if __name__ == "__main__":
    main()
