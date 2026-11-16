"""Analysing a small circuit: Ohm's law, dissipation, conductance, and energy.

The quantities flow through voltage, current, resistance, conductance, power, energy,
and time, and every step must land in the quantity a reader expects, with exact values.
"""

from __future__ import annotations

from fractions import Fraction

from kuchka import Conductance
from kuchka import Current
from kuchka import Energy
from kuchka import Power
from kuchka import Resistance
from kuchka import Voltage
from kuchka.units import current
from kuchka.units import temporal
from kuchka.units.electromagnetics import conductance
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import voltage
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import power

SUPPLY = voltage.Volt(12)
LOAD = resistance.Ohm(48)


def test_ohms_law_in_every_direction() -> None:
    drawn = SUPPLY / LOAD
    assert type(drawn) is Current
    assert drawn == current.Milliampere(250)
    assert type(drawn * LOAD) is Voltage
    assert drawn * LOAD == SUPPLY
    assert type(SUPPLY / drawn) is Resistance
    assert SUPPLY / drawn == LOAD


def test_the_dissipated_power_and_the_energy_over_a_shift() -> None:
    dissipated = SUPPLY * (SUPPLY / LOAD)
    assert type(dissipated) is Power
    assert dissipated == power.Watt(3)
    shift = dissipated * temporal.Hour(8)
    assert type(shift) is Energy
    assert shift == energy.WattHour(24)
    assert shift == energy.Joule(86_400)


def test_a_load_as_a_conductance_and_back() -> None:
    admittance = current.Milliampere(250) / SUPPLY
    assert type(admittance) is Conductance
    assert admittance == conductance.Siemens(Fraction(1, 48))
    assert SUPPLY * admittance == current.Milliampere(250)
    assert type(admittance * LOAD) is Fraction
    assert admittance * LOAD == Fraction(1)


def test_parallel_loads_add_as_conductances() -> None:
    first = conductance.Siemens(Fraction(1, 48))
    second = conductance.Siemens(Fraction(1, 16))
    together = first + second
    assert together == conductance.Siemens(Fraction(1, 12))
    assert SUPPLY * together == current.Ampere(1)


def test_a_supply_sag_scales_every_downstream_quantity() -> None:
    sagged = SUPPLY * Fraction(9, 10)
    assert sagged / LOAD == (SUPPLY / LOAD) * Fraction(9, 10)
    assert sagged * (sagged / LOAD) == power.Watt(3) * Fraction(81, 100)
