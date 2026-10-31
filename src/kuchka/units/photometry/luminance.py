"""Luminance constructors: CandelaPerSquareMetre, Stilb, FootLambert, and more.

Luminance is the luminous intensity of a surface per unit of its area, which is how
bright the surface looks: `1 cd/m²`, also called the nit, is the canonical unit.
Displays are specified in it: a monitor in the hundreds of nits, an HDR television in
the thousands.
The prefixed forms cover the faint (`mcd/m²`, a night sky) and the bright (`kcd/m²`).

The stilb (sb) is the CGS unit, one candela per square centimetre:
`1 sb = 10⁴ cd/m²`.
The foot-lambert (fL) is `1/pi` candela per square foot, the unit cinema screens are
specified in.
Its pi is the exact rational `kuchka.internal.constants.PI`.

`LUMINANCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINANCE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Luminance
from kuchka.quantities import UnitDef
from kuchka.units.length import FOOT

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

CANDELA_PER_SQUARE_METRE = UnitDef(
    "candela_per_square_metre",
    f"cd/m{symbols.SUPERSCRIPT_TWO}",
    1,
    LUMINANCE,
    aliases=powered("cd/m", 2),
    words=("candela per square meter", "nit"),
)
MILLICANDELA_PER_SQUARE_METRE = with_prefix(prefixes.MILLI, CANDELA_PER_SQUARE_METRE)
KILOCANDELA_PER_SQUARE_METRE = with_prefix(prefixes.KILO, CANDELA_PER_SQUARE_METRE)
STILB = UnitDef(
    "stilb",
    "sb",
    10_000,
    LUMINANCE,
    aliases=(f"cd/cm{symbols.SUPERSCRIPT_TWO}", *powered("cd/cm", 2)),
    words=("candela per square centimetre", "candela per square centimeter"),
)
FOOT_LAMBERT = UnitDef(
    "foot_lambert",
    "fL",
    1 / (PI * FOOT.scale * FOOT.scale),
    LUMINANCE,
    aliases=("ftL",),
    words=("foot-lambert", "footlambert"),
)

Luminance._canonical_unit = CANDELA_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns Luminance's canonical unit


def CandelaPerSquareMetre(value: Numeric) -> Luminance:
    """Construct a luminance from a magnitude expressed in candelas per square metre.

    Parameters
    ----------
    value : Numeric
        Luminance magnitude in cd/m².

    Returns
    -------
    Luminance
        Luminance represented in candelas per square metre.

    Examples
    --------
    A 100 cd source seen across a surface of 0.5 m² has a luminance of 200 cd/m²,
    and 200 nits is the name the same value goes by on a display data sheet:

    >>> from kuchka import Candela, SquareMetre
    >>> Candela(100) / SquareMetre(0.5)
    200 cd/m²
    >>> from kuchka.units import LUMINANCE_UNITS
    >>> LUMINANCE_UNITS["nit"](200)
    200 cd/m²

    """
    return Luminance(
        to_exact(value) * CANDELA_PER_SQUARE_METRE.scale, CANDELA_PER_SQUARE_METRE
    )


def MillicandelaPerSquareMetre(value: Numeric) -> Luminance:
    """Construct a luminance from a magnitude expressed in millicandelas per m².

    Parameters
    ----------
    value : Numeric
        Luminance magnitude in mcd/m².

    Returns
    -------
    Luminance
        Luminance represented in millicandelas per square metre.

    Examples
    --------
    >>> MillicandelaPerSquareMetre(1500).to(CANDELA_PER_SQUARE_METRE)
    1.5 cd/m²

    """
    return Luminance(
        to_exact(value) * MILLICANDELA_PER_SQUARE_METRE.scale,
        MILLICANDELA_PER_SQUARE_METRE,
    )


def KilocandelaPerSquareMetre(value: Numeric) -> Luminance:
    """Construct a luminance from a magnitude expressed in kilocandelas per m².

    Parameters
    ----------
    value : Numeric
        Luminance magnitude in kcd/m².

    Returns
    -------
    Luminance
        Luminance represented in kilocandelas per square metre.

    Examples
    --------
    An HDR display peaks at 4000 nits:

    >>> KilocandelaPerSquareMetre(4).to(CANDELA_PER_SQUARE_METRE)
    4000 cd/m²

    """
    return Luminance(
        to_exact(value) * KILOCANDELA_PER_SQUARE_METRE.scale,
        KILOCANDELA_PER_SQUARE_METRE,
    )


def Stilb(value: Numeric) -> Luminance:
    """Construct a luminance from a magnitude expressed in stilbs.

    Parameters
    ----------
    value : Numeric
        Luminance magnitude in sb.

    Returns
    -------
    Luminance
        Luminance represented in stilbs.

    Examples
    --------
    >>> Stilb(1) == KilocandelaPerSquareMetre(10)
    True

    """
    return Luminance(to_exact(value) * STILB.scale, STILB)


def FootLambert(value: Numeric) -> Luminance:
    """Construct a luminance from a magnitude expressed in foot-lamberts.

    Parameters
    ----------
    value : Numeric
        Luminance magnitude in fL.

    Returns
    -------
    Luminance
        Luminance represented in foot-lamberts.

    Examples
    --------
    The cinema standard of 14 fL is about 48 cd/m²:

    >>> from kuchka import CandelaPerSquareMetre
    >>> CandelaPerSquareMetre(47) < FootLambert(14) < CandelaPerSquareMetre(48)
    True

    """
    return Luminance(to_exact(value) * FOOT_LAMBERT.scale, FOOT_LAMBERT)


LUMINANCE_UNITS: Mapping[str, Callable[[Numeric], Luminance]] = unit_table(
    "LUMINANCE_UNITS",
    {
        MILLICANDELA_PER_SQUARE_METRE: MillicandelaPerSquareMetre,
        CANDELA_PER_SQUARE_METRE: CandelaPerSquareMetre,
        KILOCANDELA_PER_SQUARE_METRE: KilocandelaPerSquareMetre,
        STILB: Stilb,
        FOOT_LAMBERT: FootLambert,
    },
)

__all__ = [
    "CANDELA_PER_SQUARE_METRE",
    "FOOT_LAMBERT",
    "KILOCANDELA_PER_SQUARE_METRE",
    "LUMINANCE_UNITS",
    "MILLICANDELA_PER_SQUARE_METRE",
    "STILB",
    "CandelaPerSquareMetre",
    "FootLambert",
    "KilocandelaPerSquareMetre",
    "MillicandelaPerSquareMetre",
    "Stilb",
]
