"""Area: the arithmetic that produces it and its relationships to Length and Volume.

This module covers what is specific to Area:
- `Length * Length -> Area`, its inverse,
- `Area / Length -> Length`, and the exact non-SI units,
- `Hectare` and `Acre`.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
"""

from decimal import Decimal

from kuchka import Area
from kuchka.units import length
from kuchka.units.geometry import area as area_units


def test_hectare_scales_correctly():
    assert area_units.Hectare(1) == area_units.SquareMeter(10_000)


def test_hectare_addition():
    assert area_units.Hectare(1) + area_units.SquareMeter(5_000) == area_units.Hectare(
        Decimal("1.5")
    )


def test_acre_is_exact_via_the_international_yard():
    """1 acre = 4840 international square yards, exact since the 1959 agreement."""
    assert area_units.Acre(1) == area_units.SquareMeter(Decimal("4046.8564224"))


def test_square_inch_matches_inch_squared():
    """Squaring `Inch`'s own exact scale should equal `SquareInch`'s directly."""
    assert length.Inch(1) * length.Inch(1) == area_units.SquareInch(1)


def test_square_kilometre_and_square_millimetre_scale_correctly():
    assert area_units.SquareKilometer(1) == area_units.SquareMeter(1_000_000)
    assert area_units.SquareMillimeter(1_000_000) == area_units.SquareMeter(1)


def test_isinstance_of_area():
    assert isinstance(area_units.SquareMeter(5), Area)
    assert isinstance(area_units.Hectare(5), Area)
    assert isinstance(area_units.Acre(5), Area)


def test_scalar_multiplication_and_division():
    assert area_units.SquareMeter(2) * 3 == area_units.SquareMeter(6)
    assert area_units.SquareMeter(6) / 3 == area_units.SquareMeter(2)


def test_ordering_within_area():
    assert area_units.SquareMeter(500) < area_units.Hectare(1)
    assert area_units.Acre(1) > area_units.SquareMeter(4000)
