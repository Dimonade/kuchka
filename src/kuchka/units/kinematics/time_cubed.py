"""Time-cubed constructors: seconds cubed, with their prefixes, minutes, and hours.

`TimeCubed` is a duration times a duration times a duration, the cube the
constant-jerk formulas are written with.
The second cubed is the canonical unit, and the other constructors are the exact cubes
of the duration units: a minute cubed is 216000 s³.

Examples
--------
A body that starts at rest, with no acceleration, under a constant jerk of 6 m/s³
covers `j * t³ / 6`, however the factors are written:

>>> from kuchka import MetrePerSecondCubed, Second
>>> jerk = MetrePerSecondCubed(6)
>>> jerk * Second(2) * Second(2) * Second(2) / 6
8 m
>>> jerk * Second(2) ** 3 / 6
8 m

`TIME_CUBED_UNITS` maps symbols such as ``"s³"`` and ``"ms³"`` to their constructors,
for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Time
    The duration a time cubed is the cube of.
~kuchka.quantities.Jerk
    A jerk times a time cubed is a length.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import TIME_CUBED
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import TimeCubed
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

_THREE = symbols.SUPERSCRIPT_THREE

NANOSECOND_CUBED = UnitDef(
    "nanosecond_cubed",
    f"ns{_THREE}",
    NANOSECOND.scale**3,
    TIME_CUBED,
    aliases=powered("ns", 3),
    words=("nanosecond cubed", "nanoseconds cubed"),
)
MICROSECOND_CUBED = UnitDef(
    "microsecond_cubed",
    f"{symbols.MICRO}s{_THREE}",
    MICROSECOND.scale**3,
    TIME_CUBED,
    aliases=(*powered("us", 3), *powered(f"{symbols.SMALL_MICRO}s", 3)),
    words=("microsecond cubed", "microseconds cubed"),
)
MILLISECOND_CUBED = UnitDef(
    "millisecond_cubed",
    f"ms{_THREE}",
    MILLISECOND.scale**3,
    TIME_CUBED,
    aliases=powered("ms", 3),
    words=("millisecond cubed", "milliseconds cubed"),
)
SECOND_CUBED = UnitDef(
    "second_cubed",
    f"s{_THREE}",
    SECOND.scale**3,
    TIME_CUBED,
    aliases=(*powered("s", 3), *powered("sec", 3)),
    words=("second cubed", "seconds cubed"),
)
MINUTE_CUBED = UnitDef(
    "minute_cubed",
    f"min{_THREE}",
    MINUTE.scale**3,
    TIME_CUBED,
    aliases=powered("min", 3),
    words=("minute cubed", "minutes cubed"),
)
HOUR_CUBED = UnitDef(
    "hour_cubed",
    f"h{_THREE}",
    HOUR.scale**3,
    TIME_CUBED,
    aliases=(*powered("h", 3), *powered("hr", 3)),
    words=("hour cubed", "hours cubed"),
)

TimeCubed._canonical_unit = SECOND_CUBED  # noqa: SLF001 -- this module owns TimeCubed's canonical unit


def NanosecondCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from nanoseconds cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in ns³.

    Returns
    -------
    TimeCubed
        Time cubed represented in nanoseconds cubed.

    Examples
    --------
    A nanosecond cubed is 1E-27 s³:

    >>> from decimal import Decimal
    >>> NanosecondCubed(1) == SecondCubed(Decimal("1e-27"))
    True

    """
    return TimeCubed(to_exact(value) * NANOSECOND_CUBED.scale, NANOSECOND_CUBED)


def MicrosecondCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from microseconds cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in µs³.

    Returns
    -------
    TimeCubed
        Time cubed represented in microseconds cubed.

    Examples
    --------
    A thousand million microseconds cubed are one millisecond cubed:

    >>> MicrosecondCubed(1_000_000_000) == MillisecondCubed(1)
    True

    """
    return TimeCubed(to_exact(value) * MICROSECOND_CUBED.scale, MICROSECOND_CUBED)


def MillisecondCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from milliseconds cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in ms³.

    Returns
    -------
    TimeCubed
        Time cubed represented in milliseconds cubed.

    Examples
    --------
    A control loop with a 10 ms period has a period cubed of 1000 ms³:

    >>> from kuchka import Millisecond
    >>> Millisecond(10) ** 3 == MillisecondCubed(1000)
    True

    """
    return TimeCubed(to_exact(value) * MILLISECOND_CUBED.scale, MILLISECOND_CUBED)


def SecondCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from seconds cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in s³.

    Returns
    -------
    TimeCubed
        Time cubed represented in seconds cubed.

    Examples
    --------
    A length divided by a jerk is a time cubed, which is `6 * s / j` for a body
    that starts at rest and at zero acceleration:

    >>> from kuchka import Metre, MetrePerSecondCubed
    >>> Metre(8) / MetrePerSecondCubed(1)
    8 s³

    """
    return TimeCubed(to_exact(value) * SECOND_CUBED.scale, SECOND_CUBED)


def MinuteCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from minutes cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in min³.

    Returns
    -------
    TimeCubed
        Time cubed represented in minutes cubed.

    Examples
    --------
    A minute cubed is 216000 s³:

    >>> MinuteCubed(1) == SecondCubed(216_000)
    True

    """
    return TimeCubed(to_exact(value) * MINUTE_CUBED.scale, MINUTE_CUBED)


def HourCubed(value: Numeric) -> TimeCubed:
    """Construct a time cubed from hours cubed.

    Parameters
    ----------
    value : Numeric
        Time cubed in h³.

    Returns
    -------
    TimeCubed
        Time cubed represented in hours cubed.

    Examples
    --------
    An hour cubed is 46656000000 s³:

    >>> HourCubed(1) == SecondCubed(46_656_000_000)
    True

    """
    return TimeCubed(to_exact(value) * HOUR_CUBED.scale, HOUR_CUBED)


TIME_CUBED_UNITS: Mapping[str, Callable[[Numeric], TimeCubed]] = unit_table(
    "TIME_CUBED_UNITS",
    {
        NANOSECOND_CUBED: NanosecondCubed,
        MICROSECOND_CUBED: MicrosecondCubed,
        MILLISECOND_CUBED: MillisecondCubed,
        SECOND_CUBED: SecondCubed,
        MINUTE_CUBED: MinuteCubed,
        HOUR_CUBED: HourCubed,
    },
)

__all__ = [
    "HOUR_CUBED",
    "MICROSECOND_CUBED",
    "MILLISECOND_CUBED",
    "MINUTE_CUBED",
    "NANOSECOND_CUBED",
    "SECOND_CUBED",
    "TIME_CUBED_UNITS",
    "HourCubed",
    "MicrosecondCubed",
    "MillisecondCubed",
    "MinuteCubed",
    "NanosecondCubed",
    "SecondCubed",
]
