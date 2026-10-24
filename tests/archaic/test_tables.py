"""Every archaic table builds the quantity it names, in the unit it names."""

from __future__ import annotations

import pickle
from fractions import Fraction

import pytest

from kuchka.internal.unit_table import UnitTable
from kuchka.internal.unit_table import units_of
from kuchka.quantities import UnitDef
from tests.archaic.tables import ARCHAIC_TABLES
from tests.archaic.tables import TABLE_IDS

TABLES = list(ARCHAIC_TABLES.values())
UNIT_CASES: list[tuple[str, UnitDef]] = [
    (table_id, unit)
    for table_id, table in ARCHAIC_TABLES.items()
    for unit in units_of(table)
    if isinstance(unit, UnitDef)
]
MINIMUM_TABLES = 8
SAMPLE_MAGNITUDE = 3
UNIT_IDS = [f"{table_id}:{unit.name}" for table_id, unit in UNIT_CASES]


def test_the_archaic_package_has_tables() -> None:
    assert len(ARCHAIC_TABLES) >= MINIMUM_TABLES
    assert all(isinstance(table, UnitTable) for table in TABLES)


@pytest.mark.parametrize(("table_id", "unit"), UNIT_CASES, ids=UNIT_IDS)
def test_a_constructor_builds_its_unit_with_the_scale_of_its_definition(
    table_id: str, unit: UnitDef
) -> None:
    constructor = ARCHAIC_TABLES[table_id][unit.symbol]
    value = constructor(SAMPLE_MAGNITUDE)
    cls = type(value)
    assert value.unit == unit
    assert value.value_in(unit) == SAMPLE_MAGNITUDE
    assert value.magnitude == SAMPLE_MAGNITUDE * unit.scale
    assert value.unit in cls._applicable_units


@pytest.mark.parametrize(("table_id", "unit"), UNIT_CASES, ids=UNIT_IDS)
def test_every_spelling_of_a_unit_resolves_to_its_constructor(
    table_id: str, unit: UnitDef
) -> None:
    table = ARCHAIC_TABLES[table_id]
    wanted = table[unit.symbol]
    spellings = [
        unit.name,
        *unit.aliases,
        *unit.words,
    ]
    for spelling in spellings:
        assert table[spelling] is wanted


@pytest.mark.parametrize("table_id", TABLE_IDS)
def test_a_table_iterates_each_display_symbol_once(table_id: str) -> None:
    table = ARCHAIC_TABLES[table_id]
    symbols = list(table)
    assert len(symbols) == len(set(symbols)) == len(units_of(table))


@pytest.mark.parametrize("table_id", TABLE_IDS)
def test_an_archaic_value_converts_to_a_published_unit_and_pickles_there(
    table_id: str,
) -> None:
    table = ARCHAIC_TABLES[table_id]
    value = next(iter(table.values()))(Fraction(1, 3))
    canonical = type(value)._canonical_unit  # noqa: SLF001
    in_canonical = value.to(canonical)
    assert pickle.loads(pickle.dumps(in_canonical)) == in_canonical
    with pytest.raises(pickle.PicklingError):
        pickle.dumps(value)
