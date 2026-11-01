"""A themed unit package imports only the top level and the packages before it."""

from __future__ import annotations

from pathlib import Path

import pytest

import kuchka
from tests.support import layering

UNITS = Path(kuchka.__file__).parent / "units"

RANK = {
    "": 0,
    "temporal": 1,
    "geometry": 1,
    "information": 1,
    "photometry": 2,
    "radiation": 1,
    "thermodynamics": 1,
    "kinematics": 2,
    "mechanics": 3,
    "electromagnetics": 4,
    "chemistry": 4,
}
"""Packages in dependency order; the top level is rank zero.

Two packages of the same rank do not import each other.
"""

LEAVES = layering.leaves(UNITS, skip=frozenset({"archaic"}))


def test_every_package_has_a_rank() -> None:
    packages = {layering.package_of(UNITS, leaf) for leaf in LEAVES}
    assert packages <= RANK.keys(), f"unranked: {sorted(packages - RANK.keys())}"


@pytest.mark.parametrize("leaf", LEAVES, ids=lambda p: str(p.relative_to(UNITS)))
def test_a_leaf_imports_only_earlier_packages_and_its_own(leaf: Path) -> None:
    assert not layering.violations(UNITS, "kuchka.units", RANK, leaf)
