"""Find the families of prefixed units in a set of units, from their symbols.

A unit is a member of the family of a base unit when its symbol is a prefix symbol
followed by the symbol of the base, and its scale is the scale of the base times the
factor of the prefix.
Only the prefixes that step by a thousand make a decimal family, and the binary
prefixes make families of their own.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.internal import prefixes

if TYPE_CHECKING:
    from collections.abc import Iterable

STEP = 3
DECIMAL_BASE = 10
BINARY_BASE = 2

DECIMAL_PREFIXES = [
    prefix
    for prefix in vars(prefixes).values()
    if isinstance(prefix, prefixes.Prefix)
    and prefix.base == DECIMAL_BASE
    and prefix.exponent != 0
    and prefix.exponent % STEP == 0
]
BINARY_PREFIXES = [
    prefix
    for prefix in vars(prefixes).values()
    if isinstance(prefix, prefixes.Prefix) and prefix.base == BINARY_BASE
]


DELTA = "\u0394"
"""A temperature difference spells its prefix after the delta sign: `ΔmK`."""


def families(units: Iterable, prefix_list: list) -> dict[str, dict[int, object]]:
    """Return, per base symbol, the unit it has at each exponent, the base at 0."""
    units = list(units)
    found: dict[str, dict[int, object]] = {}
    for marker in ("", DELTA):
        marked = [unit for unit in units if unit.symbol.startswith(marker)]
        if marker == "":
            marked = [unit for unit in units if not unit.symbol.startswith(DELTA)]
        by_bare = {unit.symbol.removeprefix(marker): unit for unit in marked}
        for unit in marked:
            bare = unit.symbol.removeprefix(marker)
            for prefix in prefix_list:
                if not bare.startswith(prefix.symbol):
                    continue
                base = by_bare.get(bare[len(prefix.symbol) :])
                if base is not None and unit.scale == base.scale * Fraction(
                    prefix.factor
                ):
                    family = found.setdefault(base.symbol, {0: base})
                    family[prefix.exponent] = unit
    return found


def decimal_families(units: Iterable) -> dict[str, dict[int, object]]:
    """Return the decimal families of `units`."""
    return families(units, DECIMAL_PREFIXES)


def binary_families(units: Iterable) -> dict[str, dict[int, object]]:
    """Return the binary families of `units`."""
    return families(units, BINARY_PREFIXES)
