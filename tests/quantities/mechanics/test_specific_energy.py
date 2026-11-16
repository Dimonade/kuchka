"""SpecificEnergy: its units and the products and quotients that produce it.

The generic contracts (arithmetic, conversion, formatting, spellings) run for every
unit of the table; this module covers what is specific to specific energy.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from kuchka import Energy
from kuchka import EnergyDensity
from kuchka import IncompatibleDimensionError
from kuchka import Kilogram
from kuchka import SpecificEnergy
from kuchka import parse
from kuchka.units import length
from kuchka.units import mass
from kuchka.units.kinematics import acceleration
from kuchka.units.mechanics import density
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import specific_energy as se


def test_a_watt_hour_per_kilogram_is_exactly_3600_joules_per_kilogram() -> None:
    assert se.WattHourPerKilogram(1) == se.JoulePerKilogram(3600)
    assert se.KilowattHourPerKilogram(1) == se.WattHourPerKilogram(1000)


def test_the_metric_and_food_units_are_exact_multiples_of_the_joule_per_kilogram() -> (
    None
):
    assert se.JoulePerGram(1) == se.KilojoulePerKilogram(1)
    assert se.MegajoulePerKilogram(1) == se.KilojoulePerKilogram(1000)
    assert se.KilocaloriePerKilogram(1) == se.JoulePerKilogram(4184)


def test_a_battery_pack_converts_between_wh_per_kg_and_mj_per_kg() -> None:
    assert se.WattHourPerKilogram(250).to(
        se.MEGAJOULE_PER_KILOGRAM
    ) == se.MegajoulePerKilogram(Decimal("0.9"))


def test_energy_over_mass_is_a_specific_energy_and_back() -> None:
    stored = energy.WattHour(500) / mass.Kilogram(2)
    assert type(stored) is SpecificEnergy
    assert stored == se.WattHourPerKilogram(250)
    assert type(stored * Kilogram(2)) is Energy
    assert stored * Kilogram(2) == energy.WattHour(500)


def test_the_other_ways_to_reach_the_dimension_agree_with_energy_over_mass() -> None:
    height = acceleration.MetrePerSecondSquared(10) * length.Metre(5)
    assert type(height) is SpecificEnergy
    assert height == se.JoulePerKilogram(50)
    head = pressure.Bar(2) / density.KilogramPerCubicMetre(1000)
    assert head == se.JoulePerKilogram(200)


def test_a_specific_energy_times_a_density_is_an_energy_density() -> None:
    pack = se.WattHourPerKilogram(250) * density.KilogramPerLitre(2)
    assert type(pack) is EnergyDensity
    assert pack == energy_density.WattHourPerLitre(500)
    assert pack / density.KilogramPerLitre(2) == se.WattHourPerKilogram(250)


def test_text_resolves_through_the_table() -> None:
    assert parse("250 Wh/kg", SpecificEnergy) == se.WattHourPerKilogram(250)
    assert parse(
        "43 megajoules per kilogram", SpecificEnergy
    ) == se.MegajoulePerKilogram(43)


def test_a_density_does_not_stand_in_for_a_specific_energy() -> None:
    with pytest.raises(IncompatibleDimensionError):
        se.JoulePerKilogram(1) + density.KilogramPerCubicMetre(1)  # type: ignore[operator]
