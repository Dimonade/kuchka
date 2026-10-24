"""Energy: the arithmetic that produces it, its two inverses, and its prefixes.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Energy:
the `Power * Time` relationship, its inverses, and pulse-scale prefix arithmetic.
"""

from decimal import Decimal

from kuchka import Energy
from kuchka.units import energy as energy_units


def test_energy_prefixes_scale_correctly():
    assert energy_units.Picojoule(1) == energy_units.Joule(Decimal("1E-12"))
    assert energy_units.Nanojoule(1) == energy_units.Joule(Decimal("1E-9"))
    assert energy_units.Microjoule(1) == energy_units.Joule(Decimal("1E-6"))
    assert energy_units.Millijoule(1) == energy_units.Joule(Decimal("0.001"))
    assert energy_units.Kilojoule(1) == energy_units.Joule(1000)


def test_laser_pulse_energy_arithmetic():
    """The motivating case: pulse energies quoted in mJ/uJ shouldn't need care."""
    pulse = energy_units.Millijoule(2) + energy_units.Microjoule(500)
    assert pulse == energy_units.Millijoule(Decimal("2.5"))


def test_isinstance_of_energy():
    assert isinstance(energy_units.Joule(1), Energy)


def test_electronvolt_scale_is_exact_from_elementary_charge():
    """Regression test: the old code computed 10e-6 (=1e-5) instead of 1e-6."""
    assert energy_units.Microelectronvolt(1) == energy_units.Electronvolt(
        Decimal("1e-6")
    )
    assert energy_units.Millielectronvolt(1) == energy_units.Electronvolt(
        Decimal("1e-3")
    )
    assert energy_units.Kiloelectronvolt(1) == energy_units.Electronvolt(1000)
    assert energy_units.Megaelectronvolt(1) == energy_units.Electronvolt(Decimal("1e6"))
    assert energy_units.Gigaelectronvolt(1) == energy_units.Electronvolt(Decimal("1e9"))
    assert energy_units.Teraelectronvolt(1) == energy_units.Electronvolt(
        Decimal("1e12")
    )
    assert energy_units.Petaelectronvolt(1) == energy_units.Electronvolt(
        Decimal("1e15")
    )


def test_teraelectronvolt_is_not_an_alias_of_gigaelectronvolt():
    """Test that TERAELECTRONVOLT used to carry GIGAELECTRONVOLT's name/symbol.

    This is a regression test.
    """
    assert repr(energy_units.Teraelectronvolt(1)) == "1 TeV"


def test_erg_is_exact():
    assert energy_units.Erg(10_000_000) == energy_units.Joule(1)


def test_calorie_and_kilocalorie_are_the_same_function():
    assert energy_units.Kilocalorie is energy_units.Calorie
    assert energy_units.Kilocalorie(650) == energy_units.Calorie(650)


def test_calorie_matches_joules():
    assert energy_units.Calorie(1) == energy_units.Joule(4184)


def test_thermochemical_calorie_is_smaller_than_the_food_calorie():
    assert energy_units.ThermochemicalCalorie(1) == energy_units.Joule(Decimal("4.184"))
    assert energy_units.ThermochemicalCalorie(1000) == energy_units.Calorie(1)


def test_gigajoule_and_terajoule_scale_correctly():
    assert energy_units.Gigajoule(1) == energy_units.Megajoule(1000)
    assert energy_units.Terajoule(1) == energy_units.Gigajoule(1000)


def test_tonne_of_tnt_converts_to_joules_exactly() -> None:
    assert energy_units.TonneOfTNT(1) == energy_units.Joule(Decimal(4184000000))


def test_kilotonne_of_tnt_converts_to_joules_exactly() -> None:
    assert energy_units.KilotonneOfTNT(1) == energy_units.Joule(Decimal(4184000000000))


def test_megatonne_of_tnt_converts_to_joules_exactly() -> None:
    assert energy_units.MegatonneOfTNT(1) == energy_units.Joule(
        Decimal(4184000000000000)
    )
