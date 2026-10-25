"""Acceleration: the arithmetic that produces it, and its role in Newton's second law.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Acceleration:
`Velocity / Time -> Acceleration` and its inverse (spelled out alongside `Velocity`'s
own tests), and `Mass * Acceleration -> Force` -- F = ma -- and its two inverses.
"""

from decimal import Decimal

import pytest

from kuchka.quantities import Acceleration
from kuchka.units import length
from kuchka.units import mass
from kuchka.units import temporal
from kuchka.units.kinematics import acceleration as acc
from kuchka.units.kinematics import velocity


def test_newtons_second_law_round_trip():
    m = mass.Kilogram(70)
    a = acc.MetrePerSecondSquared(2)
    f = m * a
    assert f / m == a
    assert f / a == m


def test_isinstance_of_acceleration():
    assert isinstance(acc.MetrePerSecondSquared(1), Acceleration)


def test_scalar_multiplication_and_division():
    assert acc.MetrePerSecondSquared(2) * 3 == acc.MetrePerSecondSquared(6)
    assert acc.MetrePerSecondSquared(6) / 3 == acc.MetrePerSecondSquared(2)


def test_ordering_within_acceleration():
    assert acc.MetrePerSecondSquared(1) < acc.MetrePerSecondSquared(2)


def test_metric_and_american_acceleration_names_are_true_aliases() -> None:
    assert acc.MeterPerSecondSquared is acc.MetrePerSecondSquared
    assert acc.METER_PER_SECOND_SQUARED is acc.METRE_PER_SECOND_SQUARED


def test_gal_converts_exactly_to_si_acceleration() -> None:
    assert acc.Gal(100) == acc.MetrePerSecondSquared(1)


def test_milligal_converts_exactly_to_si_acceleration() -> None:
    assert acc.Milligal(1) == acc.MetrePerSecondSquared(Decimal("0.00001"))


def test_microgal_converts_exactly_to_si_acceleration() -> None:
    assert acc.Microgal(1) == acc.MetrePerSecondSquared(Decimal("0.00000001"))


def test_acceleration_changes_velocity_over_time() -> None:
    acceleration_value = acc.MetrePerSecondSquared(3)

    assert acceleration_value * temporal.Second(4) == velocity.MetrePerSecond(12)


def test_constant_braking_gives_expected_stopping_time() -> None:
    initial_speed = velocity.KilometrePerHour(90)
    braking = acc.MetrePerSecondSquared(-5)

    assert -initial_speed / braking == temporal.Second(5)


@pytest.mark.xfail(
    reason="Time ** int is not implemented yet",
    strict=True,
)
def test_constant_braking_gives_expected_stopping_distance() -> None:
    initial_speed = velocity.KilometrePerHour(90)
    braking = acc.MetrePerSecondSquared(-5)
    stopping_time = -initial_speed / braking

    stopping_distance = initial_speed * stopping_time + braking * stopping_time**2 / 2  # ty: ignore[unsupported-operator]  # type: ignore[operator]

    assert stopping_distance == length.Metre(62.5)
