"""Angle: exact rational units, wraparound arithmetic, and Radian as canonical.

`Radian` is the canonical unit and an ordinary constructor.
`Degree`, `Turn`, `Gradian`, `ArcMinute`, `ArcSecond` are scaled relative to it through
kuchka's own fixed rational representation of pi.
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
from kuchka.units import ANGLE_UNITS
from kuchka.units.angular import _PI


def test_degree_construction_is_exact():
    assert Degree(90).magnitude == _PI / 2


def test_radian_is_canonical():
    assert Radian(1).magnitude == Fraction(1)


def test_radian_construction_stores_the_value_exactly():
    reading = Radian(1.5707963)
    assert reading.magnitude == Fraction("1.5707963")


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (Gradian(100), Degree(90)),
        (ArcMinute(60), Degree(1)),
        (ArcSecond(3600), Degree(1)),
        (ArcSecond(60), ArcMinute(1)),
        (Turn(1), Degree(360)),
        (Radian(_PI), Degree(180)),
        (Radian(2 * _PI), Turn(1)),
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


def test_pi_cancels_between_non_radian_units():
    """The ratio between any two non-`Radian` angles is exact and rational.

    Independent of kuchka's own choice of pi -- it cancels algebraically.
    """
    assert Degree(180).magnitude / Turn(1).magnitude == Fraction(1, 2)


def test_radian_built_from_an_independent_pi_source_does_not_compare_equal():
    """`math.pi` and kuchka's own `_PI` are different numbers.

    Documented, intentional: different precisions, different values.
    """
    import math

    assert Radian(math.pi) != Degree(180)


def test_addition_wraps_exactly():
    assert Degree(350) + Degree(20) == Degree(10)


def test_subtraction_wraps_exactly():
    assert Degree(10) - Degree(20) == Degree(350)


def test_difference_gives_shortest_signed_path():
    assert Degree(10).difference(Degree(350)) == Degree(20)


def test_construction_does_not_auto_normalize():
    assert Degree(370).magnitude == 370 * (_PI / 180)


def test_normalize_wraps():
    assert Degree(370).normalize() == Degree(10)


def test_to_between_any_pair_is_exact():
    assert Degree(90).to(Radian(1).unit).value_in(Radian(1).unit) == _PI / 2
    assert Degree(90).to(Turn(1).unit).value_in(Turn(1).unit) == Fraction(1, 4)


def test_no_ordering():
    with pytest.raises(TypeError):
        Degree(10) < Degree(20)  # noqa: B015


def test_units_mix_freely_since_they_are_all_angle():
    """Degree/Gradian/Turn/ArcMinute/ArcSecond/Radian are all one `Angle` type.

    The same relationship `Volt`/`Millivolt` have as `Voltage`.
    """
    assert Degree(10) + Gradian(10) == Degree(19)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Degree(10) + 5


def test_angle_units_table_resolves_every_symbol():
    assert ANGLE_UNITS["rad"](1) == Radian(1)
    assert ANGLE_UNITS["\u00b0"](45) == Degree(45)
    assert ANGLE_UNITS["tr"](1) == Turn(1)
    assert ANGLE_UNITS["gon"](100) == Gradian(100)
