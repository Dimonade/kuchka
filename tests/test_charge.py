"""Charge: the arithmetic that produces it, its two inverses, and its prefixes.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Charge:
the `Current * Time` relationship and its inverses.
"""

from decimal import Decimal

import pytest

from kuchka import Ampere
from kuchka import Charge
from kuchka import Coulomb
from kuchka import Current
from kuchka import IncompatibleDimensionError
from kuchka import Microcoulomb
from kuchka import Milliampere
from kuchka import Millicoulomb
from kuchka import Second
from kuchka import Time
from kuchka import Volt


def test_current_times_time_is_charge():
    charge = Milliampere(2) * Second(5)
    assert isinstance(charge, Charge)
    assert charge == Coulomb(Decimal("0.01"))


def test_time_times_current_is_charge_commutatively():
    assert Second(5) * Milliampere(2) == Milliampere(2) * Second(5)


def test_charge_divided_by_time_is_current():
    current = Coulomb(1) / Second(4)
    assert isinstance(current, Current)
    assert current == Ampere(Decimal("0.25"))


def test_charge_divided_by_current_is_time():
    duration = Coulomb(1) / Ampere(4)
    assert isinstance(duration, Time)
    assert duration == Second(Decimal("0.25"))


def test_charge_prefixes_scale_correctly():
    assert Microcoulomb(1000) == Millicoulomb(1)
    assert Millicoulomb(1000) == Coulomb(1)


def test_charge_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        Coulomb(1) + Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_isinstance_of_charge():
    assert isinstance(Coulomb(1), Charge)
