"""Check that the repository is ready to be released as the version it declares.

The checks are the ones of the release checklist that a machine can make: the version
is bumped and agrees everywhere, the changelog has a dated entry for it, and PyPI does
not have it yet.
Everything else of the checklist (the tests, the linters, the doctests, the examples,
the tox environments) is run by the CI.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "kuchka"
INDEX_URL = f"https://pypi.org/pypi/{PACKAGE}/json"
RC_PREFIX = "rc/"
ATTEMPTS = 3
RETRY_SECONDS = 5
TIMEOUT_SECONDS = 20

VERSION = re.compile(
    r"^(?P<release>\d+(?:\.\d+)*)"
    r"(?:(?P<pre>(?:a|b|rc)\d+))?"
    r"(?:\.post\d+)?"
    r"(?:\.dev\d+)?$"
)
FINAL = re.compile(r"^\d+(?:\.\d+)*$")
HEADING = re.compile(r"^## \[(?P<version>[^\]]+)\](?: - (?P<label>.*))?$")


def release_numbers(version: str) -> tuple[int, ...]:
    """Return the numbers of a final version, so that versions can be ordered."""
    return tuple(int(part) for part in version.split("."))


def declared_version() -> str:
    """Return the version declared in `pyproject.toml`."""
    with (REPOSITORY_ROOT / "pyproject.toml").open("rb") as handle:
        return str(tomllib.load(handle)["project"]["version"])


def locked_version() -> str | None:
    """Return the version of the project that `uv.lock` holds, if it holds one."""
    with (REPOSITORY_ROOT / "uv.lock").open("rb") as handle:
        packages = tomllib.load(handle)["package"]
    for package in packages:
        if package["name"] == PACKAGE:
            return str(package["version"])
    return None


def changelog_sections() -> list[tuple[str, str, str]]:
    """Return the `(version, label, body)` of each section, newest first."""
    text = (REPOSITORY_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    sections: list[tuple[str, str, list[str]]] = []
    for line in text.splitlines():
        if match := HEADING.match(line):
            sections.append((match["version"], match["label"] or "", []))
        elif sections:
            sections[-1][2].append(line)
    return [
        (version, label, "\n".join(body).strip()) for version, label, body in sections
    ]


def published_versions() -> list[str]:
    """Return the versions that the index lists, or raise `OSError`."""
    last_error: Exception | None = None
    for attempt in range(ATTEMPTS):
        if attempt:
            time.sleep(RETRY_SECONDS)
        try:
            # The URL is the fixed https address of the index.
            with urllib.request.urlopen(INDEX_URL, timeout=TIMEOUT_SECONDS) as response:
                return list(json.load(response)["releases"])
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            last_error = error
    message = f"could not read {INDEX_URL}: {last_error}"
    raise OSError(message)


def check_changelog(version: str, *, final: bool, today: dt.date) -> list[str]:
    """Return the problems of the changelog entry for `version`."""
    sections = changelog_sections()
    wanted = VERSION.fullmatch(version)
    base = wanted["release"] if wanted else version
    target = version if final else base
    matching = [section for section in sections if section[0] == target]
    if not matching:
        return [f"CHANGELOG.md has no `## [{target}]` section"]
    _, label, body = matching[0]
    problems = []
    if not body:
        problems.append(f"the CHANGELOG.md section of {target} is empty")
    if not final:
        return problems
    if sections[0][0] != version:
        problems.append(
            f"the newest CHANGELOG.md section is {sections[0][0]}, not {version}"
        )
    try:
        released = dt.date.fromisoformat(label.strip())
    except ValueError:
        problems.append(
            f"the CHANGELOG.md heading of {version} must end in ` - YYYY-MM-DD`,"
            f" not {label!r}"
        )
    else:
        if released > today + dt.timedelta(days=1):
            problems.append(
                f"the release date {released} of {version} is in the future"
            )
    return problems


def check_version(
    version: str, *, final: bool, published: list[str] | None
) -> list[str]:
    """Return the problems of the version, against the files and the index."""
    problems = []
    if not VERSION.fullmatch(version):
        problems.append(f"{version!r} is not a version this check understands")
    if final and not FINAL.fullmatch(version):
        problems.append(f"{version} is not a final version, and a final one is due")
    locked = locked_version()
    if locked != version:
        problems.append(
            f"uv.lock holds {PACKAGE} {locked}, not {version}; run `uv lock`"
        )
    if published is None:
        return problems
    if version in published:
        problems.append(f"{version} is already on PyPI, and a file cannot be replaced")
    if final and FINAL.fullmatch(version):
        newer = [
            other
            for other in published
            if FINAL.fullmatch(other)
            and release_numbers(other) > release_numbers(version)
        ]
        if newer:
            problems.append(f"PyPI already has {max(newer, key=release_numbers)}")
    return problems


def main(arguments: list[str]) -> int:
    """Run the checks and report each problem."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--final",
        action="store_true",
        help="A final release is due: the version is final, newest, and dated.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Do not ask PyPI which versions it has.",
    )
    parser.add_argument(
        "--branch",
        help="The branch to merge; `rc/X.Y.Z` must carry the version X.Y.Z.",
    )
    parsed = parser.parse_args(arguments)

    version = declared_version()
    published: list[str] | None = None
    problems: list[str] = []
    if parsed.branch and parsed.branch.startswith(RC_PREFIX):
        named = parsed.branch.removeprefix(RC_PREFIX)
        if named != version:
            problems.append(
                f"the branch {parsed.branch} is for {named}, not for {version}"
            )
    if not parsed.offline:
        try:
            published = published_versions()
        except OSError as error:
            problems.append(str(error))

    problems += check_version(version, final=parsed.final, published=published)
    problems += check_changelog(
        version,
        final=parsed.final,
        today=dt.datetime.now(tz=dt.UTC).date(),
    )

    for problem in problems:
        sys.stderr.write(f"FAILED: {problem}\n")
    if problems:
        return 1
    sys.stdout.write(f"{PACKAGE} {version} is ready to be released.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
