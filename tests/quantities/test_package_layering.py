"""A themed quantity package imports only the top level and the packages before it.

Only imports that run when the module is imported count.
An overload may name any type, because a type checker reads it and nothing runs it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import kuchka
from tests.support import layering

QUANTITIES = Path(kuchka.__file__).parent / "quantities"

RANK = {
    "": 0,
    "geometry": 1,
    "information": 1,
    "photometry": 1,
    "radiation": 5,
    "thermodynamics": 1,
    "kinematics": 2,
    "mechanics": 3,
    "electromagnetics": 4,
    "chemistry": 4,
}
"""Packages in dependency order; the top level is rank zero, `base` included."""

LEAVES = layering.leaves(QUANTITIES)


def test_every_package_has_a_rank() -> None:
    packages = {layering.package_of(QUANTITIES, leaf) for leaf in LEAVES}
    assert packages <= RANK.keys() | {"base"}, f"unranked: {sorted(packages)}"


@pytest.mark.parametrize(
    "leaf",
    [leaf for leaf in LEAVES if layering.package_of(QUANTITIES, leaf) != "base"],
    ids=lambda p: str(p.relative_to(QUANTITIES)),
)
def test_a_leaf_imports_only_earlier_packages_and_its_own(leaf: Path) -> None:
    assert not layering.violations(QUANTITIES, "kuchka.quantities", RANK, leaf)
