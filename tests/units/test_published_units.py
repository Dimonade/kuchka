"""Everything a published table refers to is itself published by `kuchka.units`.

A unit a table holds has to be exported under a name, because a value displayed in it is
pickled by that name, and a constructor a table holds has to be exported, because the
table is documented as the way to reach it.
"""

from __future__ import annotations

import pytest

import kuchka
import kuchka.units as published
from tests.support.kinds import PUBLISHED_UNITS
from tests.support.kinds import UNIT_TABLES

# Tables derived from another by wrapping its constructors, which are not exported.
# `EXPOSURE_UNITS` is derived in part: its `C/kg` entry reads a `SpecificCharge`.
DERIVED_TABLES = (
    "EXPOSURE_RATE_UNITS",
    "EXPOSURE_UNITS",
    "IMPEDANCE_UNITS",
    "INSTANT_UNITS",
    "MAGNETIZATION_UNITS",
    "REACTANCE_UNITS",
    "SAMPLING_PERIOD_UNITS",
    "STRESS_UNITS",
)


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_every_unit_of_a_table_is_published_under_a_name(name: str) -> None:
    published_units = {id(unit) for unit in PUBLISHED_UNITS.values()}
    for unit in UNIT_TABLES[name].units:
        assert id(unit) in published_units, (
            f"{unit.name} is in {name} but not published"
        )


@pytest.mark.parametrize("name", [n for n in UNIT_TABLES if n not in DERIVED_TABLES])
def test_every_constructor_of_a_table_is_published_under_its_name(name: str) -> None:
    for symbol, constructor in UNIT_TABLES[name].items():
        exported = getattr(published, constructor.__name__, None)
        assert exported is constructor, f"{name}[{symbol!r}] is not published"
        assert getattr(kuchka, constructor.__name__, None) is constructor
