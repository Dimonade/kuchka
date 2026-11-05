"""A point turning at a radius moves along its rim, and the lever arm reads back."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import Force
from kuchka import Frequency
from kuchka import Length
from kuchka import Torque
from kuchka import Velocity
from kuchka.internal.constants import PI
from kuchka.units import length
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import angular_acceleration as angacc
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import force
from kuchka.units.mechanics import torque


@pytest.mark.parametrize(
    "build",
    [lambda w, r: w * r, lambda w, r: r * w],
    ids=["w*r", "r*w"],
)
def test_an_angular_velocity_at_a_radius_is_a_rim_speed(build) -> None:
    rim = build(angvel.RadianPerSecond(300), length.Metre(Fraction(1, 5)))
    assert type(rim) is Velocity
    assert rim == velocity.MetrePerSecond(60)


def test_a_turn_rate_at_a_radius_moves_a_circumference_per_turn() -> None:
    rim = angvel.RevolutionPerMinute(60) * length.Metre(1)
    assert rim == velocity.MetrePerSecond(2 * PI)


def test_a_rim_speed_per_angular_velocity_is_the_radius() -> None:
    radius = velocity.MetrePerSecond(60) / angvel.RadianPerSecond(300)
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 5))


def test_the_centripetal_acceleration_reads_from_the_rim_speed() -> None:
    radius = length.Metre(Fraction(1, 5))
    rim = angvel.RadianPerSecond(300) * radius
    centripetal = rim**2 / radius
    assert type(centripetal) is Acceleration
    assert centripetal == acceleration.MetrePerSecondSquared(18_000)


def test_a_velocity_per_radius_stays_a_frequency() -> None:
    rate = velocity.MetrePerSecond(60) / length.Metre(Fraction(1, 5))
    assert type(rate) is Frequency


@pytest.mark.parametrize(
    "build",
    [lambda a, r: a * r, lambda a, r: r * a],
    ids=["a*r", "r*a"],
)
def test_an_angular_acceleration_at_a_radius_is_tangential(build) -> None:
    tangential = build(angacc.RadianPerSecondSquared(150), length.Metre(Fraction(1, 5)))
    assert type(tangential) is Acceleration
    assert tangential == acceleration.MetrePerSecondSquared(30)


def test_a_tangential_acceleration_per_angular_acceleration_is_the_radius() -> None:
    radius = acceleration.MetrePerSecondSquared(30) / angacc.RadianPerSecondSquared(150)
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 5))


def test_a_torque_per_force_is_the_lever_arm() -> None:
    arm = torque.NewtonMetre(10) / force.Newton(50)
    assert type(arm) is Length
    assert arm == length.Metre(Fraction(1, 5))


def test_a_torque_per_lever_arm_is_the_force() -> None:
    push = torque.NewtonMetre(10) / length.Metre(Fraction(1, 5))
    assert type(push) is Force
    assert push == force.Newton(50)


def test_a_force_at_a_lever_arm_round_trips() -> None:
    turning = Torque.from_force(force.Newton(50), length.Metre(Fraction(1, 5)))
    assert turning / length.Metre(Fraction(1, 5)) == force.Newton(50)
    assert turning / force.Newton(50) == length.Metre(Fraction(1, 5))
