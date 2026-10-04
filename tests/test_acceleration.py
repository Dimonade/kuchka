"""Acceleration: the arithmetic that produces it, and its role in Newton's second law.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Acceleration:
`Velocity / Time -> Acceleration` and its inverse (spelled out alongside `Velocity`'s
own tests), and `Mass * Acceleration -> Force` -- F = ma -- and its two inverses.
"""

from decimal import Decimal

import pytest

from kuchka import Acceleration
from kuchka import Force
from kuchka import Gal
from kuchka import Kilogram
from kuchka import KilometrePerHour
from kuchka import Kilonewton
from kuchka import Mass
from kuchka import MeterPerSecondSquared
from kuchka import Metre
from kuchka import MetrePerSecond
from kuchka import MetrePerSecondSquared
from kuchka import Microgal
from kuchka import Milligal
from kuchka import Newton
from kuchka import Second
from kuchka.units import METER_PER_SECOND_SQUARED
from kuchka.units import METRE_PER_SECOND_SQUARED


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


def test_metric_and_american_acceleration_names_are_true_aliases() -> None:
    assert MeterPerSecondSquared is MetrePerSecondSquared
    assert METER_PER_SECOND_SQUARED is METRE_PER_SECOND_SQUARED


def test_gal_converts_exactly_to_si_acceleration() -> None:
    assert Gal(100) == MetrePerSecondSquared(1)


def test_milligal_converts_exactly_to_si_acceleration() -> None:
    assert Milligal(1) == MetrePerSecondSquared(Decimal("0.00001"))


def test_microgal_converts_exactly_to_si_acceleration() -> None:
    assert Microgal(1) == MetrePerSecondSquared(Decimal("0.00000001"))


def test_acceleration_changes_velocity_over_time() -> None:
    acceleration_value = MetrePerSecondSquared(3)

    assert acceleration_value * Second(4) == MetrePerSecond(12)


def test_force_divided_by_mass_gives_acceleration() -> None:
    assert Kilonewton(3) / Kilogram(1500) == MetrePerSecondSquared(2)


def test_constant_braking_gives_expected_stopping_time() -> None:
    initial_speed = KilometrePerHour(90)
    braking = MetrePerSecondSquared(-5)

    assert -initial_speed / braking == Second(5)


@pytest.mark.xfail(
    reason="Time ** int is not implemented yet",
    strict=True,
)
def test_constant_braking_gives_expected_stopping_distance() -> None:
    initial_speed = KilometrePerHour(90)
    braking = MetrePerSecondSquared(-5)
    stopping_time = -initial_speed / braking

    stopping_distance = initial_speed * stopping_time + braking * stopping_time**2 / 2  # ty: ignore[unsupported-operator]  # type: ignore[operator]

    assert stopping_distance == Metre(62.5)
