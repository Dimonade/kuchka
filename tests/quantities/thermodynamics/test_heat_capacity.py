"""Heat capacity and specific heat capacity: energy per degree, and per mass degree."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Celsius
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import Energy
from kuchka import HeatCapacity
from kuchka import HeatingRate
from kuchka import IncompatibleDimensionError
from kuchka import Joule
from kuchka import JoulePerKilogram
from kuchka import Kilogram
from kuchka import Power
from kuchka import SpecificEnergy
from kuchka import SpecificHeatCapacity
from kuchka import TemperatureDelta
from kuchka import Watt
from kuchka import parse
from kuchka.units.mechanics.velocity_squared import SquareMetrePerSecondSquared
from kuchka.units.thermodynamics import heat_capacity as hc
from kuchka.units.thermodynamics import heating_rate
from kuchka.units.thermodynamics import specific_heat_capacity as shc


def test_an_energy_over_a_temperature_difference_is_a_heat_capacity() -> None:
    result = Joule(12) / DeltaKelvin(3)
    assert type(result) is HeatCapacity
    assert result == hc.JoulePerKelvin(4)
    assert Joule(12) / DeltaCelsius(3) == result


def test_a_heat_capacity_times_a_difference_is_the_heat_in_either_order() -> None:
    capacity = hc.KilojoulePerKelvin(1.2)
    heat = capacity * DeltaKelvin(80)
    assert type(heat) is Energy
    assert heat == Joule(96_000)
    assert DeltaKelvin(80) * capacity == heat


def test_an_energy_over_a_heat_capacity_is_a_temperature_difference() -> None:
    rise = Joule(96_000) / hc.KilojoulePerKelvin(1.2)
    assert type(rise) is TemperatureDelta
    assert rise == DeltaKelvin(80)


def test_a_power_and_a_heat_capacity_give_a_heating_rate_and_back() -> None:
    capacity = hc.JoulePerKelvin(4)
    rate = Watt(8) / capacity
    assert type(rate) is HeatingRate
    assert rate == heating_rate.KelvinPerSecond(2)
    power = capacity * rate
    assert type(power) is Power
    assert power == Watt(8)


def test_a_heat_capacity_over_a_mass_is_a_specific_heat_capacity_and_back() -> None:
    specific = hc.JoulePerKelvin(4) / Kilogram(2)
    assert type(specific) is SpecificHeatCapacity
    assert specific == shc.JoulePerKilogramKelvin(2)
    capacity = specific * Kilogram(2)
    assert type(capacity) is HeatCapacity
    assert Kilogram(2) * specific == capacity
    assert capacity == hc.JoulePerKelvin(4)


def test_a_specific_energy_over_a_difference_is_a_specific_heat_capacity() -> None:
    result = JoulePerKilogram(6) / DeltaKelvin(3)
    assert type(result) is SpecificHeatCapacity
    assert result == shc.JoulePerKilogramKelvin(2)
    assert JoulePerKilogram(6) / result == DeltaKelvin(3)


def test_a_specific_heat_capacity_times_a_difference_is_a_specific_energy() -> None:
    result = shc.JoulePerKilogramKelvin(2) * DeltaKelvin(3)
    assert type(result) is SpecificEnergy
    assert result == JoulePerKilogram(6)
    assert DeltaKelvin(3) * shc.JoulePerKilogramKelvin(2) == result


def test_the_heat_of_a_mass_is_the_same_however_it_is_grouped() -> None:
    water = shc.KilojoulePerKilogramKelvin(4.184)
    by_capacity = (water * Kilogram(2)) * DeltaKelvin(30)
    by_specific_energy = (water * DeltaKelvin(30)) * Kilogram(2)
    by_mass_first = Kilogram(2) * (water * DeltaKelvin(30))
    assert type(by_capacity) is Energy
    assert by_capacity == by_specific_energy == by_mass_first == Joule(251_040)


def test_a_velocity_squared_over_a_difference_is_also_a_specific_heat_capacity() -> (
    None
):
    result = SquareMetrePerSecondSquared(6) / DeltaKelvin(3)
    assert type(result) is SpecificHeatCapacity
    assert result == shc.JoulePerKilogramKelvin(2)


def test_a_temperature_reading_is_not_a_difference() -> None:
    with pytest.raises(TypeError):
        Joule(1) / Celsius(20)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_heat_capacity_does_not_mix_with_other_kinds() -> None:
    with pytest.raises(IncompatibleDimensionError):
        hc.JoulePerKelvin(1) + shc.JoulePerKilogramKelvin(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        hc.JoulePerKelvin(1) + Joule(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_units_are_exact() -> None:
    assert hc.KilojoulePerKelvin(1) == hc.JoulePerKelvin(1000)
    assert shc.KilojoulePerKilogramKelvin(1) == shc.JoulePerKilogramKelvin(1000)
    assert shc.ThermochemicalCaloriePerGramKelvin(1) == (
        shc.JoulePerKilogramKelvin(4184)
    )
    assert shc.KilojoulePerKilogramKelvin(Fraction(4184, 1000)) == (
        shc.ThermochemicalCaloriePerGramKelvin(1)
    )


def test_a_celsius_degree_in_the_denominator_is_a_kelvin() -> None:
    assert parse("1.2 kJ/\u00b0C", HeatCapacity) == hc.KilojoulePerKelvin(1.2)
    assert parse("4184 J/(kg\u00b7\u00b0C)", SpecificHeatCapacity) == (
        shc.ThermochemicalCaloriePerGramKelvin(1)
    )


def test_the_texts_are_read_by_the_quantity_they_are_given() -> None:
    assert parse("385 J/K", HeatCapacity) == hc.JoulePerKelvin(385)
    assert parse("4.184 kJ/kg/K", SpecificHeatCapacity) == (
        shc.KilojoulePerKilogramKelvin(4.184)
    )
    assert parse("1 cal/(g K)", SpecificHeatCapacity) == (
        shc.ThermochemicalCaloriePerGramKelvin(1)
    )
    assert parse("0.385 kJ/(kg*K)", SpecificHeatCapacity) == (
        shc.JoulePerKilogramKelvin(385)
    )
