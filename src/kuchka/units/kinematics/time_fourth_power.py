"""Time-to-the-fourth constructors: seconds, with their prefixes, minutes, and hours.

`TimeFourthPower` is a duration multiplied by itself four times, the power the
constant-snap formulas are written with.
The second to the fourth power is the canonical unit, and the other constructors are
the exact fourth powers of the duration units: a minute to the fourth power is
12960000 s⁴.

Examples
--------
A body that starts at rest, with no acceleration and no jerk, under a constant snap of
24 m/s⁴ covers `snap * t⁴ / 24`, however the factors are written:

>>> from kuchka import MetrePerSecondFourthPower
>>> from kuchka import Second
>>> snap = MetrePerSecondFourthPower(24)
>>> snap * Second(2) * Second(2) * Second(2) * Second(2) / 24
16 m
>>> snap * Second(2) ** 4 / 24
16 m

`TIME_FOURTH_POWER_UNITS` maps symbols such as ``"s⁴"`` and ``"ms⁴"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Time
    The duration a time to the fourth power is the fourth power of.
~kuchka.quantities.Snap
    A snap times a time to the fourth power is a length.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import TIME_FOURTH_POWER
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import TimeFourthPower
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

_FOUR = symbols.SUPERSCRIPT_FOUR

NANOSECOND_FOURTH_POWER = UnitDef(
    "nanosecond_to the fourth power",
    f"ns{_FOUR}",
    NANOSECOND.scale**4,
    TIME_FOURTH_POWER,
    aliases=powered("ns", 4),
    words=("nanosecond to the fourth power", "nanoseconds to the fourth power"),
)
MICROSECOND_FOURTH_POWER = UnitDef(
    "microsecond_to the fourth power",
    f"{symbols.MICRO}s{_FOUR}",
    MICROSECOND.scale**4,
    TIME_FOURTH_POWER,
    aliases=(*powered("us", 4), *powered(f"{symbols.SMALL_MICRO}s", 4)),
    words=("microsecond to the fourth power", "microseconds to the fourth power"),
)
MILLISECOND_FOURTH_POWER = UnitDef(
    "millisecond_to the fourth power",
    f"ms{_FOUR}",
    MILLISECOND.scale**4,
    TIME_FOURTH_POWER,
    aliases=powered("ms", 4),
    words=("millisecond to the fourth power", "milliseconds to the fourth power"),
)
SECOND_FOURTH_POWER = UnitDef(
    "second_to the fourth power",
    f"s{_FOUR}",
    SECOND.scale**4,
    TIME_FOURTH_POWER,
    aliases=(*powered("s", 4), *powered("sec", 4)),
    words=("second to the fourth power", "seconds to the fourth power"),
)
MINUTE_FOURTH_POWER = UnitDef(
    "minute_to the fourth power",
    f"min{_FOUR}",
    MINUTE.scale**4,
    TIME_FOURTH_POWER,
    aliases=powered("min", 4),
    words=("minute to the fourth power", "minutes to the fourth power"),
)
HOUR_FOURTH_POWER = UnitDef(
    "hour_to the fourth power",
    f"h{_FOUR}",
    HOUR.scale**4,
    TIME_FOURTH_POWER,
    aliases=(*powered("h", 4), *powered("hr", 4)),
    words=("hour to the fourth power", "hours to the fourth power"),
)

TimeFourthPower._canonical_unit = SECOND_FOURTH_POWER  # noqa: SLF001 -- this module owns TimeFourthPower's canonical unit


def NanosecondFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from nanoseconds to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in ns⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in nanoseconds to the fourth power.

    Examples
    --------
    A nanosecond to the fourth power is 1E-36 s⁴:

    >>> from decimal import Decimal
    >>> NanosecondFourthPower(1) == SecondFourthPower(Decimal("1e-36"))
    True

    """
    return TimeFourthPower(
        to_exact(value) * NANOSECOND_FOURTH_POWER.scale, NANOSECOND_FOURTH_POWER
    )


def MicrosecondFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from microseconds to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in µs⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in microseconds to the fourth power.

    Examples
    --------
    A million million microseconds to the fourth power are one millisecond
    to the fourth power:

    >>> MicrosecondFourthPower(10**12) == MillisecondFourthPower(1)
    True

    """
    return TimeFourthPower(
        to_exact(value) * MICROSECOND_FOURTH_POWER.scale, MICROSECOND_FOURTH_POWER
    )


def MillisecondFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from milliseconds to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in ms⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in milliseconds to the fourth power.

    Examples
    --------
    A control loop with a 10 ms period has a period to the fourth power of
    10000 ms⁴:

    >>> from kuchka import Millisecond
    >>> Millisecond(10) ** 4 == MillisecondFourthPower(10_000)
    True

    """
    return TimeFourthPower(
        to_exact(value) * MILLISECOND_FOURTH_POWER.scale, MILLISECOND_FOURTH_POWER
    )


def SecondFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from seconds to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in s⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in seconds to the fourth power.

    Examples
    --------
    A length divided by a snap is a time to the fourth power, which is `24 * s / snap`
    for a body that starts at rest, with no acceleration and no jerk:

    >>> from kuchka import Metre
    >>> from kuchka import MetrePerSecondFourthPower
    >>> Metre(48) / MetrePerSecondFourthPower(24)
    2 s⁴

    """
    return TimeFourthPower(
        to_exact(value) * SECOND_FOURTH_POWER.scale, SECOND_FOURTH_POWER
    )


def MinuteFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from minutes to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in min⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in minutes to the fourth power.

    Examples
    --------
    A minute to the fourth power is 12960000 s⁴:

    >>> MinuteFourthPower(1) == SecondFourthPower(12_960_000)
    True

    """
    return TimeFourthPower(
        to_exact(value) * MINUTE_FOURTH_POWER.scale, MINUTE_FOURTH_POWER
    )


def HourFourthPower(value: Numeric) -> TimeFourthPower:
    """Construct a time to the fourth power from hours to the fourth power.

    Parameters
    ----------
    value : Numeric
        Time to the fourth power in h⁴.

    Returns
    -------
    TimeFourthPower
        Time to the fourth power represented in hours to the fourth power.

    Examples
    --------
    An hour to the fourth power is 167961600000000 s⁴:

    >>> HourFourthPower(1) == SecondFourthPower(167_961_600_000_000)
    True

    """
    return TimeFourthPower(to_exact(value) * HOUR_FOURTH_POWER.scale, HOUR_FOURTH_POWER)


TIME_FOURTH_POWER_UNITS: Mapping[str, Callable[[Numeric], TimeFourthPower]] = (
    unit_table(
        "TIME_FOURTH_POWER_UNITS",
        {
            NANOSECOND_FOURTH_POWER: NanosecondFourthPower,
            MICROSECOND_FOURTH_POWER: MicrosecondFourthPower,
            MILLISECOND_FOURTH_POWER: MillisecondFourthPower,
            SECOND_FOURTH_POWER: SecondFourthPower,
            MINUTE_FOURTH_POWER: MinuteFourthPower,
            HOUR_FOURTH_POWER: HourFourthPower,
        },
    )
)

__all__ = [
    "HOUR_FOURTH_POWER",
    "MICROSECOND_FOURTH_POWER",
    "MILLISECOND_FOURTH_POWER",
    "MINUTE_FOURTH_POWER",
    "NANOSECOND_FOURTH_POWER",
    "SECOND_FOURTH_POWER",
    "TIME_FOURTH_POWER_UNITS",
    "HourFourthPower",
    "MicrosecondFourthPower",
    "MillisecondFourthPower",
    "MinuteFourthPower",
    "NanosecondFourthPower",
    "SecondFourthPower",
]
