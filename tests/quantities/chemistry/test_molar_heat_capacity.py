"""Molar heat capacity and molar entropy: per mole, and the closed role."""

from __future__ import annotations

import pytest

from kuchka import AmountOfSubstance
from kuchka import DeltaKelvin
from kuchka import Energy
from kuchka import Entropy
from kuchka import HeatCapacity
from kuchka import IncompatibleDimensionError
from kuchka import Joule
from kuchka import MolarEnergy
from kuchka import MolarEntropy
from kuchka import MolarHeatCapacity
from kuchka import parse
from kuchka.units.amount import Mole
from kuchka.units.chemistry import molar_energy
from kuchka.units.chemistry import molar_entropy
from kuchka.units.chemistry import molar_heat_capacity as mhc
from kuchka.units.thermodynamics import heat_capacity as hc


def test_a_heat_capacity_over_an_amount_is_a_molar_heat_capacity_and_back() -> None:
    result = hc.JoulePerKelvin(25) / Mole(2)
    assert type(result) is MolarHeatCapacity
    assert result == mhc.JoulePerMoleKelvin(12.5)
    capacity = result * Mole(2)
    assert type(capacity) is HeatCapacity
    assert Mole(2) * result == capacity
    assert capacity == hc.JoulePerKelvin(25)


def test_a_molar_energy_over_a_difference_is_a_molar_heat_capacity() -> None:
    result = molar_energy.JoulePerMole(100) / DeltaKelvin(10)
    assert type(result) is MolarHeatCapacity
    assert result == mhc.JoulePerMoleKelvin(10)
    back = result * DeltaKelvin(10)
    assert type(back) is MolarEnergy
    assert back == molar_energy.JoulePerMole(100)


def test_the_heat_of_an_amount_is_the_same_however_it_is_grouped() -> None:
    helium = mhc.JoulePerMoleKelvin(12.5)
    by_amount = (helium * Mole(2)) * DeltaKelvin(10)
    by_difference = (helium * DeltaKelvin(10)) * Mole(2)
    assert type(by_amount) is Energy
    assert by_amount == by_difference == Joule(250)


def test_an_entropy_over_an_amount_is_a_molar_entropy_and_back() -> None:
    change = hc.JoulePerKelvin(25).to_entropy()
    molar = change / Mole(2)
    assert type(molar) is MolarEntropy
    assert molar == mhc.JoulePerMoleKelvin(12.5).to_molar_entropy()
    total = molar * Mole(2)
    assert type(total) is Entropy
    assert Mole(2) * molar == total
    assert total == change
    amount = change / molar
    assert type(amount) is AmountOfSubstance
    assert amount == Mole(2)


def test_a_molar_entropy_is_not_a_molar_heat_capacity() -> None:
    molar = mhc.JoulePerMoleKelvin(12.5).to_molar_entropy()
    assert type(molar.to_molar_heat_capacity()) is MolarHeatCapacity
    with pytest.raises(IncompatibleDimensionError, match="to_molar_heat_capacity"):
        molar * DeltaKelvin(2)
    with pytest.raises(IncompatibleDimensionError):
        molar + mhc.JoulePerMoleKelvin(12.5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_molar_heat_capacity_does_not_mix_with_the_other_heat_capacities() -> None:
    with pytest.raises(IncompatibleDimensionError):
        mhc.JoulePerMoleKelvin(1) + hc.JoulePerKelvin(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_units_are_exact() -> None:
    assert mhc.KilojoulePerMoleKelvin(1) == mhc.JoulePerMoleKelvin(1000)
    assert mhc.ThermochemicalCaloriePerMoleKelvin(1) == mhc.JoulePerMoleKelvin(4.184)


def test_the_entropy_unit_of_chemistry_tables_keeps_its_display() -> None:
    kept = mhc.ThermochemicalCaloriePerMoleKelvin(2).to_molar_entropy()
    assert repr(kept) == "2 cal/(mol\u00b7K)"


def test_the_texts_are_read_by_the_quantity_they_are_given() -> None:
    assert parse("12.47 J/(mol K)", MolarHeatCapacity) == mhc.JoulePerMoleKelvin(12.47)
    assert parse("75.3 J/mol/K", MolarHeatCapacity) == mhc.JoulePerMoleKelvin(75.3)
    assert parse("1 cal/(mol\u00b7\u00b0C)", MolarHeatCapacity) == (
        mhc.ThermochemicalCaloriePerMoleKelvin(1)
    )
    assert parse("188.8 J/(mol K)", MolarEntropy) == (
        mhc.JoulePerMoleKelvin(188.8).to_molar_entropy()
    )


def test_the_derived_table_accepts_what_its_origin_accepts() -> None:
    assert set(molar_entropy.MOLAR_ENTROPY_UNITS) == set(mhc.MOLAR_HEAT_CAPACITY_UNITS)
