"""Momentum: its units, and the products that produce it and that it takes part in.

The generic contracts run for every unit of the table; this module covers what is
specific to momentum.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from kuchka import Energy
from kuchka import Force
from kuchka import IncompatibleDimensionError
from kuchka import Mass
from kuchka import Momentum
from kuchka import Velocity
from kuchka import parse
from kuchka.units import mass
from kuchka.units import temporal
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import impulse
from kuchka.units.mechanics import momentum as mom


def test_the_units_are_exact_multiples_of_the_kilogram_metre_per_second() -> None:
    assert mom.GramCentimetrePerSecond(100_000) == mom.KilogramMetrePerSecond(1)
    assert mom.PoundFootPerSecond(1) == mom.KilogramMetrePerSecond(
        Decimal("0.138254954376")
    )


def test_a_mass_times_a_velocity_is_a_momentum() -> None:
    cart = mass.Kilogram(2) * velocity.MetrePerSecond(3)
    assert type(cart) is Momentum
    assert cart == mom.KilogramMetrePerSecond(6)
    assert type(velocity.MetrePerSecond(3) * mass.Kilogram(2)) is Momentum


def test_a_kinetic_energy_is_written_without_brackets() -> None:
    speed = velocity.MetrePerSecond(3)
    kinetic = mass.Kilogram(2) * speed * speed / 2
    assert type(kinetic) is Energy
    assert kinetic == energy.Joule(9)


def test_the_quotients_of_a_momentum() -> None:
    cart = mom.KilogramMetrePerSecond(6)
    assert type(cart / mass.Kilogram(2)) is Velocity
    assert type(cart / velocity.MetrePerSecond(3)) is Mass
    assert type(cart / temporal.Second(2)) is Force
    assert cart / temporal.Second(2) == impulse.NewtonSecond(3) / temporal.Second(1)


def test_text_resolves_through_the_table() -> None:
    assert parse("6 kg·m/s", Momentum) == mom.KilogramMetrePerSecond(6)
    assert parse("6 kg*m/s", Momentum) == mom.KilogramMetrePerSecond(6)
    assert parse("6 kg⋅m/s", Momentum) == mom.KilogramMetrePerSecond(6)
    assert parse("3 g cm/s", Momentum) == mom.GramCentimetrePerSecond(3)


def test_an_impulse_does_not_stand_in_for_a_momentum() -> None:
    with pytest.raises(IncompatibleDimensionError, match=r"to_momentum"):
        mom.KilogramMetrePerSecond(1) + impulse.NewtonSecond(1)  # type: ignore[operator]
