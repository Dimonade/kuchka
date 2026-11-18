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

from fractions import Fraction

import pytest

from kuchka.internal import prefixes
from kuchka.internal.unit_table import units_of
from tests.support.kinds import UNIT_TABLES

STEP = 3
DECIMAL_BASE = 10
DECIMAL_PREFIXES = [
    prefix
    for prefix in vars(prefixes).values()
    if isinstance(prefix, prefixes.Prefix)
    and prefix.base == DECIMAL_BASE
    and prefix.exponent != 0
    and prefix.exponent % STEP == 0
]


def families(table) -> dict[str, dict[int, str]]:
    """Return, per base symbol of `table`, the symbol it holds at each exponent."""
    units = list(units_of(table))
    by_symbol = {unit.symbol: unit for unit in units}
    found: dict[str, dict[int, str]] = {}
    for unit in units:
        for prefix in DECIMAL_PREFIXES:
            if not unit.symbol.startswith(prefix.symbol):
                continue
            base = by_symbol.get(unit.symbol[len(prefix.symbol) :])
            if base is not None and unit.scale == base.scale * Fraction(prefix.factor):
                family = found.setdefault(base.symbol, {0: base.symbol})
                family[prefix.exponent] = unit.symbol
    return found


@pytest.mark.parametrize("name", sorted(UNIT_TABLES))
def test_a_prefixed_family_has_no_gap(name: str) -> None:
    for base, family in families(UNIT_TABLES[name]).items():
        missing = [
            exponent
            for exponent in range(min(family), max(family) + 1, STEP)
            if exponent not in family
        ]
        assert not missing, (
            f"{name}: the family of {base} skips the exponents {missing}"
        )
