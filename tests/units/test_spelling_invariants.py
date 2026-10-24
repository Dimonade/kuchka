"""Invariants of every `*_UNITS` table, discovered from `kuchka.units`.

A table or a spelling added later is checked without editing this file: the cases are
the units each published table holds.
"""

from __future__ import annotations

import pytest

from kuchka.internal.spelling import fold
from kuchka.internal.spelling import normalize
from kuchka.internal.unit_table import UnitTable
from tests.support.kinds import UNIT_TABLES

TABLE_NAMES = sorted(UNIT_TABLES)
UNIT_CASES = [
    (name, unit) for name, table in UNIT_TABLES.items() for unit in table.units
]
UNIT_CASE_IDS = [f"{name}-{unit.symbol}" for name, unit in UNIT_CASES]
TEXT_THAT_IS_NO_UNIT = ("", " ", "nope", "5", "5 mV", "??")


def test_every_unit_table_is_discovered() -> None:
    assert len(UNIT_TABLES) > 25  # noqa: PLR2004 -- a floor, so discovery cannot silently empty
    assert all(isinstance(table, UnitTable) for table in UNIT_TABLES.values())


@pytest.mark.parametrize(("name", "unit"), UNIT_CASES, ids=UNIT_CASE_IDS)
def test_every_spelling_of_a_unit_resolves_back_to_it(name: str, unit) -> None:
    table = UNIT_TABLES[name]
    expected = table[unit.symbol]
    # A table derived from another builds values in the canonical unit of its own type,
    # so the display unit is checked only where the table names its units itself.
    if not name.startswith(("INSTANT", "SAMPLING", "STRESS")):
        assert expected(1).unit is unit
    for alias in unit.aliases:
        assert table[alias] is expected, alias
    for word in (unit.name, *unit.words):
        assert table[word] is expected, word
    for word in (unit.name.replace("_", " "), *unit.words):
        assert table[word.upper()] is expected, word
        assert table[word.title()] is expected, word
        assert table[f"{word}s"] is expected, word


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_display_symbols_are_unique_within_a_table(name: str) -> None:
    symbols = list(UNIT_TABLES[name])
    assert len(symbols) == len(set(symbols))


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_no_symbol_or_alias_means_two_units(name: str) -> None:
    claimed: dict[str, object] = {}
    for unit in UNIT_TABLES[name].units:
        for spelling in (unit.symbol, *unit.aliases):
            owner = claimed.setdefault(normalize(spelling), unit)
            assert owner is unit, f"{name}: {spelling!r}"


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_no_name_or_word_means_two_units(name: str) -> None:
    claimed: dict[str, object] = {}
    for unit in UNIT_TABLES[name].units:
        for word in (unit.name, *unit.words):
            owner = claimed.setdefault(fold(word), unit)
            assert owner is unit, f"{name}: {word!r}"


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_no_word_is_another_units_word_with_a_plural_s(name: str) -> None:
    words = {
        fold(word): unit
        for unit in UNIT_TABLES[name].units
        for word in (unit.name, *unit.words)
    }
    for word, unit in words.items():
        stem = words.get(word.removesuffix("s"))
        if word.endswith("s") and stem is not None:
            assert stem is unit, f"{name}: {word!r}"


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_no_symbol_reads_as_another_units_word(name: str) -> None:
    words = {
        fold(word): unit
        for unit in UNIT_TABLES[name].units
        for word in (unit.name, *unit.words)
    }
    for unit in UNIT_TABLES[name].units:
        for spelling in (unit.symbol, *unit.aliases):
            other = words.get(fold(spelling))
            assert other is None or other is unit, f"{name}: {spelling!r}"


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_changing_the_case_of_a_symbol_never_resolves_a_different_unit(
    name: str,
) -> None:
    table = UNIT_TABLES[name]
    words = {fold(word) for unit in table.units for word in (unit.name, *unit.words)}
    for unit in table.units:
        for spelling in (unit.symbol, *unit.aliases):
            swapped = spelling.swapcase()
            if normalize(swapped) == normalize(spelling) or fold(swapped) in words:
                continue
            if swapped in table:
                # Resolving at all means the swapped text is itself a claimed symbol.
                assert any(
                    normalize(swapped) == normalize(claim)
                    for other in table.units
                    for claim in (other.symbol, *other.aliases)
                ), f"{name}: {swapped!r}"


@pytest.mark.parametrize("name", TABLE_NAMES)
def test_every_table_rejects_text_that_is_no_unit(name: str) -> None:
    table = UNIT_TABLES[name]
    for text in TEXT_THAT_IS_NO_UNIT:
        assert text not in table


def test_temporal_tables_derived_from_time_accept_the_same_text() -> None:
    reference = UNIT_TABLES["TIME_UNITS"]
    for derived in ("INSTANT_UNITS", "SAMPLING_PERIOD_UNITS"):
        table = UNIT_TABLES[derived]
        assert list(table) == list(reference)
        for unit in reference.units:
            for spelling in (unit.symbol, *unit.aliases, *unit.words, unit.name):
                assert spelling in table, (derived, spelling)
