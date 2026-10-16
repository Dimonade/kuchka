"""The published `*_UNITS` tables are read-only maps from display symbol to constructor.

They exist for the one place a unit arrives as a string: an I/O boundary such as a
configuration file, a CSV header, or a hardware descriptor.
Each table is closed to one physical dimension, and iterating it yields the display
symbols of its units.
The cases are the tables `kuchka.units` publishes, so a table added later is checked
without an edit here; the other notations a table accepts are in `test_spelling_*`.
"""

from __future__ import annotations

import pytest

from tests.support.kinds import UNIT_TABLES

FOREIGN_SYMBOLS = ("mA", "V", "Hz", "Bd", "m", "kg", "Wb")


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_iterating_a_table_yields_the_display_symbols_of_its_units(name: str) -> None:
    table = UNIT_TABLES[name]
    assert list(table) == [unit.symbol for unit in table.units]


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_every_constructor_builds_a_value_of_one_type(name: str) -> None:
    table = UNIT_TABLES[name]
    kinds = {type(constructor(5)) for constructor in table.values()}
    assert len(kinds) == 1, kinds


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_a_table_is_closed_to_the_symbols_of_other_dimensions(name: str) -> None:
    table = UNIT_TABLES[name]
    for symbol in set(FOREIGN_SYMBOLS) - set(table):
        assert symbol not in table, symbol


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_a_table_cannot_be_written_to(name: str) -> None:
    table = UNIT_TABLES[name]
    symbol = next(iter(table))
    with pytest.raises(TypeError):
        table[symbol] = table[symbol]  # type: ignore[index]
    with pytest.raises(TypeError):
        del table[symbol]  # type: ignore[attr-defined,misc]
