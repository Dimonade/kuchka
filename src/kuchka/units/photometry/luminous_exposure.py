"""Luminous exposure constructors: lux-seconds, lux-hours, and kilolux-hours.

Luminous exposure is illuminance accumulated over time: `1 lx·s = 1 lm·s/m²`.
The lux second is the canonical unit.
The lux hour is 3600 lux seconds, and is the unit museums and conservators budget
light in, since the damage light does to a pigment grows with the exposure it has had.
The kilolux hour suits daylight, where a lux hour is a small number.

`LUMINOUS_EXPOSURE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import LUMINOUS_EXPOSURE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import LuminousExposure
from kuchka.quantities import UnitDef
from kuchka.units.temporal.time import HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

LUX_SECOND = UnitDef(
    "lux_second",
    f"lx{symbols.MIDDLE_DOT}s",
    1,
    LUMINOUS_EXPOSURE,
    aliases=("lx*s", "lx s"),
)
LUX_HOUR = UnitDef(
    "lux_hour",
    f"lx{symbols.MIDDLE_DOT}h",
    HOUR.scale,
    LUMINOUS_EXPOSURE,
    aliases=("lx*h", "lx h"),
)
KILOLUX_HOUR = with_prefix(prefixes.KILO, LUX_HOUR)

LuminousExposure._canonical_unit = LUX_SECOND  # noqa: SLF001 -- this module owns LuminousExposure's canonical unit


def LuxSecond(value: Numeric) -> LuminousExposure:
    """Construct a luminous exposure from a magnitude expressed in lux seconds.

    Parameters
    ----------
    value : Numeric
        Luminous exposure magnitude in lx·s.

    Returns
    -------
    LuminousExposure
        Luminous exposure represented in lux seconds.

    Examples
    --------
    A 500 lx work surface lit for 10 s receives 5000 lx·s:

    >>> from kuchka import Lux
    >>> from kuchka import Second
    >>> Lux(500) * Second(10)
    5000 lx·s

    """
    return LuminousExposure(to_exact(value) * LUX_SECOND.scale, LUX_SECOND)


def LuxHour(value: Numeric) -> LuminousExposure:
    """Construct a luminous exposure from a magnitude expressed in lux hours.

    Parameters
    ----------
    value : Numeric
        Luminous exposure magnitude in lx·h.

    Returns
    -------
    LuminousExposure
        Luminous exposure represented in lux hours.

    Examples
    --------
    A watercolour lit at 50 lx for an 8 hour opening day takes 400 lx·h of exposure:

    >>> from kuchka import Hour
    >>> from kuchka import Lux
    >>> (Lux(50) * Hour(8)).to(LUX_HOUR)
    400 lx·h

    """
    return LuminousExposure(to_exact(value) * LUX_HOUR.scale, LUX_HOUR)


def KiloluxHour(value: Numeric) -> LuminousExposure:
    """Construct a luminous exposure from a magnitude expressed in kilolux hours.

    Parameters
    ----------
    value : Numeric
        Luminous exposure magnitude in klx·h.

    Returns
    -------
    LuminousExposure
        Luminous exposure represented in kilolux hours.

    Examples
    --------
    Ten hours of 20 klx daylight is 200 klx·h:

    >>> from kuchka import Hour
    >>> from kuchka import Kilolux
    >>> (Kilolux(20) * Hour(10)).to(KILOLUX_HOUR)
    200 klx·h

    """
    return LuminousExposure(to_exact(value) * KILOLUX_HOUR.scale, KILOLUX_HOUR)


LUMINOUS_EXPOSURE_UNITS: Mapping[str, Callable[[Numeric], LuminousExposure]] = (
    unit_table(
        "LUMINOUS_EXPOSURE_UNITS",
        {
            LUX_SECOND: LuxSecond,
            LUX_HOUR: LuxHour,
            KILOLUX_HOUR: KiloluxHour,
        },
    )
)

__all__ = [
    "KILOLUX_HOUR",
    "LUMINOUS_EXPOSURE_UNITS",
    "LUX_HOUR",
    "LUX_SECOND",
    "KiloluxHour",
    "LuxHour",
    "LuxSecond",
]
