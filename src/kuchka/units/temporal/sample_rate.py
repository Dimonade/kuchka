"""Unit constructors for SampleRate: how often an acquisition system takes a reading.

    from kuchka import SamplesPerSecond, KilosamplesPerSecond

    rate = SamplesPerSecond(500)
    high_speed_rate = KilosamplesPerSecond(420)

`SampleRate` is dimensionally identical to `Frequency` and shares its display symbols,
but is never produced by generic arithmetic.

`SAMPLE_RATE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import SampleRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SAMPLES_PER_SECOND = UnitDef("samples_per_second", "Sa/s", Decimal(1), FREQUENCY)
KILOSAMPLES_PER_SECOND = UnitDef(
    "kilosamples_per_second",
    "kSa/s",
    Decimal(1000),
    FREQUENCY,
)
MEGASAMPLES_PER_SECOND = UnitDef(
    "megasamples_per_second",
    "MSa/s",
    Decimal(1_000_000),
    FREQUENCY,
)

SampleRate._canonical_unit = SAMPLES_PER_SECOND  # noqa: SLF001 -- this module owns SampleRate's canonical unit


def SamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in samples per second."""
    return SampleRate(to_exact(value) * SAMPLES_PER_SECOND.scale, SAMPLES_PER_SECOND)


def KilosamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in kilosamples per second."""
    return SampleRate(
        to_exact(value) * KILOSAMPLES_PER_SECOND.scale,
        KILOSAMPLES_PER_SECOND,
    )


def MegasamplesPerSecond(value: Numeric) -> SampleRate:
    """Construct a SampleRate from a magnitude expressed in megasamples per second."""
    return SampleRate(
        to_exact(value) * MEGASAMPLES_PER_SECOND.scale,
        MEGASAMPLES_PER_SECOND,
    )


SAMPLE_RATE_UNITS: Mapping[str, Callable[[Numeric], SampleRate]] = MappingProxyType(
    {
        SAMPLES_PER_SECOND.symbol: SamplesPerSecond,
        KILOSAMPLES_PER_SECOND.symbol: KilosamplesPerSecond,
        MEGASAMPLES_PER_SECOND.symbol: MegasamplesPerSecond,
    }
)

__all__ = [
    "KILOSAMPLES_PER_SECOND",
    "MEGASAMPLES_PER_SECOND",
    "SAMPLES_PER_SECOND",
    "SAMPLE_RATE_UNITS",
    "KilosamplesPerSecond",
    "MegasamplesPerSecond",
    "SamplesPerSecond",
]
