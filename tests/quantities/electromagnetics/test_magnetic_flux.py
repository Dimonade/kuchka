"""MagneticFlux: the volt-second, and the quantities it relates to.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to the weber.
"""

from __future__ import annotations

import pytest

from kuchka import Energy
from kuchka import IncompatibleDimensionError
from kuchka import MagneticFlux
from kuchka import MagneticFluxDensity
from kuchka import Resistance
from kuchka import Time
from kuchka import Voltage
from kuchka.units import current
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import magnetic_flux
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import voltage
from kuchka.units.geometry import area
from kuchka.units.temporal import time as time_units


def test_a_volt_held_for_a_second_is_a_weber() -> None:
    flux = voltage.Volt(1) * time_units.Second(1)
    assert isinstance(flux, MagneticFlux)
    assert flux == magnetic_flux.Weber(1)


def test_a_flux_change_over_time_is_a_voltage() -> None:
    induced = magnetic_flux.Milliweber(30) / time_units.Millisecond(10)
    assert isinstance(induced, Voltage)
    assert induced == voltage.Volt(3)


def test_a_flux_over_a_voltage_is_a_time() -> None:
    held = magnetic_flux.Weber(6) / voltage.Volt(2)
    assert isinstance(held, Time)
    assert held == time_units.Second(3)


def test_a_flux_over_an_area_is_a_flux_density() -> None:
    density = magnetic_flux.Weber(6) / area.SquareMetre(3)
    assert isinstance(density, MagneticFluxDensity)
    assert density == magnetic_flux_density.Tesla(2)


def test_a_resistance_and_a_charge_make_a_flux() -> None:
    flux = resistance.Ohm(4) * charge.Coulomb(5)
    assert isinstance(flux, MagneticFlux)
    assert flux == magnetic_flux.Weber(20)
    assert isinstance(magnetic_flux.Weber(20) / charge.Coulomb(5), Resistance)


def test_a_flux_times_a_current_is_an_energy() -> None:
    work = magnetic_flux.Weber(3) * current.Ampere(2)
    assert isinstance(work, Energy)


def test_a_flux_is_not_a_charge() -> None:
    with pytest.raises(IncompatibleDimensionError):
        magnetic_flux.Weber(1) + charge.Coulomb(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_weber_is_known_by_its_volt_second_spellings_at_the_boundary() -> None:
    from kuchka.units import MAGNETIC_FLUX_UNITS

    assert MAGNETIC_FLUX_UNITS["V·s"] is magnetic_flux.Weber
    assert repr(MAGNETIC_FLUX_UNITS["volt second"](2)) == "2 Wb"
