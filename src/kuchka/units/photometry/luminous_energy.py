"""Luminous energy constructors: lumen-seconds and lumen-hours.

Luminous energy is luminous flux accumulated over time: `1 lm·s = 1 cd·sr·s`.
The lumen second is the canonical unit, and the historical talbot is the same unit.
The lumen hour is 3600 lumen seconds, and is how the light a lamp delivers over its
running time is counted.

`LUMINOUS_ENERGY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_ENERGY
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousEnergy
from kuchka.quantities import UnitDef
from kuchka.units.temporal.time import HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

LUMEN_SECOND = UnitDef(
    "lumen_second",
    f"lm{symbols.MIDDLE_DOT}s",
    1,
    LUMINOUS_ENERGY,
    aliases=("lm*s", "lm s", "cd*sr*s"),
    words=("talbot",),
)
LUMEN_HOUR = UnitDef(
    "lumen_hour",
    f"lm{symbols.MIDDLE_DOT}h",
    HOUR.scale,
    LUMINOUS_ENERGY,
    aliases=("lm*h", "lm h"),
)

LuminousEnergy._canonical_unit = LUMEN_SECOND  # noqa: SLF001 -- this module owns LuminousEnergy's canonical unit


def LumenSecond(value: Numeric) -> LuminousEnergy:
    """Construct a luminous energy from a magnitude expressed in lumen seconds.

    Parameters
    ----------
    value : Numeric
        Luminous energy magnitude in lm·s.

    Returns
    -------
    LuminousEnergy
        Luminous energy represented in lumen seconds.

    Examples
    --------
    A 1000 lm flash that lasts 2 ms emits 2 lm·s:

    >>> from kuchka import Lumen
    >>> from kuchka import Millisecond
    >>> Lumen(1000) * Millisecond(2)
    2 lm·s

    """
    return LuminousEnergy(to_exact(value) * LUMEN_SECOND.scale, LUMEN_SECOND)


def LumenHour(value: Numeric) -> LuminousEnergy:
    """Construct a luminous energy from a magnitude expressed in lumen hours.

    Parameters
    ----------
    value : Numeric
        Luminous energy magnitude in lm·h.

    Returns
    -------
    LuminousEnergy
        Luminous energy represented in lumen hours.

    Examples
    --------
    A 800 lm lamp that runs for 2 hours delivers 1600 lm·h:

    >>> from kuchka import Hour
    >>> from kuchka import Lumen
    >>> (Lumen(800) * Hour(2)).to(LUMEN_HOUR)
    1600 lm·h

    """
    return LuminousEnergy(to_exact(value) * LUMEN_HOUR.scale, LUMEN_HOUR)


LUMINOUS_ENERGY_UNITS: Mapping[str, Callable[[Numeric], LuminousEnergy]] = unit_table(
    "LUMINOUS_ENERGY_UNITS",
    {
        LUMEN_SECOND: LumenSecond,
        LUMEN_HOUR: LumenHour,
    },
)

__all__ = [
    "LUMEN_HOUR",
    "LUMEN_SECOND",
    "LUMINOUS_ENERGY_UNITS",
    "LumenHour",
    "LumenSecond",
]
