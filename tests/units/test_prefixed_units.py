"""Each prefixed unit has the scale its prefix gives it, known independently.

The expected scales are hand-written in `prefix_scales`, relative to a named unit.
That each unit constructor builds values at its unit's scale, for every unit and
magnitude, is covered once for all units in `test_unit_scaling`.
"""

from __future__ import annotations

import functools
import importlib
import pkgutil
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

import kuchka.units as published
from tests.support.families import UNIT_CASES
from tests.units.prefix_scales import PREFIXED_UNIT_SCALES

if TYPE_CHECKING:
    import types

IDS = [f"{module}.{unit}" for module, unit, _, _ in PREFIXED_UNIT_SCALES]


@functools.cache
def _unit_module(name: str) -> types.ModuleType:
    """Return the unit module called `name`, wherever it sits under `kuchka.units`."""
    matches = [
        info.name
        for info in pkgutil.walk_packages(published.__path__, f"{published.__name__}.")
        if info.name.rsplit(".", 1)[-1] == name and ".archaic." not in info.name
    ]
    assert len(matches) == 1, f"{name!r} names {len(matches)} unit modules"
    return importlib.import_module(matches[0])


def lookup(module: str, constant: str):
    """Return the unit constant `constant` of the units module `module`."""
    return getattr(_unit_module(module), constant)


@pytest.mark.parametrize(
    ("module", "unit", "base", "scale"), PREFIXED_UNIT_SCALES, ids=IDS
)
def test_a_prefixed_unit_has_its_known_scale(
    module: str, unit: str, base: str, scale: str
) -> None:
    expected = lookup(module, base).scale * Fraction(Decimal(scale))
    assert lookup(module, unit).scale == expected


@pytest.mark.parametrize(
    ("module", "unit", "base", "scale"), PREFIXED_UNIT_SCALES, ids=IDS
)
def test_the_constructor_of_a_prefixed_unit_builds_that_many_of_its_base(
    module: str, unit: str, base: str, scale: str
) -> None:
    prefixed = next(c for c in UNIT_CASES if c.unit is lookup(module, unit))
    reference = next(
        c
        for c in UNIT_CASES
        if c.unit is lookup(module, base) and c.family is prefixed.family
    )
    assert prefixed.constructor(1) == reference.constructor(Decimal(scale))
