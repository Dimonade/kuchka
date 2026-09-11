"""Conductance: the reciprocal of Resistance, and Ohm's law in its conductance form.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Conductance: `1 / Resistance -> Conductance`
and its inverse `1 / Conductance -> Resistance`, and `Voltage * Conductance ->
Current` alongside its own inverses.
"""

from decimal import Decimal

import pytest

from kuchka import Ampere
from kuchka import Conductance
from kuchka import Current
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Kilosiemens
from kuchka import Microsiemens
from kuchka import Millisiemens
from kuchka import Ohm
from kuchka import Resistance
from kuchka import Siemens
from kuchka import Volt
from kuchka import Voltage


def test_resistance_reciprocal_is_conductance():
    conductance = 1 / Ohm(5)
    assert isinstance(conductance, Conductance)
    assert conductance == Siemens(Decimal("0.2"))


def test_conductance_reciprocal_is_resistance():
    resistance = 1 / Siemens(Decimal("0.2"))
    assert isinstance(resistance, Resistance)
    assert resistance == Ohm(5)


def test_resistance_conductance_reciprocal_round_trips():
    original = Ohm(5)
    assert 1 / (1 / original) == original


def test_voltage_times_conductance_is_current():
    current = Volt(10) * Siemens(Decimal("0.5"))
    assert isinstance(current, Current)
    assert current == Ampere(5)


def test_conductance_times_voltage_is_current_commutatively():
    assert Volt(10) * Siemens(Decimal("0.5")) == Siemens(Decimal("0.5")) * Volt(10)


def test_current_divided_by_voltage_is_conductance():
    conductance = Ampere(5) / Volt(10)
    assert isinstance(conductance, Conductance)
    assert conductance == Siemens(Decimal("0.5"))


def test_current_divided_by_conductance_is_voltage():
    voltage = Ampere(5) / Siemens(Decimal("0.5"))
    assert isinstance(voltage, Voltage)
    assert voltage == Volt(10)


def test_ohms_law_agrees_whether_expressed_as_resistance_or_conductance():
    resistance_form = Volt(10) / Ohm(5)
    conductance_form = Volt(10) * (1 / Ohm(5))
    assert resistance_form == conductance_form == Ampere(2)


def test_conductance_prefixes_scale_correctly():
    assert Microsiemens(1000) == Millisiemens(1)
    assert Millisiemens(1000) == Siemens(1)
    assert Kilosiemens(1) == Siemens(1000)


def test_isinstance_of_conductance():
    assert isinstance(Siemens(5), Conductance)
    assert isinstance(Millisiemens(5), Conductance)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Siemens(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_conductance_is_incompatible_with_resistance():
    with pytest.raises(IncompatibleDimensionError):
        Siemens(5) + Ohm(5)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    assert (Siemens(5) == Ohm(5)) is False


def test_scalar_multiplication_and_division():
    assert Siemens(2) * 3 == Siemens(6)
    assert Siemens(6) / 3 == Siemens(2)


def test_ordering_within_conductance():
    assert Microsiemens(500) < Millisiemens(1)
    assert Kilosiemens(1) > Siemens(500)
