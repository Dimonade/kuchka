"""Mass, and the Tonne/Megagram alias.

`Tonne` is not a separate unit definition that happens to share Megagram's scale --
it is the exact same function object.

This module exists to prove that at every level: identity, construction, display,
and round-tripping through `.to(...)`.
"""

from decimal import Decimal

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Mass
from kuchka.internal import symbols
from kuchka.units import mass


def test_tonne_and_megagram_are_the_same_function():
    """Test Megagram and Tonne not merely equal-behaving -- the exact same object."""
    assert mass.Tonne is mass.Megagram


def test_tonne_is_megagram():
    assert mass.Tonne(1) == mass.Megagram(1)
    assert mass.Tonne(5) == mass.Megagram(5)


def test_megagram_is_tonne():
    assert mass.Megagram(1) == mass.Tonne(1)
    assert mass.Megagram(Decimal("2.5")) == mass.Tonne(Decimal("2.5"))


def test_tonne_scales_correctly_against_kilogram():
    assert mass.Tonne(1) == mass.Kilogram(1000)


def test_tonne_displays_as_megagram():
    """Tonne is a plain alias, so it carries Megagram's unit symbol, not its own."""
    assert mass.Tonne(1).unit is mass.MEGAGRAM
    assert repr(mass.Tonne(1)) == "1 Mg"


def test_tonne_to_megagram_round_trip():
    original = mass.Tonne(1)
    round_tripped = original.to(mass.MEGAGRAM).to(mass.KILOGRAM).to(mass.MEGAGRAM)
    assert round_tripped == original
    assert round_tripped == mass.Megagram(1)


def test_tonne_to_kilogram_round_trip_is_exact():
    original = mass.Tonne(Decimal("2.5"))
    as_kilograms = original.to(mass.KILOGRAM)
    assert as_kilograms == mass.Kilogram(2500)
    assert as_kilograms.to(mass.MEGAGRAM) == original


def test_tonne_arithmetic_mixes_freely_with_megagram():
    assert mass.Tonne(1) + mass.Megagram(1) == mass.Tonne(2)
    assert mass.Megagram(1) + mass.Tonne(1) == mass.Megagram(2)


@pytest.mark.parametrize(
    ("prefixed", "canonical", "scale"),
    [
        (mass.Nanogram, mass.Kilogram, Decimal("0.000000000001")),
        (mass.Microgram, mass.Kilogram, Decimal("0.000000001")),
        (mass.Milligram, mass.Kilogram, Decimal("0.000001")),
        (mass.Gram, mass.Kilogram, Decimal("0.001")),
        (mass.Megagram, mass.Kilogram, Decimal(1000)),
        (mass.Tonne, mass.Kilogram, Decimal(1000)),
    ],
    ids=["nanogram", "microgram", "milligram", "gram", "megagram", "tonne"],
)
def test_mass_prefixes_scale_correctly(prefixed, canonical, scale):
    assert prefixed(1) == canonical(scale)


def test_isinstance_of_mass():
    assert isinstance(mass.Kilogram(5), Mass)
    assert isinstance(mass.Tonne(5), Mass)
    assert isinstance(mass.Megagram(5), Mass)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        mass.Kilogram(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_gram_and_kilogram_scale_correctly():
    assert mass.Gram(1000) == mass.Kilogram(1)


def test_scalar_multiplication_and_division():
    assert mass.Kilogram(2) * 3 == mass.Kilogram(6)
    assert mass.Tonne(6) / 3 == mass.Tonne(2)


def test_ordering_within_mass():
    assert mass.Gram(500) < mass.Kilogram(1)
    assert mass.Kilogram(1) < mass.Tonne(1)


def test_picogram_scales_correctly():
    assert mass.Picogram(1000) == mass.Nanogram(1)


def test_picogram_is_a_mass():
    assert isinstance(mass.Picogram(5), Mass)


def test_grain_is_exact():
    """One grain is exactly 1/7000 of the international avoirdupois pound."""
    assert mass.Grain(7000) == mass.Pound(1)


def test_grain_is_a_mass():
    assert isinstance(mass.Grain(147), Mass)


def test_pound_is_a_mass():
    assert isinstance(mass.Pound(50), Mass)


def test_sixteen_ounces_make_a_pound_exactly():
    assert mass.Ounce(16) == mass.Pound(1)


def test_four_hundred_thirty_seven_point_five_grains_make_an_ounce():
    assert mass.Grain(Decimal("437.5")) == mass.Ounce(1)


def test_isinstance_of_the_imperial_mass_units():
    assert isinstance(mass.Pound(5), Mass)
    assert isinstance(mass.Ounce(5), Mass)


def test_ordering_across_the_imperial_mass_ladder():
    assert mass.Ounce(1) < mass.Pound(1)


def test_dalton_is_a_mass():
    assert isinstance(mass.Dalton(18), Mass)


def test_hemoglobin_is_heavier_than_water_in_daltons():
    assert mass.Dalton(64_500) > mass.Dalton(18)


def test_earth_is_lighter_than_the_sun():
    assert mass.EarthMass(1) < mass.SolarMass(1)
    assert mass.EarthMass(318) < mass.SolarMass(1)  # roughly Jupiter's mass


def test_isinstance_of_the_astronomical_mass_units():
    assert isinstance(mass.SolarMass(1), Mass)
    assert isinstance(mass.EarthMass(1), Mass)


def test_sagittarius_a_dwarfs_an_ordinary_car():
    """Pins the module docstring's own worked example as a regression test."""
    yaris = mass.Kilogram(1_000)
    sagittarius_a = mass.SolarMass(4_300_000)
    assert round(sagittarius_a / yaris) == 8_550_188_800_000_000_000_000_000_000_000_000  # noqa: PLR2004  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_megagram_and_tonne_have_distinct_boundary_symbols():
    """Test `MASS_UNITS` must expose "Mg" and "t" as separate keys.

    A draft once set `TONNE = MEGAGRAM` and used `TONNE.symbol` as the dict key --
    since that symbol is "Mg", not "t", it silently dropped the "t" entry.

    This is a regression test.
    """
    assert mass.MASS_UNITS["Mg"] is mass.Megagram
    assert mass.MASS_UNITS["t"] is mass.Tonne
    assert mass.MASS_UNITS["t"] is mass.MASS_UNITS["Mg"]


def test_solar_and_earth_mass_symbols_are_defined():
    """Test both astronomical symbols must exist for this module to import.

    This is a regression test.
    """
    assert symbols.SUN == "\u2609"
    assert symbols.EARTH == "\u2641"
    assert repr(mass.SolarMass(1)) == f"1 M{symbols.SUN}"
    assert repr(mass.EarthMass(1)) == f"1 M{symbols.EARTH}"
