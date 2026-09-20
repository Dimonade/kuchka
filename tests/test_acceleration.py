"""Acceleration: the arithmetic that produces it, and its role in Newton's second law.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Acceleration:
`Velocity / Time -> Acceleration` and its inverse (spelled out alongside `Velocity`'s
own tests), and `Mass * Acceleration -> Force` -- F = ma -- and its two inverses.
"""

from kuchka import Acceleration
from kuchka import Force
from kuchka import Kilogram
from kuchka import Mass
from kuchka import MetrePerSecond
from kuchka import MetrePerSecondSquared
from kuchka import Newton
from kuchka import Second


def test_mass_times_acceleration_is_force():
    force = Kilogram(2) * MetrePerSecondSquared(5)
    assert isinstance(force, Force)
    assert force == Newton(10)


def test_acceleration_times_mass_is_force_commutatively():
    force_a = Kilogram(2) * MetrePerSecondSquared(5)
    force_b = MetrePerSecondSquared(5) * Kilogram(2)
    assert force_a == force_b


def test_force_divided_by_mass_is_acceleration():
    acceleration = Newton(10) / Kilogram(2)
    assert isinstance(acceleration, Acceleration)
    assert acceleration == MetrePerSecondSquared(5)


def test_force_divided_by_acceleration_is_mass():
    mass = Newton(10) / MetrePerSecondSquared(5)
    assert isinstance(mass, Mass)
    assert mass == Kilogram(2)


def test_newtons_second_law_round_trip():
    mass = Kilogram(70)
    acceleration = MetrePerSecondSquared(2)
    force = mass * acceleration
    assert force / mass == acceleration
    assert force / acceleration == mass


def test_acceleration_times_time_is_velocity():
    velocity = MetrePerSecondSquared(5) * Second(2)
    assert velocity == MetrePerSecond(10)


def test_time_times_acceleration_is_velocity_commutatively():
    assert Second(2) * MetrePerSecondSquared(5) == MetrePerSecondSquared(5) * Second(2)


def test_isinstance_of_acceleration():
    assert isinstance(MetrePerSecondSquared(1), Acceleration)


def test_scalar_multiplication_and_division():
    assert MetrePerSecondSquared(2) * 3 == MetrePerSecondSquared(6)
    assert MetrePerSecondSquared(6) / 3 == MetrePerSecondSquared(2)


def test_ordering_within_acceleration():
    assert MetrePerSecondSquared(1) < MetrePerSecondSquared(2)
