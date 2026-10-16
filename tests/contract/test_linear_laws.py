"""The algebraic laws every linear quantity obeys, checked over every family and unit.

Every `LinearQuantity` subclass shares one implementation of addition, negation,
scaling, and conversion, so the laws are not repeated per type: each test draws the
family, or the unit of a family, as part of its generated input.
A law broken by one type or one unit shows up as a falsifying example that names it.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from hypothesis import given
from hypothesis import settings

from tests.support.strategies import FAMILY_STRATEGY
from tests.support.strategies import FINITE_DECIMALS
from tests.support.strategies import NONZERO_SCALARS
from tests.support.strategies import SCALARS
from tests.support.strategies import UNIT_CASE_STRATEGY

if TYPE_CHECKING:
    from kuchka.quantities import LinearQuantity
    from tests.support.families import Family
    from tests.support.families import UnitCase

EVERY_FAMILY = settings(max_examples=1000, deadline=None)
EVERY_UNIT = settings(max_examples=2000, deadline=None)


def scale_by(quantity: LinearQuantity, factor: int) -> LinearQuantity:
    """Multiply by a plain scalar; the result is a quantity of the same type."""
    result = quantity * factor
    assert type(result) is type(quantity)
    return result


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS, b=FINITE_DECIMALS)
def test_addition_is_commutative(family: Family, a: Decimal, b: Decimal) -> None:
    assert family.canonical(a) + family.canonical(b) == family.canonical(
        b
    ) + family.canonical(a)


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS, b=FINITE_DECIMALS, c=FINITE_DECIMALS)
def test_addition_is_associative(
    family: Family, a: Decimal, b: Decimal, c: Decimal
) -> None:
    left = (family.canonical(a) + family.canonical(b)) + family.canonical(c)
    right = family.canonical(a) + (family.canonical(b) + family.canonical(c))
    assert left == right


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS)
def test_zero_is_the_additive_identity(family: Family, a: Decimal) -> None:
    quantity, zero = family.canonical(a), family.canonical(0)
    assert quantity + zero == quantity
    assert zero + quantity == quantity


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS)
def test_a_quantity_and_its_negation_cancel(family: Family, a: Decimal) -> None:
    quantity, zero = family.canonical(a), family.canonical(0)
    assert quantity + -quantity == zero
    assert quantity - quantity == zero
    assert -quantity == family.canonical(-a)


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS)
def test_one_is_the_scalar_identity(family: Family, a: Decimal) -> None:
    quantity = family.canonical(a)
    assert quantity * 1 == quantity
    assert 1 * quantity == quantity


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS, x=SCALARS, y=SCALARS)
def test_scalar_multiplication_is_associative(
    family: Family, a: Decimal, x: int, y: int
) -> None:
    quantity = family.canonical(a)
    assert scale_by(scale_by(quantity, x), y) == scale_by(quantity, x * y)


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS, b=FINITE_DECIMALS, x=SCALARS)
def test_scalar_multiplication_distributes_over_addition(
    family: Family, a: Decimal, b: Decimal, x: int
) -> None:
    both = scale_by(family.canonical(a) + family.canonical(b), x)
    assert both == scale_by(family.canonical(a), x) + scale_by(family.canonical(b), x)


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS, x=NONZERO_SCALARS)
def test_scalar_multiplication_and_division_are_inverses(
    family: Family, a: Decimal, x: int
) -> None:
    quantity = family.canonical(a)
    assert scale_by(quantity, x) / x == quantity


@EVERY_FAMILY
@given(family=FAMILY_STRATEGY, a=FINITE_DECIMALS)
def test_a_negative_magnitude_is_a_quantity_and_signed_zero_is_zero(
    family: Family, a: Decimal
) -> None:
    negative = family.canonical(-abs(a) - 1)
    assert negative.magnitude < 0
    assert negative == -family.canonical(abs(a) + 1)
    assert family.canonical(Decimal(0)) == family.canonical(Decimal("-0"))


@EVERY_UNIT
@given(case=UNIT_CASE_STRATEGY, a=FINITE_DECIMALS)
def test_conversion_round_trips_and_never_changes_the_value(
    case: UnitCase, a: Decimal
) -> None:
    family = case.family
    quantity = family.canonical(a)
    converted = quantity.to(case.unit)
    assert converted == quantity
    assert converted.magnitude == quantity.magnitude
    assert converted.to(family.canonical_unit) == quantity


@EVERY_UNIT
@given(case=UNIT_CASE_STRATEGY, a=FINITE_DECIMALS, b=FINITE_DECIMALS)
def test_conversion_commutes_with_addition(
    case: UnitCase, a: Decimal, b: Decimal
) -> None:
    canonical = case.family.canonical
    separately = canonical(a).value_in(case.unit) + canonical(b).value_in(case.unit)
    together = (canonical(a) + canonical(b)).value_in(case.unit)
    assert separately == together


@EVERY_UNIT
@given(case=UNIT_CASE_STRATEGY, a=FINITE_DECIMALS, x=SCALARS)
def test_conversion_commutes_with_scalar_multiplication(
    case: UnitCase, a: Decimal, x: int
) -> None:
    canonical = case.family.canonical
    assert canonical(a).value_in(case.unit) * x == scale_by(canonical(a), x).value_in(
        case.unit
    )
