"""Illuminance constructors: the lux and its prefixes, the phot, and the foot-candle.

The lux (lx) is the SI unit of illuminance: one lumen per square metre,
`1 lx = 1 lm/m² = 1 cd·sr/m²`, and it is the canonical unit.
The phot (ph) is the CGS unit, one lumen per square centimetre, so `1 ph = 10⁴ lx`.
The foot-candle (fc) is one lumen per square foot, derived from kuchka's exact foot, so
`1 fc` is about 10.764 lx.

`ILLUMINANCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ILLUMINANCE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Illuminance
from kuchka.quantities import UnitDef
from kuchka.units.length import FOOT

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

LUX_NAME = "lux"
LUX_SYMBOL = "lx"

MILLILUX = prefixed_unit(prefixes.MILLI, LUX_NAME, LUX_SYMBOL, ILLUMINANCE)
LUX = prefixed_unit(
    prefixes.UNIT,
    LUX_NAME,
    LUX_SYMBOL,
    ILLUMINANCE,
    aliases=(
        f"lm/m{symbols.SUPERSCRIPT_TWO}",
        *powered("lm/m", 2),
    ),
    words=("lumen per square metre", "lumen per square meter"),
)
KILOLUX = prefixed_unit(prefixes.KILO, LUX_NAME, LUX_SYMBOL, ILLUMINANCE)
PHOT = UnitDef(
    "phot",
    "ph",
    10_000,
    ILLUMINANCE,
    aliases=(f"lm/cm{symbols.SUPERSCRIPT_TWO}", *powered("lm/cm", 2)),
    words=("lumen per square centimetre", "lumen per square centimeter"),
)
FOOT_CANDLE = UnitDef(
    "foot_candle",
    "fc",
    1 / (FOOT.scale * FOOT.scale),
    ILLUMINANCE,
    aliases=("fc", f"lm/ft{symbols.SUPERSCRIPT_TWO}", *powered("lm/ft", 2)),
    words=("foot-candle", "footcandle", "foot candle", "lumen per square foot"),
)

Illuminance._canonical_unit = LUX  # noqa: SLF001 -- this module owns Illuminance's canonical unit


def Millilux(value: Numeric) -> Illuminance:
    """Construct an illuminance from a magnitude expressed in millilux.

    Parameters
    ----------
    value : Numeric
        Illuminance magnitude in mlx.

    Returns
    -------
    Illuminance
        Illuminance represented in millilux.

    Examples
    --------
    Moonlight on a clear night is a fraction of a lux:

    >>> Millilux(250).to(LUX)
    0.25 lx

    """
    return Illuminance(to_exact(value) * MILLILUX.scale, MILLILUX)


def Lux(value: Numeric) -> Illuminance:
    """Construct an illuminance from a magnitude expressed in lux.

    Parameters
    ----------
    value : Numeric
        Illuminance magnitude in lx.

    Returns
    -------
    Illuminance
        Illuminance represented in lux.

    Examples
    --------
    A 800 lm lamp spread evenly over a 4 m² desk area gives 200 lx:

    >>> from kuchka import Lumen
    >>> from kuchka import SquareMetre
    >>> Lumen(800) / SquareMetre(4)
    200 lx
    >>> Lux(200) * SquareMetre(4)
    800 lm

    """
    return Illuminance(to_exact(value) * LUX.scale, LUX)


def Kilolux(value: Numeric) -> Illuminance:
    """Construct an illuminance from a magnitude expressed in kilolux.

    Parameters
    ----------
    value : Numeric
        Illuminance magnitude in klx.

    Returns
    -------
    Illuminance
        Illuminance represented in kilolux.

    Examples
    --------
    Full daylight is around 100 klx:

    >>> Kilolux(100).to(LUX)
    100000 lx

    """
    return Illuminance(to_exact(value) * KILOLUX.scale, KILOLUX)


def Phot(value: Numeric) -> Illuminance:
    """Construct an illuminance from a magnitude expressed in phots.

    Parameters
    ----------
    value : Numeric
        Illuminance magnitude in ph.

    Returns
    -------
    Illuminance
        Illuminance represented in phots.

    Examples
    --------
    >>> Phot(1).to(LUX)
    10000 lx

    """
    return Illuminance(to_exact(value) * PHOT.scale, PHOT)


def FootCandle(value: Numeric) -> Illuminance:
    """Construct an illuminance from a magnitude expressed in foot-candles.

    Parameters
    ----------
    value : Numeric
        Illuminance magnitude in fc.

    Returns
    -------
    Illuminance
        Illuminance represented in foot-candles.

    Examples
    --------
    A foot-candle is a lumen on a square foot:

    >>> from kuchka import Foot
    >>> from kuchka import Lumen
    >>> FootCandle(10) == Lumen(10) / (Foot(1) * Foot(1))
    True

    """
    return Illuminance(to_exact(value) * FOOT_CANDLE.scale, FOOT_CANDLE)


ILLUMINANCE_UNITS: Mapping[str, Callable[[Numeric], Illuminance]] = unit_table(
    "ILLUMINANCE_UNITS",
    {
        MILLILUX: Millilux,
        LUX: Lux,
        KILOLUX: Kilolux,
        PHOT: Phot,
        FOOT_CANDLE: FootCandle,
    },
)

__all__ = [
    "FOOT_CANDLE",
    "ILLUMINANCE_UNITS",
    "KILOLUX",
    "LUX",
    "MILLILUX",
    "PHOT",
    "FootCandle",
    "Kilolux",
    "Lux",
    "Millilux",
    "Phot",
]
