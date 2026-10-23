"""`parse` reads every spelling of every unit of every quantity type.

The cases come from the library: each concrete quantity type, and each spelling its own
table accepts, so a type or a unit added later is covered without an edit.
"""

from __future__ import annotations

import pytest

from kuchka import parse
from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import UNIT_TABLES


def _spellings(table: object) -> list[str]:
    """Every text the table accepts: the symbols, the aliases, and the spoken forms."""
    return sorted(set(table._exact) | set(table._words))  # type: ignore[attr-defined]  # noqa: SLF001


@pytest.mark.parametrize("quantity", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_type_has_the_table_it_is_published_with(quantity: type) -> None:
    table = quantity._unit_table  # type: ignore[attr-defined]  # noqa: SLF001
    assert any(table is published for published in UNIT_TABLES.values())


@pytest.mark.parametrize("quantity", QUANTITY_TYPES, ids=TYPE_IDS)
def test_every_spelling_of_a_unit_reads_as_that_unit(quantity: type) -> None:
    table = quantity._unit_table  # type: ignore[attr-defined]  # noqa: SLF001
    for spelling in _spellings(table):
        parsed = parse(f"3 {spelling}", quantity)
        expected = table[spelling](3)
        assert type(parsed) is quantity, spelling
        assert parsed == expected, spelling
        assert repr(parsed) == repr(expected), spelling


@pytest.mark.parametrize("quantity", QUANTITY_TYPES, ids=TYPE_IDS)
def test_the_space_between_the_number_and_the_unit_is_optional(quantity: type) -> None:
    table = quantity._unit_table  # type: ignore[attr-defined]  # noqa: SLF001
    for unit in table.units:
        if unit.symbol[0].isdigit():
            continue  # the digits would continue the number: this unit takes a space
        spaced = parse(f"7 {unit.symbol}", quantity)
        assert parse(f"7{unit.symbol}", quantity) == spaced, unit.symbol
