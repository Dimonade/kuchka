"""Dynamic and kinematic viscosity: the arithmetic and the units."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Area
from kuchka import Density
from kuchka import DynamicViscosity
from kuchka import Force
from kuchka import Frequency
from kuchka import KinematicViscosity
from kuchka import MassFlowRate
from kuchka import Proportion
from kuchka import Ratio
from kuchka import Stress
from kuchka.internal import symbols
from kuchka.units import length
from kuchka.units import temporal
from kuchka.units.geometry import area
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import density
from kuchka.units.mechanics import dynamic_viscosity as dv
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import force
from kuchka.units.mechanics import kinematic_viscosity as kv
from kuchka.units.mechanics import pressure

MU = dv.PascalSecond(6)
NU = kv.SquareMetrePerSecond(6)


@pytest.mark.parametrize(
    "build",
    [
        lambda: pressure.Pascal(2) * temporal.Second(3),
        lambda: temporal.Second(3) * pressure.Pascal(2),
        lambda: energy_density.JoulePerCubicMetre(2) * temporal.Second(3),
        lambda: density.KilogramPerCubicMetre(3) * kv.SquareMetrePerSecond(2),
    ],
    ids=["p*t", "t*p", "u*t", "rho*nu"],
)
def test_a_dynamic_viscosity_is_what_it_is_made_of(build) -> None:
    viscosity = build()
    assert type(viscosity) is DynamicViscosity
    assert viscosity == MU


@pytest.mark.parametrize(
    "build",
    [
        lambda: area.SquareMetre(18) / temporal.Second(3),
        lambda: area.SquareMetre(2) * temporal.Hertz(3),
        lambda: velocity.MetrePerSecond(2) * length.Metre(3),
        lambda: length.Metre(3) * velocity.MetrePerSecond(2),
        lambda: MU / density.KilogramPerCubicMetre(1),
    ],
    ids=["A/t", "A*f", "v*L", "L*v", "mu/rho"],
)
def test_a_kinematic_viscosity_is_what_it_is_made_of(build) -> None:
    viscosity = build()
    assert type(viscosity) is KinematicViscosity
    assert viscosity == NU


def test_a_viscosity_over_the_other_is_a_density() -> None:
    ratio = MU / kv.SquareMetrePerSecond(2)
    assert type(ratio) is Density
    assert ratio == density.KilogramPerCubicMetre(3)


def test_a_kinematic_viscosity_over_a_speed_or_a_length_or_times_a_time() -> None:
    assert NU / velocity.MetrePerSecond(3) == length.Metre(2)
    assert NU / length.Metre(3) == velocity.MetrePerSecond(2)
    assert NU * temporal.Second(2) == area.SquareMetre(12)
    assert type(NU * temporal.Second(2)) is Area


def test_the_reynolds_number_has_one_value_in_every_order() -> None:
    rho, dynamic = density.KilogramPerCubicMetre(2), dv.PascalSecond(12)
    speed, size = velocity.MetrePerSecond(6), length.Metre(3)
    for re in (
        speed * size / NU,
        size * speed / NU,
        speed * size * rho / dynamic,
        rho * (speed * size) / dynamic,
    ):
        assert type(re) is Proportion
        assert re == Ratio(3)


@pytest.mark.parametrize(
    "build",
    [lambda: MU * temporal.Hertz(2), lambda: temporal.Hertz(2) * MU],
    ids=["mu*gamma", "gamma*mu"],
)
def test_a_viscosity_times_a_shear_rate_is_a_shear_stress(build) -> None:
    stress = build()
    assert type(stress) is Stress
    assert stress == pressure.Pascal(12).to_stress()


def test_a_shear_stress_over_a_shear_rate_is_a_viscosity() -> None:
    stress = pressure.Pascal(12).to_stress()
    viscosity = stress / temporal.Hertz(2)
    assert type(viscosity) is DynamicViscosity
    assert viscosity == MU
    rate = stress / MU
    assert type(rate) is Frequency
    assert rate == temporal.Hertz(2)


def test_a_shear_rate_is_a_speed_over_a_distance() -> None:
    plate = MU * (velocity.MetrePerSecond(4) / length.Metre(2))
    assert type(plate) is Stress
    assert plate == pressure.Pascal(12).to_stress()


def test_the_stokes_drag_is_a_force() -> None:
    radius, speed = length.Metre(3), velocity.MetrePerSecond(2)
    drag = 6 * MU * radius * speed
    assert type(drag) is Force
    assert type(MU * radius) is MassFlowRate
    assert drag == force.Newton(216)


@pytest.mark.parametrize(
    "build",
    [
        lambda: pressure.Pascal(12).to_stress() / temporal.Hertz(2),
        lambda: pressure.Pascal(2).to_stress() * temporal.Second(3),
        lambda: temporal.Second(3) * pressure.Pascal(2).to_stress(),
    ],
    ids=["tau/gamma", "tau*t", "t*tau"],
)
def test_a_stress_over_a_rate_and_times_a_time_are_one_viscosity(build) -> None:
    viscosity = build()
    assert type(viscosity) is DynamicViscosity
    assert viscosity == MU


@pytest.mark.parametrize(
    ("unit", "pascal_seconds"),
    [
        (dv.MillipascalSecond, Fraction(1, 1000)),
        (dv.MicropascalSecond, Fraction(1, 10**6)),
        (dv.Poise, Fraction(1, 10)),
        (dv.Centipoise, Fraction(1, 1000)),
    ],
    ids=["mPa s", "uPa s", "P", "cP"],
)
def test_the_dynamic_viscosity_units_have_exact_scales(unit, pascal_seconds) -> None:
    assert unit(1) == dv.PascalSecond(pascal_seconds)


@pytest.mark.parametrize(
    ("unit", "square_metres_per_second"),
    [
        (kv.SquareCentimetrePerSecond, Fraction(1, 10**4)),
        (kv.SquareMillimetrePerSecond, Fraction(1, 10**6)),
        (kv.SquareMicrometrePerSecond, Fraction(1, 10**12)),
        (kv.Stokes, Fraction(1, 10**4)),
        (kv.Centistokes, Fraction(1, 10**6)),
    ],
    ids=["cm2/s", "mm2/s", "um2/s", "St", "cSt"],
)
def test_the_kinematic_viscosity_units_have_exact_scales(
    unit, square_metres_per_second
) -> None:
    assert unit(1) == kv.SquareMetrePerSecond(square_metres_per_second)


def test_the_tables_list_the_units_by_symbol() -> None:
    two, micro, dot = symbols.SUPERSCRIPT_TWO, symbols.MICRO, "\u00b7"
    assert set(dv.DYNAMIC_VISCOSITY_UNITS) == {
        f"Pa{dot}s",
        f"mPa{dot}s",
        f"{micro}Pa{dot}s",
        "P",
        "cP",
    }
    assert set(kv.KINEMATIC_VISCOSITY_UNITS) == {
        f"m{two}/s",
        f"cm{two}/s",
        f"mm{two}/s",
        f"{micro}m{two}/s",
        "St",
        "cSt",
    }
