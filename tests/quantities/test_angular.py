"""Angle: exact rational units, wraparound arithmetic, and Turn as canonical.

`Turn` is the canonical unit.
`Degree`, `Gradian`, `ArcMinute`, and `ArcSecond` are plain rational fractions of a
turn, so they and `Turn` convert and compare exactly with no pi involved.
`Radian` is related to a turn through pi; see the radian conversion tests for that.
"""

from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.units import angular


def test_degree_construction_is_exact():
    assert angular.Degree(90).magnitude == Fraction(1, 4)


def test_turn_is_canonical():
    assert angular.Turn(1).magnitude == Fraction(1)
    assert angular.Turn(Fraction(1, 3)).magnitude == Fraction(1, 3)


@pytest.mark.parametrize(
    ("unit", "turns"),
    [
        (angular.TURN, Fraction(1)),
        (angular.DEGREE, Fraction(1, 360)),
        (angular.GRADIAN, Fraction(1, 400)),
        (angular.ARCMINUTE, Fraction(1, 21600)),
        (angular.ARCSECOND, Fraction(1, 1296000)),
    ],
    ids=["turn", "degree", "gradian", "arcminute", "arcsecond"],
)
def test_every_non_radian_unit_is_a_plain_fraction_of_a_turn(unit, turns):
    assert unit.scale == turns


def test_radian_construction_stores_the_value_exactly():
    reading = angular.Radian(1.5707963)
    assert reading.value_in(angular.RADIAN) == Fraction("1.5707963")


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (angular.Gradian(100), angular.Degree(90)),
        (angular.ArcMinute(60), angular.Degree(1)),
        (angular.ArcSecond(3600), angular.Degree(1)),
        (angular.ArcSecond(60), angular.ArcMinute(1)),
        (angular.Turn(1), angular.Degree(360)),
        (angular.Radian(PI), angular.Degree(180)),
        (angular.Radian(2 * PI), angular.Turn(1)),
    ],
    ids=[
        "gradian",
        "arcminute",
        "arcsecond",
        "arcsecond-of-arcminute",
        "turn",
        "radian-of-pi",
        "radian-of-two-pi",
    ],
)
def test_cross_unit_equality_is_exact(a, b):
    assert a == b


def test_the_ratio_between_two_non_radian_angles_is_rational():
    assert angular.Degree(180).magnitude / angular.Turn(1).magnitude == Fraction(1, 2)


def test_addition_wraps_exactly():
    assert angular.Degree(350) + angular.Degree(20) == angular.Degree(10)


def test_subtraction_wraps_exactly():
    assert angular.Degree(10) - angular.Degree(20) == angular.Degree(350)


def test_difference_gives_shortest_signed_path():
    assert angular.Degree(10).difference(angular.Degree(350)) == angular.Degree(20)


def test_construction_does_not_auto_normalize():
    assert angular.Degree(370).magnitude == Fraction(370, 360)


def test_normalize_wraps():
    assert angular.Degree(370).normalize() == angular.Degree(10)


def test_to_between_non_radian_units_is_exact():
    assert angular.Degree(90).to(angular.TURN).value_in(angular.TURN) == Fraction(1, 4)
    assert angular.Degree(90).to(angular.GRADIAN).value_in(angular.GRADIAN) == Fraction(
        100
    )
    assert angular.Turn(1).to(angular.ARCSECOND).value_in(
        angular.ARCSECOND
    ) == Fraction(1296000)


def test_no_ordering():
    with pytest.raises(TypeError):
        angular.Degree(10) < angular.Degree(20)  # noqa: B015  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_units_mix_freely_since_they_are_all_angle():
    """Degree/Gradian/Turn/ArcMinute/ArcSecond/Radian are all one `Angle` type.

    The same relationship `Volt`/`Millivolt` have as `Voltage`.
    """
    assert angular.Degree(10) + angular.Gradian(10) == angular.Degree(19)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        angular.Degree(10) + 5  # ty: ignore[unsupported-operator]  # type: ignore[operator]


def test_angle_units_table_resolves_every_symbol():
    assert angular.ANGLE_UNITS["rad"](1) == angular.Radian(1)
    assert angular.ANGLE_UNITS[symbols.DEGREE](45) == angular.Degree(45)
    assert angular.ANGLE_UNITS["tr"](1) == angular.Turn(1)
    assert angular.ANGLE_UNITS["gon"](100) == angular.Gradian(100)


def test_every_arithmetic_result_lies_within_one_turn() -> None:
    a, b = angular.Degree(350), angular.Degree(20)
    results = {
        "sum": a + b,
        "difference": b - a,
        "scaled": a * 3,
        "reflected scale": 3 * a,
        "quotient": a / 2,
        "negation": -a,
    }
    for name, result in results.items():
        assert 0 <= result.magnitude < 1, name
    assert (a + b).magnitude == Fraction(1, 36)
    assert (b - a).magnitude == Fraction(1, 12)
