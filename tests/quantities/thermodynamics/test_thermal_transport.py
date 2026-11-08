"""Heat flux and thermal conductivity: the arithmetic and the units."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AmbiguousKindError
from kuchka import Area
from kuchka import HeatFlux
from kuchka import Power
from kuchka import ThermalConductivity
from kuchka.internal import symbols
from kuchka.units import temporal
from kuchka.units.geometry import area
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import power
from kuchka.units.mechanics import pressure
from kuchka.units.thermodynamics import heat_flux as hf
from kuchka.units.thermodynamics import thermal_conductivity as tc

FLUX = hf.WattPerSquareMetre(6)


@pytest.mark.parametrize(
    "build",
    [
        lambda: power.Watt(18) / area.SquareMetre(3),
        lambda: energy.Joule(18) / temporal.Second(3) / area.SquareMetre(1),
        lambda: pressure.Pascal(2) * velocity.MetrePerSecond(3),
        lambda: velocity.MetrePerSecond(3) * pressure.Pascal(2),
        lambda: energy_density.JoulePerCubicMetre(2) * velocity.MetrePerSecond(3),
    ],
    ids=["P/A", "E/t/A", "p*v", "v*p", "u*v"],
)
def test_a_heat_flux_is_what_it_is_made_of(build) -> None:
    flux = build()
    assert type(flux) is HeatFlux
    assert flux == FLUX


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda: FLUX * area.SquareMetre(3), Power, power.Watt(18)),
        (lambda: area.SquareMetre(3) * FLUX, Power, power.Watt(18)),
        (lambda: power.Watt(18) / FLUX, Area, area.SquareMetre(3)),
    ],
    ids=["q*A", "A*q", "P/q"],
)
def test_a_heat_flux_in_a_product_or_a_quotient(build, expected_type, expected) -> None:
    result = build()
    assert type(result) is expected_type
    assert result == expected


def test_a_heat_flux_over_a_speed_is_a_pressure_or_an_energy_density() -> None:
    with pytest.raises(AmbiguousKindError):
        FLUX / velocity.MetrePerSecond(3)


@pytest.mark.parametrize(
    ("unit", "watts_per_square_metre"),
    [
        (hf.MilliwattPerSquareMetre, Fraction(1, 1000)),
        (hf.KilowattPerSquareMetre, 1000),
        (hf.MegawattPerSquareMetre, 10**6),
        (hf.WattPerSquareCentimetre, 10**4),
        (hf.MilliwattPerSquareCentimetre, 10),
        (hf.MicrowattPerSquareCentimetre, Fraction(1, 100)),
    ],
    ids=["mW/m2", "kW/m2", "MW/m2", "W/cm2", "mW/cm2", "uW/cm2"],
)
def test_the_heat_flux_units_have_exact_scales(unit, watts_per_square_metre) -> None:
    assert unit(1) == hf.WattPerSquareMetre(watts_per_square_metre)


@pytest.mark.parametrize(
    ("unit", "watts_per_metre_kelvin"),
    [
        (tc.MilliwattPerMetreKelvin, Fraction(1, 1000)),
        (tc.KilowattPerMetreKelvin, 1000),
        (tc.WattPerCentimetreKelvin, 100),
    ],
    ids=["mW/(m K)", "kW/(m K)", "W/(cm K)"],
)
def test_the_thermal_conductivity_units_have_exact_scales(
    unit, watts_per_metre_kelvin
) -> None:
    assert unit(1) == tc.WattPerMetreKelvin(watts_per_metre_kelvin)


def test_a_thermal_conductivity_is_its_own_kind() -> None:
    assert type(tc.WattPerMetreKelvin(401)) is ThermalConductivity


def test_the_tables_list_the_units_by_symbol() -> None:
    two, micro, dot = symbols.SUPERSCRIPT_TWO, symbols.MICRO, "\u00b7"
    assert set(hf.HEAT_FLUX_UNITS) == {
        f"W/m{two}",
        f"mW/m{two}",
        f"kW/m{two}",
        f"MW/m{two}",
        f"W/cm{two}",
        f"mW/cm{two}",
        f"{micro}W/cm{two}",
    }
    assert set(tc.THERMAL_CONDUCTIVITY_UNITS) == {
        f"W/(m{dot}K)",
        f"mW/(m{dot}K)",
        f"kW/(m{dot}K)",
        f"W/(cm{dot}K)",
    }
