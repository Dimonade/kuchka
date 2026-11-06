"""The units of a time squared and of an angular velocity squared are exact squares."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.kinematics import angular_velocity_squared as angvel2
from kuchka.units.kinematics import time_squared
from kuchka.units.temporal import time as time_units


@pytest.mark.parametrize(
    ("duration", "squared"),
    [
        (time_units.Nanosecond, time_squared.NanosecondSquared),
        (time_units.Microsecond, time_squared.MicrosecondSquared),
        (time_units.Millisecond, time_squared.MillisecondSquared),
        (time_units.Second, time_squared.SecondSquared),
        (time_units.Minute, time_squared.MinuteSquared),
        (time_units.Hour, time_squared.HourSquared),
    ],
    ids=["ns", "us", "ms", "s", "min", "h"],
)
def test_a_duration_times_itself_is_the_squared_unit(duration, squared) -> None:
    assert duration(3) * duration(3) == squared(9)


@pytest.mark.parametrize(
    ("squared", "seconds_squared"),
    [
        (time_squared.NanosecondSquared, Fraction(1, 10**18)),
        (time_squared.MicrosecondSquared, Fraction(1, 10**12)),
        (time_squared.MillisecondSquared, Fraction(1, 10**6)),
        (time_squared.MinuteSquared, 3_600),
        (time_squared.HourSquared, 12_960_000),
    ],
    ids=["ns", "us", "ms", "min", "h"],
)
def test_each_time_squared_unit_has_its_scale_in_seconds_squared(
    squared, seconds_squared
) -> None:
    assert squared(1) == time_squared.SecondSquared(seconds_squared)


def test_the_time_squared_table_lists_the_units_by_symbol() -> None:
    assert set(time_squared.TIME_SQUARED_UNITS) == {
        f"ns{symbols.SUPERSCRIPT_TWO}",
        f"{symbols.MICRO}s{symbols.SUPERSCRIPT_TWO}",
        f"ms{symbols.SUPERSCRIPT_TWO}",
        f"s{symbols.SUPERSCRIPT_TWO}",
        f"min{symbols.SUPERSCRIPT_TWO}",
        f"h{symbols.SUPERSCRIPT_TWO}",
    }


@pytest.mark.parametrize(
    ("rate", "squared"),
    [
        (angvel.TurnPerSecond, angvel2.TurnSquaredPerSecondSquared),
        (angvel.RadianPerSecond, angvel2.RadianSquaredPerSecondSquared),
        (angvel.DegreePerSecond, angvel2.DegreeSquaredPerSecondSquared),
    ],
    ids=["turn", "radian", "degree"],
)
def test_a_rate_times_itself_is_the_squared_unit(rate, squared) -> None:
    assert rate(3) * rate(3) == squared(9)


def test_a_turn_squared_is_two_pi_squared_radians_squared() -> None:
    turns = angvel2.TurnSquaredPerSecondSquared(1)
    assert turns == angvel2.RadianSquaredPerSecondSquared((2 * PI) ** 2)


def test_a_turn_squared_is_129600_degrees_squared() -> None:
    turns = angvel2.TurnSquaredPerSecondSquared(1)
    assert turns == angvel2.DegreeSquaredPerSecondSquared(129_600)


def test_the_angular_velocity_squared_table_lists_the_units_by_symbol() -> None:
    assert set(angvel2.ANGULAR_VELOCITY_SQUARED_UNITS) == {
        f"tr{symbols.SUPERSCRIPT_TWO}/s{symbols.SUPERSCRIPT_TWO}",
        f"rad{symbols.SUPERSCRIPT_TWO}/s{symbols.SUPERSCRIPT_TWO}",
        f"{symbols.DEGREE}{symbols.SUPERSCRIPT_TWO}/s{symbols.SUPERSCRIPT_TWO}",
    }
