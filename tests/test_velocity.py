"""Velocity: the arithmetic that produces it, its inverses, and its prefixed units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Velocity: the `Length / Time` relationship and
its inverses, `Velocity / Time -> Acceleration` and its inverse, and the two non-SI
units, `KilometrePerHour` and `MilePerHour`.
"""

from decimal import Decimal
from fractions import Fraction

from kuchka import Acceleration
from kuchka import KilometrePerHour
from kuchka import Length
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import MetrePerSecondSquared
from kuchka import MilePerHour
from kuchka import Second
from kuchka import Time
from kuchka import Velocity
from kuchka.units import KILOMETRE_PER_HOUR
from kuchka.units import MILE_PER_HOUR
from kuchka.units import KilometerPerHour


def test_length_divided_by_time_is_velocity():
    velocity = Metre(10) / Second(2)
    assert isinstance(velocity, Velocity)
    assert velocity == MetrePerSecond(5)


def test_velocity_times_time_is_length():
    distance = MetrePerSecond(5) * Second(2)
    assert isinstance(distance, Length)
    assert distance == Metre(10)


def test_length_divided_by_velocity_is_time():
    duration = Metre(10) / MetrePerSecond(5)
    assert isinstance(duration, Time)
    assert duration == Second(2)


def test_velocity_length_time_round_trip():
    original = Metre(42)
    duration = Second(6)
    velocity = original / duration
    assert velocity * duration == original


def test_isinstance_of_velocity():
    assert isinstance(MetrePerSecond(1), Velocity)


def test_velocity_divided_by_time_is_acceleration():
    acceleration = MetrePerSecond(10) / Second(2)
    assert isinstance(acceleration, Acceleration)
    assert acceleration == MetrePerSecondSquared(5)


def test_velocity_divided_by_acceleration_is_time():
    duration = MetrePerSecond(10) / MetrePerSecondSquared(5)
    assert isinstance(duration, Time)
    assert duration == Second(2)


def test_velocity_acceleration_time_round_trip():
    original = MetrePerSecond(20)
    duration = Second(4)
    acceleration = original / duration
    assert acceleration * duration == original


def test_kilometre_per_hour_scale_is_exact():
    assert KilometrePerHour(1).magnitude == Fraction(5, 18)


def test_kilometre_per_hour_converts_exactly():
    assert KilometrePerHour(36) == MetrePerSecond(10)


def test_kilometre_per_hour_round_trip():
    original = MetrePerSecond(10)
    assert original.to(KILOMETRE_PER_HOUR).to(MetrePerSecond(1).unit) == original


def test_kilometer_per_hour_is_an_alias():
    assert KilometerPerHour is KilometrePerHour


def test_mile_per_hour_scale_is_exact():
    """A mile has been exactly 1609.344 m since 1959, so mph converts exactly too."""
    assert MilePerHour(1).magnitude == Decimal("0.44704")


def test_mile_per_hour_converts_exactly():
    assert MilePerHour(1).to(MILE_PER_HOUR).value_in(MILE_PER_HOUR) == Decimal(1)
    assert MilePerHour(100) == MetrePerSecond(Decimal("44.704"))


def test_mile_per_hour_round_trip():
    original = MetrePerSecond(Decimal("44.704"))
    assert original.to(MILE_PER_HOUR) == MilePerHour(100)


def test_kilometre_per_hour_and_mile_per_hour_mix_freely():
    """Both are ordinary Velocity, so arithmetic between them needs no conversion."""
    assert isinstance(KilometrePerHour(10) + MilePerHour(10), Velocity)


def test_isinstance_of_kilometre_per_hour_and_mile_per_hour():
    assert isinstance(KilometrePerHour(5), Velocity)
    assert isinstance(MilePerHour(5), Velocity)


def test_ordering_between_kilometre_per_hour_and_mile_per_hour():
    """1 mph (0.44704 m/s) is faster than 1 km/h (~0.2778 m/s)."""
    assert MilePerHour(1) > KilometrePerHour(1)
