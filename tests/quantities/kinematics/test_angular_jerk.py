"""Angular jerk: the arithmetic that produces it, its bridge, and its units."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AngularAcceleration
from kuchka import AngularDisplacement
from kuchka import AngularJerk
from kuchka import AngularVelocity
from kuchka import Frequency
from kuchka import Jerk
from kuchka import Length
from kuchka import Time
from kuchka import UnrepresentableDimensionError
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import length
from kuchka.units import temporal
from kuchka.units.kinematics import angular_acceleration as angacc
from kuchka.units.kinematics import angular_jerk as angjerk
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.kinematics import jerk
from kuchka.units.kinematics import time_cubed

RAMP = angjerk.RadianPerSecondCubed(6)
DURATION = temporal.Second(2)


def test_an_angular_acceleration_over_a_time_is_an_angular_jerk() -> None:
    rate = angacc.RadianPerSecondSquared(3) / temporal.Second(2)
    assert type(rate) is AngularJerk
    assert rate == angjerk.RadianPerSecondCubed(Fraction(3, 2))


def test_an_angular_acceleration_times_a_frequency_is_an_angular_jerk() -> None:
    rate = angacc.RadianPerSecondSquared(6) * temporal.Hertz(2)
    assert type(rate) is AngularJerk
    assert rate == angjerk.RadianPerSecondCubed(12)


def test_an_angular_velocity_over_a_time_squared_is_an_angular_jerk() -> None:
    rate = angvel.RadianPerSecond(24) / (DURATION * DURATION)
    assert type(rate) is AngularJerk
    assert rate == angjerk.RadianPerSecondCubed(6)


def test_an_angle_over_a_time_cubed_is_an_angular_jerk() -> None:
    rate = angular.RadianDisplacement(48) / time_cubed.SecondCubed(8)
    assert type(rate) is AngularJerk
    assert rate == angjerk.RadianPerSecondCubed(6)


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (
            lambda j, t: j * t,
            AngularAcceleration,
            angacc.RadianPerSecondSquared(12),
        ),
        (
            lambda j, t: t * j * t,
            AngularVelocity,
            angvel.RadianPerSecond(24),
        ),
        (
            lambda j, t: j * t * t * t,
            AngularDisplacement,
            angular.RadianDisplacement(48),
        ),
        (
            lambda j, t: j * t**3,
            AngularDisplacement,
            angular.RadianDisplacement(48),
        ),
        (
            lambda j, t: t**3 * j,
            AngularDisplacement,
            angular.RadianDisplacement(48),
        ),
    ],
    ids=["j*t", "t*j*t", "j*t*t*t", "j*t**3", "t**3*j"],
)
def test_an_angular_jerk_over_time_has_one_value_in_every_order(
    build, expected_type, expected
) -> None:
    result = build(RAMP, DURATION)
    assert type(result) is expected_type
    assert result == expected


def test_an_angular_acceleration_over_an_angular_jerk_is_a_time() -> None:
    build_up = angacc.RadianPerSecondSquared(12) / RAMP
    assert type(build_up) is Time
    assert build_up == temporal.Second(2)


def test_an_angular_jerk_over_an_angular_acceleration_is_a_frequency() -> None:
    rate = RAMP / angacc.RadianPerSecondSquared(3)
    assert type(rate) is Frequency
    assert rate == temporal.Hertz(2)


@pytest.mark.parametrize(
    "build",
    [lambda j, r: j * r, lambda j, r: r * j],
    ids=["j*r", "r*j"],
)
def test_an_angular_jerk_times_a_radius_is_the_tangential_jerk(build) -> None:
    tangential = build(RAMP, length.Metre(Fraction(1, 5)))
    assert type(tangential) is Jerk
    assert tangential == jerk.MetrePerSecondCubed(Fraction(6, 5))


def test_a_tangential_jerk_over_an_angular_jerk_is_the_radius() -> None:
    radius = jerk.MetrePerSecondCubed(Fraction(6, 5)) / RAMP
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 5))


def test_a_value_across_the_bridge_and_back_is_unchanged() -> None:
    tangential = RAMP * length.Metre(3)
    assert tangential / RAMP == length.Metre(3)


def test_the_bridge_factor_of_a_turn_rate_is_two_pi() -> None:
    rim = angjerk.TurnPerSecondCubed(1) * length.Metre(1)
    assert rim == jerk.MetrePerSecondCubed(2 * PI)


def test_a_jerk_over_a_radius_has_no_type() -> None:
    with pytest.raises(UnrepresentableDimensionError):
        jerk.MetrePerSecondCubed(6) / length.Metre(2)


def test_the_units_of_an_angular_jerk_have_exact_scales() -> None:
    assert angjerk.DegreePerSecondCubed(360) == angjerk.TurnPerSecondCubed(1)
    assert angjerk.RadianPerSecondCubed(2 * PI) == angjerk.TurnPerSecondCubed(1)


def test_the_angular_jerk_table_lists_the_units_by_symbol() -> None:
    assert set(angjerk.ANGULAR_JERK_UNITS) == {
        f"tr/s{symbols.SUPERSCRIPT_THREE}",
        f"rad/s{symbols.SUPERSCRIPT_THREE}",
        f"{symbols.DEGREE}/s{symbols.SUPERSCRIPT_THREE}",
    }


def test_an_angular_jerk_displays_in_the_unit_it_was_built_in() -> None:
    assert str(angjerk.DegreePerSecondCubed(90)) == "90 °/s³"
    assert str(RAMP * DURATION) == "12 rad/s²"
