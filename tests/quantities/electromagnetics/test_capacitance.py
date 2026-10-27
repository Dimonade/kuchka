"""Capacitance: the farad, and the quantities it relates to.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to the farad.
"""

from __future__ import annotations

import pytest

from kuchka import Capacitance
from kuchka import Charge
from kuchka import Conductance
from kuchka import IncompatibleDimensionError
from kuchka import Voltage
from kuchka.units.electromagnetics import capacitance
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import conductance
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import frequency
from kuchka.units.temporal import time


def test_a_charge_per_volt_is_a_capacitance() -> None:
    stored = charge.Millicoulomb(6) / voltage.Volt(3)
    assert isinstance(stored, Capacitance)
    assert stored == capacitance.Millifarad(2)


def test_a_capacitance_charged_to_a_voltage_holds_a_charge() -> None:
    held = capacitance.Microfarad(100) * voltage.Volt(5)
    assert isinstance(held, Charge)
    assert held == charge.Microcoulomb(500)


def test_a_charge_over_a_capacitance_is_a_voltage() -> None:
    assert isinstance(charge.Coulomb(6) / capacitance.Farad(2), Voltage)
    assert charge.Coulomb(6) / capacitance.Farad(2) == voltage.Volt(3)


def test_a_siemens_held_for_a_second_is_a_farad() -> None:
    result = conductance.Siemens(2) * time.Second(3)
    assert isinstance(result, Capacitance)
    assert result == capacitance.Farad(6)


def test_a_capacitance_at_a_frequency_is_a_conductance() -> None:
    admittance = capacitance.Microfarad(1) * frequency.Kilohertz(1)
    assert isinstance(admittance, Conductance)
    assert admittance == conductance.Millisiemens(1)


def test_a_capacitance_is_not_a_charge() -> None:
    with pytest.raises(IncompatibleDimensionError):
        capacitance.Farad(1) + charge.Coulomb(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_farad_is_known_by_its_symbol_at_the_boundary() -> None:
    from kuchka.units import CAPACITANCE_UNITS

    assert CAPACITANCE_UNITS["uF"] is capacitance.Microfarad
