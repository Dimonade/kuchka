"""The tables accept the notations people write and refuse the ones that are wrong.

The expectations are hand-written in `notations`: what must resolve, to which unit, and
what must not.
"""

from __future__ import annotations

import pytest

from tests.support.kinds import UNIT_TABLES
from tests.units.notations import ACCEPTED
from tests.units.notations import LEGACY
from tests.units.notations import REJECTED

ACCEPTED_IDS = [f"{table}-{text}" for table, text, _ in ACCEPTED]
REJECTED_IDS = [f"{table}-{text!r}-{why}" for table, text, why in REJECTED]


@pytest.mark.parametrize(("table", "text", "symbol"), ACCEPTED, ids=ACCEPTED_IDS)
def test_the_notation_resolves_to_the_intended_unit(
    table: str, text: str, symbol: str
) -> None:
    resolved = UNIT_TABLES[table][text]
    assert resolved(1).unit.symbol == symbol
    assert resolved(5) == UNIT_TABLES[table][symbol](5)


@pytest.mark.parametrize(("table", "text"), LEGACY)
def test_the_keys_of_earlier_tables_still_resolve(table: str, text: str) -> None:
    assert text in UNIT_TABLES[table]


def test_a_derived_table_resolves_the_same_text_to_its_own_quantity() -> None:
    period = UNIT_TABLES["SAMPLING_PERIOD_UNITS"]
    assert period["msec"](5) == period["ms"](5)
    instant = UNIT_TABLES["INSTANT_UNITS"]
    assert instant["Hours"](2) == instant["h"](2)


@pytest.mark.parametrize(("table", "text", "why"), REJECTED, ids=REJECTED_IDS)
def test_the_notation_is_refused(table: str, text: str, why: str) -> None:
    del why
    assert text not in UNIT_TABLES[table]
    with pytest.raises(KeyError):
        UNIT_TABLES[table][text]
