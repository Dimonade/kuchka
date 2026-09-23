"""Unit constructors for Time: Microsecond, Millisecond, Second, Minute, Hour.

    from kuchka import Second, Millisecond, Minute

    period = Millisecond(2)
    timeout = Second(30) + Minute(1)

`Second` is the canonical, SI-coherent unit -- the one arithmetic results (e.g.
`Length / Velocity`) come back expressed in.
`Minute` and `Hour` are non-SI but omnipresent enough to define directly, both exact:
neither carries leap-second modelling, since the intent is measurement and timeout
accounting, not calendar or civil-time arithmetic.

`TIME_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import TIME
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Time
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SECOND_NAME = "second"
SECOND_SYMBOL = "s"

MICROSECOND = prefixed_unit(MICRO, SECOND_NAME, SECOND_SYMBOL, TIME)
MILLISECOND = prefixed_unit(MILLI, SECOND_NAME, SECOND_SYMBOL, TIME)
SECOND = prefixed_unit(UNIT, SECOND_NAME, SECOND_SYMBOL, TIME)

Time._canonical_unit = SECOND  # noqa: SLF001 -- this module owns Time's canonical unit


def Microsecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in microseconds."""
    return Time(to_exact(value) * MICROSECOND.scale, MICROSECOND)


def Millisecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in milliseconds."""
    return Time(to_exact(value) * MILLISECOND.scale, MILLISECOND)


def Second(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in seconds."""
    return Time(to_exact(value) * SECOND.scale, SECOND)


# Non-SI but omnipresent - Minutes, Hours.

MINUTE = UnitDef("minute", "min", Decimal(60), TIME)
HOUR = UnitDef("hour", "h", Decimal(3600), TIME)


def Minute(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in minutes.

    Exact: a minute has always been exactly 60 seconds, with no leap-second modelling.
    The reason for this is to use it for measurement and timeout purposes, while trying
    to avoid a calendar or civil-time madhouse accounting.
    """
    return Time(to_exact(value) * MINUTE.scale, MINUTE)


def Hour(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in hours."""
    return Time(to_exact(value) * HOUR.scale, HOUR)


TIME_UNITS: Mapping[str, Callable[[Numeric], Time]] = MappingProxyType(
    {
        MICROSECOND.symbol: Microsecond,
        MILLISECOND.symbol: Millisecond,
        SECOND.symbol: Second,
        MINUTE.symbol: Minute,
        HOUR.symbol: Hour,
    }
)

__all__ = [
    "HOUR",
    "MICROSECOND",
    "MILLISECOND",
    "MINUTE",
    "SECOND",
    "TIME_UNITS",
    "Hour",
    "Microsecond",
    "Millisecond",
    "Minute",
    "Second",
]
