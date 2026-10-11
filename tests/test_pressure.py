"""Pressure: F / A and P * V = work, plus its SI-prefixed, metric, and imperial units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Pressure: `Force / Area -> Pressure` and its
two inverses, `Pressure * Volume -> Energy` (P-V work) and its inverse, and
the non-SI units `Bar`, `Atmosphere`, and `PoundPerSquareInch`.
"""

from decimal import Decimal

import pytest

from kuchka import Area
from kuchka import Atmosphere
from kuchka import Bar
from kuchka import CubicMetre
from kuchka import Energy
from kuchka import EnergyDensity
from kuchka import Force
from kuchka import Hectopascal
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Joule
from kuchka import JoulePerCubicMetre
from kuchka import Kilopascal
from kuchka import Megapascal
from kuchka import Millibar
from kuchka import Newton
from kuchka import Pascal
from kuchka import PoundPerSquareInch
from kuchka import Pressure
from kuchka import SquareInch
from kuchka import SquareMetre
from kuchka import Volt
from kuchka import Volume


def test_force_divided_by_area_is_pressure():
    pressure = Newton(10) / SquareMetre(2)
    assert isinstance(pressure, Pressure)
    assert pressure == Pascal(5)


def test_pressure_times_area_is_force():
    force = Pascal(5) * SquareMetre(2)
    assert isinstance(force, Force)
    assert force == Newton(10)


def test_area_times_pressure_is_force_commutatively():
    assert SquareMetre(2) * Pascal(5) == Pascal(5) * SquareMetre(2)


def test_force_divided_by_pressure_is_area():
    area = Newton(10) / Pascal(5)
    assert isinstance(area, Area)
    assert area == SquareMetre(2)


def test_force_area_pressure_round_trip():
    force = Newton(20)
    area = SquareMetre(4)
    pressure = force / area
    assert pressure * area == force
    assert force / pressure == area


def test_pressure_times_volume_is_energy():
    energy = Pascal(5) * CubicMetre(2)
    assert isinstance(energy, Energy)
    assert energy == Joule(10)


def test_volume_times_pressure_is_energy_commutatively():
    assert Pascal(5) * CubicMetre(2) == CubicMetre(2) * Pascal(5)


def test_energy_divided_by_pressure_is_volume():
    volume = Joule(10) / Pascal(5)
    assert isinstance(volume, Volume)
    assert volume == CubicMetre(2)


def test_energy_divided_by_volume_is_an_energy_density_not_a_pressure():
    result = Joule(10) / CubicMetre(2)
    assert isinstance(result, EnergyDensity)
    assert not isinstance(result, Pressure)


def test_pressure_volume_energy_round_trip():
    pressure = Pascal(8)
    volume = CubicMetre(3)
    energy = pressure * volume
    assert energy / pressure == volume
    assert energy / volume == JoulePerCubicMetre(8)


def test_pressure_prefixes_scale_correctly():
    assert Hectopascal(1) == Pascal(100)
    assert Kilopascal(1) == Pascal(1000)
    assert Megapascal(1) == Pascal(1_000_000)


def test_bar_is_exact():
    assert Bar(1) == Pascal(100_000)


def test_millibar_and_hectopascal_coincide_exactly():
    """Same physical quantity, different naming tradition -- not an alias pair."""
    assert Millibar(1) == Hectopascal(1)
    assert Millibar is not Hectopascal


def test_atmosphere_is_exact():
    assert Atmosphere(1) == Pascal(101_325)


def test_pound_per_square_inch_matches_the_defining_formula():
    """Psi is derived from POUND_FORCE / SQUARE_INCH, not a separate literal."""
    from_definition = Newton(Decimal("4.4482216152605")) / SquareInch(1)
    assert PoundPerSquareInch(1) == from_definition


def test_pound_per_square_inch_matches_known_value():
    assert round(PoundPerSquareInch(1).magnitude, 6) == Decimal("6894.757293")


def test_isinstance_of_pressure():
    assert isinstance(Pascal(5), Pressure)
    assert isinstance(Bar(5), Pressure)
    assert isinstance(Atmosphere(5), Pressure)
    assert isinstance(PoundPerSquareInch(5), Pressure)


def test_scalar_multiplication_and_division():
    assert Pascal(2) * 3 == Pascal(6)
    assert Pascal(6) / 3 == Pascal(2)


def test_ordering_within_pressure():
    assert Hectopascal(5) < Kilopascal(1)
    assert Bar(1) > Pascal(500)
    assert Atmosphere(1) > Bar(1)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Pascal(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_pressure_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        Pascal(1) + Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types
