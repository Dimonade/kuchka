"""A mass at a radius is a `MomentOfInertia`, and rotational dynamics close on it."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AngularMomentum
from kuchka import Area
from kuchka import Energy
from kuchka import FirstMomentOfMass
from kuchka import MomentOfInertia
from kuchka import Torque
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.units import length
from kuchka.units import mass
from kuchka.units.geometry import area
from kuchka.units.kinematics import angular_acceleration as angacc
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.mechanics import angular_momentum
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import first_moment_of_mass as unbalance
from kuchka.units.mechanics import moment_of_inertia as inertia
from kuchka.units.mechanics import torque
from kuchka.units.temporal import time

KG_M2 = f"kg{symbols.MIDDLE_DOT}m²"


def test_a_mass_times_an_area_is_a_moment_of_inertia() -> None:
    result = mass.Kilogram(2) * area.SquareMetre(Fraction(1, 25))
    assert type(result) is MomentOfInertia
    assert result == inertia.KilogramSquareMetre(Fraction(2, 25))
    assert str(result) == f"0.08 {KG_M2}"


@pytest.mark.parametrize(
    "build",
    [
        lambda m, r: m * r * r,
        lambda m, r: r * m * r,
        lambda m, r: r * r * m,
        lambda m, r: m * (r * r),
        lambda m, r: m * r**2,
        lambda m, r: r**2 * m,
    ],
    ids=["m*r*r", "r*m*r", "r*r*m", "m*(r*r)", "m*r**2", "r**2*m"],
)
def test_a_mass_at_a_radius_is_a_moment_of_inertia_in_any_order(build) -> None:
    result = build(mass.Kilogram(2), length.Metre(Fraction(1, 5)))
    assert type(result) is MomentOfInertia
    assert result == inertia.KilogramSquareMetre(Fraction(2, 25))


def test_a_mass_times_a_length_is_a_first_moment_of_mass() -> None:
    result = mass.Gram(3) * length.Millimetre(40)
    assert type(result) is FirstMomentOfMass
    assert result == unbalance.GramMillimetre(120)


@pytest.mark.parametrize(
    ("divisor", "expected"),
    [
        (mass.Kilogram(2), area.SquareMetre(Fraction(1, 25))),
        (area.SquareMetre(Fraction(1, 25)), mass.Kilogram(2)),
        (length.Metre(Fraction(1, 5)), unbalance.KilogramMetre(Fraction(2, 5))),
        (unbalance.KilogramMetre(Fraction(2, 5)), length.Metre(Fraction(1, 5))),
    ],
    ids=["per-mass", "per-area", "per-length", "per-unbalance"],
)
def test_a_moment_of_inertia_divides_back_into_its_parts(divisor, expected) -> None:
    result = inertia.KilogramSquareMetre(Fraction(2, 25)) / divisor
    assert type(result) is type(expected)
    assert result == expected


def test_the_radius_of_gyration_is_the_root_of_inertia_per_mass() -> None:
    gyration = inertia.KilogramSquareMetre(Fraction(2, 25)) / mass.Kilogram(8)
    assert type(gyration) is Area
    assert gyration == length.Metre(Fraction(1, 10)) ** 2


def test_inertia_times_angular_acceleration_is_torque() -> None:
    result = inertia.KilogramSquareCentimetre(30) * angacc.RadianPerSecondSquared(400)
    assert type(result) is Torque
    assert result == torque.NewtonMetre(Fraction(6, 5))


def test_torque_per_inertia_is_angular_acceleration() -> None:
    result = torque.NewtonMetre(Fraction(6, 5)) / inertia.KilogramSquareCentimetre(30)
    assert result == angacc.RadianPerSecondSquared(400)


def test_inertia_times_angular_velocity_is_angular_momentum() -> None:
    spin = inertia.KilogramSquareMetre(Fraction(1, 25)) * angvel.RadianPerSecond(300)
    assert type(spin) is AngularMomentum
    assert spin == angular_momentum.KilogramSquareMetrePerSecond(12)
    assert str(spin) == f"12 {KG_M2}/s"


def test_a_torque_held_for_a_time_is_angular_momentum() -> None:
    spin = torque.NewtonMetre(2) * time.Second(6)
    assert type(spin) is AngularMomentum
    assert spin == angular_momentum.NewtonMetreSecond(12)


def test_rotational_kinetic_energy_is_half_inertia_times_omega_squared() -> None:
    rate = angvel.RadianPerSecond(300)
    stored = Fraction(1, 2) * inertia.KilogramSquareCentimetre(30) * rate * rate
    assert type(stored) is Energy
    assert stored == energy.Joule(135)


def test_a_flywheel_from_its_mass_and_radius_stores_energy() -> None:
    disc = Fraction(1, 2) * mass.Kilogram(2) * length.Metre(Fraction(1, 5)) ** 2
    assert type(disc * angacc.RadianPerSecondSquared(10)) is Torque
    rate = angvel.RadianPerSecond(100)
    assert Fraction(1, 2) * disc * rate * rate == energy.Joule(200)


def test_inertia_units_scale_exactly() -> None:
    assert inertia.KilogramSquareMetre(1) == inertia.KilogramSquareMetrePerSquareTurn(
        (2 * PI) ** 2
    )
    assert inertia.KilogramSquareMetre(1) == inertia.KilogramSquareCentimetre(10_000)
    assert inertia.KilogramSquareCentimetre(1) == inertia.GramSquareCentimetre(1000)
    assert inertia.PoundSquareFoot(1) == inertia.PoundSquareInch(144)
    pound = mass.Pound(1)
    foot = length.Foot(1)
    assert inertia.PoundSquareFoot(1) == pound * foot * foot


def test_angular_momentum_units_scale_exactly() -> None:
    assert angular_momentum.KilogramSquareMetrePerSecond(
        1
    ) == angular_momentum.NewtonMetreSecond(1)
    assert angular_momentum.KilogramSquareMetrePerSecond(
        1
    ) == angular_momentum.JouleSecondPerTurn(2 * PI)


def test_first_moment_of_mass_units_scale_exactly() -> None:
    assert unbalance.KilogramMetre(1) == unbalance.GramCentimetre(100_000)
    assert unbalance.GramCentimetre(1) == unbalance.GramMillimetre(10)
    assert unbalance.OunceInch(1) == mass.Ounce(1) * length.Inch(1)


def test_the_tables_list_the_units_by_symbol() -> None:
    dot = symbols.MIDDLE_DOT
    assert set(inertia.MOMENT_OF_INERTIA_UNITS) == {
        f"{KG_M2}/tr²",
        KG_M2,
        f"kg{dot}cm²",
        f"g{dot}cm²",
        f"lb{dot}ft²",
        f"lb{dot}in²",
    }
    assert set(angular_momentum.ANGULAR_MOMENTUM_UNITS) == {
        f"J{dot}s/tr",
        f"{KG_M2}/s",
        f"N{dot}m{dot}s",
    }
    assert set(unbalance.FIRST_MOMENT_OF_MASS_UNITS) == {
        f"kg{dot}m",
        f"g{dot}cm",
        f"g{dot}mm",
        f"oz{dot}in",
    }
    assert set(angacc.ANGULAR_ACCELERATION_UNITS) == {
        "tr/s²",
        "rad/s²",
        f"{symbols.DEGREE}/s²",
        "rpm/s",
    }


def test_the_canonical_unit_is_what_magnitude_reads_in() -> None:
    assert inertia.KilogramSquareMetrePerSquareTurn(3).magnitude == Fraction(3)
    assert angular_momentum.JouleSecondPerTurn(3).magnitude == Fraction(3)
    assert angacc.TurnPerSecondSquared(3).magnitude == Fraction(3)
    assert unbalance.KilogramMetre(3).magnitude == Fraction(3)
