"""`format_parts` joined is `format`, for every unit of every quantity type."""

from __future__ import annotations

from fractions import Fraction

import pytest

from tests.support.kinds import UNIT_TABLES

SPECS = ("", ".2f", ".0f", ".3e", "+.1f", ",.2f")
MAGNITUDES = (Fraction(0), Fraction(5, 2), Fraction(7, 3), Fraction(21, 5))
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]


@pytest.mark.parametrize(
    ("name", "symbol"), UNITS, ids=[f"{name}-{symbol}" for name, symbol in UNITS]
)
def test_the_parts_joined_are_the_formatted_measurement(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        value = table[symbol](magnitude)
        for spec in SPECS:
            magnitude_text, unit_text = value.format_parts(spec)
            assert unit_text == value.unit.symbol
            assert f"{magnitude_text} {unit_text}" == format(value, spec)
        assert " ".join(value.format_parts()) == repr(value) == str(value)
