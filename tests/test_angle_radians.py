"""Radian is the one angular unit tied to a turn by an irrational number.

A turn is two pi radians, so a radian scale needs pi.
kuchka holds pi as an exact rational to 100 decimal places and uses it for the
`Radian` scale alone.
Every other angular unit is a plain fraction of a turn.
A value built in radians gives back exactly what was put in, and converts to the other
units with an error below one part in 1E+100.
A radian value computed in floating point is a rounded approximation of an angle and
does not equal the same angle in degrees; `Angle.is_close` compares those.
"""

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

from kuchka import Degree
from kuchka import Gradian
from kuchka import Radian
from kuchka import Turn
from kuchka.internal.constants import PI
from kuchka.numeric import to_exact
from kuchka.units import ARCSECOND
from kuchka.units import DEGREE
from kuchka.units import RADIAN

if TYPE_CHECKING:
    from kuchka.numeric import Numeric

PRECISION = Fraction(1, 10**98)
"""Two digits looser than the 100 decimals of `PI`, to leave rounding headroom."""


def _true_pi(decimals: int) -> Fraction:
    """Pi from Machin's formula, in integer arithmetic, independent of `PI`."""

    def arctan_of_inverse(x: int, unity: int) -> int:
        total = term = unity // x
        x_squared = x * x
        n = 1
        sign = -1
        while term:
            term //= x_squared
            n += 2
            total += sign * (term // n)
            sign = -sign
        return total

    unity = 10 ** (decimals + 10)
    pi = 4 * (4 * arctan_of_inverse(5, unity) - arctan_of_inverse(239, unity))
    return Fraction(pi, unity)


TRUE_PI = _true_pi(130)


# The pi constant.


def test_pi_is_correct_to_one_hundred_decimals() -> None:
    assert abs(PI - TRUE_PI) < Fraction(1, 10**100)


def test_pi_is_a_decimal_fraction_of_one_hundred_places() -> None:
    assert isinstance(PI, Fraction)
    assert 10**100 % PI.denominator == 0


def test_the_radian_scale_is_one_over_two_pi_turns() -> None:
    assert RADIAN.scale == 1 / (2 * PI)


# Conversion accuracy.


def test_one_radian_is_180_over_pi_degrees_to_ninety_eight_decimals() -> None:
    converted = Radian(1).to(DEGREE).value_in(DEGREE)
    assert abs(converted - 180 / TRUE_PI) < PRECISION


def test_one_degree_is_pi_over_180_radians_to_ninety_eight_decimals() -> None:
    converted = Degree(1).to(RADIAN).value_in(RADIAN)
    assert abs(converted - TRUE_PI / 180) < PRECISION


def test_one_radian_in_arcseconds_is_correct_to_ninety_eight_decimals() -> None:
    converted = Radian(1).to(ARCSECOND).value_in(ARCSECOND)
    assert abs(converted - 648000 / TRUE_PI) < PRECISION * 10**6


def test_every_displayed_digit_of_a_converted_radian_is_correct() -> None:
    assert repr(Radian(1).to(DEGREE)).startswith("57.29577951308232087679815481 ")


def test_a_half_turn_is_pi_radians_to_ninety_eight_decimals() -> None:
    converted = Turn(Fraction(1, 2)).to(RADIAN).value_in(RADIAN)
    assert abs(converted - TRUE_PI) < PRECISION


# Radian round trips are exact.


@pytest.mark.parametrize(
    "value",
    [0, 1, -1, 1.5707963, Fraction(1, 3), Decimal("3.14159265358979323846"), 10**20],
    ids=["zero", "one", "minus_one", "float", "third", "long_pi", "large"],
)
def test_a_radian_value_reads_back_exactly_in_radians(value: Numeric) -> None:
    assert Radian(value).value_in(RADIAN) == to_exact(value)


def test_a_radian_value_survives_a_detour_through_another_unit() -> None:
    reading = Radian(Fraction(2, 7))
    assert reading.to(DEGREE).to(RADIAN).value_in(RADIAN) == Fraction(2, 7)


def test_the_library_pi_in_radians_is_exactly_half_a_turn() -> None:
    assert Radian(PI) == Degree(180)
    assert Radian(PI) == Turn(Fraction(1, 2))
    assert Radian(2 * PI) == Turn(1)


# A float is not pi.


@pytest.mark.parametrize(
    ("degrees", "radians"),
    [
        (90, math.pi / 2),
        (45, math.pi / 4),
        (60, math.pi / 3),
        (30, math.pi / 6),
        (180, math.pi),
    ],
    ids=["90", "45", "60", "30", "180"],
)
def test_float_radians_are_not_exactly_equal_to_the_matching_degrees(
    degrees: int, radians: float
) -> None:
    assert Degree(degrees) != Radian(radians)


def test_float_radians_differ_from_the_exact_angle_by_less_than_a_float_step() -> None:
    reading = Radian(math.pi / 2)
    exact = Degree(90).to(RADIAN).value_in(RADIAN)
    assert abs(reading.value_in(RADIAN) - exact) < Fraction(1, 10**15)


def test_degree_family_values_never_involve_pi() -> None:
    for angle in (Degree(90), Gradian(100), Turn(Fraction(1, 4))):
        assert angle.magnitude.denominator <= ARCSECOND.scale.denominator
