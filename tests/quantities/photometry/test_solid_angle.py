"""SolidAngle: its own axis, which a square metre per square metre does not reach."""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from kuchka import AngularDisplacement
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Proportion
from kuchka import SolidAngle
from kuchka import UnrepresentableDimensionError
from kuchka.dimensions import ANGLE
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import SOLID_ANGLE
from kuchka.units import angular
from kuchka.units import length
from kuchka.units import proportion
from kuchka.units import solid_angle
from kuchka.units.geometry import area


def test_a_solid_angle_is_not_dimensionless_nor_an_angle_squared() -> None:
    assert SOLID_ANGLE != DIMENSIONLESS
    assert SOLID_ANGLE != ANGLE * ANGLE
    assert repr(SOLID_ANGLE) == "∢¹"


def test_a_square_metre_over_a_square_metre_is_a_proportion() -> None:
    ratio = area.SquareMetre(2) / area.SquareMetre(8)
    assert isinstance(ratio, Proportion)
    assert ratio == proportion.Ratio(Fraction(1, 4))


def test_two_plane_angles_multiply_to_nothing_registered() -> None:
    swept = angular.RadianDisplacement(1)
    with pytest.raises(UnrepresentableDimensionError):
        swept * swept
    assert isinstance(swept, AngularDisplacement)


def test_a_square_metre_on_a_sphere_of_two_metres_is_a_quarter_steradian() -> None:
    cut = SolidAngle.from_area(area.SquareMetre(1), length.Metre(2))
    assert cut == solid_angle.Steradian(Fraction(1, 4))


def test_the_area_and_the_radius_may_be_in_any_unit() -> None:
    cut = SolidAngle.from_area(area.SquareCentimetre(1), length.Millimetre(100))
    assert cut == solid_angle.Millisteradian(10)


@pytest.mark.parametrize("radius", [length.Metre(0), length.Metre(-1)])
def test_a_sphere_needs_a_positive_radius(radius: object) -> None:
    with pytest.raises(InvalidMeasurementError):
        SolidAngle.from_area(area.SquareMetre(1), radius)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_from_area_refuses_other_quantities() -> None:
    with pytest.raises(IncompatibleDimensionError):
        SolidAngle.from_area(length.Metre(1), length.Metre(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(IncompatibleDimensionError):
        SolidAngle.from_area(area.SquareMetre(1), area.SquareMetre(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_a_square_degree_is_pi_over_180_squared_steradians() -> None:
    expected = (math.pi / 180) ** 2
    in_steradians = solid_angle.SquareDegree(1).value_in(solid_angle.STERADIAN)
    assert float(in_steradians) == pytest.approx(expected, rel=1e-15)


def test_the_whole_sphere_is_about_41253_square_degrees() -> None:
    full = 4 * math.pi
    in_degrees = solid_angle.Steradian(full).value_in(solid_angle.SQUARE_DEGREE)
    assert float(in_degrees) == pytest.approx(41252.96, abs=0.01)


def test_the_squared_angle_units_chain_exactly() -> None:
    assert solid_angle.SquareArcMinute(3600) == solid_angle.SquareDegree(1)
    assert solid_angle.SquareArcSecond(3600) == solid_angle.SquareArcMinute(1)


def test_a_microsteradian_is_a_millionth() -> None:
    assert solid_angle.Microsteradian(1_000_000) == solid_angle.Steradian(1)


def test_the_squared_units_are_known_by_their_ascii_spellings() -> None:
    from kuchka.units import SOLID_ANGLE_UNITS

    assert SOLID_ANGLE_UNITS["deg^2"] is solid_angle.SquareDegree
    assert SOLID_ANGLE_UNITS["arcmin2"] is solid_angle.SquareArcMinute
    assert SOLID_ANGLE_UNITS["µsr"] is solid_angle.Microsteradian
