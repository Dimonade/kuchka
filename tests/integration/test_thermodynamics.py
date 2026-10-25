"""A gas in a cylinder: pressure, volume, work, and temperature changes.

Pressure and energy density share a dimension and are different concepts, so the
chain keeps them apart: the work of expansion is a pressure times a volume, and the
energy a fuel holds is an energy density times a volume.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Energy
from kuchka import EnergyDensity
from kuchka import Force
from kuchka import IncompatibleDimensionError
from kuchka import Pressure
from kuchka import Volume
from kuchka.units import thermal
from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import force
from kuchka.units.mechanics import pressure

PISTON = area.SquareCentimetre(50)


def test_the_force_on_a_piston_and_the_pressure_it_makes() -> None:
    load = force.Newton(500)
    made = load / PISTON
    assert type(made) is Pressure
    assert made == pressure.Kilopascal(100)
    assert type(made * PISTON) is Force
    assert made * PISTON == load


def test_the_work_of_an_expansion_is_pressure_times_volume() -> None:
    work = pressure.Bar(2) * volume.Litre(3)
    assert type(work) is Energy
    assert work == energy.Joule(600)
    assert work / pressure.Bar(2) == volume.Litre(3)
    assert type(work / pressure.Bar(2)) is Volume


def test_the_same_energy_per_volume_is_an_energy_density_and_not_a_pressure() -> None:
    work = pressure.Bar(2) * volume.Litre(3)
    per_volume = work / volume.Litre(3)
    assert type(per_volume) is EnergyDensity
    assert per_volume == energy_density.JoulePerCubicMetre(200_000)
    with pytest.raises(IncompatibleDimensionError):
        per_volume + pressure.Bar(2)  # type: ignore[operator]


def test_a_fuel_tank_holds_its_energy_density_times_its_volume() -> None:
    fuel = energy_density.MegajoulePerCubicMetre(34_000)
    held = fuel * volume.Litre(50)
    assert type(held) is Energy
    assert held == energy.Megajoule(1700)


def test_a_temperature_rise_is_a_delta_and_a_reading_is_absolute() -> None:
    start = thermal.Celsius(20)
    rise = thermal.DeltaKelvin(35)
    end = start + rise
    assert end == thermal.Celsius(55)
    assert end - start == rise
    assert end.to(thermal.KELVIN).value_in(thermal.KELVIN) == Fraction(32815, 100)
