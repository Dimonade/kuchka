"""Luminous efficacy constructors: lumens per watt.

Luminous efficacy is the luminous flux a source gives per watt it takes in, so it rates
a lamp: `1 lm/W = 1 cd·sr/W`, and the lumen per watt is the canonical unit.
A filament lamp gives about 15 lm/W and a good LED more than 100 lm/W.
No source can exceed 683 lm/W, the efficacy of ideal green light at 555 nm.

`LUMINOUS_EFFICACY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_EFFICACY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousEfficacy
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

LUMEN_PER_WATT = UnitDef(
    "lumen_per_watt",
    "lm/W",
    1,
    LUMINOUS_EFFICACY,
    aliases=("cd*sr/W",),
)

LuminousEfficacy._canonical_unit = LUMEN_PER_WATT  # noqa: SLF001 -- this module owns LuminousEfficacy's canonical unit


def LumenPerWatt(value: Numeric) -> LuminousEfficacy:
    """Construct a luminous efficacy from a magnitude expressed in lumens per watt.

    Parameters
    ----------
    value : Numeric
        Luminous efficacy magnitude in lm/W.

    Returns
    -------
    LuminousEfficacy
        Luminous efficacy represented in lumens per watt.

    Examples
    --------
    A 10 W LED lamp rated at 100 lm/W gives 1000 lm:

    >>> from kuchka import Watt
    >>> LumenPerWatt(100) * Watt(10)
    1000 lm
    >>> from kuchka import Lumen
    >>> Lumen(1000) / Watt(10)
    100 lm/W

    """
    return LuminousEfficacy(to_exact(value) * LUMEN_PER_WATT.scale, LUMEN_PER_WATT)


LUMINOUS_EFFICACY_UNITS: Mapping[str, Callable[[Numeric], LuminousEfficacy]] = (
    unit_table(
        "LUMINOUS_EFFICACY_UNITS",
        {
            LUMEN_PER_WATT: LumenPerWatt,
        },
    )
)

__all__ = [
    "LUMEN_PER_WATT",
    "LUMINOUS_EFFICACY_UNITS",
    "LumenPerWatt",
]
