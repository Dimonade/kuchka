"""Charge per length, per area, and per volume: the arithmetic and the units."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Area
from kuchka import Charge
from kuchka import Current
from kuchka import Length
from kuchka import LinearChargeDensity
from kuchka import MagneticFieldStrength
from kuchka import SpecificCharge
from kuchka import SurfaceChargeDensity
from kuchka import Volume
from kuchka import VolumeChargeDensity
from kuchka.internal import symbols
from kuchka.units import current
from kuchka.units import length
from kuchka.units.chemistry import molar_charge
from kuchka.units.chemistry import molar_concentration
from kuchka.units.electromagnetics import charge
from kuchka.units.electromagnetics import linear_charge_density as lcd
from kuchka.units.electromagnetics import magnetic_field_strength
from kuchka.units.electromagnetics import permittivity
from kuchka.units.electromagnetics import specific_charge
from kuchka.units.electromagnetics import surface_charge_density as scd
from kuchka.units.electromagnetics import voltage
from kuchka.units.electromagnetics import volume_charge_density as vcd
from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import density

CHARGE = charge.Coulomb(6)


@pytest.mark.parametrize(
    ("divisor", "expected_type", "expected"),
    [
        (length.Metre(3), LinearChargeDensity, lcd.CoulombPerMetre(2)),
        (area.SquareMetre(3), SurfaceChargeDensity, scd.CoulombPerSquareMetre(2)),
        (volume.CubicMetre(3), VolumeChargeDensity, vcd.CoulombPerCubicMetre(2)),
    ],
    ids=["per length", "per area", "per volume"],
)
def test_a_charge_over_an_extent_is_a_charge_density(
    divisor, expected_type, expected
) -> None:
    density_ = CHARGE / divisor
    assert type(density_) is expected_type
    assert density_ == expected


@pytest.mark.parametrize(
    ("density_", "extent", "expected_type", "expected"),
    [
        (lcd.CoulombPerMetre(2), length.Metre(3), Charge, CHARGE),
        (scd.CoulombPerSquareMetre(2), area.SquareMetre(3), Charge, CHARGE),
        (vcd.CoulombPerCubicMetre(2), volume.CubicMetre(3), Charge, CHARGE),
        (scd.CoulombPerSquareMetre(2), length.Metre(3), LinearChargeDensity, None),
        (vcd.CoulombPerCubicMetre(2), length.Metre(3), SurfaceChargeDensity, None),
    ],
    ids=["lambda*L", "sigma*A", "rho*V", "sigma*L", "rho*L"],
)
def test_a_charge_density_times_an_extent_drops_one_order(
    density_, extent, expected_type, expected
) -> None:
    for result in (density_ * extent, extent * density_):
        assert type(result) is expected_type
        if expected is not None:
            assert result == expected


def test_a_charge_density_over_a_length_gains_one_order() -> None:
    assert type(lcd.CoulombPerMetre(6) / length.Metre(3)) is SurfaceChargeDensity
    assert type(scd.CoulombPerSquareMetre(6) / length.Metre(3)) is VolumeChargeDensity
    assert scd.CoulombPerSquareMetre(6) / length.Metre(3) == vcd.CoulombPerCubicMetre(2)


@pytest.mark.parametrize(
    ("density_", "expected_type", "expected"),
    [
        (lcd.CoulombPerMetre(3), Length, length.Metre(2)),
        (scd.CoulombPerSquareMetre(3), Area, area.SquareMetre(2)),
        (vcd.CoulombPerCubicMetre(3), Volume, volume.CubicMetre(2)),
    ],
    ids=["Q/lambda", "Q/sigma", "Q/rho"],
)
def test_a_charge_over_a_charge_density_is_the_extent(
    density_, expected_type, expected
) -> None:
    extent = CHARGE / density_
    assert type(extent) is expected_type
    assert extent == expected


def test_a_current_over_a_speed_is_a_linear_charge_density() -> None:
    line = current.Ampere(6) / velocity.MetrePerSecond(3)
    assert type(line) is LinearChargeDensity
    assert line == lcd.CoulombPerMetre(2)


def test_a_linear_charge_density_moving_is_a_current() -> None:
    flow = lcd.CoulombPerMetre(2) * velocity.MetrePerSecond(3)
    assert type(flow) is Current
    assert flow == current.Ampere(6)


def test_a_surface_charge_density_moving_is_a_surface_current() -> None:
    sheet = scd.CoulombPerSquareMetre(2) * velocity.MetrePerSecond(3)
    assert type(sheet) is MagneticFieldStrength
    assert sheet == magnetic_field_strength.AmperePerMetre(6)


def test_a_permittivity_times_a_voltage_is_a_linear_charge_density() -> None:
    line = permittivity.FaradPerMetre(2) * voltage.Volt(3)
    assert type(line) is LinearChargeDensity
    assert line == lcd.CoulombPerMetre(6)


def test_a_specific_charge_times_a_mass_density_is_a_volume_charge_density() -> None:
    cloud = specific_charge.CoulombPerKilogram(2) * density.KilogramPerCubicMetre(3)
    assert type(cloud) is VolumeChargeDensity
    assert cloud == vcd.CoulombPerCubicMetre(6)
    back = cloud / density.KilogramPerCubicMetre(3)
    assert type(back) is SpecificCharge
    assert back == specific_charge.CoulombPerKilogram(2)


def test_a_molar_charge_times_a_concentration_is_a_volume_charge_density() -> None:
    ions = molar_charge.CoulombPerMole(2) * molar_concentration.MolePerCubicMetre(3)
    assert type(ions) is VolumeChargeDensity
    assert ions == vcd.CoulombPerCubicMetre(6)


@pytest.mark.parametrize(
    ("unit", "coulombs_per_extent"),
    [
        (lcd.MillicoulombPerMetre, Fraction(1, 10**3)),
        (lcd.MicrocoulombPerMetre, Fraction(1, 10**6)),
        (lcd.NanocoulombPerMetre, Fraction(1, 10**9)),
        (lcd.PicocoulombPerMetre, Fraction(1, 10**12)),
    ],
    ids=["mC/m", "uC/m", "nC/m", "pC/m"],
)
def test_the_linear_units_have_exact_scales(unit, coulombs_per_extent) -> None:
    assert unit(1) == lcd.CoulombPerMetre(coulombs_per_extent)


@pytest.mark.parametrize(
    ("unit", "coulombs_per_square_metre"),
    [
        (scd.MillicoulombPerSquareMetre, Fraction(1, 10**3)),
        (scd.MicrocoulombPerSquareMetre, Fraction(1, 10**6)),
        (scd.NanocoulombPerSquareMetre, Fraction(1, 10**9)),
        (scd.CoulombPerSquareCentimetre, 10_000),
        (scd.MicrocoulombPerSquareCentimetre, Fraction(1, 10**2)),
        (scd.MilliampereHourPerSquareCentimetre, 36_000),
    ],
    ids=["mC/m2", "uC/m2", "nC/m2", "C/cm2", "uC/cm2", "mAh/cm2"],
)
def test_the_surface_units_have_exact_scales(unit, coulombs_per_square_metre) -> None:
    assert unit(1) == scd.CoulombPerSquareMetre(coulombs_per_square_metre)


@pytest.mark.parametrize(
    ("unit", "coulombs_per_cubic_metre"),
    [
        (vcd.MillicoulombPerCubicMetre, Fraction(1, 10**3)),
        (vcd.MicrocoulombPerCubicMetre, Fraction(1, 10**6)),
        (vcd.NanocoulombPerCubicMetre, Fraction(1, 10**9)),
        (vcd.CoulombPerCubicCentimetre, 1_000_000),
        (vcd.AmpereHourPerLitre, 3_600_000),
    ],
    ids=["mC/m3", "uC/m3", "nC/m3", "C/cm3", "Ah/L"],
)
def test_the_volume_units_have_exact_scales(unit, coulombs_per_cubic_metre) -> None:
    assert unit(1) == vcd.CoulombPerCubicMetre(coulombs_per_cubic_metre)


def test_the_tables_list_the_units_by_symbol() -> None:
    two, three = symbols.SUPERSCRIPT_TWO, symbols.SUPERSCRIPT_THREE
    micro = symbols.MICRO
    assert set(lcd.LINEAR_CHARGE_DENSITY_UNITS) == {
        "C/m",
        "mC/m",
        f"{micro}C/m",
        "nC/m",
        "pC/m",
    }
    assert set(scd.SURFACE_CHARGE_DENSITY_UNITS) == {
        f"C/m{two}",
        f"mC/m{two}",
        f"{micro}C/m{two}",
        f"nC/m{two}",
        f"C/cm{two}",
        f"mC/cm{two}",
        f"{micro}C/cm{two}",
        f"mAh/cm{two}",
    }
    assert set(vcd.VOLUME_CHARGE_DENSITY_UNITS) == {
        f"C/m{three}",
        f"mC/m{three}",
        f"{micro}C/m{three}",
        f"nC/m{three}",
        f"C/cm{three}",
        "Ah/L",
    }
