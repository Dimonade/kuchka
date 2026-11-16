"""Conductance: the reciprocal of Resistance, and Ohm's law in its conductance form.

Generic algebraic properties (commutativity, associativity, prefix conversion, ...)
are covered once for every registered quantity family elsewhere;
this module covers what is specific to Conductance: `1 / Resistance -> Conductance`
and its inverse `1 / Conductance -> Resistance`, and `Voltage * Conductance ->
Current` alongside its own inverses.
"""

from decimal import Decimal

import pytest

from kuchka import Conductance
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Resistance
from kuchka.units import current as current_units
from kuchka.units.electromagnetics import conductance as conductance_units
from kuchka.units.electromagnetics import resistance as resistance_units
from kuchka.units.electromagnetics import voltage as voltage_units


def test_resistance_reciprocal_is_conductance():
    conductance = 1 / resistance_units.Ohm(5)
    assert isinstance(conductance, Conductance)
    assert conductance == conductance_units.Siemens(Decimal("0.2"))


def test_conductance_reciprocal_is_resistance():
    resistance = 1 / conductance_units.Siemens(Decimal("0.2"))
    assert isinstance(resistance, Resistance)
    assert resistance == resistance_units.Ohm(5)


def test_resistance_conductance_reciprocal_round_trips():
    original = resistance_units.Ohm(5)
    assert 1 / (1 / original) == original


def test_ohms_law_agrees_whether_expressed_as_resistance_or_conductance():
    resistance_form = voltage_units.Volt(10) / resistance_units.Ohm(5)
    conductance_form = voltage_units.Volt(10) * (1 / resistance_units.Ohm(5))
    assert resistance_form == conductance_form == current_units.Ampere(2)


def test_conductance_prefixes_scale_correctly():
    assert conductance_units.Microsiemens(1000) == conductance_units.Millisiemens(1)
    assert conductance_units.Millisiemens(1000) == conductance_units.Siemens(1)
    assert conductance_units.Kilosiemens(1) == conductance_units.Siemens(1000)


def test_isinstance_of_conductance():
    assert isinstance(conductance_units.Siemens(5), Conductance)
    assert isinstance(conductance_units.Millisiemens(5), Conductance)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        conductance_units.Siemens(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_conductance_is_incompatible_with_resistance():
    with pytest.raises(IncompatibleDimensionError):
        conductance_units.Siemens(5) + resistance_units.Ohm(5)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    assert (conductance_units.Siemens(5) == resistance_units.Ohm(5)) is False


def test_scalar_multiplication_and_division():
    assert conductance_units.Siemens(2) * 3 == conductance_units.Siemens(6)
    assert conductance_units.Siemens(6) / 3 == conductance_units.Siemens(2)


def test_ordering_within_conductance():
    assert conductance_units.Microsiemens(500) < conductance_units.Millisiemens(1)
    assert conductance_units.Kilosiemens(1) > conductance_units.Siemens(500)
