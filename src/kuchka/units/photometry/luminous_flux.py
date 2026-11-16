"""Luminous flux constructors: the lumen and its prefixes.

The lumen (lm) is the SI unit of luminous flux: one candela over one steradian,
`1 lm = 1 cd·sr`.
It is the canonical unit, and a steradian is the canonical solid angle, so a luminous
intensity times a solid angle is a flux with no factor between them.

Luminous flux counts light as the eye sees it, so a lumen is not a watt:
the conversion depends on the wavelength and is not part of this module.

`LUMINOUS_FLUX_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_FLUX
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousFlux

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

LUMEN_NAME = "lumen"
LUMEN_SYMBOL = "lm"

MILLILUMEN = prefixed_unit(prefixes.MILLI, LUMEN_NAME, LUMEN_SYMBOL, LUMINOUS_FLUX)
LUMEN = prefixed_unit(
    prefixes.UNIT,
    LUMEN_NAME,
    LUMEN_SYMBOL,
    LUMINOUS_FLUX,
    aliases=("cd*sr", f"cd{symbols.MIDDLE_DOT}sr", "cd sr"),
    words=("candela steradian",),
)
KILOLUMEN = prefixed_unit(prefixes.KILO, LUMEN_NAME, LUMEN_SYMBOL, LUMINOUS_FLUX)

LuminousFlux._canonical_unit = LUMEN  # noqa: SLF001 -- this module owns LuminousFlux's canonical unit


def Millilumen(value: Numeric) -> LuminousFlux:
    """Construct a luminous flux from a magnitude expressed in millilumens.

    Parameters
    ----------
    value : Numeric
        Luminous flux magnitude in mlm.

    Returns
    -------
    LuminousFlux
        Luminous flux represented in millilumens.

    Examples
    --------
    >>> Millilumen(1500).to(LUMEN)
    1.5 lm

    """
    return LuminousFlux(to_exact(value) * MILLILUMEN.scale, MILLILUMEN)


def Lumen(value: Numeric) -> LuminousFlux:
    """Construct a luminous flux from a magnitude expressed in lumens.

    Parameters
    ----------
    value : Numeric
        Luminous flux magnitude in lm.

    Returns
    -------
    LuminousFlux
        Luminous flux represented in lumens.

    Examples
    --------
    A lamp of 120 cd that emits uniformly into a cone of 2 sr gives:

    >>> from kuchka import Candela
    >>> from kuchka import Steradian
    >>> Candela(120) * Steradian(2)
    240 lm
    >>> Lumen(240) / Steradian(2)
    120 cd

    """
    return LuminousFlux(to_exact(value) * LUMEN.scale, LUMEN)


def Kilolumen(value: Numeric) -> LuminousFlux:
    """Construct a luminous flux from a magnitude expressed in kilolumens.

    Parameters
    ----------
    value : Numeric
        Luminous flux magnitude in klm.

    Returns
    -------
    LuminousFlux
        Luminous flux represented in kilolumens.

    Examples
    --------
    >>> Kilolumen(2.5).to(LUMEN)
    2500 lm

    """
    return LuminousFlux(to_exact(value) * KILOLUMEN.scale, KILOLUMEN)


LUMINOUS_FLUX_UNITS: Mapping[str, Callable[[Numeric], LuminousFlux]] = unit_table(
    "LUMINOUS_FLUX_UNITS",
    {
        MILLILUMEN: Millilumen,
        LUMEN: Lumen,
        KILOLUMEN: Kilolumen,
    },
)

__all__ = [
    "KILOLUMEN",
    "LUMEN",
    "LUMINOUS_FLUX_UNITS",
    "MILLILUMEN",
    "Kilolumen",
    "Lumen",
    "Millilumen",
]
