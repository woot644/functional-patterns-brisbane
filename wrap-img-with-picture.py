"""Wrap <img src="...jpg|png"> tags in <picture> with a WebP <source>.

Idempotent: skips any <img> already wrapped by an adjacent <picture>/<source>.
Preserves all attributes on the original <img>. Processes all .html files in
src/ recursively.

Before:
    <img src="images/foo.jpg" alt="..." class="...">
After:
    <picture><source type="image/webp" srcset="images/foo.webp"><img src="images/foo.jpg" alt="..." class="..."></picture>
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent / "src"

# Match <img ... src="...jpg|jpeg|png" ...> on a single line. Captures the
# entire tag and the src path. Non-greedy to avoid swallowing multiple tags.
IMG_RE = re.compile(
    r'<img\b([^>]*?)\bsrc="([^"]+?\.(?:jpg|jpeg|png))"([^>]*?)\s*/?>',
    re.IGNORECASE,
)


def wrap_img(match: re.Match[str], already_wrapped_spans: set[int]) -> str:
    start = match.start()
    if start in already_wrapped_spans:
        return match.group(0)

    pre_attrs = match.group(1)
    src_path = match.group(2)
    post_attrs = match.group(3)
    webp_path = re.sub(r"\.(jpg|jpeg|png)$", ".webp", src_path, flags=re.IGNORECASE)

    # Reassemble the <img> tag as-is (preserving original attributes) then
    # wrap it in <picture>.
    original_img = f'<img{pre_attrs}src="{src_path}"{post_attrs}>'
    return (
        f'<picture><source type="image/webp" srcset="{webp_path}">'
        f'{original_img}</picture>'
    )


def find_already_wrapped(content: str) -> set[int]:
    """Return the start positions of <img> tags that are already inside <picture>."""
    wrapped: set[int] = set()
    for m in re.finditer(
        r'<picture>\s*<source type="image/webp" srcset="[^"]+">\s*(<img\b)',
        content,
        re.IGNORECASE,
    ):
        wrapped.add(m.start(1))
    return wrapped


def process(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    wrapped_positions = find_already_wrapped(content)

    replacements = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal replacements
        if match.start() in wrapped_positions:
            return match.group(0)
        replacements += 1
        return wrap_img(match, wrapped_positions)

    new_content = IMG_RE.sub(_sub, content)

    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
    return replacements


def main() -> None:
    html_files = sorted(ROOT.rglob("*.html"))
    total = 0
    files_changed = 0
    for path in html_files:
        n = process(path)
        if n:
            files_changed += 1
            total += n
            print(f"  {path.relative_to(ROOT)}: wrapped {n} img tag(s)")
    print()
    print(f"Files changed: {files_changed}, img tags wrapped: {total}")


if __name__ == "__main__":
    main()
