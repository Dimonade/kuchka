"""Radian conversions are accurate, and their round trips are exact."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

from kuchka.internal.constants import PI
from kuchka.numeric import to_exact
from kuchka.units import angular

if TYPE_CHECKING:
    from kuchka.numeric import Numeric


PRECISION = Fraction(1, 10**98)


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


def test_one_radian_is_180_over_pi_degrees_to_ninety_eight_decimals() -> None:
    converted = angular.Radian(1).to(angular.DEGREE).value_in(angular.DEGREE)
    assert abs(converted - 180 / TRUE_PI) < PRECISION


def test_one_degree_is_pi_over_180_radians_to_ninety_eight_decimals() -> None:
    converted = angular.Degree(1).to(angular.RADIAN).value_in(angular.RADIAN)
    assert abs(converted - TRUE_PI / 180) < PRECISION


def test_one_radian_in_arcseconds_is_correct_to_ninety_eight_decimals() -> None:
    converted = angular.Radian(1).to(angular.ARCSECOND).value_in(angular.ARCSECOND)
    assert abs(converted - 648000 / TRUE_PI) < PRECISION * 10**6


def test_every_displayed_digit_of_a_converted_radian_is_correct() -> None:
    assert repr(angular.Radian(1).to(angular.DEGREE)).startswith(
        "57.29577951308232087679815481 "
    )


def test_a_half_turn_is_pi_radians_to_ninety_eight_decimals() -> None:
    converted = angular.Turn(Fraction(1, 2)).to(angular.RADIAN).value_in(angular.RADIAN)
    assert abs(converted - TRUE_PI) < PRECISION


@pytest.mark.parametrize(
    "value",
    [0, 1, -1, 1.5707963, Fraction(1, 3), Decimal("3.14159265358979323846"), 10**20],
    ids=["zero", "one", "minus_one", "float", "third", "long_pi", "large"],
)
def test_a_radian_value_reads_back_exactly_in_radians(value: Numeric) -> None:
    assert angular.Radian(value).value_in(angular.RADIAN) == to_exact(value)


def test_a_radian_value_survives_a_detour_through_another_unit() -> None:
    reading = angular.Radian(Fraction(2, 7))
    assert reading.to(angular.DEGREE).to(angular.RADIAN).value_in(
        angular.RADIAN
    ) == Fraction(2, 7)


def test_the_library_pi_in_radians_is_exactly_half_a_turn() -> None:
    assert angular.Radian(PI) == angular.Degree(180)
    assert angular.Radian(PI) == angular.Turn(Fraction(1, 2))
    assert angular.Radian(2 * PI) == angular.Turn(1)
