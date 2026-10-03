"""Angle: exact rational units, wraparound arithmetic, and Turn as canonical.

`Turn` is the canonical unit.
`Degree`, `Gradian`, `ArcMinute`, and `ArcSecond` are plain rational fractions of a
turn, so they and `Turn` convert and compare exactly with no pi involved.
`Radian` is related to a turn through pi; see the radian conversion tests for that.
"""

from fractions import Fraction

import pytest

from kuchka import ArcMinute
from kuchka import ArcSecond
from kuchka import Degree
from kuchka import Gradian
from kuchka import InvalidMeasurementError
from kuchka import Radian
from kuchka import Turn
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.units import ANGLE_UNITS
from kuchka.units import ARCMINUTE
from kuchka.units import ARCSECOND
from kuchka.units import DEGREE
from kuchka.units import GRADIAN
from kuchka.units import RADIAN
from kuchka.units import TURN


def test_degree_construction_is_exact():
    assert Degree(90).magnitude == Fraction(1, 4)


def test_turn_is_canonical():
    assert Turn(1).magnitude == Fraction(1)
    assert Turn(Fraction(1, 3)).magnitude == Fraction(1, 3)


@pytest.mark.parametrize(
    ("unit", "turns"),
    [
        (TURN, Fraction(1)),
        (DEGREE, Fraction(1, 360)),
        (GRADIAN, Fraction(1, 400)),
        (ARCMINUTE, Fraction(1, 21600)),
        (ARCSECOND, Fraction(1, 1296000)),
    ],
    ids=["turn", "degree", "gradian", "arcminute", "arcsecond"],
)
def test_every_non_radian_unit_is_a_plain_fraction_of_a_turn(unit, turns):
    assert unit.scale == turns


def test_radian_construction_stores_the_value_exactly():
    reading = Radian(1.5707963)
    assert reading.value_in(RADIAN) == Fraction("1.5707963")


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (Gradian(100), Degree(90)),
        (ArcMinute(60), Degree(1)),
        (ArcSecond(3600), Degree(1)),
        (ArcSecond(60), ArcMinute(1)),
        (Turn(1), Degree(360)),
        (Radian(PI), Degree(180)),
        (Radian(2 * PI), Turn(1)),
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
    assert Degree(180).magnitude / Turn(1).magnitude == Fraction(1, 2)


def test_addition_wraps_exactly():
    assert Degree(350) + Degree(20) == Degree(10)


def test_subtraction_wraps_exactly():
    assert Degree(10) - Degree(20) == Degree(350)


def test_difference_gives_shortest_signed_path():
    assert Degree(10).difference(Degree(350)) == Degree(20)


def test_construction_does_not_auto_normalize():
    assert Degree(370).magnitude == Fraction(370, 360)


def test_normalize_wraps():
    assert Degree(370).normalize() == Degree(10)


def test_to_between_non_radian_units_is_exact():
    assert Degree(90).to(TURN).value_in(TURN) == Fraction(1, 4)
    assert Degree(90).to(GRADIAN).value_in(GRADIAN) == Fraction(100)
    assert Turn(1).to(ARCSECOND).value_in(ARCSECOND) == Fraction(1296000)


def test_no_ordering():
    with pytest.raises(TypeError):
        Degree(10) < Degree(20)  # noqa: B015  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_units_mix_freely_since_they_are_all_angle():
    """Degree/Gradian/Turn/ArcMinute/ArcSecond/Radian are all one `Angle` type.

    The same relationship `Volt`/`Millivolt` have as `Voltage`.
    """
    assert Degree(10) + Gradian(10) == Degree(19)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Degree(10) + 5  # ty: ignore[unsupported-operator]  # type: ignore[operator]


def test_angle_units_table_resolves_every_symbol():
    assert ANGLE_UNITS["rad"](1) == Radian(1)
    assert ANGLE_UNITS[symbols.DEGREE](45) == Degree(45)
    assert ANGLE_UNITS["tr"](1) == Turn(1)
    assert ANGLE_UNITS["gon"](100) == Gradian(100)
