"""Jerk: the arithmetic that produces it, its units, and the time cube it pairs with."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import Frequency
from kuchka import Jerk
from kuchka import Length
from kuchka import Time
from kuchka import TimeCubed
from kuchka import Velocity
from kuchka.internal import symbols
from kuchka.units import length
from kuchka.units import temporal
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import jerk
from kuchka.units.kinematics import time_cubed
from kuchka.units.kinematics import velocity

RAMP = jerk.MetrePerSecondCubed(6)
DURATION = temporal.Second(2)


def test_an_acceleration_over_a_time_is_a_jerk() -> None:
    rate = acceleration.MetrePerSecondSquared(3) / temporal.Second(2)
    assert type(rate) is Jerk
    assert rate == jerk.MetrePerSecondCubed(Fraction(3, 2))


def test_an_acceleration_times_a_frequency_is_a_jerk() -> None:
    rate = acceleration.MetrePerSecondSquared(6) * temporal.Hertz(2)
    assert type(rate) is Jerk
    assert rate == jerk.MetrePerSecondCubed(12)


def test_a_velocity_over_a_time_squared_is_a_jerk() -> None:
    rate = velocity.MetrePerSecond(24) / (DURATION * DURATION)
    assert type(rate) is Jerk
    assert rate == jerk.MetrePerSecondCubed(6)


def test_a_length_over_a_time_cubed_is_a_jerk() -> None:
    rate = length.Metre(48) / time_cubed.SecondCubed(8)
    assert type(rate) is Jerk
    assert rate == jerk.MetrePerSecondCubed(6)


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda j, t: j * t, Acceleration, acceleration.MetrePerSecondSquared(12)),
        (lambda j, t: t * j, Acceleration, acceleration.MetrePerSecondSquared(12)),
        (lambda j, t: j * t * t, Velocity, velocity.MetrePerSecond(24)),
        (lambda j, t: t * t * j, Velocity, velocity.MetrePerSecond(24)),
        (lambda j, t: t * j * t, Velocity, velocity.MetrePerSecond(24)),
        (lambda j, t: j * t * t * t, Length, length.Metre(48)),
        (lambda j, t: t * (t * (t * j)), Length, length.Metre(48)),
        (lambda j, t: j * t**3, Length, length.Metre(48)),
        (lambda j, t: t**3 * j, Length, length.Metre(48)),
    ],
    ids=[
        "j*t",
        "t*j",
        "j*t*t",
        "t*t*j",
        "t*j*t",
        "j*t*t*t",
        "t*(t*(t*j))",
        "j*t**3",
        "t**3*j",
    ],
)
def test_a_jerk_over_time_has_one_value_in_every_order(
    build, expected_type, expected
) -> None:
    result = build(RAMP, DURATION)
    assert type(result) is expected_type
    assert result == expected


def test_an_acceleration_over_a_jerk_is_the_time_to_build_it_up() -> None:
    build_up = acceleration.MetrePerSecondSquared(12) / RAMP
    assert type(build_up) is Time
    assert build_up == temporal.Second(2)


def test_a_jerk_over_an_acceleration_is_a_frequency() -> None:
    rate = RAMP / acceleration.MetrePerSecondSquared(3)
    assert type(rate) is Frequency
    assert rate == temporal.Hertz(2)


def test_a_product_of_three_durations_is_a_time_cubed() -> None:
    cubed = DURATION * DURATION * DURATION
    assert type(cubed) is TimeCubed
    assert cubed == time_cubed.SecondCubed(8)


def test_a_time_cubed_per_time_is_a_time_squared() -> None:
    squared = time_cubed.SecondCubed(8) / DURATION
    assert squared == temporal.Second(2) * temporal.Second(2)


def test_the_units_of_a_jerk_have_exact_scales() -> None:
    assert jerk.MillimetrePerSecondCubed(1) == jerk.MetrePerSecondCubed(
        Decimal("0.001")
    )
    assert jerk.MillimetrePerSecondCubed(5000) == jerk.MetrePerSecondCubed(5)


def test_metric_and_american_jerk_names_are_true_aliases() -> None:
    assert jerk.MeterPerSecondCubed is jerk.MetrePerSecondCubed
    assert jerk.METER_PER_SECOND_CUBED is jerk.METRE_PER_SECOND_CUBED
    assert jerk.MillimeterPerSecondCubed is jerk.MillimetrePerSecondCubed
    assert jerk.MILLIMETER_PER_SECOND_CUBED is jerk.MILLIMETRE_PER_SECOND_CUBED


def test_the_jerk_table_lists_the_units_by_symbol() -> None:
    assert set(jerk.JERK_UNITS) == {
        f"m/s{symbols.SUPERSCRIPT_THREE}",
        f"mm/s{symbols.SUPERSCRIPT_THREE}",
    }


def test_a_jerk_displays_in_its_own_unit() -> None:
    assert str(jerk.MillimetrePerSecondCubed(500)) == "500 mm/s³"
    assert str(RAMP * DURATION) == "12 m/s²"
