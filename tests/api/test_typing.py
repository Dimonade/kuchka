"""Confirmation that the static-typing is working.

``tests/typing_fixtures/should_fail.py`` contains a mix of lines that must type-check
cleanly and lines that must be rejected by mypy,
each marked with ``# type: ignore[...]``.
Under ``--strict``, an unused ``type: ignore`` is itself an error --
so a clean mypy run against that fixture is only possible if every marked line actually
produced the expected static error *and* nothing else went wrong.
That is what the mypy test checks.
Pyright is held to the same rule, in strict mode with
``reportUnnecessaryTypeIgnoreComment``, since it honours ``# type: ignore`` comments of
any code.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support import libraries
from tests.support.static_checkers import require_or_skip

_FIXTURES = Path(__file__).parent / "typing_fixtures"
FIXTURES: dict[str, tuple[Path, str | None, tuple[str, ...]]] = {
    "should_fail": (_FIXTURES / "should_fail.py", None, ("mypy", "pyright")),
    "attrs_converter": (_FIXTURES / "attrs_converter.py", None, ("mypy", "pyright")),
    "attrs_named_converter": (
        _FIXTURES / "attrs_named_converter.py",
        "attrs",
        ("mypy", "pyright"),
    ),
    "attrs_fields": (_FIXTURES / "attrs_fields.py", "attrs", ("mypy", "pyright")),
    "pydantic_fields": (
        _FIXTURES / "pydantic_fields.py",
        "pydantic",
        ("mypy", "pyright"),
    ),
}
"""Each fixture, the library it needs installed, and the checkers it is held to."""


def _fixture(name: str) -> Path:
    """Return the path of fixture `name`, skipping or failing for a missing library."""
    path, library, _ = FIXTURES[name]
    if library is not None:
        libraries.require_or_skip(library)
    return path


KNOWN_GAPS: dict[tuple[str, str], str] = {
    ("mypy", "attrs_fields"): (
        "mypy's attrs plugin reads only named functions, types, and lambdas as "
        "converters, so `converter=parse_field(Voltage)` is reported as unsupported "
        "and the `__init__` parameter is `Any`; see the ticket on typing `attrs` "
        "quantity fields. When this test starts to pass, mypy reads such converters: "
        "remove the entry and update docs/concepts/wire_form.md."
    ),
}
"""The fixtures a checker does not hold yet, by (checker, fixture), and why."""


def _for(checker: str) -> list[object]:
    """Return the fixtures that `checker` is held to, a known gap marked `xfail`."""
    params: list[object] = []
    for name, (_, _, checkers) in FIXTURES.items():
        if checker not in checkers:
            continue
        reason = KNOWN_GAPS.get((checker, name))
        marks = [pytest.mark.xfail(strict=True, reason=reason)] if reason else []
        params.append(pytest.param(name, marks=marks))
    return params


@pytest.mark.parametrize("name", _for("mypy"))
def test_mypy_agrees_with_runtime_on_the_fixture(name: str) -> None:
    require_or_skip("mypy")
    fixture = _fixture(name)
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(fixture)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "mypy did not cleanly accept/reject exactly the lines the fixture "
        f"expects it to.\n\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


@pytest.mark.parametrize("name", _for("pyright"))
def test_pyright_agrees_with_runtime_on_the_fixture(name: str, tmp_path: Path) -> None:
    require_or_skip("pyright")
    fixture = _fixture(name)
    shutil.copy(fixture, tmp_path / fixture.name)
    (tmp_path / "pyrightconfig.json").write_text(
        json.dumps(
            {
                "typeCheckingMode": "strict",
                "reportUnnecessaryTypeIgnoreComment": True,
                "enableTypeIgnoreComments": True,
            }
        )
    )
    result = subprocess.run(
        ["pyright", "--pythonpath", sys.executable, fixture.name],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )
    assert result.returncode == 0, (
        "pyright did not cleanly accept/reject exactly the lines the fixture "
        f"expects it to.\n\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
