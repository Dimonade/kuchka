"""Confirmation that the static-typing is working.

``tests/typing_fixtures/should_fail.py`` contains a mix of lines that must type-check
cleanly and lines that must be rejected by mypy,
each marked with ``# type: ignore[...]``.
Under ``--strict``, an unused ``type: ignore`` is itself an error --
so a clean mypy run against that fixture is only possible if every marked line actually
produced the expected static error *and* nothing else went wrong.
That is what this test checks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "typing_fixtures" / "should_fail.py"


def _mypy_available() -> bool:
    try:
        import mypy  # noqa: F401
    except ImportError:
        return False
    return True


@pytest.mark.skipif(not _mypy_available(), reason="mypy is not installed")
def test_mypy_agrees_with_runtime_on_the_fixture() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(FIXTURE)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "mypy did not cleanly accept/reject exactly the lines the fixture "
        f"expects it to.\n\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
