"""Unit constructors for time, frequency, and data-acquisition quantities.

The module brings together temporal coordinates, durations, periodic phenomena, and
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
Telemetry systems record events against a common timeline.
Mission control sends a command at mission elapsed time 84,500 seconds and receives its
acknowledgement 37 seconds later.
The acknowledgement also arrives before the five-minute response deadline:

>>> from kuchka import Second
>>> command_sent = Second(84_500).to_instant()
>>> acknowledgement = Second(84_537).to_instant()
>>> acknowledgement - command_sent
37 s
>>> acknowledgement < command_sent + Second(300)
True

Astronomical observations often involve counting periodic events over extended
intervals.
A pulsar emitting 30 radio pulses per second produces 18,000 pulses during a
ten-minute observation:

>>> from kuchka import Hertz
>>> Hertz(30) * Second(600)
Fraction(18000, 1)

The same relationship applies to rotating machinery, oscillators, and periodic
electrical signals: frequency multiplied by an observation interval gives the number of
cycles occurring during that interval.

Data acquisition introduces two reciprocal quantities.
An ECG recorder sampling every 2 milliseconds acquires 500 samples per second:

>>> from kuchka import Millisecond
>>> sampling_period = Millisecond(2).to_sampling_period()
>>> sample_rate = 1 / sampling_period
>>> sample_rate
500 Sa/s

Consider a 50 Hz component caused by mains interference in the recording.
The acquisition system collects ten samples during each complete interference cycle:

>>> sample_rate.to_frequency() / Hertz(50)
10 1

The signal frequency describes the phenomenon being measured.
The sample rate describes how frequently the acquisition system observes it.
Their ratio gives the number of samples per signal cycle.

Digital communication introduces another rate with dimension T⁻¹.
A telemetry device transmits a 1,152-byte data block over a UART connection configured
for 8-N-1 framing.
Each byte occupies ten symbol periods: one start bit, eight data bits, and one stop
bit.

At 9,600 Bd, the transmission takes 1.2 seconds.
Switching to a 115,200 Bd connection reduces the transmission time by a factor of
twelve:

>>> from kuchka import Baud
>>> slow_link = Baud(9_600)
>>> fast_link = Baud(115_200)
>>> Second(1.2) * (slow_link / fast_link)
0.1 s

The comparison uses the dimensionless ratio of two baud rates to scale a known
transmission duration.
It does not treat baud rate as an ordinary frequency or multiply it directly by a time
interval.

Notes
-----
`Instant` and `SamplingPeriod` share the underlying time units defined by `Time`.
Conversions through `.to_instant()` and `.to_sampling_period()` change the semantic
quantity type without introducing competing unit definitions.

`Instant` represents a point on a timeline, not a duration or an implicit Unix
timestamp.
Its origin depends on the timeline established by the application.

`Frequency`, `SampleRate`, and `BaudRate` all have dimension T⁻¹, but represent
different quantities:

- `Frequency` counts cycles or recurring events.
- `SampleRate` counts acquired samples.
- `BaudRate` counts transmitted symbols.

`SamplingPeriod` is reciprocal to `SampleRate`.
`BaudRate` is deliberately not treated as interchangeable with `Frequency`.
It does not combine directly with `Time` to produce a dimensionless count.

`SampleRate` shares its display symbols with `Frequency`, including Hz, while remaining
a distinct quantity type.
`BaudRate` has its own symbol, Bd.
A shared physical dimension or display symbol does not establish semantic equivalence.

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
