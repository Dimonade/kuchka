"""The generated top-level module is current, and its generator behaves.

`kuchka._api` is generated from the leaf modules' `__all__` by `tools/generate_api.py`.
Editing a leaf's `__all__` without regenerating leaves the top level out of step,
which is what the first test catches.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

    import pytest

GENERATOR_PATH = Path(__file__).resolve().parent.parent / "tools" / "generate_api.py"


def _load_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("generate_api", GENERATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = _load_generator()


def test_the_generated_module_is_current() -> None:
    assert generator.TARGET.read_text() == generator.render(), (
        "src/kuchka/_api.py is out of date; run `just generate-api`."
    )


def test_check_mode_succeeds_on_a_current_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "_api.py"
    target.write_text(generator.render())
    monkeypatch.setattr(generator, "TARGET", target)
    assert generator.main(["--check"]) == 0


def test_check_mode_fails_on_a_stale_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = tmp_path / "_api.py"
    target.write_text("__all__ = []\n")
    monkeypatch.setattr(generator, "TARGET", target)
    assert generator.main(["--check"]) == 1
    assert "just generate-api" in capsys.readouterr().err
    assert target.read_text() == "__all__ = []\n"


def test_check_mode_fails_on_a_missing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(generator, "TARGET", tmp_path / "absent.py")
    assert generator.main(["--check"]) == 1


def test_write_mode_produces_the_rendered_text(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "_api.py"
    monkeypatch.setattr(generator, "TARGET", target)
    assert generator.main([]) == 0
    assert target.read_text() == generator.render()


def test_the_generator_promotes_constructors_and_quantity_types_only() -> None:
    quantities, constructors = generator.promoted_names()
    assert "Voltage" in quantities
    assert "Volt" in constructors
    assert not any(name.isupper() for name in constructors)
    assert not set(quantities) & set(constructors)


def test_the_generated_module_lists_each_name_once() -> None:
    quantities, constructors = generator.promoted_names()
    assert len(quantities) == len(set(quantities))
    assert len(constructors) == len(set(constructors))
