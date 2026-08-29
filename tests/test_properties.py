"""Algebraic and numeric invariants, checked once and run against every quantity family.

Every `LinearQuantity` subclass (`Voltage`, `Current`, `Time`, `Length`, ...) obeys the
same small set of laws:
    - addition is commutative and associative,
    - zero is an additive identity,
    - scalar multiplication distributes over addition, and
    - none of that degrades into the binary-float `0.1 + 0.2 != 0.3` surprise `Decimal`
        exists to avoid.

Every test here is parametrized over every registered linear quantity and, where the
property spans a range of magnitudes, driven by Hypothesis.

Only the canonical constructor for each family is used: conversion-specific properties,
run against every unit a family has, live alongside this module in their own tests.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from hypothesis import given
from tests.quantity_families import BINARY_IMPRECISE_TRIPLES
from tests.quantity_families import EXTREME_MAGNITUDES
from tests.quantity_families import FAMILIES
from tests.quantity_families import FAMILY_IDS
from tests.quantity_families import FINITE_DECIMALS
from tests.quantity_families import NONZERO_SCALARS
from tests.quantity_families import SCALARS
from tests.quantity_families import scale_by

if TYPE_CHECKING:
    from tests.quantity_families import QuantityFamily

pytestmark = pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)


# Addition:
#   - commutative,
#   - associative,
#   - has an identity,
#   - has an inverse.


@given(a=FINITE_DECIMALS, b=FINITE_DECIMALS)
def test_addition_is_commutative(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
) -> None:
    forward = family.canonical(a) + family.canonical(b)
    backward = family.canonical(b) + family.canonical(a)
    assert forward == backward


@given(a=FINITE_DECIMALS, b=FINITE_DECIMALS, c=FINITE_DECIMALS)
def test_addition_is_associative(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
    c: Decimal,
) -> None:
    left = (family.canonical(a) + family.canonical(b)) + family.canonical(c)
    right = family.canonical(a) + (family.canonical(b) + family.canonical(c))
    assert left == right


@given(a=FINITE_DECIMALS)
def test_zero_is_the_additive_identity(family: QuantityFamily, a: Decimal) -> None:
    quantity = family.canonical(a)
    zero = family.canonical(0)
    assert quantity + zero == quantity
    assert zero + quantity == quantity


@given(a=FINITE_DECIMALS)
def test_a_quantity_and_its_negation_sum_to_zero(
    family: QuantityFamily,
    a: Decimal,
) -> None:
    assert family.canonical(a) + -family.canonical(a) == family.canonical(0)
    assert family.canonical(a) - family.canonical(a) == family.canonical(0)


@given(a=FINITE_DECIMALS)
def test_negation_matches_negating_the_input(
    family: QuantityFamily,
    a: Decimal,
) -> None:
    assert -family.canonical(a) == family.canonical(-a)


# Scalar multiplication:
#   - identity,
#   - associative,
#   - distributes over addition.


@given(a=FINITE_DECIMALS)
def test_one_is_the_multiplicative_identity(family: QuantityFamily, a: Decimal) -> None:
    quantity = family.canonical(a)
    assert quantity * 1 == quantity
    assert 1 * quantity == quantity


@given(a=FINITE_DECIMALS, scalar_a=SCALARS, scalar_b=SCALARS)
def test_scalar_multiplication_is_associative(
    family: QuantityFamily,
    a: Decimal,
    scalar_a: int,
    scalar_b: int,
) -> None:
    quantity = family.canonical(a)
    assert (quantity * scalar_a) * scalar_b == quantity * (scalar_a * scalar_b)


@given(a=FINITE_DECIMALS, b=FINITE_DECIMALS, scalar=SCALARS)
def test_scalar_multiplication_distributes_over_addition(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
    scalar: int,
) -> None:
    left = scale_by(family.canonical(a) + family.canonical(b), scalar)
    right_a = scale_by(family.canonical(a), scalar)
    right_b = scale_by(family.canonical(b), scalar)
    assert left == right_a + right_b


@given(a=FINITE_DECIMALS, scalar=NONZERO_SCALARS)
def test_scalar_multiplication_and_division_are_inverses(
    family: QuantityFamily,
    a: Decimal,
    scalar: int,
) -> None:
    quantity = family.canonical(a)
    assert scale_by(quantity, scalar) / scalar == quantity


# Binary to Decimal bug/trap case: `0.1 + 0.2` on the canonical unit.


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    BINARY_IMPRECISE_TRIPLES,
    ids=[f"{a}+{b}={expected}" for a, b, expected in BINARY_IMPRECISE_TRIPLES],
)
def test_float_literals_are_parsed_as_typed_not_as_binary_floats(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
    expected: Decimal,
) -> None:
    """A `float` literal path to the same trap, checked through `Decimal` construction.

    `Volt(0.1) + Volt(0.2) == Volt(0.3)` holds because float construction routes
    through `str()` first, preserving the digits as typed.
    """
    forward = family.canonical(float(a)) + family.canonical(float(b))
    assert forward == family.canonical(expected)


# Zero, negatives, and signed zero.


def test_positive_and_negative_zero_construct_equal_quantities(
    family: QuantityFamily,
) -> None:
    assert family.canonical(Decimal(0)) == family.canonical(Decimal("-0"))


@given(a=FINITE_DECIMALS)
def test_a_negative_magnitude_is_a_valid_quantity(
    family: QuantityFamily,
    a: Decimal,
) -> None:
    """A quantity's magnitude carries its own sign; construction accepts either."""
    negative = family.canonical(-abs(a) - 1)
    assert negative.magnitude < 0
    assert negative == -family.canonical(abs(a) + 1)


# Huge and tiny exponents.


@pytest.mark.parametrize("magnitude", EXTREME_MAGNITUDES, ids=str)
def test_construction_is_exact_at_extreme_magnitudes(
    family: QuantityFamily,
    magnitude: Decimal,
) -> None:
    assert family.canonical(magnitude).magnitude == magnitude
