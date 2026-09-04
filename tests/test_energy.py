"""Energy: the arithmetic that produces it, its two inverses, and its prefixes.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Energy:
the `Power * Time` relationship, its inverses, and pulse-scale prefix arithmetic.
"""

from decimal import Decimal

from kuchka import Energy
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
