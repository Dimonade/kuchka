"""VelocitySquared: a velocity times a velocity, beside the specific energy.

The generic contracts run for every unit of the table; this module covers what is
specific to a squared velocity.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import Energy
from kuchka import IncompatibleDimensionError
from kuchka import Length
from kuchka import Pressure
from kuchka import SpecificEnergy
from kuchka import VelocitySquared
from kuchka import parse
from kuchka.units import length
from kuchka.units import mass
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import density
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import specific_energy as se
from kuchka.units.mechanics import velocity_squared as vs


def test_a_velocity_times_a_velocity_is_a_velocity_squared() -> None:
    squared = velocity.MetrePerSecond(3) * velocity.MetrePerSecond(4)
    assert type(squared) is VelocitySquared
    assert squared == vs.SquareMetrePerSecondSquared(12)


def test_a_square_kilometre_per_second_squared_is_exactly_a_million() -> None:
    assert vs.SquareKilometrePerSecondSquared(1) == vs.SquareMetrePerSecondSquared(
        1_000_000
    )
    assert velocity.KilometrePerHour(36) * velocity.KilometrePerHour(36) == (
        vs.SquareMetrePerSecondSquared(100)
    )


def test_the_products_and_quotients_of_a_velocity_squared() -> None:
    squared = vs.SquareMetrePerSecondSquared(9)
    assert type(squared * mass.Kilogram(2)) is Energy
    assert type(squared / length.Metre(3)) is Acceleration
    assert type(squared / (squared / length.Metre(3))) is Length


def test_a_density_times_a_velocity_squared_is_a_pressure() -> None:
    squared = velocity.MetrePerSecond(10) * velocity.MetrePerSecond(10)
    dynamic = density.KilogramPerCubicMetre(Fraction(6, 5)) * squared / 2
    assert type(dynamic) is Pressure
    assert dynamic == pressure.Pascal(60)


def test_a_velocity_squared_converts_to_its_kinetic_energy_per_mass() -> None:
    squared = velocity.MetrePerSecond(4) * velocity.MetrePerSecond(4)
    assert type(squared.to_specific_energy()) is SpecificEnergy
    assert squared.to_specific_energy() == se.JoulePerKilogram(8)
    assert VelocitySquared.from_specific_energy(se.JoulePerKilogram(8)) == squared


def test_the_two_do_not_mix_without_a_conversion() -> None:
    squared = vs.SquareMetrePerSecondSquared(16)
    with pytest.raises(IncompatibleDimensionError, match="to_specific_energy"):
        squared + se.JoulePerKilogram(1)  # type: ignore[operator]
    assert squared != se.JoulePerKilogram(16)


def test_text_resolves_through_the_table() -> None:
    assert parse("9 m²/s²", VelocitySquared) == vs.SquareMetrePerSecondSquared(9)
    assert parse("9 m^2/s^2", VelocitySquared) == vs.SquareMetrePerSecondSquared(9)
    assert parse("9 km**2/s**2", VelocitySquared) == vs.SquareKilometrePerSecondSquared(
        9
    )
