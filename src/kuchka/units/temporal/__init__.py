"""Unit constructors for time, frequency, and data-acquisition quantities.

The module covers temporal coordinates, durations, periodic phenomena, and
acquisition-domain rates.
Several quantities share physical dimensions and unit scales without representing
interchangeable concepts:

- `Time` (T¹) represents a duration, timeout, or elapsed interval.
- `Instant` represents a point on a timeline. Subtracting two instants gives a
  `Time`; adding a `Time` to an `Instant` shifts the point in time.
- `Frequency` (T⁻¹) measures cycles or recurring events per second.
- `SamplingPeriod` represents the interval between successive samples.
- `SampleRate` measures samples acquired per second and is reciprocal to
  `SamplingPeriod`.
- `BaudRate` measures symbols transmitted per second, not necessarily bits or
  cycles.

Examples
--------
A spacecraft's mission clock records events relative to a mission epoch.
Mission control receives an acknowledgement three seconds after sending a command.
A five-second response timeout therefore has two seconds remaining:

>>> from kuchka import Second
>>> command_sent = Second(84_500).to_instant()
>>> acknowledgement = Second(84_503).to_instant()
>>> acknowledgement - command_sent
3 s
>>> command_sent + Second(5) - acknowledgement
2 s

The same distinction is useful in distributed systems, medical monitoring, and
industrial automation: an event timestamp identifies when something happened, whereas a
timeout describes how long an operation may take.

Astronomical observations often involve counting periodic events over long intervals.
A pulsar producing 30 radio pulses per second emits 18,000 pulses during a ten-minute
observation:

>>> from kuchka import Hertz, Second
>>> Hertz(30) * Second(10 * 60)
18000

Data acquisition introduces two reciprocal quantities.
An ECG recorder sampling every 2 milliseconds acquires 500 samples per second:

>>> from kuchka import Millisecond, SamplesPerSecond
>>> sampling_period = Millisecond(2).to_sampling_period()
>>> 1 / sampling_period == SamplesPerSecond(500)
True

The distinction between signal frequency and sample rate becomes particularly important
when examining mains interference in medical recordings.
A 50 Hz interference component completes one cycle every 20 milliseconds.
At a sampling period of 2 milliseconds, the recorder acquires ten sample intervals per
cycle:

>>> Millisecond(20).to_sampling_period() / sampling_period
10

The signal frequency describes the phenomenon being measured.
The sample rate describes the acquisition system observing it.
Their ratio expresses how many samples are collected during each signal cycle.

Digital communication introduces another rate with dimension T⁻¹.
A binary UART connection operating at 115200 Bd with 8-N-1 framing uses ten symbol
periods per payload byte: one start bit, eight data bits, and one stop bit.
Under continuous transmission, its theoretical payload throughput is:

>>> from kuchka import Baud
>>> Baud(115_200) * Second(1) / 10
11520

That is 11,520 bytes per second, excluding idle periods and higher-level protocol
overhead.
This calculation assumes binary signalling, where each symbol represents one bit.
With other modulation schemes, the relationship between symbol rate and bit rate can be
different.

Notes
-----
`Time.to_instant()` and `Time.to_sampling_period()` reinterpret a time measurement in
different semantic domains.
Both use the underlying time units already defined by `Time`; they do not introduce
competing unit scales.

An `Instant` has no implicit UTC or Unix epoch.
Its origin belongs to the timeline defined by the application.
Subtracting two instants produces a `Time`, while adding or subtracting a `Time` shifts
an instant.

`SamplingPeriod` and `SampleRate` form a genuine reciprocal pair:
`1 / sampling_period` produces a `SampleRate`, and `1 / sample_rate` produces a
`SamplingPeriod`.

`Frequency`, `SampleRate`, and `BaudRate` all have dimension T⁻¹, but their meanings
are different.
`Frequency` counts cycles or recurring events, `SampleRate` counts acquired samples,
and `BaudRate` counts transmitted symbols.

`SampleRate` shares its display symbols with `Frequency`, including Hz, while remaining
a distinct quantity type.
`BaudRate` has its own symbol, Bd.
A shared dimension or display symbol does not establish semantic equivalence.

See Also
--------
~kuchka.quantities.Time
Quantity type representing a duration or time interval.

~kuchka.quantities.Instant
Quantity type representing a point in time.

~kuchka.quantities.Frequency
Quantity type representing cycles or recurring events per unit time.

~kuchka.quantities.SamplingPeriod
Quantity type representing the interval between successive samples.

~kuchka.quantities.SampleRate
Quantity type representing samples acquired per unit time.

~kuchka.quantities.BaudRate
Quantity type representing symbols transmitted per unit time.
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
