"""Algebraic and numeric invariants, run against every quantity family.

Every `LinearQuantity` subclass (`Voltage`, `Current`, `Time`, `Length`, ...)
is supposed to obey the same small set of laws:
    - addition is commutative and associative,
    - zero is an additive identity,
    - scalar multiplication distributes over addition,
    - conversion round-trips and commutes with addition and scalar multiplication,
    - none of the above should ever degrade into the binary-float `0.1 + 0.2 != 0.3`
        surprise `Decimal` exists to avoid (see `numeric.py`).

Every test is parametrized over `quantity_families.FAMILIES` and, where the property is
about a range of magnitudes, driven by Hypothesis.

NOTE: `Temperature` (affine, not linear -- see `kuchka.temperature`) and `Inch`
(the one unit in this library whose scale is not a power of ten, so its
`.value_in(...)` is not always an exact decimal division) are deliberately outside this
module's scope; see `test_temperature.py` and `test_length.py` for why they get their
own, narrower treatment instead.
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


# Conversion:
#   - round-trips,
#   - commutes with addition and scalar multiplication.


@given(a=FINITE_DECIMALS)
def test_converting_and_converting_back_recovers_the_original(
    family: QuantityFamily,
    a: Decimal,
) -> None:
    quantity = family.canonical(a)
    round_tripped = quantity.to(family.alt_unit).to(family.canonical_unit)
    assert round_tripped == quantity
    assert round_tripped.magnitude == quantity.magnitude


@given(a=FINITE_DECIMALS)
def test_conversion_never_changes_the_value_only_the_display(
    family: QuantityFamily,
    a: Decimal,
) -> None:
    quantity = family.canonical(a)
    assert quantity.to(family.alt_unit) == quantity
    assert quantity.to(family.alt_unit).magnitude == quantity.magnitude


@given(a=FINITE_DECIMALS, b=FINITE_DECIMALS)
def test_conversion_commutes_with_addition(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
) -> None:
    """`convert(a) + convert(b) == convert(a + b)`, checked through `.value_in(...)`.

    NOTE: `==` between two quantities ignores display unit (see
    `LinearQuantity.__eq__`), so this has to be asked through `.value_in(...)`
    to actually exercise the conversion arithmetic.
    """
    left = family.canonical(a).value_in(family.alt_unit) + family.canonical(b).value_in(
        family.alt_unit,
    )
    right = (family.canonical(a) + family.canonical(b)).value_in(family.alt_unit)
    assert left == right


@given(a=FINITE_DECIMALS, scalar=SCALARS)
def test_conversion_commutes_with_scalar_multiplication(
    family: QuantityFamily,
    a: Decimal,
    scalar: int,
) -> None:
    left = family.canonical(a).value_in(family.alt_unit) * scalar
    right = scale_by(family.canonical(a), scalar).value_in(family.alt_unit)
    assert left == right


# Binary to Decimal bug/trap case: `0.1 + 0.2`.


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    BINARY_IMPRECISE_TRIPLES,
    ids=[f"{a}+{b}={expected}" for a, b, expected in BINARY_IMPRECISE_TRIPLES],
)
def test_decimal_addition_avoids_the_binary_float_rounding_trap(
    family: QuantityFamily,
    a: Decimal,
    b: Decimal,
    expected: Decimal,
) -> None:
    """`0.1 + 0.2 == 0.30000000000000004` in `float`.

    This is the whole reason `numeric.py` exists: SI prefixes are powers of ten,
    exact in `Decimal`, not exact in binary `float`.

    Run at both the canonical unit and the alt prefix, since the interesting failure
    mode would be a prefix constructor that quietly routes through `float` on the way
    to `Decimal`.
    """
    assert family.canonical(a) + family.canonical(b) == family.canonical(expected)
    assert family.alt(a) + family.alt(b) == family.alt(expected)


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
    """The same trap, entered through a `float` literal instead of a `Decimal`.

    `to_decimal` routes `float` through `str()` first specifically so that
    `Volt(0.1) + Volt(0.2) == Volt(0.3)` holds even though the underlying Python floats
    do not.
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
    """Construction places no domain restriction on sign; see test_construction.py."""
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


@pytest.mark.parametrize("magnitude", EXTREME_MAGNITUDES, ids=str)
def test_round_trip_conversion_is_exact_at_extreme_magnitudes(
    family: QuantityFamily,
    magnitude: Decimal,
) -> None:
    quantity = family.canonical(magnitude)
    round_tripped = quantity.to(family.alt_unit).to(family.canonical_unit)
    assert round_tripped == quantity
    assert round_tripped.magnitude == magnitude
