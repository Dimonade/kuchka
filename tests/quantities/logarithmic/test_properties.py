"""Properties of levels over a range of values."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from hypothesis import given
from hypothesis import strategies as st

from kuchka import LogarithmicRatio
from kuchka.units import logarithmic

LEVELS = st.decimals(
    allow_nan=False,
    allow_infinity=False,
    min_value=Decimal(-300),
    max_value=Decimal(300),
    places=3,
)


RELATIVE_TOLERANCE = Fraction(1, 10**24)


def _relatively_close(a: Fraction, b: Fraction) -> bool:
    return abs(a - b) <= RELATIVE_TOLERANCE * abs(b)


@given(a=LEVELS, b=LEVELS)
def test_addition_is_commutative(a, b):
    assert logarithmic.Decibel(a) + logarithmic.Decibel(b) == logarithmic.Decibel(
        b
    ) + logarithmic.Decibel(a)


@given(a=LEVELS, b=LEVELS, c=LEVELS)
def test_addition_is_associative(a, b, c):
    left = (logarithmic.Decibel(a) + logarithmic.Decibel(b)) + logarithmic.Decibel(c)
    right = logarithmic.Decibel(a) + (logarithmic.Decibel(b) + logarithmic.Decibel(c))
    assert left == right


@given(a=LEVELS)
def test_zero_is_the_identity_and_negation_the_inverse(a):
    assert logarithmic.Decibel(a) + logarithmic.Decibel(0) == logarithmic.Decibel(a)
    assert logarithmic.Decibel(a) + (-logarithmic.Decibel(a)) == logarithmic.Decibel(0)
    negated = -logarithmic.Decibel(a)
    assert -negated == logarithmic.Decibel(a)


@given(a=LEVELS, b=LEVELS)
def test_adding_levels_multiplies_the_power_ratios(a, b):
    combined = (
        (logarithmic.Decibel(a) + logarithmic.Decibel(b)).to_power_ratio().magnitude
    )
    product = (
        logarithmic.Decibel(a).to_power_ratio().magnitude
        * logarithmic.Decibel(b).to_power_ratio().magnitude
    )
    assert _relatively_close(combined, product)


@given(a=LEVELS, b=LEVELS)
def test_subtracting_levels_divides_the_field_ratios(a, b):
    combined = (
        (logarithmic.Decibel(a) - logarithmic.Decibel(b)).to_field_ratio().magnitude
    )
    quotient = (
        logarithmic.Decibel(a).to_field_ratio().magnitude
        / logarithmic.Decibel(b).to_field_ratio().magnitude
    )
    assert _relatively_close(combined, quotient)


@given(a=LEVELS)
def test_a_level_survives_a_round_trip_through_a_ratio(a):
    level = logarithmic.Decibel(a)
    via_power = LogarithmicRatio.from_power_ratio(level.to_power_ratio())
    via_field = LogarithmicRatio.from_field_ratio(level.to_field_ratio())
    assert abs(via_power.magnitude - level.magnitude) < Fraction(1, 10**20)
    assert abs(via_field.magnitude - level.magnitude) < Fraction(1, 10**20)


@given(a=LEVELS, b=LEVELS)
def test_ordering_of_levels_matches_ordering_of_ratios(a, b):
    if logarithmic.Decibel(a) < logarithmic.Decibel(b):
        assert (
            logarithmic.Decibel(a).to_power_ratio()
            < logarithmic.Decibel(b).to_power_ratio()
        )
    elif logarithmic.Decibel(a) > logarithmic.Decibel(b):
        assert (
            logarithmic.Decibel(a).to_power_ratio()
            > logarithmic.Decibel(b).to_power_ratio()
        )
    else:
        assert (
            logarithmic.Decibel(a).to_power_ratio()
            == logarithmic.Decibel(b).to_power_ratio()
        )


@given(a=LEVELS)
def test_field_ratio_of_a_level_is_the_power_ratio_of_its_half(a):
    assert (
        logarithmic.Decibel(a).to_field_ratio()
        == (logarithmic.Decibel(a) / 2).to_power_ratio()
    )
