"""Unit constructors for SamplingPeriod: the interval between two samples.

    from kuchka import MillisecondSamplingPeriod

    period = MillisecondSamplingPeriod(2)

`SamplingPeriod` is dimensionally identical to `Time` and shares its display symbols,
but is never produced by generic arithmetic.

`SAMPLING_PERIOD_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import TIME
from kuchka.internal import symbols
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import SamplingPeriod
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SAMPLING_PERIOD_MICROSECOND = UnitDef(
    "sampling_period_microsecond",
    f"{symbols.MICRO}s",
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

SamplingPeriod._canonical_unit = SAMPLING_PERIOD_SECOND  # noqa: SLF001 -- this module owns SamplingPeriod's canonical unit


def MicrosecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in microseconds."""
    return SamplingPeriod(
        to_exact(value) * SAMPLING_PERIOD_MICROSECOND.scale,
        SAMPLING_PERIOD_MICROSECOND,
    )


def MillisecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in milliseconds."""
    return SamplingPeriod(
        to_exact(value) * SAMPLING_PERIOD_MILLISECOND.scale,
        SAMPLING_PERIOD_MILLISECOND,
    )


def SecondSamplingPeriod(value: Numeric) -> SamplingPeriod:
    """Construct a SamplingPeriod from a magnitude expressed in seconds."""
    return SamplingPeriod(
        to_exact(value) * SAMPLING_PERIOD_SECOND.scale,
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

__all__ = [
    "SAMPLING_PERIOD_MICROSECOND",
    "SAMPLING_PERIOD_MILLISECOND",
    "SAMPLING_PERIOD_SECOND",
    "SAMPLING_PERIOD_UNITS",
    "MicrosecondSamplingPeriod",
    "MillisecondSamplingPeriod",
    "SecondSamplingPeriod",
]
