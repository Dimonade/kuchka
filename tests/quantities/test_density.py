"""Density: the arithmetic that produces it, its two inverses, and its units.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Density: the `Mass / Volume` relationship,
its two inverses, and the `GramPerCubicCentimetre`/`KilogramPerLitre` coincidence.
"""

from decimal import Decimal

import pytest

from kuchka import Density
from kuchka import IncompatibleDimensionError
from kuchka.units import density as density_units
from kuchka.units import mass as mass_units
from kuchka.units import voltage
from kuchka.units import volume as volume_units


def test_density_mass_volume_round_trip():
    mass = mass_units.Kilogram(1000)
    volume = volume_units.CubicMetre(1)
    density = mass / volume
    assert density * volume == mass
    assert mass / density == volume


def test_water_is_a_gram_per_cubic_centimetre_or_a_kilogram_per_litre():
    """Water's density is the textbook check for the naming-tradition coincidence."""
    water = density_units.GramPerCubicCentimetre(1)
    assert water == density_units.KilogramPerLitre(1)
    assert water == density_units.KilogramPerCubicMetre(1000)


def test_gram_per_cubic_centimetre_and_kilogram_per_litre_are_not_the_same_object():
    assert density_units.GramPerCubicCentimetre is not density_units.KilogramPerLitre


def test_gram_per_cubic_centimetre_matches_millilitre_and_gram():
    from kuchka import Gram

    density = Gram(5) / volume_units.Millilitre(5)
    assert density == density_units.GramPerCubicCentimetre(1)


def test_isinstance_of_density():
    assert isinstance(density_units.KilogramPerCubicMetre(5), Density)
    assert isinstance(density_units.GramPerCubicCentimetre(5), Density)
    assert isinstance(density_units.KilogramPerLitre(5), Density)


def test_scalar_multiplication_and_division():
    assert density_units.KilogramPerCubicMetre(
        2
    ) * 3 == density_units.KilogramPerCubicMetre(6)
    assert density_units.KilogramPerCubicMetre(
        6
    ) / 3 == density_units.KilogramPerCubicMetre(2)


def test_ordering_within_density():
    assert density_units.GramPerCubicCentimetre(
        1
    ) > density_units.KilogramPerCubicMetre(500)
    assert density_units.KilogramPerLitre(1) == density_units.GramPerCubicCentimetre(1)


def test_density_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        density_units.KilogramPerCubicMetre(1) + voltage.Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_kilogram_per_litre_matches_kilogram_and_litre_directly():
    density = mass_units.Kilogram(Decimal("2.5")) / volume_units.Litre(1)
    assert density == density_units.KilogramPerLitre(Decimal("2.5"))
