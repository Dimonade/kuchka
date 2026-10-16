"""Every unit of every linear family scales into the canonical unit exactly.

The cases are the units each published `*_UNITS` table holds, so a unit added to the
library is covered without an edit here.
A unit is where a scale can be wrong, and a conversion is a relabelling that never
computes, so what varies per unit is checked per unit, and what does not vary per unit
is checked once, over all of them, in `test_linear_laws`.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

from tests.support.families import UNIT_CASE_IDS
from tests.support.families import UNIT_CASES
from tests.support.values import BINARY_IMPRECISE_TRIPLES
from tests.support.values import EXTREME_MAGNITUDES

if TYPE_CHECKING:
    from tests.support.families import UnitCase


@pytest.mark.parametrize("case", UNIT_CASES, ids=UNIT_CASE_IDS)
def test_the_constructor_builds_its_type_in_its_unit(case: UnitCase) -> None:
    built = case.constructor(1)
    assert type(built) is case.family.quantity
    assert built.magnitude == case.unit.scale
    # A table derived from another (`SamplingPeriod` from `Time`) builds its values
    # in the canonical unit; a table of its own displays the unit it names.
    assert built.unit in (case.unit, case.family.canonical_unit)


@pytest.mark.parametrize("case", UNIT_CASES, ids=UNIT_CASE_IDS)
def test_the_constructor_applies_the_scale_at_any_magnitude(case: UnitCase) -> None:
    for magnitude in EXTREME_MAGNITUDES:
        built = case.constructor(magnitude)
        assert built.magnitude == Fraction(magnitude) * case.unit.scale, magnitude
        assert built.value_in(case.unit) == Fraction(magnitude), magnitude


@pytest.mark.parametrize("case", UNIT_CASES, ids=UNIT_CASE_IDS)
def test_decimal_sums_stay_exact_where_binary_floats_do_not(case: UnitCase) -> None:
    for a, b, expected in BINARY_IMPRECISE_TRIPLES:
        assert case.constructor(a) + case.constructor(b) == case.constructor(expected)
        assert case.constructor(float(a)) + case.constructor(float(b)) == (
            case.constructor(expected)
        )
        total = case.constructor(a) + case.constructor(b)
        assert total.value_in(case.unit) == Fraction(expected)


@pytest.mark.parametrize("case", UNIT_CASES, ids=UNIT_CASE_IDS)
def test_conversion_relabels_the_display_unit_and_nothing_else(
    case: UnitCase,
) -> None:
    family = case.family
    for magnitude in EXTREME_MAGNITUDES:
        original = family.canonical(magnitude)
        converted = original.to(case.unit)
        assert converted.unit is case.unit, magnitude
        assert converted == original, magnitude
        assert converted.magnitude == original.magnitude, magnitude
        back = converted.to(family.canonical_unit)
        assert back == original, magnitude
        assert back.unit is family.canonical_unit, magnitude
