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

MICROSECOND = UnitDef("microsecond", "\u00b5s", Decimal("0.000001"), TIME)
MILLISECOND = UnitDef("millisecond", "ms", Decimal("0.001"), TIME)
SECOND = UnitDef("second", "s", Decimal(1), TIME)

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


TIME_UNITS: Mapping[str, Callable[[Numeric], Time]] = MappingProxyType({
    "us": Microsecond,
    "ms": Millisecond,
    "s": Second,
})


# Frequency

HERTZ = UnitDef("hertz", "Hz", Decimal(1), FREQUENCY)
KILOHERTZ = UnitDef("kilohertz", "kHz", Decimal(1000), FREQUENCY)
MEGAHERTZ = UnitDef("megahertz", "MHz", Decimal(1_000_000), FREQUENCY)

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


FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = MappingProxyType({
    "Hz": Hertz,
    "kHz": Kilohertz,
    "MHz": Megahertz,
})


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
    MappingProxyType({
        "us": MicrosecondSamplingPeriod,
        "ms": MillisecondSamplingPeriod,
        "s": SecondSamplingPeriod,
    })
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


SAMPLE_RATE_UNITS: Mapping[str, Callable[[Numeric], SampleRate]] = MappingProxyType({
    "Sa/s": SamplesPerSecond,
    "kSa/s": KilosamplesPerSecond,
    "MSa/s": MegasamplesPerSecond,
})


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


BAUD_RATE_UNITS: Mapping[str, Callable[[Numeric], BaudRate]] = MappingProxyType({
    "Bd": Baud,
    "kBd": Kilobaud,
})
