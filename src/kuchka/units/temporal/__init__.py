"""Unit constructors for Time, Frequency, and the acquisition-domain vocabulary.

    from kuchka import Second, Millisecond, Hertz

    period = Millisecond(2)
    rate = Hertz(500)
    reading = Second(1_700_000_000).to_instant()
    window = period.to_sampling_period()

A number of families share this package because they share two physical dimensions and
one recurring theme -- a dimension is not a concept, and a symbol is not a type:

- `time.py` -- `Time` (T¹), the SI-general span: a duration, a timeout, an interval.
- `instant.py` -- `Instant`'s canonical unit.
  `Time.to_instant()` is the point-in-time counterpart to `Time` itself.
  Subtracting two instants gives a `Time`, adding a `Time` to an `Instant` shifts the
  reading.
- `frequency.py` -- `Frequency` (T⁻¹), the SI-general rate.
- `sampling_period.py` -- `SamplingPeriod`'s canonical unit.
  `Time.to_sampling_period()` reaches it, and it converts to and from `SampleRate`
  directly, since a sample period genuinely is the reciprocal of a sample rate.
- `sample_rate.py` -- `SampleRate`, an acquisition-domain rate sharing `Frequency`'s
  dimension, reciprocal to `SamplingPeriod`.
- `baud_rate.py` -- `BaudRate`, sharing `Frequency`'s dimension without being its
  reciprocal partner.
  Baud counts symbols per second, not bits or cycles.

`SamplingPeriod` and `Instant` share `Time`'s own coordinate units outright.
A millisecond sampling period is measured with the same `MILLISECOND` `Time` already
defines, reached through `.to_sampling_period()` / `.to_instant()`.
`SampleRate` shares its display symbols with `Frequency` the same way, while remaining
its own type.
`BaudRate` gets its own symbol, `Bd`, as that is how it actually appears in the wild.
"""

from __future__ import annotations

from kuchka.units.temporal import baud_rate
from kuchka.units.temporal import frequency
from kuchka.units.temporal import instant
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import sampling_period
from kuchka.units.temporal import time
from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
from kuchka.units.temporal.instant import *
from kuchka.units.temporal.sample_rate import *
from kuchka.units.temporal.sampling_period import *
from kuchka.units.temporal.time import *

__all__: list[str] = []
__all__ += baud_rate.__all__
__all__ += frequency.__all__
__all__ += instant.__all__
__all__ += sample_rate.__all__
__all__ += sampling_period.__all__
__all__ += time.__all__
