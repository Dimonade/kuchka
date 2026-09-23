"""Unit constructors for Time, Frequency, and the acquisition-domain vocabulary.

    from kuchka import Millisecond, Hertz

    period = Millisecond(2)
    rate = Hertz(500)

A number of families share this package, as they all share a recurring theme and two
physical dimensions:

- `time.py` -- `Time` (T^1), the SI-general span: a duration, a timeout, an interval.
- `frequency.py` -- `Frequency` (T^-1), the SI-general rate.
- `sampling_period.py` / `sample_rate.py` -- `SamplingPeriod` and `SampleRate`, an
  acquisition-domain pair sharing `Time`'s and `Frequency`'s dimensions respectively,
  convertible to and from each other directly since a sample period genuinely is the
  reciprocal of a sample rate.
- `baud_rate.py` -- `BaudRate`, sharing `Frequency`'s dimension without being its
  reciprocal partner: baud counts symbols per second, not bits or cycles.

`SamplingPeriod` and `SampleRate` share their display symbols with `Time` and
`Frequency` (both read out in seconds and hertz on a datasheet), even though they are
different Python types.
"""

from __future__ import annotations

from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
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
    "SAMPLING_PERIOD_MICROSECOND",
    "SAMPLING_PERIOD_MILLISECOND",
    "SAMPLING_PERIOD_SECOND",
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
    "MicrosecondSamplingPeriod",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Minute",
    "Petahertz",
    "SamplesPerSecond",
    "Second",
    "SecondSamplingPeriod",
    "Terahertz",
]
