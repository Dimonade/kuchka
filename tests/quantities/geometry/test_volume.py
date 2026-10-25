"""Volume: the arithmetic that produces it, its two inverses, and the litre family.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Volume: `Area * Length -> Volume` and
`Length * Area -> Volume`, the two inverses `Volume / Length -> Area` and
`Volume / Area -> Length`, and the litre family's coincidental overlap with the
cubic-metric units.
"""

from decimal import Decimal

from kuchka import Volume
from kuchka.units import length
from kuchka.units.geometry import area
from kuchka.units.geometry import volume as volume_units


def test_volume_length_area_round_trip():
    original = area.SquareMeter(12)
    depth = length.Meter(2)
    volume = original * depth
    assert volume / depth == original


def test_litre_is_a_cubic_decimetre():
    assert volume_units.Litre(1) == volume_units.CubicMetre(Decimal("0.001"))


def test_millilitre_and_cubic_centimetre_coincide_exactly():
    """Same physical quantity, different naming tradition -- not an alias pair."""
    assert volume_units.Millilitre(1) == volume_units.CubicCentimetre(1)
    assert volume_units.Millilitre is not volume_units.CubicCentimetre


def test_microlitre_and_cubic_millimetre_coincide_exactly():
    assert volume_units.Microlitre(1) == volume_units.CubicMillimetre(1)


def test_litre_prefixes_scale_correctly():
    assert volume_units.Microlitre(1_000_000) == volume_units.Litre(1)
    assert volume_units.Millilitre(1_000) == volume_units.Litre(1)


def test_isinstance_of_volume():
    assert isinstance(volume_units.CubicMetre(5), Volume)
    assert isinstance(volume_units.Litre(5), Volume)


def test_scalar_multiplication_and_division():
    assert volume_units.CubicMetre(2) * 3 == volume_units.CubicMetre(6)
    assert volume_units.Litre(6) / 3 == volume_units.Litre(2)


def test_ordering_within_volume():
    assert volume_units.Millilitre(500) < volume_units.Litre(1)
