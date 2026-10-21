"""SI and IEC binary prefixes definition.

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
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.internal import symbols
from kuchka.quantities.base.units import UnitDef

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


@dataclass(frozen=True, slots=True)
class Prefix:
    """A prefix - its name, display symbol, base, and exponent.

    The factor is `base ** exponent`: the SI prefixes are powers of ten, and the IEC
    binary prefixes (`kibi`, `mebi`, ...) are powers of two.
    `aliases` are other symbols for the same prefix: `u` for micro, which is what a
    keyboard offers in place of the micro sign.
    """

    name: str
    symbol: str
    exponent: int
    aliases: tuple[str, ...] = ()
    base: int = 10

    @property
    def factor(self) -> Decimal:
        """The exact scale factor.

        A power of ten is built through `scaleb`.
        Any other base is an integer power, built from the integer so that no
        arithmetic context can round it (`Decimal(2) ** 100` would).
        """
        if self.base == _DECIMAL_BASE:
            return Decimal(1).scaleb(self.exponent)
        return Decimal(self.base**self.exponent)


_DECIMAL_BASE = 10

UNIT = Prefix("", "", 0)
"""No prefix to let the unprefixed unit to go through the same helper."""

QUECTO = Prefix("quecto", "q", -30)
RONTO = Prefix("ronto", "r", -27)
YOCTO = Prefix("yocto", "y", -24)
ZEPTO = Prefix("zepto", "z", -21)
ATTO = Prefix("atto", "a", -18)
FEMTO = Prefix("femto", "f", -15)
PICO = Prefix("pico", "p", -12)
NANO = Prefix("nano", "n", -9)
MICRO = Prefix("micro", symbols.MICRO, -6, aliases=("u",))
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
EXA = Prefix("exa", "E", 18)
ZETTA = Prefix("zetta", "Z", 21)
YOTTA = Prefix("yotta", "Y", 24)
RONNA = Prefix("ronna", "R", 27)
QUETTA = Prefix("quetta", "Q", 30)


KIBI = Prefix("kibi", "Ki", 10, base=2)
MEBI = Prefix("mebi", "Mi", 20, base=2)
GIBI = Prefix("gibi", "Gi", 30, base=2)
TEBI = Prefix("tebi", "Ti", 40, base=2)
PEBI = Prefix("pebi", "Pi", 50, base=2)
EXBI = Prefix("exbi", "Ei", 60, base=2)
ZEBI = Prefix("zebi", "Zi", 70, base=2)
YOBI = Prefix("yobi", "Yi", 80, base=2)


def with_prefix(
    prefix: Prefix,
    base: UnitDef,
    *,
    aliases: tuple[str, ...] = (),
    words: tuple[str, ...] = (),
) -> UnitDef:
    """Build a `UnitDef` for `prefix` applied to the unit `base`.

    The scale is the scale of `base` times the factor of the prefix, held as an exact
    fraction, so the base may be any linear unit: the metre, the gram, or a unit of an
    old measurement system such as the shell of the krakenpeople.
    The name and the symbol join the prefix and the base.
    The unit is known by every pairing of a prefix symbol, or prefix alias, with a base
    symbol or base alias, and by the prefix name before each word of the base.
    `aliases` and `words` add spellings of this one unit that no pairing produces,
    such as `t` for the megagram.
    """
    symbol = f"{prefix.symbol}{base.symbol}"
    paired = tuple(
        spelling
        for prefix_symbol in (prefix.symbol, *prefix.aliases)
        for base_symbol in (base.symbol, *base.aliases)
        if (spelling := f"{prefix_symbol}{base_symbol}") != symbol
    )
    return UnitDef(
        f"{prefix.name}{base.name}",
        symbol,
        base.scale * Fraction(prefix.factor),
        base.dimension,
        aliases=(*paired, *aliases),
        words=(*(f"{prefix.name}{word}" for word in base.words), *words),
    )


def prefixed_unit(  # noqa: PLR0913 -- the spelling extras are keyword-only
    prefix: Prefix,
    base_name: str,
    base_symbol: str,
    dimension: Dimension,
    *,
    coherent_offset: int = 0,
    base_aliases: tuple[str, ...] = (),
    base_words: tuple[str, ...] = (),
    aliases: tuple[str, ...] = (),
    words: tuple[str, ...] = (),
) -> UnitDef:
    """Build a `UnitDef` for `prefix` applied to a dimension's coherent SI unit.

    `coherent_offset` corrects for a dimension whose canonical unit, namely, what
    `UnitDef.scale` is expressed relative to, is not itself the coherent SI unit.

    Mass is one such example - its canonical unit is kilogram, not gram, so every
    mass prefix needs an extra `-3` baked in.

    Every other dimension's canonical unit already is its own coherent unit, so the
    default of 0 is correct for them.

    `base_aliases` are other symbols for the base unit (`ohm` for the ohm), and
    `base_words` other names for it (`meter` for the metre).
    The spellings pair up as `with_prefix` describes.
    """
    base = UnitDef(
        base_name,
        base_symbol,
        Decimal(1).scaleb(coherent_offset),
        dimension,
        aliases=base_aliases,
        words=base_words,
    )
    return with_prefix(prefix, base, aliases=aliases, words=words)


__all__ = [
    "Prefix",
    "prefixed_unit",
    "with_prefix",
]
