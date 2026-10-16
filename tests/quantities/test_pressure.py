"""Pressure: F / A and P * V = work, plus its SI-prefixed, metric, and imperial units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Pressure: `Force / Area -> Pressure` and its
two inverses, `Pressure * Volume -> Energy` (P-V work) and its inverse, and
the non-SI units `Bar`, `Atmosphere`, and `PoundPerSquareInch`.
"""

from decimal import Decimal

import pytest

from kuchka import EnergyDensity
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Pressure
from kuchka.units import area as area_units
from kuchka.units import energy as energy_units
from kuchka.units import energy_density as edens
from kuchka.units import force as force_units
from kuchka.units import pressure as pressure_units
from kuchka.units import voltage
from kuchka.units import volume as volume_units


def test_force_area_pressure_round_trip():
    force = force_units.Newton(20)
    area = area_units.SquareMetre(4)
    pressure = force / area
    assert pressure * area == force
    assert force / pressure == area


def test_energy_divided_by_volume_is_an_energy_density_not_a_pressure():
    result = energy_units.Joule(10) / volume_units.CubicMetre(2)
    assert isinstance(result, EnergyDensity)
    assert not isinstance(result, Pressure)


def test_pressure_volume_energy_round_trip():
    pressure = pressure_units.Pascal(8)
    volume = volume_units.CubicMetre(3)
    energy = pressure * volume
    assert energy / pressure == volume
    assert energy / volume == edens.JoulePerCubicMetre(8)


def test_pressure_prefixes_scale_correctly():
    assert pressure_units.Hectopascal(1) == pressure_units.Pascal(100)
    assert pressure_units.Kilopascal(1) == pressure_units.Pascal(1000)
    assert pressure_units.Megapascal(1) == pressure_units.Pascal(1_000_000)


def test_bar_is_exact():
    assert pressure_units.Bar(1) == pressure_units.Pascal(100_000)


def test_millibar_and_hectopascal_coincide_exactly():
    """Same physical quantity, different naming tradition -- not an alias pair."""
    assert pressure_units.Millibar(1) == pressure_units.Hectopascal(1)
    assert pressure_units.Millibar is not pressure_units.Hectopascal


def test_atmosphere_is_exact():
    assert pressure_units.Atmosphere(1) == pressure_units.Pascal(101_325)


def test_pound_per_square_inch_matches_the_defining_formula():
    """Psi is derived from POUND_FORCE / SQUARE_INCH, not a separate literal."""
    from_definition = force_units.Newton(
        Decimal("4.4482216152605")
    ) / area_units.SquareInch(1)
    assert pressure_units.PoundPerSquareInch(1) == from_definition


def test_pound_per_square_inch_matches_known_value():
    assert round(pressure_units.PoundPerSquareInch(1).magnitude, 6) == Decimal(
        "6894.757293"
    )


def test_isinstance_of_pressure():
    assert isinstance(pressure_units.Pascal(5), Pressure)
    assert isinstance(pressure_units.Bar(5), Pressure)
    assert isinstance(pressure_units.Atmosphere(5), Pressure)
    assert isinstance(pressure_units.PoundPerSquareInch(5), Pressure)


def test_scalar_multiplication_and_division():
    assert pressure_units.Pascal(2) * 3 == pressure_units.Pascal(6)
    assert pressure_units.Pascal(6) / 3 == pressure_units.Pascal(2)


def test_ordering_within_pressure():
    assert pressure_units.Hectopascal(5) < pressure_units.Kilopascal(1)
    assert pressure_units.Bar(1) > pressure_units.Pascal(500)
    assert pressure_units.Atmosphere(1) > pressure_units.Bar(1)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        pressure_units.Pascal(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_pressure_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        pressure_units.Pascal(1) + voltage.Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types
