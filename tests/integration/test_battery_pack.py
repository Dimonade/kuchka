"""Sizing a battery pack: energy, volume, power, runtime, and charge.

A pack is built from cells whose capacity is quoted in watt-hours and whose size in
litres.
The answers cross the energy, power, volume, voltage, current, charge, and time types,
and each step has to land in the right quantity.
"""

from __future__ import annotations

from fractions import Fraction

from kuchka import Charge
from kuchka import Current
from kuchka import Energy
from kuchka import EnergyDensity
from kuchka import Power
from kuchka import Pressure
from kuchka import Time
from kuchka.units import charge
from kuchka.units import current
from kuchka.units import energy
from kuchka.units import energy_density as ed
from kuchka.units import power
from kuchka.units import pressure
from kuchka.units import temporal
from kuchka.units import voltage
from kuchka.units import volume

CELLS = 96
CELL_ENERGY = energy.WattHour(875)
CELL_VOLUME = volume.Litre(Fraction(4, 5))
NOMINAL = voltage.Volt(400)


def test_the_pack_energy_adds_up_and_reads_in_kilowatt_hours() -> None:
    pack = CELL_ENERGY * CELLS
    assert type(pack) is Energy
    assert pack == energy.KilowattHour(84)
    assert pack.to(energy.KILOWATT_HOUR).value_in(energy.KILOWATT_HOUR) == Fraction(84)


def test_the_pack_energy_density_is_an_energy_density_and_never_a_pressure() -> None:
    density = (CELL_ENERGY * CELLS) / (CELL_VOLUME * CELLS)
    assert type(density) is EnergyDensity
    assert density == ed.WattHourPerLitre(Fraction(4375, 4))
    assert not isinstance(density, Pressure)
    in_megajoules = density.to(ed.MEGAJOULE_PER_CUBIC_METRE)
    assert in_megajoules.value_in(ed.MEGAJOULE_PER_CUBIC_METRE) == Fraction(
        3_937_500, 1000
    )


def test_a_pressure_does_not_stand_in_for_an_energy_density() -> None:
    density = ed.WattHourPerLitre(1000)
    assert density != pressure.Pascal(density.magnitude)
    assert density.to(ed.JOULE_PER_CUBIC_METRE).magnitude == Fraction(3_600_000_000)


def test_runtime_at_a_constant_draw() -> None:
    pack = CELL_ENERGY * CELLS
    runtime = pack / power.Kilowatt(12)
    assert type(runtime) is Time
    assert runtime == temporal.Hour(7)
    assert runtime.to(temporal.HOUR).value_in(temporal.HOUR) == Fraction(7)


def test_the_draw_current_and_the_charge_moved_over_the_runtime() -> None:
    draw = power.Kilowatt(12) / NOMINAL
    assert type(draw) is Current
    assert draw == current.Ampere(30)
    moved = draw * temporal.Hour(7)
    assert type(moved) is Charge
    assert moved == charge.AmpereHour(210)


def test_charging_power_is_voltage_times_current() -> None:
    charging = NOMINAL * current.Ampere(125)
    assert type(charging) is Power
    assert charging == power.Kilowatt(50)
    assert (CELL_ENERGY * CELLS) / charging == temporal.Minute(Fraction(504, 5))
