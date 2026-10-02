"""SI prefixes definition.

The central registry exists for two reasons:
- remove the need to manually type the same things, and
- reduce the risk of typos and special character rolling (micro*).

NOTE: This must be thoroughly and tested against manually written tables.
The reason is that an error in the registry will seep into all the units, and will not
be displayed.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.internal import symbols
from kuchka.quantities.base.units import UnitDef

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


@dataclass(frozen=True, slots=True)
class Prefix:
    """SI prefix - its name, display symbol, and power-of-ten exponent."""

    name: str
    symbol: str
    exponent: int

    @property
    def factor(self) -> Decimal:
        """The exact scale factor, built through `scaleb`."""
        return Decimal(1).scaleb(self.exponent)


UNIT = Prefix("", "", 0)
"""No prefix to let the unprefixed unit to go through the same helper."""

ATTO = Prefix("atto", "a", -18)
FEMTO = Prefix("femto", "f", -15)
PICO = Prefix("pico", "p", -12)
NANO = Prefix("nano", "n", -9)
MICRO = Prefix("micro", symbols.MICRO, -6)
MILLI = Prefix("milli", "m", -3)
CENTI = Prefix("centi", "c", -2)
DECI = Prefix("deci", "d", -1)
DECA = Prefix("deca", "da", 1)
HECTO = Prefix("hecto", "h", 2)
KILO = Prefix("kilo", "k", 3)
MEGA = Prefix("mega", "M", 6)
GIGA = Prefix("giga", "G", 9)
TERA = Prefix("tera", "T", 12)
PETA = Prefix("peta", "P", 15)
EXA = Prefix("exa", "E")


def prefixed_unit(
    prefix: Prefix,
    base_name: str,
    base_symbol: str,
    dimension: Dimension,
    *,
    coherent_offset: int = 0,
) -> UnitDef:
    """Build a `UnitDef` for `prefix` applied to a dimension's coherent SI unit.

    `coherent_offset` corrects for a dimension whose canonical unit, namely, what
    `UnitDef.scale` is expressed relative to, is not itself the coherent SI unit.

    Mass is one such example - its canonical unit is kilogram, not gram, so every
    mass prefix needs an extra `-3` baked in.

    Every other dimension's canonical unit already is its own coherent unit, so the
    default of 0 is correct for them.
    """
    return UnitDef(
        f"{prefix.name}{base_name}",
        f"{prefix.symbol}{base_symbol}",
        Decimal(1).scaleb(prefix.exponent + coherent_offset),
        dimension,
    )


__all__ = [
    "Prefix",
    "prefixed_unit",
]
