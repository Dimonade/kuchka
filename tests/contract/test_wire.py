"""The wire form round-trips every unit of every quantity type, exactly.

`dump` writes the exact magnitude in the unit a measurement displays in and the unit's
symbol, and `load` reads that back into the same value in the same unit, for every
published unit and every shape.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from hypothesis import example
from hypothesis import given
from hypothesis import strategies as st

from kuchka import Voltage
from kuchka import wire
from kuchka.units import angular
from kuchka.units import logarithmic
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage
from tests.support.kinds import UNIT_TABLES

MAGNITUDES = (
    Fraction(0),
    Fraction(5),
    Fraction(7, 3),
    Fraction(21, 5),
    Fraction(1, 1024),
    Fraction(1, 10**12),
    Fraction(10**30),
)
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]
UNIT_IDS = [f"{name}-{symbol}" for name, symbol in UNITS]


@pytest.mark.parametrize(("name", "symbol"), UNITS, ids=UNIT_IDS)
def test_every_unit_round_trips_through_the_wire_form(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        original = table[symbol](magnitude)
        text = wire.dump(original)
        restored = wire.load(text, type(original))
        assert restored == original, text
        assert restored.unit is original.unit, text
        assert wire.dump(restored) == text, text


def test_a_negative_magnitude_round_trips_in_every_shape() -> None:
    for original in (
        voltage.Volt(Fraction(-5, 3)),
        thermal.Celsius(-40),
        thermal.Celsius(Fraction(-1, 3)),
        thermal.Fahrenheit(Fraction(-1, 3)),
        angular.Degree(Fraction(-90)),
        logarithmic.Decibel(Fraction(-3)),
        proportion.Percent(Fraction(-1, 3)),
    ):
        restored = wire.load(wire.dump(original), type(original))
        assert restored == original, original
        assert restored.unit is original.unit, original


@given(
    magnitude=st.fractions(min_value=-(10**6), max_value=10**6, max_denominator=10**6)
)
@example(magnitude=Fraction(1, 3))
@example(magnitude=Fraction(0))
def test_every_magnitude_round_trips_and_is_written_as_a_decimal_only_when_exact(
    magnitude: Fraction,
) -> None:
    original = voltage.Millivolt(magnitude)
    text = wire.dump(original)
    assert wire.load(text, Voltage) == original
    number = text.removesuffix(" mV")
    assert Fraction(number) == magnitude
    denominator = magnitude.denominator
    for factor in (2, 5):
        while denominator % factor == 0:
            denominator //= factor
    assert ("/" in number) is (denominator != 1)
