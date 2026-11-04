"""Entropy and specific entropy: closed roles of heat capacity and specific heat."""

from __future__ import annotations

import pytest

from kuchka import DeltaKelvin
from kuchka import Energy
from kuchka import Entropy
from kuchka import HeatCapacity
from kuchka import IncompatibleDimensionError
from kuchka import Joule
from kuchka import Kilogram
from kuchka import Mass
from kuchka import Proportion
from kuchka import SpecificEntropy
from kuchka import SpecificHeatCapacity
from kuchka import parse
from kuchka.units.thermodynamics import entropy
from kuchka.units.thermodynamics import heat_capacity as hc
from kuchka.units.thermodynamics import specific_entropy
from kuchka.units.thermodynamics import specific_heat_capacity as shc


def test_a_heat_capacity_is_read_as_an_entropy_by_name() -> None:
    result = hc.KilojoulePerKelvin(1.2).to_entropy()
    assert type(result) is Entropy
    assert result.value_in(hc.KILOJOULE_PER_KELVIN) == hc.KilojoulePerKelvin(
        1.2
    ).value_in(hc.KILOJOULE_PER_KELVIN)
    assert repr(result) == "1.2 kJ/K"


def test_an_entropy_is_read_back_as_a_heat_capacity_by_name() -> None:
    capacity = hc.JoulePerKelvin(5).to_entropy().to_heat_capacity()
    assert type(capacity) is HeatCapacity
    assert capacity == hc.JoulePerKelvin(5)


def test_the_thermal_energy_of_a_constant_goes_through_the_heat_capacity() -> None:
    thermal = hc.JoulePerKelvin(5).to_entropy().to_heat_capacity() * DeltaKelvin(300)
    assert type(thermal) is Energy
    assert thermal == Joule(1500)


def test_an_entropy_times_a_temperature_difference_is_refused() -> None:
    change = hc.JoulePerKelvin(5).to_entropy()
    with pytest.raises(IncompatibleDimensionError, match="to_heat_capacity"):
        change * DeltaKelvin(2)
    with pytest.raises(IncompatibleDimensionError, match="to_heat_capacity"):
        DeltaKelvin(2) * change
    with pytest.raises(IncompatibleDimensionError):
        Joule(1) / change


def test_an_entropy_and_a_heat_capacity_do_not_add_or_compare() -> None:
    change = hc.JoulePerKelvin(5).to_entropy()
    with pytest.raises(IncompatibleDimensionError):
        change + hc.JoulePerKelvin(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        change < hc.JoulePerKelvin(5)  # type: ignore[operator]  # noqa: B015  # ty: ignore[unsupported-operator]


def test_an_entropy_scales_and_divides_by_itself() -> None:
    change = hc.JoulePerKelvin(6).to_entropy()
    assert change * 2 == hc.JoulePerKelvin(12).to_entropy()
    assert change + change == hc.JoulePerKelvin(12).to_entropy()
    ratio = change / hc.JoulePerKelvin(3).to_entropy()
    assert type(ratio) is Proportion


def test_an_entropy_over_a_mass_is_a_specific_entropy_and_back() -> None:
    change = hc.JoulePerKelvin(6).to_entropy()
    specific = change / Kilogram(2)
    assert type(specific) is SpecificEntropy
    assert specific == shc.JoulePerKilogramKelvin(3).to_specific_entropy()
    total = specific * Kilogram(2)
    assert type(total) is Entropy
    assert Kilogram(2) * specific == total
    assert total == change
    mass = change / specific
    assert type(mass) is Mass
    assert mass == Kilogram(2)


def test_a_specific_entropy_is_not_a_specific_heat_capacity() -> None:
    specific = shc.JoulePerKilogramKelvin(3).to_specific_entropy()
    assert type(specific.to_specific_heat_capacity()) is SpecificHeatCapacity
    with pytest.raises(IncompatibleDimensionError, match="to_specific_heat_capacity"):
        specific * DeltaKelvin(2)
    with pytest.raises(IncompatibleDimensionError):
        specific + shc.JoulePerKilogramKelvin(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_heat_capacity_over_a_mass_stays_a_specific_heat_capacity() -> None:
    result = hc.JoulePerKelvin(6) / Kilogram(2)
    assert type(result) is SpecificHeatCapacity


def test_the_calorie_per_kelvin_units_are_exact_and_shared() -> None:
    assert hc.ThermochemicalCaloriePerKelvin(1) == hc.JoulePerKelvin(4.184)
    assert hc.KilocaloriePerKelvin(1) == hc.ThermochemicalCaloriePerKelvin(1000)
    kept = hc.ThermochemicalCaloriePerKelvin(2).to_entropy()
    assert repr(kept) == "2 cal/K"


def test_the_entropy_texts_are_read_by_the_quantity_they_are_given() -> None:
    assert parse("5 J/K", Entropy) == hc.JoulePerKelvin(5).to_entropy()
    assert parse("2 kcal/K", Entropy) == hc.KilocaloriePerKelvin(2).to_entropy()
    assert parse("3 J/(kg K)", SpecificEntropy) == (
        shc.JoulePerKilogramKelvin(3).to_specific_entropy()
    )
    assert type(parse("5 J/K", HeatCapacity)) is HeatCapacity


def test_the_derived_tables_accept_what_their_origin_accepts() -> None:
    assert set(entropy.ENTROPY_UNITS) == set(hc.HEAT_CAPACITY_UNITS)
    assert set(specific_entropy.SPECIFIC_ENTROPY_UNITS) == set(
        shc.SPECIFIC_HEAT_CAPACITY_UNITS
    )
