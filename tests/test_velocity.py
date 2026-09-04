"""Velocity: the arithmetic that produces it and its two inverses.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Velocity:
the `Length / Time` relationship and its inverses.
"""

from kuchka import Length
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import Second
from kuchka import Time
from kuchka import Velocity


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
