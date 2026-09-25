"""Energy: the arithmetic that produces it, its two inverses, and its prefixes.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Energy:
the `Power * Time` relationship, its inverses, and pulse-scale prefix arithmetic.
"""

from kuchka.units import Millielectronvolt

from decimal import Decimal

from kuchka import (
    Energy,
    Microelectronvolt,
    Electronvolt,
    Kiloelectronvolt,
    Megaelectronvolt,
    Gigaelectronvolt,
    Teraelectronvolt,
    Petaelectronvolt,
    Erg,
    Kilocalorie,
    Calorie,
    ThermochemicalCalorie,
    Gigajoule,
    Terajoule,
    Megajoule,
)
from kuchka import Joule
from kuchka import Kilojoule
from kuchka import Microjoule
from kuchka import Millijoule
from kuchka import Nanojoule
from kuchka import Picojoule
from kuchka import Power
from kuchka import Second
from kuchka import Time
from kuchka import Watt


def test_power_times_time_is_energy():
    energy = Watt(10) * Second(5)
    assert isinstance(energy, Energy)
    assert energy == Joule(50)


def test_time_times_power_is_energy_commutatively():
    assert Second(5) * Watt(10) == Watt(10) * Second(5)


def test_energy_divided_by_time_is_power():
    power = Joule(50) / Second(5)
    assert isinstance(power, Power)
    assert power == Watt(10)


def test_energy_divided_by_power_is_time():
    duration = Joule(50) / Watt(10)
    assert isinstance(duration, Time)
    assert duration == Second(5)


def test_energy_prefixes_scale_correctly():
    assert Picojoule(1) == Joule(Decimal("1E-12"))
    assert Nanojoule(1) == Joule(Decimal("1E-9"))
    assert Microjoule(1) == Joule(Decimal("1E-6"))
    assert Millijoule(1) == Joule(Decimal("0.001"))
    assert Kilojoule(1) == Joule(1000)


def test_laser_pulse_energy_arithmetic():
    """The motivating case: pulse energies quoted in mJ/uJ shouldn't need care."""
    pulse = Millijoule(2) + Microjoule(500)
    assert pulse == Millijoule(Decimal("2.5"))


def test_isinstance_of_energy():
    assert isinstance(Joule(1), Energy)


def test_electronvolt_scale_is_exact_from_elementary_charge():
    """Regression test: the old code computed 10e-6 (=1e-5) instead of 1e-6."""
    assert Microelectronvolt(1) == Electronvolt(Decimal("1e-6"))
    assert Millielectronvolt(1) == Electronvolt(Decimal("1e-3"))
    assert Kiloelectronvolt(1) == Electronvolt(1000)
    assert Megaelectronvolt(1) == Electronvolt(Decimal("1e6"))
    assert Gigaelectronvolt(1) == Electronvolt(Decimal("1e9"))
    assert Teraelectronvolt(1) == Electronvolt(Decimal("1e12"))
    assert Petaelectronvolt(1) == Electronvolt(Decimal("1e15"))


def test_teraelectronvolt_is_not_an_alias_of_gigaelectronvolt():
    """Regression test: TERAELECTRONVOLT used to carry GIGAELECTRONVOLT's name/symbol."""
    assert repr(Teraelectronvolt(1)) == "1 TeV"


def test_erg_is_exact():
    assert Erg(10_000_000) == Joule(1)


def test_calorie_and_kilocalorie_are_the_same_function():
    assert Kilocalorie is Calorie
    assert Kilocalorie(650) == Calorie(650)


def test_calorie_matches_joules():
    assert Calorie(1) == Joule(4184)


def test_thermochemical_calorie_is_smaller_than_the_food_calorie():
    assert ThermochemicalCalorie(1) == Joule(Decimal("4.184"))
    assert ThermochemicalCalorie(1000) == Calorie(1)


def test_gigajoule_and_terajoule_scale_correctly():
    assert Gigajoule(1) == Megajoule(1000)
    assert Terajoule(1) == Gigajoule(1000)
