"""`parse` reads archaic units when the caller allows them, from the modules imported.

Every archaic table is discovered from the package, so a unit added later is covered
without an edit.
The ambiguity of a text that two tables claim is tested on made-up types, since no
unit of the library is claimed twice.
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any

import pytest

from kuchka import ArchaicPolicy
from kuchka import Length
from kuchka import ParseError
from kuchka import UnknownUnitError
from kuchka import parse
from kuchka.dimensions import VOLTAGE
from kuchka.internal.unit_table import UnitTable
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.units import bind_table
from kuchka.quantities.base.units import bind_units
from kuchka.quantities.base.units import extend_units
from kuchka.units.archaic.russian import length as russian_length
from tests.archaic.tables import ARCHAIC_TABLES
from tests.archaic.tables import TABLE_IDS


def _quantity_of(table: UnitTable[Any]) -> type:
    return type(next(iter(table.values()))(1))


def _spellings(table: UnitTable[Any]) -> list[str]:
    return sorted(set(table._exact) | set(table._words))  # noqa: SLF001


@pytest.mark.parametrize("table_id", TABLE_IDS)
def test_the_units_of_an_archaic_table_are_covered_by_the_tables_its_type_records(
    table_id: str,
) -> None:
    """A module records its table, or a larger one that holds the same units."""
    table = ARCHAIC_TABLES[table_id]
    recorded = _quantity_of(table)._extension_tables  # noqa: SLF001
    covered = {unit for candidate in recorded for unit in candidate.units}
    assert set(table.units) <= covered


@pytest.mark.parametrize("table_id", TABLE_IDS)
def test_every_spelling_of_an_archaic_unit_reads_when_archaic_is_allowed(
    table_id: str,
) -> None:
    table = ARCHAIC_TABLES[table_id]
    quantity = _quantity_of(table)
    for spelling in _spellings(table):
        parsed = parse(f"3 {spelling}", quantity, allow_archaic=True)
        assert parsed == table[spelling](3), spelling
        assert repr(parsed) == repr(table[spelling](3)), spelling


@pytest.mark.parametrize("table_id", TABLE_IDS)
def test_an_archaic_spelling_is_refused_by_default_and_the_error_says_how_to_read_it(
    table_id: str,
) -> None:
    table = ARCHAIC_TABLES[table_id]
    quantity = _quantity_of(table)
    spelling = _spellings(table)[0]
    modern = quantity._unit_table  # noqa: SLF001
    if spelling in modern:
        pytest.skip("a modern spelling reads without the policy")
    with pytest.raises(UnknownUnitError, match="allow_archaic=True") as raised:
        parse(f"3 {spelling}", quantity)
    recorded = quantity._extension_tables  # noqa: SLF001
    assert any(candidate.label in str(raised.value) for candidate in recorded)


def test_no_spelling_names_two_units_of_one_type() -> None:
    """Allowing archaic units never makes a text of the library ambiguous.

    A table of a region may hold the units of a table of a country, so one unit can
    appear in several tables, and what must not happen is two units under one text.
    """
    quantities = {_quantity_of(table) for table in ARCHAIC_TABLES.values()}
    for quantity in quantities:
        claimed: dict[str, tuple[object, str]] = {}
        tables = [quantity._unit_table, *quantity._extension_tables]  # noqa: SLF001
        for table in tables:
            for spelling in _spellings(table):
                unit = table.resolve(spelling)[0]
                key = spelling.casefold() if spelling in table._words else spelling  # noqa: SLF001
                known, label = claimed.setdefault(key, (unit, table.label))
                assert known == unit, (
                    f"{spelling!r} is the {known} of {label} and the {unit} of "
                    f"{table.label}"
                )


def test_a_unit_that_two_recorded_tables_hold_reads_without_ambiguity() -> None:
    """The principal German miles are in both of the tables that extend `Length`."""
    from kuchka.units.archaic.german.length import meile
    from kuchka.units.archaic.german.length import regional_meilen

    shared = set(meile.GERMAN_MEILE_UNITS.units) & set(
        regional_meilen.GERMAN_MEILE_UNITS_ALL.units
    )
    assert shared
    unit = next(iter(shared))
    assert parse(
        f"2 {unit.symbol}", Length, allow_archaic=True
    ) == meile.GERMAN_MEILE_UNITS[unit.symbol](2)


def test_the_policy_is_a_value_or_its_bool_shorthand() -> None:
    expected = russian_length.Arshin(2)
    for allowed in (True, ArchaicPolicy.Allow):
        assert parse("2 arshin", Length, allow_archaic=allowed) == expected
    for denied in (False, ArchaicPolicy.Deny):
        with pytest.raises(UnknownUnitError):
            parse("2 arshin", Length, allow_archaic=denied)
    with pytest.raises(UnknownUnitError):
        parse("2 arshin", Length)


def test_modern_units_still_read_when_archaic_is_allowed() -> None:
    assert parse("2 m", Length, allow_archaic=True) == parse("2 m", Length)


def test_a_text_is_read_in_the_unit_it_was_written() -> None:
    assert repr(parse("2 arshin", Length, allow_archaic=True)) == repr(
        russian_length.Arshin(2)
    )


PROGRAM = """
import kuchka
from kuchka import Length, UnknownUnitError, parse

try:
    parse("2 arshin", Length, allow_archaic=True)
except UnknownUnitError as error:
    assert "arshin" in str(error)
else:
    raise AssertionError("an archaic unit read before its module was imported")

from kuchka.units.archaic.russian import length

assert parse("2 arshin", Length, allow_archaic=True) == length.Arshin(2)
"""


def test_only_the_archaic_modules_that_are_imported_are_read() -> None:
    result = subprocess.run(
        [sys.executable, "-c", PROGRAM], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


def _made_up_type() -> tuple[type[LinearQuantity], UnitDef]:
    class Fresh(LinearQuantity):
        dimension = VOLTAGE
        __slots__ = ()

    modern = UnitDef("fresh_unit", "fu", 1, VOLTAGE, aliases=("x",))
    bind_units(Fresh, [modern])
    bind_table(
        Fresh,
        unit_table("FRESH_UNITS", {modern: lambda v: Fresh(to_exact(v), modern)}),
    )
    return Fresh, modern


def _table_claiming(
    fresh: type[LinearQuantity], label: str, spelling: str
) -> UnitTable[Any]:
    unit = UnitDef(f"{label.lower()}_unit", f"{label.lower()}u", 2, VOLTAGE)
    unit = UnitDef(unit.name, unit.symbol, 2, VOLTAGE, aliases=(spelling,))
    return unit_table(label, {unit: lambda v: fresh(to_exact(v) * 2, unit)})


def test_a_text_that_a_modern_and_an_archaic_unit_claim_is_ambiguous() -> None:
    fresh, modern = _made_up_type()
    extend_units(fresh, _table_claiming(fresh, "OLD_UNITS", "x"))
    with pytest.raises(ParseError, match="FRESH_UNITS, OLD_UNITS"):
        parse("1 x", fresh, allow_archaic=True)
    assert parse("1 x", fresh) == fresh(to_exact(1), modern)


def test_a_text_that_two_archaic_units_claim_is_ambiguous() -> None:
    fresh, _ = _made_up_type()
    extend_units(fresh, _table_claiming(fresh, "OLD_UNITS", "y"))
    extend_units(fresh, _table_claiming(fresh, "OLDER_UNITS", "y"))
    with pytest.raises(ParseError, match="OLD_UNITS, OLDER_UNITS"):
        parse("1 y", fresh, allow_archaic=True)
    with pytest.raises(UnknownUnitError, match="allow_archaic=True"):
        parse("1 y", fresh)
