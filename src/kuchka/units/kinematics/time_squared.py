"""Time-squared constructors: seconds squared, with their prefixes, minutes, and hours.

`TimeSquared` is a duration times a duration, the square the constant-acceleration
formulas are written with.
The second squared is the canonical unit, and the other constructors are the exact
squares of the duration units: a minute squared is 3600 s².

Examples
--------
A mass dropped for two seconds falls through `g * t * t / 2`, however the factors are
written:

>>> from kuchka import MetrePerSecondSquared
>>> from kuchka import Second
>>> g = MetrePerSecondSquared(9.81)
>>> g * Second(2) * Second(2) / 2
19.62 m
>>> Second(2) * Second(2) * g / 2
19.62 m

The braking term of a stopping distance, `a * t² / 2`, for a deceleration of 5 m/s²
over five seconds:

>>> SecondSquared(25) * MetrePerSecondSquared(-5) / 2
-62.5 m

`TIME_SQUARED_UNITS` maps symbols such as ``"s²"`` and ``"ms²"`` to their constructors,
for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Time
    The duration a time squared is the square of.
~kuchka.quantities.Acceleration
    An acceleration times a time squared is a length.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import TIME_SQUARED
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import TimeSquared
from kuchka.quantities import UnitDef
from kuchka.units.temporal.time import HOUR
from kuchka.units.temporal.time import MICROSECOND
from kuchka.units.temporal.time import MILLISECOND
from kuchka.units.temporal.time import MINUTE
from kuchka.units.temporal.time import NANOSECOND
from kuchka.units.temporal.time import SECOND

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_TWO = symbols.SUPERSCRIPT_TWO

NANOSECOND_SQUARED = UnitDef(
    "nanosecond_squared",
    f"ns{_TWO}",
    NANOSECOND.scale**2,
    TIME_SQUARED,
    aliases=powered("ns", 2),
    words=("nanosecond squared", "nanoseconds squared"),
)
MICROSECOND_SQUARED = UnitDef(
    "microsecond_squared",
    f"{symbols.MICRO}s{_TWO}",
    MICROSECOND.scale**2,
    TIME_SQUARED,
    aliases=(*powered("us", 2), *powered(f"{symbols.SMALL_MICRO}s", 2)),
    words=("microsecond squared", "microseconds squared"),
)
MILLISECOND_SQUARED = UnitDef(
    "millisecond_squared",
    f"ms{_TWO}",
    MILLISECOND.scale**2,
    TIME_SQUARED,
    aliases=powered("ms", 2),
    words=("millisecond squared", "milliseconds squared"),
)
SECOND_SQUARED = UnitDef(
    "second_squared",
    f"s{_TWO}",
    SECOND.scale**2,
    TIME_SQUARED,
    aliases=(*powered("s", 2), *powered("sec", 2)),
    words=("second squared", "seconds squared"),
)
MINUTE_SQUARED = UnitDef(
    "minute_squared",
    f"min{_TWO}",
    MINUTE.scale**2,
    TIME_SQUARED,
    aliases=powered("min", 2),
    words=("minute squared", "minutes squared"),
)
HOUR_SQUARED = UnitDef(
    "hour_squared",
    f"h{_TWO}",
    HOUR.scale**2,
    TIME_SQUARED,
    aliases=(*powered("h", 2), *powered("hr", 2)),
    words=("hour squared", "hours squared"),
)

TimeSquared._canonical_unit = SECOND_SQUARED  # noqa: SLF001 -- this module owns TimeSquared's canonical unit


def NanosecondSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from nanoseconds squared.

    Parameters
    ----------
    value : Numeric
        Time squared in ns².

    Returns
    -------
    TimeSquared
        Time squared represented in nanoseconds squared.

    Examples
    --------
    A nanosecond squared is 1E-18 s²:

    >>> from decimal import Decimal
    >>> NanosecondSquared(1) == SecondSquared(Decimal("1e-18"))
    True

    """
    return TimeSquared(to_exact(value) * NANOSECOND_SQUARED.scale, NANOSECOND_SQUARED)


def MicrosecondSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from microseconds squared.

    Parameters
    ----------
    value : Numeric
        Time squared in µs².

    Returns
    -------
    TimeSquared
        Time squared represented in microseconds squared.

    Examples
    --------
    A million microseconds squared are one millisecond squared:

    >>> MicrosecondSquared(1_000_000) == MillisecondSquared(1)
    True

    """
    return TimeSquared(to_exact(value) * MICROSECOND_SQUARED.scale, MICROSECOND_SQUARED)


def MillisecondSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from milliseconds squared.

    Parameters
    ----------
    value : Numeric
        Time squared in ms².

    Returns
    -------
    TimeSquared
        Time squared represented in milliseconds squared.

    Examples
    --------
    A control loop with a 10 ms period has a period squared of 100 ms²:

    >>> from kuchka import Millisecond
    >>> Millisecond(10) * Millisecond(10) == MillisecondSquared(100)
    True

    """
    return TimeSquared(to_exact(value) * MILLISECOND_SQUARED.scale, MILLISECOND_SQUARED)


def SecondSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from seconds squared.

    Parameters
    ----------
    value : Numeric
        Time squared in s².

    Returns
    -------
    TimeSquared
        Time squared represented in seconds squared.

    Examples
    --------
    A length divided by an acceleration is a time squared, which is `2 * s / a`
    for a body that starts at rest:

    >>> from kuchka import Metre
    >>> from kuchka import MetrePerSecondSquared
    >>> Metre(19.62) / MetrePerSecondSquared(9.81)
    2 s²

    """
    return TimeSquared(to_exact(value) * SECOND_SQUARED.scale, SECOND_SQUARED)


def MinuteSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from minutes squared.

    Parameters
    ----------
    value : Numeric
        Time squared in min².

    Returns
    -------
    TimeSquared
        Time squared represented in minutes squared.

    Examples
    --------
    A minute squared is 3600 s²:

    >>> MinuteSquared(1) == SecondSquared(3600)
    True

    """
    return TimeSquared(to_exact(value) * MINUTE_SQUARED.scale, MINUTE_SQUARED)


def HourSquared(value: Numeric) -> TimeSquared:
    """Construct a time squared from hours squared.

    Parameters
    ----------
    value : Numeric
        Time squared in h².

    Returns
    -------
    TimeSquared
        Time squared represented in hours squared.

    Examples
    --------
    A vehicle gaining 100 km/h every hour accelerates at 100 km/h², and in two hours
    it covers `a * t² / 2`:

    >>> from kuchka import Hour
    >>> from kuchka import KilometrePerHour
    >>> KilometrePerHour(100) / Hour(1) * HourSquared(4) / 2
    200000 m

    """
    return TimeSquared(to_exact(value) * HOUR_SQUARED.scale, HOUR_SQUARED)


TIME_SQUARED_UNITS: Mapping[str, Callable[[Numeric], TimeSquared]] = unit_table(
    "TIME_SQUARED_UNITS",
    {
        NANOSECOND_SQUARED: NanosecondSquared,
        MICROSECOND_SQUARED: MicrosecondSquared,
        MILLISECOND_SQUARED: MillisecondSquared,
        SECOND_SQUARED: SecondSquared,
        MINUTE_SQUARED: MinuteSquared,
        HOUR_SQUARED: HourSquared,
    },
)

__all__ = [
    "HOUR_SQUARED",
    "MICROSECOND_SQUARED",
    "MILLISECOND_SQUARED",
    "MINUTE_SQUARED",
    "NANOSECOND_SQUARED",
    "SECOND_SQUARED",
    "TIME_SQUARED_UNITS",
    "HourSquared",
    "MicrosecondSquared",
    "MillisecondSquared",
    "MinuteSquared",
    "NanosecondSquared",
    "SecondSquared",
]
