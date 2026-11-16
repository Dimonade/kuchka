"""Snap: its arithmetic, its units, and the fourth power of time it pairs with."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import Frequency
from kuchka import Jerk
from kuchka import Length
from kuchka import Snap
from kuchka import Time
from kuchka import TimeFourthPower
from kuchka import Velocity
from kuchka.internal import symbols
from kuchka.units import length
from kuchka.units import temporal
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import jerk
from kuchka.units.kinematics import snap
from kuchka.units.kinematics import time_cubed
from kuchka.units.kinematics import time_fourth_power as fourth
from kuchka.units.kinematics import velocity

JOUNCE = snap.MetrePerSecondFourthPower(3)
DURATION = temporal.Second(2)


def test_a_jerk_over_a_time_is_a_snap() -> None:
    rate = jerk.MetrePerSecondCubed(3) / temporal.Second(2)
    assert type(rate) is Snap
    assert rate == snap.MetrePerSecondFourthPower(Fraction(3, 2))


def test_a_jerk_times_a_frequency_is_a_snap() -> None:
    rate = jerk.MetrePerSecondCubed(6) * temporal.Hertz(2)
    assert type(rate) is Snap
    assert rate == snap.MetrePerSecondFourthPower(12)


def test_an_acceleration_over_a_time_squared_is_a_snap() -> None:
    rate = acceleration.MetrePerSecondSquared(12) / (DURATION * DURATION)
    assert type(rate) is Snap
    assert rate == snap.MetrePerSecondFourthPower(3)


def test_a_velocity_over_a_time_cubed_is_a_snap() -> None:
    rate = velocity.MetrePerSecond(24) / time_cubed.SecondCubed(8)
    assert type(rate) is Snap
    assert rate == snap.MetrePerSecondFourthPower(3)


def test_a_length_over_a_time_to_the_fourth_power_is_a_snap() -> None:
    rate = length.Metre(48) / fourth.SecondFourthPower(16)
    assert type(rate) is Snap
    assert rate == snap.MetrePerSecondFourthPower(3)


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda s, t: s * t, Jerk, jerk.MetrePerSecondCubed(6)),
        (lambda s, t: t * s, Jerk, jerk.MetrePerSecondCubed(6)),
        (lambda s, t: s * t * t, Acceleration, acceleration.MetrePerSecondSquared(12)),
        (lambda s, t: t * s * t, Acceleration, acceleration.MetrePerSecondSquared(12)),
        (lambda s, t: s * t * t * t, Velocity, velocity.MetrePerSecond(24)),
        (lambda s, t: s * t**3, Velocity, velocity.MetrePerSecond(24)),
        (lambda s, t: s * t * t * t * t, Length, length.Metre(48)),
        (lambda s, t: t * (t * (t * (t * s))), Length, length.Metre(48)),
        (lambda s, t: s * t**4, Length, length.Metre(48)),
        (lambda s, t: t**4 * s, Length, length.Metre(48)),
        (lambda s, t: s * (t * t) ** 2, Length, length.Metre(48)),
    ],
    ids=[
        "s*t",
        "t*s",
        "s*t*t",
        "t*s*t",
        "s*t*t*t",
        "s*t**3",
        "s*t*t*t*t",
        "t*(t*(t*(t*s)))",
        "s*t**4",
        "t**4*s",
        "s*(t*t)**2",
    ],
)
def test_a_snap_over_time_has_one_value_in_every_order(
    build, expected_type, expected
) -> None:
    result = build(JOUNCE, DURATION)
    assert type(result) is expected_type
    assert result == expected


def test_a_jerk_over_a_snap_is_the_time_to_build_it_up() -> None:
    build_up = jerk.MetrePerSecondCubed(6) / JOUNCE
    assert type(build_up) is Time
    assert build_up == temporal.Second(2)


def test_a_snap_over_a_jerk_is_a_frequency() -> None:
    rate = JOUNCE / jerk.MetrePerSecondCubed(Fraction(3, 2))
    assert type(rate) is Frequency
    assert rate == temporal.Hertz(2)


def test_four_durations_are_a_time_to_the_fourth_power_in_every_grouping() -> None:
    powered = DURATION * DURATION * DURATION * DURATION
    assert type(powered) is TimeFourthPower
    assert powered == fourth.SecondFourthPower(16)
    assert powered == DURATION**4
    assert powered == (DURATION * DURATION) ** 2
    assert powered == DURATION * DURATION**3
    assert powered == DURATION**2 * DURATION**2


def test_the_units_of_a_snap_have_exact_scales() -> None:
    assert snap.MillimetrePerSecondFourthPower(1) == snap.MetrePerSecondFourthPower(
        Decimal("0.001")
    )
    assert snap.MillimetrePerSecondFourthPower(5000) == snap.MetrePerSecondFourthPower(
        5
    )


def test_metric_and_american_snap_names_are_true_aliases() -> None:
    assert snap.MeterPerSecondFourthPower is snap.MetrePerSecondFourthPower
    assert snap.METER_PER_SECOND_FOURTH_POWER is snap.METRE_PER_SECOND_FOURTH_POWER
    assert snap.MillimeterPerSecondFourthPower is snap.MillimetrePerSecondFourthPower


def test_the_snap_table_lists_the_units_by_symbol() -> None:
    assert set(snap.SNAP_UNITS) == {
        f"m/s{symbols.SUPERSCRIPT_FOUR}",
        f"mm/s{symbols.SUPERSCRIPT_FOUR}",
    }


def test_a_snap_displays_in_its_own_unit() -> None:
    assert str(snap.MillimetrePerSecondFourthPower(500)) == "500 mm/s⁴"
    assert str(JOUNCE * DURATION) == "6 m/s³"
