"""`AngularDisplacement` is the angle swept, which does not wrap."""

from __future__ import annotations

from fractions import Fraction

from kuchka import Angle
from kuchka import AngularDisplacement
from kuchka.dimensions import ANGLE
from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.dimensions import ENERGY
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.dimensions import TORQUE
from kuchka.internal.constants import PI
from kuchka.units import angular


def test_torque_is_energy_per_angle_and_angular_velocity_is_angle_per_time() -> None:
    assert TORQUE == ENERGY / ANGLE
    assert ANGULAR_VELOCITY == ANGLE / TIME


def test_torque_and_angular_velocity_differ_from_energy_and_frequency() -> None:
    assert TORQUE != ENERGY
    assert ANGULAR_VELOCITY != FREQUENCY


# `AngularDisplacement` is the unwrapped angle.


def test_an_angular_displacement_keeps_the_turns_it_swept() -> None:
    swept = angular.DegreeDisplacement(370)
    assert swept.value_in(angular.DEGREE) == Fraction(370)
    assert swept != angular.DegreeDisplacement(10)


def test_an_angle_wraps_where_a_displacement_does_not() -> None:
    assert angular.Degree(370) == angular.Degree(10)
    assert angular.DegreeDisplacement(370) != angular.DegreeDisplacement(10)


def test_a_displacement_adds_and_subtracts_without_wrapping() -> None:
    assert angular.DegreeDisplacement(270) + angular.DegreeDisplacement(
        270
    ) == angular.DegreeDisplacement(540)
    assert angular.DegreeDisplacement(10) - angular.DegreeDisplacement(
        20
    ) == angular.DegreeDisplacement(-10)


def test_the_displacement_units_are_exact_for_degrees_and_turns() -> None:
    assert angular.TurnDisplacement(1) == angular.DegreeDisplacement(360)
    assert angular.RadianDisplacement(PI * 2) == angular.TurnDisplacement(1)


def test_an_angle_becomes_a_displacement_within_one_turn() -> None:
    swept = angular.Degree(370).to_angular_displacement()
    assert type(swept) is AngularDisplacement
    assert swept == angular.DegreeDisplacement(10)


def test_a_displacement_wraps_into_the_angle_it_ends_at() -> None:
    angle = angular.DegreeDisplacement(370).to_angle()
    assert type(angle) is Angle
    assert angle.value_in(angular.DEGREE) == Fraction(10)
    assert angular.DegreeDisplacement(-10).to_angle().value_in(
        angular.DEGREE
    ) == Fraction(350)


def test_the_conversions_keep_the_unit_they_were_shown_in() -> None:
    assert angular.Degree(90).to_angular_displacement().unit is angular.DEGREE
    assert angular.RadianDisplacement(1).to_angle().unit is angular.RADIAN
