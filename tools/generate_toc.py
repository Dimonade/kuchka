"""Generate the table of contents of `README.md`.

The contents list every `##` and `###` heading, linked by the anchor a Markdown
renderer derives from it, between the two TOC markers of the README.
`--check` exits 1 when the contents are out of date instead of rewriting them.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
BLOCK = re.compile(r"(<!-- BEGIN TOC -->\n).*?(<!-- END TOC -->)", re.DOTALL)
HEADING = re.compile(r"(##|###) (.+)")


def contents(text: str) -> str:
    """Return the nested list of links to the `##` and `###` headings after the TOC."""
    lines: list[str] = []
    seen: dict[str, int] = {}
    fenced = False
    for line in text.partition("<!-- END TOC -->")[2].splitlines():
        fenced ^= line.startswith("```")
        if fenced or not (match := HEADING.fullmatch(line)):
            continue
        level, title = match.groups()
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchor = f"{slug}-{count}" if count else slug
        lines.append(f"{'  ' * (len(level) - 2)}- [{title}](#{anchor})")
    return "\n".join(lines) + "\n"


def main() -> int:
    """Rewrite the contents, or with `--check` report whether they are current."""
    text = README.read_text(encoding="utf-8")
    updated = BLOCK.sub(lambda m: f"{m[1]}\n{contents(text)}\n{m[2]}", text)
    if "--check" not in sys.argv:
        README.write_text(updated, encoding="utf-8")
    elif updated != text:
        sys.stderr.write("README.md contents are out of date: `just generate-toc`\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
