"""A themed unit package imports only the top level and the packages before it."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import kuchka

UNITS = Path(kuchka.__file__).parent / "units"

RANK = {
    "": 0,
    "temporal": 1,
    "geometry": 1,
    "information": 1,
    "radiation": 1,
    "kinematics": 2,
    "mechanics": 3,
    "electromagnetics": 4,
}
"""Packages in dependency order; the top level is rank zero.

Two packages of the same rank do not import each other.
"""


def _package_of(path: Path) -> str:
    relative = path.relative_to(UNITS)
    return relative.parts[0] if len(relative.parts) > 1 else ""


def _imported_packages(path: Path) -> set[str]:
    """Return the packages a module imports from, the empty string for the top level."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.ImportFrom) or node.module is None:
            continue
        parts = node.module.split(".")
        if parts[:2] != ["kuchka", "units"]:
            continue
        names = [alias.name for alias in node.names] if parts[2:] == [] else parts[2:3]
        found.update(name if name in RANK else "" for name in names)
    return found


LEAVES = sorted(
    path
    for path in UNITS.rglob("*.py")
    if path.name != "__init__.py" and "archaic" not in path.relative_to(UNITS).parts
)


def test_every_package_has_a_rank() -> None:
    packages = {_package_of(path) for path in LEAVES}
    assert packages <= RANK.keys(), f"unranked: {sorted(packages - RANK.keys())}"


@pytest.mark.parametrize("leaf", LEAVES, ids=lambda p: str(p.relative_to(UNITS)))
def test_a_leaf_imports_only_earlier_packages_and_its_own(leaf: Path) -> None:
    own = _package_of(leaf)
    for imported in _imported_packages(leaf):
        assert imported == own or RANK[imported] < RANK[own], (
            f"{leaf.relative_to(UNITS)} imports from {imported or 'the top level'}, "
            f"which does not come before {own or 'the top level'}"
        )
