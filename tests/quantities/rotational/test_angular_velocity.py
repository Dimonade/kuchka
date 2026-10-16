"""`AngularVelocity` is angle per time, and differs from the hertz."""

from __future__ import annotations

import operator

import pytest

from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import Frequency
from kuchka import IncompatibleDimensionError
from kuchka import Time
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import angular_velocity as angvel
from kuchka.units import frequency as frequency_units
from kuchka.units import time


def test_angle_per_time_is_angular_velocity_and_back() -> None:
    velocity = angular.DegreeDisplacement(90) / time.Second(1)
    assert type(velocity) is AngularVelocity
    assert velocity == angvel.DegreePerSecond(90)
    swept = angvel.RadianPerSecond(5) * time.Second(2)
    assert type(swept) is AngularDisplacement
    assert swept == angular.RadianDisplacement(10)
    assert time.Second(2) * angvel.RadianPerSecond(5) == angular.RadianDisplacement(10)
    assert type(angular.RadianDisplacement(10) / angvel.RadianPerSecond(5)) is Time


def test_the_revolution_per_minute_is_exact() -> None:
    assert angvel.RevolutionPerMinute(60) == angvel.TurnPerSecond(1)
    assert (
        angvel.RevolutionPerMinute(3000).value_in(angvel.RADIAN_PER_SECOND)
        == 3000 * 2 * PI / 60
    )


def test_a_frequency_times_an_angle_is_an_angular_velocity() -> None:
    result = frequency_units.Hertz(2) * angular.TurnDisplacement(1)
    assert type(result) is AngularVelocity
    assert result == angvel.RadianPerSecond(4 * PI)
    assert (
        type(angular.TurnDisplacement(1) * frequency_units.Hertz(2)) is AngularVelocity
    )
    assert (
        type(angvel.RadianPerSecond(4 * PI) / frequency_units.Hertz(2))
        is AngularDisplacement
    )


def test_one_hertz_is_not_an_angular_velocity() -> None:
    with pytest.raises(IncompatibleDimensionError):
        frequency_units.Hertz(1) + angvel.TurnPerSecond(1)  # type: ignore[operator]
    assert frequency_units.Hertz(1) != angvel.TurnPerSecond(1)
    with pytest.raises(IncompatibleDimensionError):
        operator.lt(frequency_units.Hertz(1), angvel.TurnPerSecond(1))


def test_a_frequency_converts_to_an_angular_velocity_by_name() -> None:
    velocity = frequency_units.Hertz(50).to_angular_velocity()
    assert type(velocity) is AngularVelocity
    assert velocity == angvel.RadianPerSecond(100 * PI)


def test_an_angular_velocity_converts_to_a_frequency_by_name() -> None:
    frequency = angvel.RevolutionPerMinute(3000).to_frequency()
    assert type(frequency) is Frequency
    assert frequency == frequency_units.Hertz(50)
    assert frequency_units.Hertz(
        50
    ).to_angular_velocity().to_frequency() == frequency_units.Hertz(50)
