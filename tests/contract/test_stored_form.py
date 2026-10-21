"""Storing a quantity: the magnitude as exact text, and the unit by its symbol.

Pickle moves a quantity between processes of one kuchka version.
It names Python classes and the unit constants by name, so it is not a storage format.
A quantity is stored as the pair its unit gives it: the exact magnitude in that unit,
written as text, and the unit's symbol.
Restoring reads the symbol through the quantity's `*_UNITS` table, which accepts the
display symbol and every other spelling of it, and rebuilds the same value.
"""

from __future__ import annotations

import json
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Any

import pytest

from kuchka.internal import symbols
from kuchka.units import thermal
from kuchka.units import thermal as thermal_units
from kuchka.units import voltage
from tests.support.kinds import UNIT_TABLES

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

MAGNITUDES = (Fraction(0), Fraction(7, 3), Fraction(5), Fraction(1, 10**12))
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]
UNIT_IDS = [f"{name}-{symbol}" for name, symbol in UNITS]


def store(value: Any) -> dict[str, str]:  # noqa: ANN401 -- a quantity of any shape
    """Return the storable form of `value`: exact magnitude text, and unit symbol."""
    return {"value": str(value.value_in(value.unit)), "unit": value.unit.symbol}


def restore(
    table: Mapping[str, Callable[[Numeric], Any]], stored: dict[str, str]
) -> Any:  # noqa: ANN401 -- a quantity of any shape
    """Rebuild a value from its storable form through `table`."""
    return table[stored["unit"]](Fraction(stored["value"]))


@pytest.mark.parametrize(("name", "symbol"), UNITS, ids=UNIT_IDS)
def test_every_unit_round_trips_through_its_stored_form(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        original = table[symbol](magnitude)
        restored = restore(table, store(original))
        assert restored == original, magnitude
        assert restored.unit is original.unit, magnitude
        assert store(restored) == store(original), magnitude


def test_a_negative_magnitude_round_trips() -> None:
    original = voltage.Volt(Fraction(-5, 3))
    assert restore(voltage.VOLTAGE_UNITS, store(original)) == original


def test_the_stored_form_is_plain_json() -> None:
    stored = store(voltage.Millivolt(Fraction(7, 3)))
    assert json.loads(json.dumps(stored)) == stored
    assert stored == {"value": "7/3", "unit": "mV"}


def test_an_exact_fraction_survives_where_a_float_would_not() -> None:
    original = voltage.Volt(Fraction(1, 3))
    assert restore(voltage.VOLTAGE_UNITS, store(original)) == original


def test_the_stored_symbol_may_be_written_in_another_spelling() -> None:
    stored = {"value": "21.5", "unit": "degrees C"}
    assert restore(thermal.TEMPERATURE_UNITS, stored) == thermal_units.Celsius(
        Fraction("21.5")
    )


def test_the_micro_sign_in_a_stored_symbol_restores() -> None:
    stored = {"value": "5", "unit": f"{symbols.MICRO}V"}
    restored = restore(voltage.VOLTAGE_UNITS, stored)
    assert restored.value_in(voltage.MICROVOLT) == Fraction(5)


def test_a_stored_unit_that_the_table_does_not_know_is_a_key_error() -> None:
    with pytest.raises(KeyError):
        restore(voltage.VOLTAGE_UNITS, {"value": "5", "unit": "A"})
