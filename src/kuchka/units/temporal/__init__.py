"""Unit constructors for Time, Frequency, and the acquisition-domain vocabulary.

    from kuchka import Second, Millisecond, Hertz

    period = Millisecond(2)
    rate = Hertz(500)
    reading = Second(1_700_000_000).as_instant()
    window = period.as_sampling_period()

A number of families share this package because they share two physical dimensions and
one recurring theme -- a dimension is not a concept, and a symbol is not a type:

- `time.py` -- `Time` (T^1), the SI-general span: a duration, a timeout, an interval.
- `instant.py` -- `Instant`'s canonical unit.
  `Time.as_instant()` is the point-in-time counterpart to `Time` itself.
  Subtracting two instants gives a `Time`, adding a `Time` to an `Instant` shifts the
  reading.
- `frequency.py` -- `Frequency` (T^-1), the SI-general rate.
- `sampling_period.py` -- `SamplingPeriod`'s canonical unit.
  `Time.as_sampling_period()` reaches it, and it converts to and from `SampleRate`
  directly, since a sample period genuinely is the reciprocal of a sample rate.
- `sample_rate.py` -- `SampleRate`, an acquisition-domain rate sharing `Frequency`'s
  dimension, reciprocal to `SamplingPeriod`.
- `baud_rate.py` -- `BaudRate`, sharing `Frequency`'s dimension without being its
  reciprocal partner.
  Baud counts symbols per second, not bits or cycles.

`SamplingPeriod` and `Instant` share `Time`'s own coordinate units outright.
A millisecond sampling period is measured with the same `MILLISECOND` `Time` already
defines, reached through `.as_sampling_period()` / `.as_instant()`.
`SampleRate` shares its display symbols with `Frequency` the same way, while remaining
its own type.
`BaudRate` gets its own symbol, `Bd`, as that is how it actually appears in the wild.

Each leaf module owns a hand-written ``__all__`` naming exactly what it defines, and
this package's own ``__all__`` is hand-written the same way, keeping
`kuchka.units`'s own ``from kuchka.units.temporal import *`` fully inspectable through
this package's own wildcard imports below.
"""

from __future__ import annotations

from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
from kuchka.units.temporal.instant import *
from kuchka.units.temporal.sample_rate import *
from kuchka.units.temporal.sampling_period import *
from kuchka.units.temporal.time import *

__all__ = [
    "BAUD",
    "BAUD_RATE_UNITS",
    "FREQUENCY_UNITS",
    "GIGAHERTZ",
    "HERTZ",
    "HOUR",
    "INSTANT_SECOND",
    "INSTANT_UNITS",
    "KILOBAUD",
    "KILOHERTZ",
    "KILOSAMPLES_PER_SECOND",
    "MEGAHERTZ",
    "MEGASAMPLES_PER_SECOND",
    "MICROSECOND",
    "MILLISECOND",
    "MINUTE",
    "PETAHERTZ",
    "SAMPLES_PER_SECOND",
    "SAMPLE_RATE_UNITS",
    "SAMPLING_PERIOD_UNITS",
    "SECOND",
    "TERAHERTZ",
    "TIME_UNITS",
    "Baud",
    "Gigahertz",
    "Hertz",
    "Hour",
    "Kilobaud",
    "Kilohertz",
    "KilosamplesPerSecond",
    "Megahertz",
    "MegasamplesPerSecond",
    "Microsecond",
    "Millisecond",
    "Minute",
    "Petahertz",
    "SamplesPerSecond",
    "Second",
    "Terahertz",
]
