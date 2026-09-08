"""Conversion invariants, checked once and run against every unit a family registers.

`.to(unit)` never recomputes a magnitude -- it relabels the display unit and keeps the
same canonical-unit value -- so round-tripping through it is exact for every unit a
dimension has, including `Inch`.

`.value_in(unit)` does compute, dividing by that unit's scale, and a property that
divides by the same scale more than once in one computation needs that division to
terminate exactly to compare cleanly;
`Inch`'s scale doesn't, so it sits out those specific properties.

Every test is parametrized over every unit each `*_UNITS` table registers, so a bug
that only shows up at a particular prefix has nowhere to hide.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from hypothesis import given

from tests.quantity_families import ALL_UNIT_CASE_IDS
from tests.quantity_families import ALL_UNIT_CASES
from tests.quantity_families import ALL_UNITDEF_CASES
from tests.quantity_families import BINARY_IMPRECISE_TRIPLES
from tests.quantity_families import EXACT_DIVISION_UNIT_CASE_IDS
from tests.quantity_families import EXACT_DIVISION_UNITDEF_CASES
from tests.quantity_families import EXTREME_MAGNITUDES
from tests.quantity_families import FINITE_DECIMALS
from tests.quantity_families import SCALARS
from tests.quantity_families import scale_by

if TYPE_CHECKING:
    from collections.abc import Callable
    from decimal import Decimal

    from kuchka.numeric import Numeric
    from kuchka.quantities import LinearQuantity
    from kuchka.quantities.base import UnitDef
    from tests.quantity_families import QuantityFamily


@pytest.mark.parametrize(("family", "unit"), ALL_UNITDEF_CASES, ids=ALL_UNIT_CASE_IDS)
@given(a=FINITE_DECIMALS)
def test_converting_and_converting_back_recovers_the_original(
    family: QuantityFamily,
    unit: UnitDef,
    a: Decimal,
) -> None:
    quantity = family.canonical(a)
    round_tripped = quantity.to(unit).to(family.canonical_unit)
    assert round_tripped == quantity
    assert round_tripped.magnitude == quantity.magnitude


@pytest.mark.parametrize(("family", "unit"), ALL_UNITDEF_CASES, ids=ALL_UNIT_CASE_IDS)
@given(a=FINITE_DECIMALS)
def test_conversion_never_changes_the_value_only_the_display(
    family: QuantityFamily,
    unit: UnitDef,
    a: Decimal,
) -> None:
    quantity = family.canonical(a)
    assert quantity.to(unit) == quantity
    assert quantity.to(unit).magnitude == quantity.magnitude


@pytest.mark.parametrize(
    ("family", "unit"),
    EXACT_DIVISION_UNITDEF_CASES,
    ids=EXACT_DIVISION_UNIT_CASE_IDS,
)
@given(a=FINITE_DECIMALS, b=FINITE_DECIMALS)
def test_conversion_commutes_with_addition(
    family: QuantityFamily,
    unit: UnitDef,
    a: Decimal,
    b: Decimal,
) -> None:
    """`convert(a) + convert(b) == convert(a + b)`, checked through `.value_in(...)`.

    Equality between two quantities ignores display unit, so the property is checked
    through `.value_in(...)` instead, which is what actually exercises the conversion
    arithmetic.
    """
    left = family.canonical(a).value_in(unit) + family.canonical(b).value_in(unit)
    right = (family.canonical(a) + family.canonical(b)).value_in(unit)
    assert left == right


@pytest.mark.parametrize(
    ("family", "unit"),
    EXACT_DIVISION_UNITDEF_CASES,
    ids=EXACT_DIVISION_UNIT_CASE_IDS,
)
@given(a=FINITE_DECIMALS, scalar=SCALARS)
def test_conversion_commutes_with_scalar_multiplication(
    family: QuantityFamily,
    unit: UnitDef,
    a: Decimal,
    scalar: int,
) -> None:
    left = family.canonical(a).value_in(unit) * scalar
    right = scale_by(family.canonical(a), scalar).value_in(unit)
    assert left == right


@pytest.mark.parametrize(("family", "unit"), ALL_UNITDEF_CASES, ids=ALL_UNIT_CASE_IDS)
@pytest.mark.parametrize("magnitude", EXTREME_MAGNITUDES, ids=str)
def test_round_trip_conversion_is_exact_at_extreme_magnitudes(
    family: QuantityFamily,
    unit: UnitDef,
    magnitude: Decimal,
) -> None:
    quantity = family.canonical(magnitude)
    round_tripped = quantity.to(unit).to(family.canonical_unit)
    assert round_tripped == quantity
    assert round_tripped.magnitude == magnitude


@pytest.mark.parametrize(
    ("family", "constructor"), ALL_UNIT_CASES, ids=ALL_UNIT_CASE_IDS
)
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    BINARY_IMPRECISE_TRIPLES,
    ids=[f"{a}+{b}={expected}" for a, b, expected in BINARY_IMPRECISE_TRIPLES],
)
def test_decimal_addition_avoids_the_binary_float_rounding_trap(
    family: QuantityFamily,
    constructor: Callable[[Numeric], LinearQuantity],
    a: Decimal,
    b: Decimal,
    expected: Decimal,
) -> None:
    """`0.1 + 0.2 == 0.30000000000000004` in `float`; exactly `0.3` here.

    SI prefixes are powers of ten, exact in `Decimal`, not exact in binary `float`.
    Checked at the canonical unit and at every registered unit a family has, since the
    interesting failure mode would be a prefix constructor that quietly routes through
    `float` on the way to `Decimal`.
    """
    assert family.canonical(a) + family.canonical(b) == family.canonical(expected)
    assert constructor(a) + constructor(b) == constructor(expected)
