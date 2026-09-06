"""SI prefixes definition.

The central registry exists for two reasons:
- remove the need to manually type the same things, and
- reduce the risk of typos and special character rolling (micro*).

NOTE: This must come thoroughly and tested against manually written tables.
The reason is that an error in the registry will seep into all the units, and will not
be displayed.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


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

FEMTO = Prefix("femto", "f", -15)
PICO = Prefix("pico", "p", -12)
NANO = Prefix("nano", "n", -9)
MICRO = Prefix("micro", "\u00b5", -6)
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
