"""Electric field strength, current density, and electric flux density."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Charge
from kuchka import Current
from kuchka import CurrentDensity
from kuchka import ElectricFieldStrength
from kuchka import ElectricFluxDensity
from kuchka import EnergyDensity
from kuchka import Force
from kuchka import IncompatibleDimensionError
from kuchka import Length
from kuchka import MagneticFieldStrength
from kuchka import Permittivity
from kuchka import SurfaceChargeDensity
from kuchka import Velocity
from kuchka import Voltage
from kuchka.internal import symbols
from kuchka.units import current
from kuchka.units import length
from kuchka.units import temporal
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import current_density as cd
from kuchka.units.electromagnetics import electric_field_strength as efs
from kuchka.units.electromagnetics import electric_flux_density as efd
from kuchka.units.electromagnetics import magnetic_field_strength
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.electromagnetics import permittivity
from kuchka.units.electromagnetics import surface_charge_density as scd
from kuchka.units.electromagnetics import voltage
from kuchka.units.electromagnetics import volume_charge_density as vcd
from kuchka.units.geometry import area
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import force

FIELD = efs.VoltPerMetre(6)
DENSITY = cd.AmperePerSquareMetre(6)
FLUX = efd.ELECTRIC_FLUX_DENSITY_UNITS["C/m2"](12)


@pytest.mark.parametrize(
    "build",
    [
        lambda: voltage.Volt(18) / length.Metre(3),
        lambda: force.Newton(18) / charge.Coulomb(3),
        lambda: magnetic_flux_density.Tesla(2) * velocity.MetrePerSecond(3),
        lambda: velocity.MetrePerSecond(3) * magnetic_flux_density.Tesla(2),
    ],
    ids=["V/L", "F/Q", "B*v", "v*B"],
)
def test_a_field_strength_is_what_it_is_made_of(build) -> None:
    field = build()
    assert type(field) is ElectricFieldStrength
    assert field == FIELD


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda: FIELD * length.Metre(3), Voltage, voltage.Volt(18)),
        (lambda: length.Metre(3) * FIELD, Voltage, voltage.Volt(18)),
        (lambda: FIELD * charge.Coulomb(3), Force, force.Newton(18)),
        (lambda: voltage.Volt(6) / efs.VoltPerMetre(3), Length, length.Metre(2)),
        (lambda: force.Newton(6) / efs.VoltPerMetre(3), Charge, charge.Coulomb(2)),
        (
            lambda: FIELD / magnetic_flux_density.Tesla(2),
            Velocity,
            velocity.MetrePerSecond(3),
        ),
    ],
    ids=["E*L", "L*E", "E*Q", "V/E", "F/E", "E/B"],
)
def test_a_field_strength_in_a_product_or_a_quotient(
    build, expected_type, expected
) -> None:
    result = build()
    assert type(result) is expected_type
    assert result == expected


def test_a_current_over_an_area_is_a_current_density() -> None:
    density = current.Ampere(6) / area.SquareMetre(3)
    assert type(density) is CurrentDensity
    assert density == cd.AmperePerSquareMetre(2)


@pytest.mark.parametrize(
    ("build", "expected_type", "expected"),
    [
        (lambda: DENSITY * area.SquareMetre(3), Current, current.Ampere(18)),
        (lambda: area.SquareMetre(3) * DENSITY, Current, current.Ampere(18)),
        (
            lambda: DENSITY * temporal.Second(3),
            SurfaceChargeDensity,
            scd.CoulombPerSquareMetre(18),
        ),
        (
            lambda: scd.CoulombPerSquareMetre(6) / temporal.Second(3),
            CurrentDensity,
            cd.AmperePerSquareMetre(2),
        ),
        (
            lambda: vcd.CoulombPerCubicMetre(6) * velocity.MetrePerSecond(3),
            CurrentDensity,
            cd.AmperePerSquareMetre(18),
        ),
        (
            lambda: DENSITY / vcd.CoulombPerCubicMetre(3),
            Velocity,
            velocity.MetrePerSecond(2),
        ),
        (
            lambda: magnetic_field_strength.AmperePerMetre(6) / length.Metre(3),
            CurrentDensity,
            cd.AmperePerSquareMetre(2),
        ),
        (
            lambda: DENSITY * length.Metre(3),
            MagneticFieldStrength,
            magnetic_field_strength.AmperePerMetre(18),
        ),
    ],
    ids=["J*A", "A*J", "J*t", "sigma/t", "rho*v", "J/rho", "H/L", "J*L"],
)
def test_a_current_density_in_a_product_or_a_quotient(
    build, expected_type, expected
) -> None:
    result = build()
    assert type(result) is expected_type
    assert result == expected


@pytest.mark.parametrize(
    "build",
    [
        lambda: permittivity.FaradPerMetre(2) * FIELD,
        lambda: FIELD * permittivity.FaradPerMetre(2),
    ],
    ids=["eps*E", "E*eps"],
)
def test_a_permittivity_times_a_field_is_an_electric_flux_density(build) -> None:
    flux = build()
    assert type(flux) is ElectricFluxDensity
    assert flux == FLUX


def test_a_flux_density_over_a_field_or_a_permittivity() -> None:
    ratio = FLUX / FIELD
    assert type(ratio) is Permittivity
    assert ratio == permittivity.FaradPerMetre(2)
    field = FLUX / permittivity.FaradPerMetre(2)
    assert type(field) is ElectricFieldStrength
    assert field == FIELD


def test_a_field_times_a_flux_density_is_an_energy_density() -> None:
    for energy in (FIELD * FLUX, FLUX * FIELD):
        assert type(energy) is EnergyDensity
        assert energy == energy_density.JoulePerCubicMetre(72)


def test_the_flux_of_a_flux_density_through_an_area_is_a_charge() -> None:
    for enclosed in (FLUX * area.SquareMetre(3), area.SquareMetre(3) * FLUX):
        assert type(enclosed) is Charge
        assert enclosed == charge.Coulomb(36)


def test_a_flux_density_and_a_surface_charge_density_convert_both_ways() -> None:
    sheet = FLUX.to_surface_charge_density()
    assert type(sheet) is SurfaceChargeDensity
    assert sheet == scd.CoulombPerSquareMetre(12)
    assert sheet.to_electric_flux_density() == FLUX


def test_a_flux_density_refuses_a_product_that_only_a_charge_density_has() -> None:
    with pytest.raises(IncompatibleDimensionError, match="to_surface_charge_density"):
        FLUX * length.Metre(2)


def test_a_flux_density_keeps_the_unit_it_was_built_in() -> None:
    assert str(efd.ELECTRIC_FLUX_DENSITY_UNITS["uC/cm2"](10)) == (
        f"10 {symbols.MICRO}C/cm{symbols.SUPERSCRIPT_TWO}"
    )


@pytest.mark.parametrize(
    ("unit", "volts_per_metre"),
    [
        (efs.MicrovoltPerMetre, Fraction(1, 10**6)),
        (efs.MillivoltPerMetre, Fraction(1, 1000)),
        (efs.KilovoltPerMetre, 1000),
        (efs.MegavoltPerMetre, 10**6),
        (efs.VoltPerCentimetre, 100),
        (efs.KilovoltPerCentimetre, 10**5),
        (efs.VoltPerMillimetre, 1000),
        (efs.KilovoltPerMillimetre, 10**6),
    ],
    ids=["uV/m", "mV/m", "kV/m", "MV/m", "V/cm", "kV/cm", "V/mm", "kV/mm"],
)
def test_the_field_strength_units_have_exact_scales(unit, volts_per_metre) -> None:
    assert unit(1) == efs.VoltPerMetre(volts_per_metre)


@pytest.mark.parametrize(
    ("unit", "amperes_per_square_metre"),
    [
        (cd.MilliamperePerSquareMetre, Fraction(1, 1000)),
        (cd.KiloamperePerSquareMetre, 1000),
        (cd.MegaamperePerSquareMetre, 10**6),
        (cd.AmperePerSquareCentimetre, 10**4),
        (cd.MilliamperePerSquareCentimetre, 10),
        (cd.MicroamperePerSquareCentimetre, Fraction(1, 100)),
        (cd.AmperePerSquareMillimetre, 10**6),
    ],
    ids=["mA/m2", "kA/m2", "MA/m2", "A/cm2", "mA/cm2", "uA/cm2", "A/mm2"],
)
def test_the_current_density_units_have_exact_scales(
    unit, amperes_per_square_metre
) -> None:
    assert unit(1) == cd.AmperePerSquareMetre(amperes_per_square_metre)


def test_the_tables_list_the_units_by_symbol() -> None:
    two, micro = symbols.SUPERSCRIPT_TWO, symbols.MICRO
    assert set(efs.ELECTRIC_FIELD_STRENGTH_UNITS) == {
        "V/m",
        f"{micro}V/m",
        "mV/m",
        "kV/m",
        "MV/m",
        "V/cm",
        "kV/cm",
        "V/mm",
        "kV/mm",
    }
    assert set(cd.CURRENT_DENSITY_UNITS) == {
        f"A/m{two}",
        f"mA/m{two}",
        f"kA/m{two}",
        f"MA/m{two}",
        f"A/cm{two}",
        f"mA/cm{two}",
        f"{micro}A/cm{two}",
        f"A/mm{two}",
    }
    assert set(efd.ELECTRIC_FLUX_DENSITY_UNITS) == {
        f"C/m{two}",
        f"mC/m{two}",
        f"{micro}C/m{two}",
        f"nC/m{two}",
        f"C/cm{two}",
        f"{micro}C/cm{two}",
    }
