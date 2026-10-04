"""Time quantities and constructors from femtoseconds to astronomical years.

`Time` represents a duration.
The second is the canonical SI base unit of time, and the unit in which derived
quantities such as `Length / Velocity` are expressed.

The constructors in this module cover exact SI decimal scales together with a small set
of exact non-SI duration units that are useful in engineering, science, and everyday
measurement.

The SI-prefix constructors span nanoseconds, picoseconds, femtoseconds, microseconds,
milliseconds, and seconds.
`Minute`, `Hour`, and `Day` provide exact human-scale durations.
`Week` and `Fortnight` are defined as exact integer numbers of 24-hour days.

`JulianYear` is an exact astronomical duration of 365.25 days.
It is distinct from a calendar year: this module measures elapsed time and does not
model calendar dates, leap years, leap seconds, time zones, or civil-time rules.

`Jiffy` is provided in its physics sense: the time required for light to travel one
femtometre in vacuum.
Because the femtometre and the speed of light are exactly defined in SI, this is
represented exactly as a rational number of seconds.

Examples
--------
Time appears at radically different scales in engineering and science.

A one-millisecond interval is long enough to be significant in embedded systems while
still being almost instantaneous to a human observer:

>>> control_period = Millisecond(1)
>>> control_period
1 ms

Microseconds are a natural scale for device timing.
A 250 µs pulse is still only a quarter of a millisecond:

>>> pulse_width = Microsecond(250)
>>> pulse_width
250 µs

The smaller scales belong to high-speed electronics and experimental physics.
A 10 ns interval is a useful scale for digital pulse timing:

>>> propagation_window = Nanosecond(10)
>>> propagation_window
10 ns

At the picosecond scale, timing measurements begin to resolve individual features of
very fast electronic and optical systems:

>>> timing_interval = Picosecond(100)
>>> timing_interval
100 ps

Ultrafast laser physics operates in the femtosecond regime:

>>> laser_pulse = Femtosecond(100)
>>> laser_pulse
100 fs

The SI second itself has an unusually concrete physical definition.
One second contains exactly 9,192,631,770 periods of the radiation corresponding to the
cesium-133 transition used to define the SI second:

>>> clock_interval = Second(1)
>>> clock_interval
1 s

Human-scale durations remain the same exact quantity.
A timeout of 30 seconds followed by one minute is exactly 90 seconds:

>>> timeout = Second(30) + Minute(1)
>>> timeout
90 s

An hour is exactly 60 minutes:

>>> work_session = Hour(2)
>>> work_session == Minute(120)
True

A day is exactly 24 hours in this duration model:

>>> day = Day(1)
>>> day
1 d

>>> day == Hour(24)
True

Longer experiments can therefore be described without introducing a new concept of time.
A two-week experiment is exactly one fortnight:

>>> experiment = Fortnight(1)
>>> experiment
1 fortnight

>>> experiment == Day(14)
True

Astronomy needs a different kind of long duration.
A Julian year is exactly 365.25 days:

>>> julian_year = JulianYear(1)
>>> julian_year
1 a

>>> julian_year == Day(365.25)
True

A Julian year therefore contains exactly 31,557,600 seconds:

>>> julian_year == Second(31_557_600)
True

For extremely small physical scales, a physics jiffy can be defined from the speed of
light.
One jiffy is the time light takes to cross one femtometre:

>>> jiffy = Jiffy(1)
>>> jiffy
1 jiffy

The duration is far below a femtosecond:

>>> jiffy < Femtosecond(1)
True

All of these values remain members of the same `Time` dimension.
A change of unit scale never changes the represented duration:

>>> Millisecond(1) == Microsecond(1000)
True

>>> Microsecond(1) == Nanosecond(1000)
True

>>> Nanosecond(1) == Picosecond(1000)
True

>>> Picosecond(1) == Femtosecond(1000)
True

Notes
-----
The second is an SI base unit.
Its definition is tied to the caesium-133 ground-state hyperfine transition frequency.

This module represents **durations**, not points on a calendar.

In particular, `Day(1)` means exactly 86,400 seconds.
It does not model a civil-time day that may contain a leap second.

Likewise, `Week(1)` means exactly seven such days and `Fortnight(1)` means exactly
fourteen such days.
They are duration units; they do not perform calendar arithmetic.

A calendar year is deliberately not represented by an unqualified `Year` constructor.
Civil and astronomical uses of "year" do not define one universally fixed number of SI
seconds.

`JulianYear` is the precise astronomical duration of exactly 365.25 days, or 31,557,600
seconds.
The International Astronomical Union recommends the Julian year for precise
astronomical interval measurements when another kind of year is not specified.

`Jiffy` is a specialised physics unit rather than an SI unit.
Here it is defined specifically as one femtometre divided by the exact speed of light
in vacuum.
The resulting value is exact even though its decimal representation is non-terminating.

The word "jiffy" also has other technical meanings.
In electrical engineering it can mean one AC power-cycle period, which is 1/50 s in a
50 Hz system and 1/60 s in a 60 Hz system.
That meaning is intentionally not represented here because it does not define one
universal duration.

Metric prefixes represent exact powers of ten.
Consequently, conversions such as

>>> Microsecond(1000) == Millisecond(1)
True

and

>>> Millisecond(1000) == Second(1)
True

are exact.

`TIME_UNITS` maps symbols such as ``"ns"``, ``"µs"``, ``"ms"``, ``"s"``, ``"min"``,
``"h"``, and ``"d"`` to their constructors.
Non-SI units such as weeks, fortnights, and Julian years can also be exposed through
the mapping using their chosen textual symbols.

See Also
--------
~kuchka.quantities.Frequency
    Reciprocal time quantity for repeating events and oscillations.
~kuchka.quantities.Length
    Distance travelled during a time interval.
~kuchka.quantities.Velocity
    Distance travelled per unit time.
~kuchka.quantities.Acceleration
    Change of velocity per unit time.

"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import TIME
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Time
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable

SECOND_NAME = "second"
SECOND_SYMBOL = "s"
SECOND_ALIASES = ("sec",)
"""Another symbol for the second, which prefixes follow: `msec`."""

FEMTOSECOND = prefixed_unit(
    prefixes.FEMTO, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)
PICOSECOND = prefixed_unit(
    prefixes.PICO, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)
NANOSECOND = prefixed_unit(
    prefixes.NANO, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)
MICROSECOND = prefixed_unit(
    prefixes.MICRO, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)
MILLISECOND = prefixed_unit(
    prefixes.MILLI, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)
SECOND = prefixed_unit(
    prefixes.UNIT, SECOND_NAME, SECOND_SYMBOL, TIME, base_aliases=SECOND_ALIASES
)


Time._canonical_unit = SECOND  # noqa: SLF001 -- this module owns Time's canonical unit


def Femtosecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in femtoseconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in femtoseconds.

    Returns
    -------
    Time
        Time represented in femtoseconds.

    Examples
    --------
    Ultrafast laser pulses are routinely measured in femtoseconds:

    >>> laser_pulse = Femtosecond(100)
    >>> laser_pulse
    100 fs

    One thousand femtoseconds make exactly one picosecond:

    >>> Femtosecond(1000) == Picosecond(1)
    True

    """
    return Time(to_exact(value) * FEMTOSECOND.scale, FEMTOSECOND)


def Picosecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in picoseconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in picoseconds.

    Returns
    -------
    Time
        Time represented in picoseconds.

    Examples
    --------
    Picosecond timing is relevant to high-speed electronic and optical measurements:

    >>> timing_interval = Picosecond(100)
    >>> timing_interval
    100 ps

    One thousand picoseconds make exactly one nanosecond:

    >>> Picosecond(1000) == Nanosecond(1)
    True

    """
    return Time(to_exact(value) * PICOSECOND.scale, PICOSECOND)


def Nanosecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in nanoseconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in nanoseconds.

    Returns
    -------
    Time
        Time represented in nanoseconds.

    Examples
    --------
    Nanoseconds are a natural scale for digital timing and high-speed measurement:

    >>> pulse_interval = Nanosecond(10)
    >>> pulse_interval
    10 ns

    One thousand nanoseconds make exactly one microsecond:

    >>> Nanosecond(1000) == Microsecond(1)
    True

    """
    return Time(to_exact(value) * NANOSECOND.scale, NANOSECOND)


def Microsecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in microseconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in microseconds.

    Returns
    -------
    Time
        Time represented in microseconds.

    Examples
    --------
    A quarter-millisecond device pulse can be expressed directly:

    >>> pulse_width = Microsecond(250)
    >>> pulse_width
    250 µs

    One thousand microseconds make exactly one millisecond:

    >>> Microsecond(1000) == Millisecond(1)
    True

    """
    return Time(to_exact(value) * MICROSECOND.scale, MICROSECOND)


def Millisecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in milliseconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in milliseconds.

    Returns
    -------
    Time
        Time represented in milliseconds.

    Examples
    --------
    A 1 ms control period is a convenient scale for embedded systems:

    >>> control_period = Millisecond(1)
    >>> control_period
    1 ms

    One thousand milliseconds make exactly one second:

    >>> Millisecond(1000) == Second(1)
    True

    """
    return Time(to_exact(value) * MILLISECOND.scale, MILLISECOND)


def Second(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in seconds.

    Parameters
    ----------
    value : Numeric
        Time magnitude in seconds.

    Returns
    -------
    Time
        Time represented in seconds.

    Examples
    --------
    The second is the canonical SI unit of time:

    >>> interval = Second(1)
    >>> interval
    1 s

    A timeout can be built naturally from smaller human-scale durations:

    >>> timeout = Second(30) + Minute(1)
    >>> timeout
    90 s

    """
    return Time(to_exact(value) * SECOND.scale, SECOND)


# Non-SI but omnipresent - Minutes, Hours.

MINUTE = UnitDef("minute", "min", Decimal(60), TIME, aliases=("mins",))
HOUR = UnitDef("hour", "h", Decimal(3600), TIME, aliases=("hr", "hrs"))
DAY = UnitDef("day", "d", Decimal(86_400), TIME, aliases=("dy",))
WEEK = UnitDef("week", "wk", Decimal(604_800), TIME, aliases=("wks",))
FORTNIGHT = UnitDef("fortnight", "fortnight", Decimal(1_209_600), TIME)
JULIAN_YEAR = UnitDef(
    "julian_year", "a", Decimal(31_557_600), TIME, aliases=("yr", "yrs")
)


def Minute(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in minutes.

    Parameters
    ----------
    value : Numeric
        Time magnitude in minutes.

    Returns
    -------
    Time
        Time represented in minutes.

    Examples
    --------
    A minute contains exactly sixty seconds:

    >>> Minute(1) == Second(60)
    True

    A 90-second timeout can be expressed naturally as one minute plus thirty seconds:

    >>> timeout = Minute(1) + Second(30)
    >>> timeout
    1.5 min

    """
    return Time(to_exact(value) * MINUTE.scale, MINUTE)


def Hour(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in hours.

    Parameters
    ----------
    value : Numeric
        Time magnitude in hours.

    Returns
    -------
    Time
        Time represented in hours.

    Examples
    --------
    Two hours contain exactly 120 minutes:

    >>> work_session = Hour(2)
    >>> work_session == Minute(120)
    True

    """
    return Time(to_exact(value) * HOUR.scale, HOUR)


def Day(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in days.

    Parameters
    ----------
    value : Numeric
        Time magnitude in days.

    Returns
    -------
    Time
        Time represented in days.

    Notes
    -----
    A day is exactly 86,400 seconds in this duration model.
    This does not model civil-time days containing a leap second.

    Examples
    --------
    A complete 24-hour duration is exactly one day:

    >>> Day(1) == Hour(24)
    True

    """
    return Time(to_exact(value) * DAY.scale, DAY)


def Week(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in weeks.

    Parameters
    ----------
    value : Numeric
        Time magnitude in weeks.

    Returns
    -------
    Time
        Time represented in weeks.

    Notes
    -----
    A week is defined here as exactly seven 24-hour days.

    Examples
    --------
    One week is exactly seven days:

    >>> Week(1) == Day(7)
    True

    """
    return Time(to_exact(value) * WEEK.scale, WEEK)


def Fortnight(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in fortnights.

    Parameters
    ----------
    value : Numeric
        Time magnitude in fortnights.

    Returns
    -------
    Time
        Time represented in fortnights.

    Notes
    -----
    A fortnight is exactly fourteen 24-hour days.

    Examples
    --------
    A fortnight is exactly two weeks:

    >>> Fortnight(1) == Week(2)
    True

    """
    return Time(to_exact(value) * FORTNIGHT.scale, FORTNIGHT)


def JulianYear(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in Julian years.

    Parameters
    ----------
    value : Numeric
        Time magnitude in Julian years.

    Returns
    -------
    Time
        Time represented in Julian years.

    Notes
    -----
    A Julian year is exactly 365.25 days, or 31,557,600 seconds.
    It is an astronomical duration and does not represent a calendar year.

    Examples
    --------
    A Julian year is exactly 365.25 days:

    >>> year = JulianYear(1)
    >>> year == Day(365.25)
    True

    The same duration is exactly 31,557,600 seconds:

    >>> year == Second(31_557_600)
    True

    """
    return Time(to_exact(value) * JULIAN_YEAR.scale, JULIAN_YEAR)


# Curiosities.


JIFFY = UnitDef(
    "jiffy",
    "jiffy",
    Fraction(1, 299_792_458_000_000_000_000_000),
    TIME,
    words=("jiffies",),
)


def Jiffy(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in physics jiffies.

    Parameters
    ----------
    value : Numeric
        Time magnitude in physics jiffies.

    Returns
    -------
    Time
        Time represented in jiffies.

    Notes
    -----
    One physics jiffy is defined here as the time required for light to travel one
    femtometre in vacuum.

    Since one femtometre is exactly ``10^-15 m`` and the speed of light in vacuum is
    exactly ``299_792_458 m/s``, the conversion is an exact rational number of seconds.

    Examples
    --------
    One physics jiffy corresponds to the time light takes to cross a femtometre:

    >>> jiffy = Jiffy(1)
    >>> jiffy
    1 jiffy

    Its duration is much shorter than one femtosecond:

    >>> jiffy < Femtosecond(1)
    True

    """
    return Time(to_exact(value) * JIFFY.scale, JIFFY)


TIME_UNITS: UnitTable[Time] = unit_table(
    "TIME_UNITS",
    {
        FEMTOSECOND: Femtosecond,
        PICOSECOND: Picosecond,
        NANOSECOND: Nanosecond,
        MICROSECOND: Microsecond,
        MILLISECOND: Millisecond,
        SECOND: Second,
        MINUTE: Minute,
        HOUR: Hour,
        DAY: Day,
        WEEK: Week,
        FORTNIGHT: Fortnight,
        JULIAN_YEAR: JulianYear,
        JIFFY: Jiffy,
    },
)

__all__ = [
    "DAY",
    "FEMTOSECOND",
    "FORTNIGHT",
    "HOUR",
    "JIFFY",
    "JULIAN_YEAR",
    "MICROSECOND",
    "MILLISECOND",
    "MINUTE",
    "NANOSECOND",
    "PICOSECOND",
    "SECOND",
    "TIME_UNITS",
    "WEEK",
    "Day",
    "Femtosecond",
    "Fortnight",
    "Hour",
    "Jiffy",
    "JulianYear",
    "Microsecond",
    "Millisecond",
    "Minute",
    "Nanosecond",
    "Picosecond",
    "Second",
    "Week",
]
