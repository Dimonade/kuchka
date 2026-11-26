"""The mapping round-trips every unit of every quantity type, exactly.

`to_dict` writes the exact value in the unit a measurement displays in, and in every
other unit of its table, and `from_dict` reads it back into an equal measurement in the
unit that was written, through JSON, for every published unit and every shape.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import wire
from tests.support.kinds import UNIT_TABLES

MAGNITUDES = (
    Fraction(0),
    Fraction(5),
    Fraction(7, 3),
    Fraction(21, 5),
    Fraction(-3, 4),
)
# An instant is displayed in seconds only, so it is written in no other unit.
FIXED_DISPLAY = {"INSTANT_UNITS"}
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]


def _through_json(mapping: dict[str, object]) -> dict[str, object]:
    return json.loads(json.dumps(mapping))  # type: ignore[no-any-return]


@pytest.mark.parametrize(
    ("name", "symbol"), UNITS, ids=[f"{name}-{symbol}" for name, symbol in UNITS]
)
def test_every_unit_round_trips_through_the_mapping(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        try:
            original = table[symbol](magnitude)
        except InvalidMeasurementError:
            continue  # a magnitude this quantity cannot hold, such as below zero kelvin
        restored = wire.from_dict(_through_json(wire.to_dict(original)), type(original))
        assert restored == original
        assert restored.unit is original.unit


@pytest.mark.parametrize("name", list(UNIT_TABLES))
def test_every_unit_of_a_table_converts_to_every_other_and_back(name: str) -> None:
    table = UNIT_TABLES[name]
    symbols = [unit.symbol for unit in table.units]
    original = table[symbols[0]](Fraction(7, 3))
    for symbol in symbols:
        if name in FIXED_DISPLAY and symbol != original.unit.symbol:
            with pytest.raises(InvalidConversionError, match="cannot be written in"):
                wire.to_dict(original, unit=symbol)
            continue
        written = wire.to_dict(original, unit=symbol)
        assert written["unit"] == symbol
        restored = wire.from_dict(_through_json(written), type(original))
        assert restored == original
        assert restored.unit.symbol == symbol
