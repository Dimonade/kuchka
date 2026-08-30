"""Mass, and the Tonne/Megagram alias.

`Tonne` is not a separate unit definition that happens to share Megagram's scale --
it is the exact same function object.

This module exists to prove that at every level: identity, construction, display,
and round-tripping through `.to(...)`.
"""

from decimal import Decimal

import pytest
from kuchka import Gram
from kuchka import InvalidMeasurementError
from kuchka import Kilogram
from kuchka import Mass
from kuchka import Megagram
from kuchka import Microgram
from kuchka import Milligram
from kuchka import Nanogram
from kuchka import Tonne
from kuchka.units import GRAM
from kuchka.units import KILOGRAM
from kuchka.units import MEGAGRAM


def test_tonne_and_megagram_are_the_same_function():
    """Test Megagram and Tonne not merely equal-behaving -- the exact same object."""
    assert Tonne is Megagram


def test_tonne_is_megagram():
    assert Tonne(1) == Megagram(1)
    assert Tonne(5) == Megagram(5)


def test_megagram_is_tonne():
    assert Megagram(1) == Tonne(1)
    assert Megagram(Decimal("2.5")) == Tonne(Decimal("2.5"))


def test_tonne_scales_correctly_against_kilogram():
    assert Tonne(1) == Kilogram(1000)


def test_tonne_displays_as_megagram():
    """Tonne is a plain alias, so it carries Megagram's unit symbol, not its own."""
    assert Tonne(1).unit is MEGAGRAM
    assert repr(Tonne(1)) == "1 Mg"


def test_tonne_to_megagram_round_trip():
    original = Tonne(1)
    round_tripped = original.to(MEGAGRAM).to(KILOGRAM).to(MEGAGRAM)
    assert round_tripped == original
    assert round_tripped == Megagram(1)


def test_tonne_to_kilogram_round_trip_is_exact():
    original = Tonne(Decimal("2.5"))
    as_kilograms = original.to(KILOGRAM)
    assert as_kilograms == Kilogram(2500)
    assert as_kilograms.to(MEGAGRAM) == original


def test_tonne_arithmetic_mixes_freely_with_megagram():
    assert Tonne(1) + Megagram(1) == Tonne(2)
    assert Megagram(1) + Tonne(1) == Megagram(2)


@pytest.mark.parametrize(
    ("prefixed", "canonical", "scale"),
    [
        (Nanogram, Kilogram, Decimal("0.000000000001")),
        (Microgram, Kilogram, Decimal("0.000000001")),
        (Milligram, Kilogram, Decimal("0.000001")),
        (Gram, Kilogram, Decimal("0.001")),
        (Megagram, Kilogram, Decimal(1000)),
        (Tonne, Kilogram, Decimal(1000)),
    ],
    ids=["nanogram", "microgram", "milligram", "gram", "megagram", "tonne"],
)
def test_mass_prefixes_scale_correctly(prefixed, canonical, scale):
    assert prefixed(1) == canonical(scale)


def test_isinstance_of_mass():
    assert isinstance(Kilogram(5), Mass)
    assert isinstance(Tonne(5), Mass)
    assert isinstance(Megagram(5), Mass)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Kilogram(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_gram_and_kilogram_scale_correctly():
    assert Gram(1000) == Kilogram(1)


def test_scalar_multiplication_and_division():
    assert Kilogram(2) * 3 == Kilogram(6)
    assert Tonne(6) / 3 == Tonne(2)


def test_ordering_within_mass():
    assert Gram(500) < Kilogram(1)
    assert Kilogram(1) < Tonne(1)
