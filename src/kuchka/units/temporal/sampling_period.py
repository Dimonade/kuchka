"""Sampling period units: the time units, read as a sampling period.

    from kuchka import Millisecond, Second

    period = Millisecond(2).to_sampling_period()
    rate = 1 / period               # -> SampleRate(500)
    round_trip = 1 / rate           # -> SamplingPeriod, back to 2 ms

A sampling period is measured in seconds the same way a duration is.
`Time`'s own `SECOND`, `MICROSECOND`, and `MILLISECOND` already say that, so
`SamplingPeriod` reuses them as its own canonical unit avoiding minting a lookalike.
`Time.to_sampling_period()` is what turns a `Time` value into the distinct
`SamplingPeriod` type, at whichever prefix the value already carries.
`Minute(1).to_sampling_period()` and `Second(60).to_sampling_period()` produce the
same reading.

`SAMPLING_PERIOD_UNITS` maps each symbol to a callable that reads a Time value as a
SamplingPeriod, for boundary code that reads a unit as a string from outside the
application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities import SamplingPeriod
from kuchka.units.temporal.time import SECOND
from kuchka.units.temporal.time import TIME_UNITS

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities import Time

SamplingPeriod._canonical_unit = SECOND  # noqa: SLF001 -- reused from Time's own SECOND


def _via_time(
    constructor: Callable[[Numeric], Time],
) -> Callable[[Numeric], SamplingPeriod]:
    """Wrap a `Time` constructor so it reads its result as a `SamplingPeriod`."""

    def read_as_sampling_period(value: Numeric) -> SamplingPeriod:
        return constructor(value).to_sampling_period()

    return read_as_sampling_period


SAMPLING_PERIOD_UNITS: Mapping[str, Callable[[Numeric], SamplingPeriod]] = (
    TIME_UNITS.map("SAMPLING_PERIOD_UNITS", _via_time)
)

__all__ = ["SAMPLING_PERIOD_UNITS"]
