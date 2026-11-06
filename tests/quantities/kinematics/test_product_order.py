"""A product of three factors has one type and value in every order it is written."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import AngularDisplacement
from kuchka import AngularVelocitySquared
from kuchka import Energy
from kuchka import Length
from kuchka import Time
from kuchka import TimeSquared
from kuchka import UnrepresentableDimensionError
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import length
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import angular_acceleration as angacc
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.kinematics import angular_velocity_squared as angvel2
from kuchka.units.kinematics import time_squared
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import moment_of_inertia as inertia
from kuchka.units.temporal import time as time_units

SPIN = angvel.RadianPerSecond(300)
RADIUS = length.Metre(Fraction(1, 5))
ROTOR = inertia.KilogramSquareMetre(Fraction(4, 100))
GRAVITY = acceleration.MetrePerSecondSquared(Fraction(981, 100))
DURATION = time_units.Second(2)


@pytest.mark.parametrize(
    "build",
    [
        lambda w, r: w * w * r,
        lambda w, r: w**2 * r,
        lambda w, r: r * w * w,
        lambda w, r: r * w**2,
        lambda w, r: w * (w * r),
    ],
    ids=["w*w*r", "w**2*r", "r*w*w", "r*w**2", "w*(w*r)"],
)
def test_a_centripetal_acceleration_reads_the_same_in_every_order(build) -> None:
    centripetal = build(SPIN, RADIUS)
    assert type(centripetal) is Acceleration
    assert centripetal == acceleration.MetrePerSecondSquared(18_000)


@pytest.mark.parametrize(
    "build",
    [
        lambda w, i: i * w * w,
        lambda w, i: w * i * w,
        lambda w, i: w * w * i,
        lambda w, i: w**2 * i,
        lambda w, i: i * w**2,
    ],
    ids=["i*w*w", "w*i*w", "w*w*i", "w**2*i", "i*w**2"],
)
def test_a_rotational_energy_reads_the_same_in_every_order(build) -> None:
    stored = build(SPIN, ROTOR)
    assert type(stored) is Energy
    assert stored == energy.Joule(3_600)


@pytest.mark.parametrize(
    "build",
    [
        lambda g, t: g * t * t,
        lambda g, t: t * t * g,
        lambda g, t: g * t**2,
        lambda g, t: t**2 * g,
        lambda g, t: g * (t * t),
        lambda g, t: t * (t * g),
    ],
    ids=["g*t*t", "t*t*g", "g*t**2", "t**2*g", "g*(t*t)", "t*(t*g)"],
)
def test_a_fall_reads_the_same_in_every_order(build) -> None:
    fallen = build(GRAVITY, DURATION)
    assert type(fallen) is Length
    assert fallen == length.Metre(Fraction(3_924, 100))


@pytest.mark.parametrize(
    "build",
    [lambda r, t: r / t / t, lambda r, t: r / (t * t), lambda r, t: r / t**2],
    ids=["r/t/t", "r/(t*t)", "r/t**2"],
)
def test_a_length_over_a_time_twice_reads_the_same_in_every_order(build) -> None:
    rate = build(RADIUS, DURATION)
    assert type(rate) is Acceleration
    assert rate == acceleration.MetrePerSecondSquared(Fraction(1, 20))


def test_a_product_of_two_angular_velocities_is_their_square() -> None:
    squared = SPIN * SPIN
    assert type(squared) is AngularVelocitySquared
    assert squared == angvel2.RadianSquaredPerSecondSquared(90_000)
    assert squared == SPIN**2


def test_a_product_of_two_durations_is_their_square() -> None:
    squared = DURATION * DURATION
    assert type(squared) is TimeSquared
    assert squared == time_squared.SecondSquared(4)
    assert squared == DURATION**2


def test_the_squares_display_in_the_units_they_are_written_in() -> None:
    assert str(SPIN * SPIN) == "90000 rad²/s²"
    assert str(DURATION * DURATION) == "4 s²"


def test_a_cube_of_a_time_has_no_type() -> None:
    with pytest.raises(UnrepresentableDimensionError):
        DURATION**3


def test_an_angle_times_an_angular_acceleration_is_an_angular_velocity_squared() -> (
    None
):
    squared = angular.RadianDisplacement(2) * angacc.RadianPerSecondSquared(150)
    assert type(squared) is AngularVelocitySquared
    assert squared == angvel2.RadianSquaredPerSecondSquared(300)


def test_a_squared_rate_per_angular_acceleration_is_an_angle() -> None:
    swept = SPIN**2 / angacc.RadianPerSecondSquared(150)
    assert type(swept) is AngularDisplacement
    assert swept == angular.RadianDisplacement(600)


@pytest.mark.parametrize(
    "build",
    [
        lambda a, t: a * t**2,
        lambda a, t: t**2 * a,
    ],
    ids=["a*t**2", "t**2*a"],
)
def test_an_angular_acceleration_over_a_time_squared_is_an_angle(build) -> None:
    swept = build(angacc.RadianPerSecondSquared(150), DURATION)
    assert type(swept) is AngularDisplacement
    assert swept == angular.RadianDisplacement(600)


def test_a_length_per_acceleration_is_a_time_squared() -> None:
    squared = length.Metre(Fraction(1962, 100)) / GRAVITY
    assert type(squared) is TimeSquared
    assert squared == time_squared.SecondSquared(2)


def test_a_time_squared_per_time_is_a_time() -> None:
    assert type(DURATION**2 / DURATION) is Time


def test_a_value_across_the_bridge_and_back_is_unchanged() -> None:
    centripetal = SPIN**2 * RADIUS
    assert centripetal / SPIN**2 == RADIUS
    assert type(centripetal / SPIN**2) is Length


def test_the_bridge_factor_of_a_turn_rate_is_two_pi_squared() -> None:
    rim = angvel.TurnPerSecond(1) ** 2 * length.Metre(1)
    assert rim == acceleration.MetrePerSecondSquared((2 * PI) ** 2)
