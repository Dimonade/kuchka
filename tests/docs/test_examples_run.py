"""The demo of every worked example runs to the end.

The tests next to each example check its functions, and `test_documentation.py` runs
the code in the prose.
Nothing else runs `demo.py`, the script a reader is told to run, so it could stop
working while every test stayed green.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parents[2] / "docs" / "examples"
DEMOS = sorted(EXAMPLES.glob("*/demo.py"))
TIMEOUT_SECONDS = 60


def test_there_are_demos_to_run() -> None:
    assert DEMOS


@pytest.mark.parametrize(
    "demo",
    DEMOS,
    ids=[str(demo.parent.name) for demo in DEMOS],
)
def test_the_demo_runs_to_the_end(demo: Path) -> None:
    # The scripts say to run them from their own directory, so that is where they run.
    result = subprocess.run(
        [sys.executable, demo.name],
        cwd=demo.parent,
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
        timeout=TIMEOUT_SECONDS,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip()
