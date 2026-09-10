"""Volume: the arithmetic that produces it, its two inverses, and the litre family.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Volume: `Area * Length -> Volume` and
`Length * Area -> Volume`, the two inverses `Volume / Length -> Area` and
`Volume / Area -> Length`, and the litre family's coincidental overlap with the
cubic-metric units.
"""

from decimal import Decimal

from kuchka import Area
from kuchka import CubicCentimetre
from kuchka import CubicMetre
from kuchka import CubicMillimetre
from kuchka import Length
from kuchka import Litre
from kuchka import Meter
from kuchka import Microlitre
from kuchka import Millilitre
from kuchka import SquareMeter
from kuchka import Volume


def test_area_times_length_is_volume():
    volume = SquareMeter(10) * Meter(3)
    assert isinstance(volume, Volume)
    assert volume == CubicMetre(30)


def test_length_times_area_is_volume_commutatively():
    assert Meter(3) * SquareMeter(10) == SquareMeter(10) * Meter(3)


def test_volume_divided_by_length_is_area():
    base = CubicMetre(30) / Meter(3)
    assert isinstance(base, Area)
    assert base == SquareMeter(10)


def test_volume_divided_by_area_is_length():
    height = CubicMetre(30) / SquareMeter(10)
    assert isinstance(height, Length)
    assert height == Meter(3)


def test_volume_length_area_round_trip():
    original = SquareMeter(12)
    depth = Meter(2)
    volume = original * depth
    assert volume / depth == original


def test_litre_is_a_cubic_decimetre():
    assert Litre(1) == CubicMetre(Decimal("0.001"))


def test_millilitre_and_cubic_centimetre_coincide_exactly():
    """Same physical quantity, different naming tradition -- not an alias pair."""
    assert Millilitre(1) == CubicCentimetre(1)
    assert Millilitre is not CubicCentimetre


def test_microlitre_and_cubic_millimetre_coincide_exactly():
    assert Microlitre(1) == CubicMillimetre(1)


def test_litre_prefixes_scale_correctly():
    assert Microlitre(1_000_000) == Litre(1)
    assert Millilitre(1_000) == Litre(1)


def test_isinstance_of_volume():
    assert isinstance(CubicMetre(5), Volume)
    assert isinstance(Litre(5), Volume)


def test_scalar_multiplication_and_division():
    assert CubicMetre(2) * 3 == CubicMetre(6)
    assert Litre(6) / 3 == Litre(2)


def test_ordering_within_volume():
    assert Millilitre(500) < Litre(1)
