"""Static type checkers behind one interface: what each says about each line.

A checker is asked about a file of `reveal_type(...)` lines and answers, per line,
either the name of the revealed type or that it refused the expression.
The names are reduced to their last dotted segment and joined with `|` in order, so
mypy's `kuchka.quantities.electromagnetics.voltage.Voltage` and pyright's `Voltage`
compare equal.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

CHECKERS = ("mypy", "pyright")


def available(checker: str) -> bool:
    """Return whether `checker` can run here: mypy as a module, pyright as a program."""
    if checker == "mypy":
        return importlib.util.find_spec("mypy") is not None
    return shutil.which("pyright") is not None


def required(checker: str) -> bool:
    """Return whether this environment promises `checker`, so its absence is a failure.

    A tox environment names the checkers it installs in `KUCHKA_CHECKERS`.
    """
    return checker in os.environ.get("KUCHKA_CHECKERS", "").split(",")


def require_or_skip(checker: str) -> None:
    """Skip the test for a missing `checker`, or fail it where one was promised."""
    if available(checker):
        return
    if required(checker):
        pytest.fail(f"{checker} is promised by this environment and is not installed")
    pytest.skip(f"{checker} is not installed")


def _names(revealed: str) -> str:
    parts = re.split(r"\||,", revealed.replace("Union[", "").replace("]", ""))
    return "|".join(sorted({part.strip().split(".")[-1] for part in parts}))


def reveal(checker: str, path: Path) -> dict[int, str | None]:
    """Return per line the revealed type's names, or `None` where it refused."""
    if checker == "mypy":
        return _reveal_with_mypy(path)
    return _reveal_with_pyright(path)


def _reveal_with_mypy(path: Path) -> dict[int, str | None]:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-error-summary", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    verdicts: dict[int, str | None] = {}
    for line in result.stdout.splitlines():
        match = re.match(r".*?:(\d+): (error|note): (.*)", line)
        if match is None:
            continue
        number, kind, message = int(match.group(1)), match.group(2), match.group(3)
        if kind == "error" and "[operator]" in message:
            verdicts[number] = None
        elif number not in verdicts and "Revealed type is" in message:
            verdicts[number] = _names(message.split('"')[1])
    return verdicts


def _reveal_with_pyright(path: Path) -> dict[int, str | None]:
    result = subprocess.run(
        ["pyright", "--outputjson", "--pythonpath", sys.executable, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    verdicts: dict[int, str | None] = {}
    for diagnostic in json.loads(result.stdout)["generalDiagnostics"]:
        number = diagnostic["range"]["start"]["line"] + 1
        if diagnostic["severity"] == "error":
            verdicts[number] = None
        elif number not in verdicts and diagnostic["message"].startswith("Type of"):
            verdicts[number] = _names(diagnostic["message"].rsplit('"', 2)[-2])
    return verdicts
