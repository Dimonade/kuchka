"""The constant pi is exact to its stated precision, and a float is not pi."""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from kuchka.internal.constants import PI
from kuchka.units import angular


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


def test_pi_is_correct_to_one_hundred_decimals() -> None:
    assert abs(PI - TRUE_PI) < Fraction(1, 10**100)


def test_pi_is_a_decimal_fraction_of_one_hundred_places() -> None:
    assert isinstance(PI, Fraction)
    assert 10**100 % PI.denominator == 0


def test_the_radian_scale_is_one_over_two_pi_turns() -> None:
    assert angular.RADIAN.scale == 1 / (2 * PI)


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
    assert angular.Degree(degrees) != angular.Radian(radians)


def test_float_radians_differ_from_the_exact_angle_by_less_than_a_float_step() -> None:
    reading = angular.Radian(math.pi / 2)
    exact = angular.Degree(90).to(angular.RADIAN).value_in(angular.RADIAN)
    assert abs(reading.value_in(angular.RADIAN) - exact) < Fraction(1, 10**15)


def test_degree_family_values_never_involve_pi() -> None:
    for angle in (
        angular.Degree(90),
        angular.Gradian(100),
        angular.Turn(Fraction(1, 4)),
    ):
        assert angle.magnitude.denominator <= angular.ARCSECOND.scale.denominator
