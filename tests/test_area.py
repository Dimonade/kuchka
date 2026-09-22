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
from kuchka import Hectare
from kuchka import Length
from kuchka import Meter
from kuchka import SquareInch
from kuchka import SquareKilometer
from kuchka import SquareMeter
from kuchka import SquareMillimeter
from kuchka.units import Acre
from kuchka.units import Inch


def test_length_times_length_is_area():
    area = Meter(5) * Meter(2)
    assert isinstance(area, Area)
    assert area == SquareMeter(10)


def test_length_times_length_is_commutative():
    assert Meter(5) * Meter(2) == Meter(2) * Meter(5)


def test_area_divided_by_length_is_length():
    side = SquareMeter(10) / Meter(5)
    assert isinstance(side, Length)
    assert side == Meter(2)


def test_hectare_scales_correctly():
    assert Hectare(1) == SquareMeter(10_000)


def test_hectare_addition():
    assert Hectare(1) + SquareMeter(5_000) == Hectare(Decimal("1.5"))


def test_acre_is_exact_via_the_international_yard():
    """1 acre = 4840 international square yards, exact since the 1959 agreement."""
    assert Acre(1) == SquareMeter(Decimal("4046.8564224"))


def test_square_inch_matches_inch_squared():
    """Squaring `Inch`'s own exact scale should equal `SquareInch`'s directly."""
    assert Inch(1) * Inch(1) == SquareInch(1)


def test_square_kilometre_and_square_millimetre_scale_correctly():
    assert SquareKilometer(1) == SquareMeter(1_000_000)
    assert SquareMillimeter(1_000_000) == SquareMeter(1)


def test_isinstance_of_area():
    assert isinstance(SquareMeter(5), Area)
    assert isinstance(Hectare(5), Area)
    assert isinstance(Acre(5), Area)


def test_scalar_multiplication_and_division():
    assert SquareMeter(2) * 3 == SquareMeter(6)
    assert SquareMeter(6) / 3 == SquareMeter(2)


def test_ordering_within_area():
    assert SquareMeter(500) < Hectare(1)
    assert Acre(1) > SquareMeter(4000)
