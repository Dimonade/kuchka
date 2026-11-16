"""Print the section of `CHANGELOG.md` that belongs to one version."""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
HEADING = re.compile(r"^## \[(?P<version>[^\]]+)\]")


def section(text: str, version: str) -> str:
    """Return the body of the `## [version]` section, without its heading."""
    lines: list[str] = []
    inside = False
    for line in text.splitlines():
        if match := HEADING.match(line):
            if inside:
                break
            inside = match["version"] == version
        elif inside:
            lines.append(line)
    return "\n".join(lines).strip()


def main(arguments: list[str]) -> int:
    """Write the section of the version named by the only argument."""
    if len(arguments) != 1:
        sys.stderr.write("usage: changelog_section.py VERSION\n")
        return 2
    body = section(CHANGELOG.read_text(encoding="utf-8"), arguments[0])
    if not body:
        sys.stderr.write(f"CHANGELOG.md has no entry for {arguments[0]}\n")
        return 1
    sys.stdout.write(body + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
