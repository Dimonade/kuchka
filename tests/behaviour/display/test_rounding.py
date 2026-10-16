"""Rounding is half away from zero, applied once."""

from __future__ import annotations

import decimal
from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka.internal.display import DISPLAY_ROUNDING
from kuchka.units import voltage


def test_the_display_rounding_mode_is_half_up() -> None:
    assert DISPLAY_ROUNDING == decimal.ROUND_HALF_UP


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        ("2.675", "2.68 V"),
        ("2.665", "2.67 V"),
        ("0.125", "0.13 V"),
        ("-2.675", "-2.68 V"),
        ("-2.665", "-2.67 V"),
        ("-0.125", "-0.13 V"),
    ],
)
def test_a_tie_rounds_away_from_zero(literal: str, expected: str) -> None:
    assert f"{voltage.Volt(Decimal(literal)):.2f}" == expected


def test_a_value_just_below_a_tie_rounds_down() -> None:
    value = voltage.Volt(Fraction(1, 8) - Fraction(1, 10**40))
    assert f"{value:.2f}" == "0.12 V"


def test_a_value_just_above_a_tie_rounds_up() -> None:
    value = voltage.Volt(Fraction(1, 8) + Fraction(1, 10**40))
    assert f"{value:.2f}" == "0.13 V"


def test_a_value_just_below_a_tie_of_the_negative_side_rounds_toward_zero() -> None:
    value = voltage.Volt(-(Fraction(1, 8) - Fraction(1, 10**40)))
    assert f"{value:.2f}" == "-0.12 V"


def test_rounding_to_the_display_digits_happens_once() -> None:
    # 0.5 - 10**-40 rounds to 0.5000000000000000000000000000 at 28 digits, a value
    # that then looks like a tie at one place.
    below = voltage.Volt(Fraction(1, 2) - Fraction(1, 10**40))
    assert f"{below:.0f}" == "0 V"
    assert f"{voltage.Volt(Fraction(1, 2)):.0f}" == "1 V"
