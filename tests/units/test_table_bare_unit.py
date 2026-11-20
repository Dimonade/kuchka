"""A table may name the unit a number with no unit is read in."""

from __future__ import annotations

import pytest

from kuchka.internal.unit_table import unit_table
from tests.units.table_fixtures import BASE
from tests.units.table_fixtures import MEGA
from tests.units.table_fixtures import MILLI
from tests.units.table_fixtures import make_ctor
from tests.units.table_fixtures import make_unit


def _entries() -> dict:
    return {unit: make_ctor(unit.name) for unit in (MILLI, MEGA, BASE)}


def test_a_table_has_no_bare_unit_unless_it_names_one() -> None:
    assert unit_table("PLAIN_UNITS", _entries()).bare is None


def test_a_table_names_its_bare_unit_and_the_constructor_of_it() -> None:
    table = unit_table("NAMED_UNITS", _entries(), bare=BASE)
    assert table.bare is not None
    unit, constructor = table.bare
    assert unit is BASE
    assert constructor(5) == ("basex", 5)


def test_a_bare_unit_is_one_of_the_units_of_the_table() -> None:
    with pytest.raises(ValueError, match="not a unit of the table"):
        unit_table("STRANGE_UNITS", _entries(), bare=make_unit("other", "o"))


def test_a_derived_table_keeps_the_bare_unit() -> None:
    table = unit_table("NAMED_UNITS", _entries(), bare=BASE)
    derived = table.map("DERIVED_UNITS", lambda constructor: constructor)
    assert derived.bare is not None
    assert derived.bare[0] is BASE


def test_a_derived_table_of_a_table_without_one_has_none() -> None:
    derived = unit_table("PLAIN_UNITS", _entries()).map(
        "DERIVED_UNITS", lambda constructor: constructor
    )
    assert derived.bare is None
