"""Density: the arithmetic that produces it, its two inverses, and its units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Density: the `Mass / Volume` relationship,
its two inverses, and the `GramPerCubicCentimetre`/`KilogramPerLitre` coincidence.
"""

from decimal import Decimal

import pytest

from kuchka import CubicMetre
from kuchka import Density
from kuchka import GramPerCubicCentimetre
from kuchka import IncompatibleDimensionError
from kuchka import Kilogram
from kuchka import KilogramPerCubicMetre
from kuchka import KilogramPerLitre
from kuchka import Litre
from kuchka import Mass
from kuchka import Millilitre
from kuchka import Volt
from kuchka import Volume


def test_mass_divided_by_volume_is_density():
    density = Kilogram(2000) / CubicMetre(1)
    assert isinstance(density, Density)
    assert density == KilogramPerCubicMetre(2000)


def test_density_times_volume_is_mass():
    mass = KilogramPerCubicMetre(2000) * CubicMetre(1)
    assert isinstance(mass, Mass)
    assert mass == Kilogram(2000)


def test_volume_times_density_is_mass_commutatively():
    assert CubicMetre(1) * KilogramPerCubicMetre(2000) == KilogramPerCubicMetre(
        2000
    ) * CubicMetre(1)


def test_mass_divided_by_density_is_volume():
    volume = Kilogram(2000) / KilogramPerCubicMetre(2000)
    assert isinstance(volume, Volume)
    assert volume == CubicMetre(1)


def test_density_mass_volume_round_trip():
    mass = Kilogram(1000)
    volume = CubicMetre(1)
    density = mass / volume
    assert density * volume == mass
    assert mass / density == volume


def test_water_is_a_gram_per_cubic_centimetre_or_a_kilogram_per_litre():
    """Water's density is the textbook check for the naming-tradition coincidence."""
    water = GramPerCubicCentimetre(1)
    assert water == KilogramPerLitre(1)
    assert water == KilogramPerCubicMetre(1000)


def test_gram_per_cubic_centimetre_and_kilogram_per_litre_are_not_the_same_object():
    assert GramPerCubicCentimetre is not KilogramPerLitre


def test_gram_per_cubic_centimetre_matches_millilitre_and_gram():
    from kuchka import Gram

    density = Gram(5) / Millilitre(5)
    assert density == GramPerCubicCentimetre(1)


def test_isinstance_of_density():
    assert isinstance(KilogramPerCubicMetre(5), Density)
    assert isinstance(GramPerCubicCentimetre(5), Density)
    assert isinstance(KilogramPerLitre(5), Density)


def test_scalar_multiplication_and_division():
    assert KilogramPerCubicMetre(2) * 3 == KilogramPerCubicMetre(6)
    assert KilogramPerCubicMetre(6) / 3 == KilogramPerCubicMetre(2)


def test_ordering_within_density():
    assert GramPerCubicCentimetre(1) > KilogramPerCubicMetre(500)
    assert KilogramPerLitre(1) == GramPerCubicCentimetre(1)


def test_density_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        KilogramPerCubicMetre(1) + Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_kilogram_per_litre_matches_kilogram_and_litre_directly():
    density = Kilogram(Decimal("2.5")) / Litre(1)
    assert density == KilogramPerLitre(Decimal("2.5"))
