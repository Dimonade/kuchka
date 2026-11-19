"""A family of prefixed units has every decimal step between its smallest and largest.

A table that holds a nanovolt and a megavolt holds the units in between, so a reading
between two of its units always has a unit of its own.
The families are found from the symbols: a unit is a member of the family of a base
unit of its table when its symbol is a prefix symbol followed by the symbol of the
base, and its scale is the scale of the base times the factor of the prefix.
Only the prefixes in steps of a thousand are steps of a family, and the binary
prefixes are a family of their own.
"""

from __future__ import annotations

import pytest

from kuchka.internal.unit_table import units_of
from tests.support.kinds import UNIT_TABLES
from tests.support.prefix_families import STEP
from tests.support.prefix_families import decimal_families


@pytest.mark.parametrize("name", sorted(UNIT_TABLES))
def test_a_prefixed_family_has_no_gap(name: str) -> None:
    for base, family in decimal_families(units_of(UNIT_TABLES[name])).items():
        missing = [
            exponent
            for exponent in range(min(family), max(family) + 1, STEP)
            if exponent not in family
        ]
        assert not missing, (
            f"{name}: the family of {base} skips the exponents {missing}"
        )
