"""Fluence and surface tension: one dimension, a principal kind and a role of it."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Area
from kuchka import Energy
from kuchka import Fluence
from kuchka import Force
from kuchka import HeatFlux
from kuchka import Length
from kuchka import Pressure
from kuchka import SurfaceTension
from kuchka import Time
from kuchka.errors import IncompatibleDimensionError
from kuchka.units import temporal
from kuchka.units.geometry import area
from kuchka.units.kinematics import velocity
from kuchka.units.length import Metre
from kuchka.units.mechanics import dynamic_viscosity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import fluence as fl
from kuchka.units.mechanics import force
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import surface_tension as st
from kuchka.units.thermodynamics import heat_flux

TENSION = st.NewtonPerMetre(3)
FLUENCE = fl.JoulePerSquareMetre(3)


@pytest.mark.parametrize(
    "build",
    [
        lambda: force.Newton(6) / Metre(2),
        lambda: pressure.Pascal(3) * Metre(1),
        lambda: Metre(1) * pressure.Pascal(3),
        lambda: energy_density.JoulePerCubicMetre(3) * Metre(1),
        lambda: dynamic_viscosity.PascalSecond(3) * velocity.MetrePerSecond(1),
    ],
    ids=["F/L", "p*L", "L*p", "u*L", "mu*v"],
)
def test_a_surface_tension_is_what_it_is_made_of(build) -> None:
    result = build()
    assert type(result) is SurfaceTension
    assert result == TENSION


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda: TENSION * Metre(2), Force, force.Newton(6)),
        (lambda: Metre(2) * TENSION, Force, force.Newton(6)),
        (lambda: TENSION * area.SquareMetre(2), Energy, energy.Joule(6)),
        (lambda: force.Newton(6) / TENSION, Length, Metre(2)),
        (lambda: energy.Joule(6) / TENSION, Area, area.SquareMetre(2)),
        (lambda: TENSION / Metre(1), Pressure, pressure.Pascal(3)),
    ],
    ids=["st*L", "L*st", "st*A", "F/st", "E/st", "st/L"],
)
def test_a_surface_tension_in_a_product_or_a_quotient(
    build, expected_type, expected
) -> None:
    result = build()
    assert type(result) is expected_type
    assert result == expected


@pytest.mark.parametrize(
    "build",
    [
        lambda: energy.Joule(6) / area.SquareMetre(2),
        lambda: heat_flux.WattPerSquareMetre(1) * temporal.Second(3),
        lambda: temporal.Second(3) * heat_flux.WattPerSquareMetre(1),
        lambda: energy.Joule(6) / area.SquareMetre(1) / 2,
    ],
    ids=["E/A", "q*t", "t*q", "E/A/2"],
)
def test_a_fluence_is_what_it_is_made_of(build) -> None:
    result = build()
    assert type(result) is Fluence
    assert result == FLUENCE


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda: FLUENCE * area.SquareMetre(2), Energy, energy.Joule(6)),
        (lambda: area.SquareMetre(2) * FLUENCE, Energy, energy.Joule(6)),
        (lambda: energy.Joule(6) / FLUENCE, Area, area.SquareMetre(2)),
        (
            lambda: FLUENCE / temporal.Second(3),
            HeatFlux,
            heat_flux.WattPerSquareMetre(1),
        ),
        (
            lambda: FLUENCE / heat_flux.WattPerSquareMetre(1),
            Time,
            temporal.Second(3),
        ),
    ],
    ids=["H*A", "A*H", "E/H", "H/t", "H/q"],
)
def test_a_fluence_in_a_product_or_a_quotient(build, expected_type, expected) -> None:
    result = build()
    assert type(result) is expected_type
    assert result == expected


def test_the_two_kinds_convert_explicitly_and_keep_the_value() -> None:
    assert FLUENCE.to_surface_tension() == TENSION
    assert type(FLUENCE.to_surface_tension()) is SurfaceTension
    assert Fluence.from_surface_tension(TENSION) == FLUENCE
    assert Fluence.from_surface_tension(FLUENCE.to_surface_tension()) == FLUENCE


@pytest.mark.parametrize(
    "build",
    [lambda: FLUENCE * Metre(1), lambda: FLUENCE / Metre(1)],
    ids=["H*L", "H/L"],
)
def test_a_fluence_is_refused_where_a_surface_tension_is_accepted(build) -> None:
    with pytest.raises(IncompatibleDimensionError, match="to_surface_tension"):
        build()


def test_a_fluence_is_not_built_from_anything_but_a_surface_tension() -> None:
    with pytest.raises(IncompatibleDimensionError):
        Fluence.from_surface_tension(force.Newton(1))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("unit", "joules_per_square_metre"),
    [
        (fl.MegajoulePerSquareMetre, 10**6),
        (fl.JoulePerSquareCentimetre, 10**4),
        (fl.MillijoulePerSquareCentimetre, 10),
        (fl.MicrojoulePerSquareCentimetre, Fraction(1, 100)),
        (fl.WattHourPerSquareMetre, 3600),
        (fl.KilowattHourPerSquareMetre, 3_600_000),
    ],
    ids=["MJ/m2", "J/cm2", "mJ/cm2", "uJ/cm2", "Wh/m2", "kWh/m2"],
)
def test_the_fluence_units_have_exact_scales(unit, joules_per_square_metre) -> None:
    assert unit(1) == fl.JoulePerSquareMetre(joules_per_square_metre)


@pytest.mark.parametrize(
    ("unit", "newtons_per_metre"),
    [
        (st.MillinewtonPerMetre, Fraction(1, 1000)),
        (st.KilonewtonPerMetre, 1000),
        (st.DynePerCentimetre, Fraction(1, 1000)),
    ],
    ids=["mN/m", "kN/m", "dyn/cm"],
)
def test_the_surface_tension_units_have_exact_scales(unit, newtons_per_metre) -> None:
    assert unit(1) == st.NewtonPerMetre(newtons_per_metre)


def test_the_cgs_unit_is_a_millinewton_per_metre_and_an_erg_per_square_centimetre() -> (
    None
):
    assert st.DynePerCentimetre(72) == st.MillinewtonPerMetre(72)
    assert st.SURFACE_TENSION_UNITS["erg/cm2"](72) == st.DynePerCentimetre(72)


def test_a_uv_dose_over_a_lamp_irradiance_is_an_exposure_time() -> None:
    dose = fl.MillijoulePerSquareCentimetre(40)
    lamp = heat_flux.MilliwattPerSquareCentimetre(0.5)
    assert dose / lamp == temporal.Second(80)


def test_five_peak_sun_hours_are_five_kilowatt_hours_and_eighteen_megajoules() -> None:
    day = heat_flux.KilowattPerSquareMetre(1) * temporal.Hour(5)
    assert day == fl.KilowattHourPerSquareMetre(5)
    assert day == fl.MegajoulePerSquareMetre(18)
