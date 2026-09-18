"""Angle: exact rational units, wraparound arithmetic, and the Radian block.

`Degree`, `Turn`, `Gradian`, `ArcMinute`, `ArcSecond` are exact rational fractions of a
turn.

NOTE: `Radian` needs pi, therefore, blocked.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import ArcMinute
from kuchka import ArcSecond
from kuchka import Degree
from kuchka import Gradian
from kuchka import PlannedDimensionError
from kuchka import Radian
from kuchka import Turn
from kuchka.units import ANGLE_UNITS


def test_degree_construction_is_exact():
    assert Degree(90).magnitude == Fraction(1, 4)


def test_turn_is_canonical():
    assert Turn(1).magnitude == Fraction(1)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (Gradian(100), Degree(90)),
        (ArcMinute(60), Degree(1)),
        (ArcSecond(3600), Degree(1)),
        (ArcSecond(60), ArcMinute(1)),
        (Turn(1), Degree(360)),
    ],
    ids=["gradian", "arcminute", "arcsecond", "arcsecond-of-arcminute", "turn"],
)
def test_cross_unit_equality_is_exact(a, b):
    assert a == b


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


def test_to_between_working_units_is_exact():
    assert Degree(90).to(Turn(1).unit).value_in(Turn(1).unit) == Fraction(1, 4)


def test_no_ordering():
    with pytest.raises(TypeError):
        Degree(10) < Degree(20)  # noqa: B015


def test_units_mix_freely_since_they_are_all_angle():
    """Degree/Gradian/Turn/ArcMinute/ArcSecond are all `Angle`, one type.

    The same relationship `Volt`/`Millivolt` have as `Voltage`.
    """
    assert Degree(10) + Gradian(10) == Degree(19)


def test_naked_number_addition_is_rejected():
    from kuchka import InvalidMeasurementError

    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Degree(10) + 5


# NOTE: Radian - still blocked.
# TODO: @dimonade


def test_radian_construction_raises():
    with pytest.raises(PlannedDimensionError):
        Radian(1)


def test_no_radian_unitdef_exists():
    import kuchka.units.angular as angular_units

    assert not hasattr(angular_units, "RADIAN")


def test_angle_units_table_maps_rad_to_the_blocked_constructor():
    assert ANGLE_UNITS["rad"] is Radian
    with pytest.raises(PlannedDimensionError):
        ANGLE_UNITS["rad"](1)


def test_angle_units_table_resolves_working_symbols():
    assert ANGLE_UNITS["\u00b0"](45) == Degree(45)
    assert ANGLE_UNITS["tr"](1) == Turn(1)
    assert ANGLE_UNITS["gon"](100) == Gradian(100)


def test_to_lossy_returns_a_decimal():
    assert isinstance(Degree(90).to_lossy(), Decimal)


def test_to_lossy_matches_known_pi_to_context_precision():
    expected = Decimal("3.1415926535897930")
    assert Degree(180).to_lossy() == expected


def test_to_lossy_of_zero_is_zero():
    assert Degree(0).to_lossy() == Decimal(0)


def test_to_lossy_of_a_full_turn_is_two_pi():
    expected = Decimal("6.283185307179586")
    assert Turn(1).to_lossy() == expected
