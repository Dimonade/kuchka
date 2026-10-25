"""Velocity: the arithmetic that produces it, its inverses, and its prefixed units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Velocity: the `Length / Time` relationship and
its inverses, `Velocity / Time -> Acceleration` and its inverse, and the two non-SI
units, `KilometrePerHour` and `MilePerHour`.
"""

from decimal import Decimal
from fractions import Fraction

from kuchka import Velocity
from kuchka.units import length
from kuchka.units.kinematics import velocity as velocity_units
from kuchka.units.temporal import time


def test_velocity_length_time_round_trip():
    original = length.Metre(42)
    duration = time.Second(6)
    velocity = original / duration
    assert velocity * duration == original


def test_isinstance_of_velocity():
    assert isinstance(velocity_units.MetrePerSecond(1), Velocity)


def test_velocity_acceleration_time_round_trip():
    original = velocity_units.MetrePerSecond(20)
    duration = time.Second(4)
    acceleration = original / duration
    assert acceleration * duration == original


def test_kilometre_per_hour_scale_is_exact():
    assert velocity_units.KilometrePerHour(1).magnitude == Fraction(5, 18)


def test_kilometre_per_hour_converts_exactly():
    assert velocity_units.KilometrePerHour(36) == velocity_units.MetrePerSecond(10)


def test_kilometre_per_hour_round_trip():
    original = velocity_units.MetrePerSecond(10)
    assert (
        original.to(velocity_units.KILOMETRE_PER_HOUR).to(
            velocity_units.MetrePerSecond(1).unit
        )
        == original
    )


def test_kilometer_per_hour_is_an_alias():
    assert velocity_units.KilometerPerHour is velocity_units.KilometrePerHour


def test_mile_per_hour_scale_is_exact():
    """A mile has been exactly 1609.344 m since 1959, so mph converts exactly too."""
    assert velocity_units.MilePerHour(1).magnitude == Decimal("0.44704")


def test_mile_per_hour_converts_exactly():
    assert velocity_units.MilePerHour(1).to(velocity_units.MILE_PER_HOUR).value_in(
        velocity_units.MILE_PER_HOUR
    ) == Decimal(1)
    assert velocity_units.MilePerHour(100) == velocity_units.MetrePerSecond(
        Decimal("44.704")
    )


def test_mile_per_hour_round_trip():
    original = velocity_units.MetrePerSecond(Decimal("44.704"))
    assert original.to(velocity_units.MILE_PER_HOUR) == velocity_units.MilePerHour(100)


def test_kilometre_per_hour_and_mile_per_hour_mix_freely():
    """Both are ordinary Velocity, so arithmetic between them needs no conversion."""
    assert isinstance(
        velocity_units.KilometrePerHour(10) + velocity_units.MilePerHour(10), Velocity
    )


def test_isinstance_of_kilometre_per_hour_and_mile_per_hour():
    assert isinstance(velocity_units.KilometrePerHour(5), Velocity)
    assert isinstance(velocity_units.MilePerHour(5), Velocity)


def test_ordering_between_kilometre_per_hour_and_mile_per_hour():
    """1 mph (0.44704 m/s) is faster than 1 km/h (~0.2778 m/s)."""
    assert velocity_units.MilePerHour(1) > velocity_units.KilometrePerHour(1)


def test_knot_converts_exactly_to_metres_per_second() -> None:
    assert velocity_units.Knot(1).to(velocity_units.METRE_PER_SECOND) == Velocity(
        Fraction(463, 900),
        velocity_units.METRE_PER_SECOND,
    )


def test_kilometres_per_hour_to_metres_per_second_is_exact() -> None:
    assert velocity_units.KilometrePerHour(90).to(velocity_units.METRE_PER_SECOND) == (
        velocity_units.MetrePerSecond(Fraction(25))
    )


def test_miles_per_hour_conversion_is_exact() -> None:
    assert velocity_units.MilePerHour(60).to(velocity_units.METRE_PER_SECOND) == (
        velocity_units.MetrePerSecond(Decimal("26.8224"))
    )
