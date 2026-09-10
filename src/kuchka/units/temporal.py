"""Unit constructors for Time, Frequency, and the acquisition-domain vocabulary.

    from kuchka import Second, Millisecond, Hertz

    period = Millisecond(2)
    rate = Hertz(500)

`SamplingPeriod` and `SampleRate` share their display symbols with `Time` and
`Frequency` (both read out in seconds and hertz on a datasheet), even though they are
different Python types;
the type is what carries the distinction, not the symbol.
`BaudRate` gets its own symbol, `Bd`, as that is how it actually appears in the wild.

`TIME_UNITS`, `FREQUENCY_UNITS`, `SAMPLING_PERIOD_UNITS`, `SAMPLE_RATE_UNITS`, and
`BAUD_RATE_UNITS` each map a symbol string to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import KILO
from kuchka.prefixes import MEGA
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import BaudRate
from kuchka.quantities import Frequency
from kuchka.quantities import SampleRate
from kuchka.quantities import SamplingPeriod
from kuchka.quantities import Time
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

# Time

SECOND_NAME = "second"
SECOND_SYMBOL = "s"

MICROSECOND = prefixed_unit(MICRO, SECOND_NAME, SECOND_SYMBOL, TIME)
MILLISECOND = prefixed_unit(MILLI, SECOND_NAME, SECOND_SYMBOL, TIME)
SECOND = prefixed_unit(UNIT, SECOND_NAME, SECOND_SYMBOL, TIME)

Time._canonical_unit = SECOND  # noqa: SLF001 -- this module owns Time's canonical unit


def Microsecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in microseconds."""
    return Time(to_decimal(value) * MICROSECOND.scale, MICROSECOND)


def Millisecond(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in milliseconds."""
    return Time(to_decimal(value) * MILLISECOND.scale, MILLISECOND)


def Second(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in seconds."""
    return Time(to_decimal(value) * SECOND.scale, SECOND)


# Non-SI but omnipresent - Minutes, Hours.

MINUTE = UnitDef("minute", "min", Decimal(60), TIME)
HOUR = UnitDef("hour", "h", Decimal(3600), TIME)


def Minute(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in minutes.

    Exact: a minute has always been exactly 60 seconds, with no leap-second modelling.
    The reason for this is to use it for measurement and timeout purposes, while trying
    to avoid a calendar or civil-time type madhouse accounting.
    """
    return Time(to_decimal(value) * MINUTE.scale, MINUTE)


def Hour(value: Numeric) -> Time:
    """Construct a Time from a magnitude expressed in hours."""
    return Time(to_decimal(value) * HOUR.scale, HOUR)


TIME_UNITS: Mapping[str, Callable[[Numeric], Time]] = MappingProxyType(
    {
        MICROSECOND.symbol: Microsecond,
        MILLISECOND.symbol: Millisecond,
        SECOND.symbol: Second,
        MINUTE.symbol: Minute,
        HOUR.symbol: Hour,
    }
)


# Frequency

HERTZ_NAME = "hertz"
HERTZ_SYMBOL = "Hz"

HERTZ = prefixed_unit(UNIT, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
KILOHERTZ = prefixed_unit(KILO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MEGAHERTZ = prefixed_unit(MEGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)


Frequency._canonical_unit = HERTZ  # noqa: SLF001 -- this module owns Frequency's canonical unit


def Hertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in hertz."""
    return Frequency(to_decimal(value) * HERTZ.scale, HERTZ)


def Kilohertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in kilohertz."""
    return Frequency(to_decimal(value) * KILOHERTZ.scale, KILOHERTZ)


def Megahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in megahertz."""
    return Frequency(to_decimal(value) * MEGAHERTZ.scale, MEGAHERTZ)


FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = MappingProxyType(
    {
        HERTZ.symbol: Hertz,
        KILOHERTZ.symbol: Kilohertz,
        MEGAHERTZ.symbol: Megahertz,
    }
)


# SamplingPeriod

SAMPLING_PERIOD_MICROSECOND = UnitDef(
    "sampling_period_microsecond",
    "\u00b5s",
    Decimal("0.000001"),
    TIME,
)
SAMPLING_PERIOD_MILLISECOND = UnitDef(
    "sampling_period_millisecond",
    "ms",
    Decimal("0.001"),
    TIME,
)
SAMPLING_PERIOD_SECOND = UnitDef("sampling_period_second", "s", Decimal(1), TIME)

SamplingPeriod._canonical_unit = SAMPLING_PERIOD_SECOND  # noqa: SLF001


def MicrosecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in microseconds."""
    return SamplingPeriod(
        to_decimal(value) * SAMPLING_PERIOD_MICROSECOND.scale,
        SAMPLING_PERIOD_MICROSECOND,
    )


def MillisecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in milliseconds."""
    return SamplingPeriod(
        to_decimal(value) * SAMPLING_PERIOD_MILLISECOND.scale,
        SAMPLING_PERIOD_MILLISECOND,
    )


def SecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in seconds."""
    return SamplingPeriod(
        to_decimal(value) * SAMPLING_PERIOD_SECOND.scale,
        SAMPLING_PERIOD_SECOND,
    )


SAMPLING_PERIOD_UNITS: Mapping[str, Callable[[Numeric], SamplingPeriod]] = (
    MappingProxyType(
        {
            SAMPLING_PERIOD_MICROSECOND.symbol: MicrosecondSamplingPeriod,
            SAMPLING_PERIOD_MILLISECOND.symbol: MillisecondSamplingPeriod,
            SAMPLING_PERIOD_SECOND.symbol: SecondSamplingPeriod,
        }
    )
)


# SampleRate

SAMPLE_PER_SECOND = UnitDef("sample_per_second", "Sa/s", Decimal(1), FREQUENCY)
KILOSAMPLE_PER_SECOND = UnitDef(
    "kilosample_per_second",
    "kSa/s",
    Decimal(1000),
    FREQUENCY,
)
MEGASAMPLE_PER_SECOND = UnitDef(
    "megasample_per_second",
    "MSa/s",
    Decimal(1_000_000),
    FREQUENCY,
)

SampleRate._canonical_unit = SAMPLE_PER_SECOND  # noqa: SLF001


def SamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in samples per second."""
    return SampleRate(to_decimal(value) * SAMPLE_PER_SECOND.scale, SAMPLE_PER_SECOND)


def KilosamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in kilosamples per second."""
    return SampleRate(
        to_decimal(value) * KILOSAMPLE_PER_SECOND.scale,
        KILOSAMPLE_PER_SECOND,
    )


def MegasamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in megasamples per second."""
    return SampleRate(
        to_decimal(value) * MEGASAMPLE_PER_SECOND.scale,
        MEGASAMPLE_PER_SECOND,
    )


SAMPLE_RATE_UNITS: Mapping[str, Callable[[Numeric], SampleRate]] = MappingProxyType(
    {
        SAMPLE_PER_SECOND.symbol: SamplesPerSecond,
        KILOSAMPLE_PER_SECOND.symbol: KilosamplesPerSecond,
        MEGASAMPLE_PER_SECOND.symbol: MegasamplesPerSecond,
    }
)


# BaudRate

BAUD = UnitDef("baud", "Bd", Decimal(1), FREQUENCY)
KILOBAUD = UnitDef("kilobaud", "kBd", Decimal(1000), FREQUENCY)

BaudRate._canonical_unit = BAUD  # noqa: SLF001


def Baud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in baud."""
    return BaudRate(to_decimal(value) * BAUD.scale, BAUD)


def Kilobaud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in kilobaud."""
    return BaudRate(to_decimal(value) * KILOBAUD.scale, KILOBAUD)


BAUD_RATE_UNITS: Mapping[str, Callable[[Numeric], BaudRate]] = MappingProxyType(
    {
        BAUD.symbol: Baud,
        KILOBAUD.symbol: Kilobaud,
    }
)

__all__ = [
    "BAUD",
    "BAUD_RATE_UNITS",
    "FREQUENCY_UNITS",
    "HERTZ",
    "HOUR",
    "KILOBAUD",
    "KILOHERTZ",
    "KILOSAMPLE_PER_SECOND",
    "MEGAHERTZ",
    "MEGASAMPLE_PER_SECOND",
    "MICROSECOND",
    "MILLISECOND",
    "MINUTE",
    "SAMPLE_PER_SECOND",
    "SAMPLE_RATE_UNITS",
    "SAMPLING_PERIOD_MICROSECOND",
    "SAMPLING_PERIOD_MILLISECOND",
    "SAMPLING_PERIOD_SECOND",
    "SAMPLING_PERIOD_UNITS",
    "SECOND",
    "TIME_UNITS",
    "Baud",
    "Hertz",
    "Hour",
    "Kilobaud",
    "Kilohertz",
    "KilosamplesPerSecond",
    "Megahertz",
    "MegasamplesPerSecond",
    "Microsecond",
    "MicrosecondSamplingPeriod",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Minute",
    "SamplesPerSecond",
    "Second",
    "SecondSamplingPeriod",
]
