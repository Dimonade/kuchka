"""Unit constructors for Frequency: hertz and SI-prefixed multiples.

    from kuchka import Hertz, Megahertz

    heart_rate = Hertz(1.2)
    carrier = Megahertz(915)

`Hertz` is the canonical, SI-coherent unit.

The frequency scale spans several very different engineering and scientific domains:

* millihertz describe slow physiological rhythms, structural oscillations,
  and long-period control systems;
* hertz describe everyday mechanical motion, sound, biological rhythms, and
  low-frequency instrumentation;
* kilohertz cover ultrasound, switching converters, audio, and instrumentation;
* megahertz are common in radio, medical imaging, and embedded electronics;
* gigahertz dominate microwave links, radar, processors, and wireless systems;
* terahertz describe submillimetre and far-infrared phenomena;
* petahertz reach the timescale of electronic transitions and ultrafast optics.

Examples
--------
Frequency values carry their physical unit through arithmetic.
A diagnostic ultrasound system uses a 5 MHz carrier, with a modeled Doppler offset of
250 kHz:

>>> carrier = Megahertz(5)
>>> doppler_shift = Kilohertz(250)
>>> received = carrier + doppler_shift
>>> received
5.25 MHz

The same frequency difference can be expressed on either scale:

>>> doppler_shift.to(MEGAHERTZ)
0.25 MHz

Frequency and period are reciprocal quantities.
A 2 MHz oscillator completes one cycle every 500 ns:

>>> from kuchka.units import NANOSECOND
>>> oscillator = Megahertz(2)
>>> period = 1 / oscillator
>>> period.to(NANOSECOND)
500 ns

Wireless systems commonly work across the gigahertz range.
A 2.4 GHz radio carrier is shifted upward by a 5 MHz offset during a frequency-hopping
sequence:

>>> carrier = Gigahertz(2.4)
>>> offset = Megahertz(5)
>>> hopped = carrier + offset
>>> hopped
2.405 GHz

The hop is still exactly 5 MHz:

>>> from kuchka.units import MEGAHERTZ
>>> (hopped - carrier).to(MEGAHERTZ)
5 MHz

An ultrasound transducer operating at 5 MHz and a 2 MHz imaging probe differ by exactly
3 MHz:

>>> diagnostic = Megahertz(5)
>>> therapeutic = Megahertz(2)
>>> diagnostic - therapeutic
3 MHz

A radio telescope can distinguish a 1.400 GHz hydrogen-line signal from a nearby
1.3998 GHz feature by working directly with the frequency difference:

>>> from kuchka.units import MEGAHERTZ
>>> hydrogen_line = Gigahertz(1.4)
>>> spectral_feature = Megahertz(1399.8)
>>> (hydrogen_line - spectral_feature).to(MEGAHERTZ)
0.2 MHz

Notes
-----
Frequency measures the number of complete cycles or repetitions occurring per unit
time.

One hertz is exactly:

``1 Hz = 1/s``

Frequency is the reciprocal of period.
For example, a 100 Hz signal has a period of exactly 0.01 seconds:

>>> signal = Hertz(100)
>>> 1 / signal
0.01 s

`FREQUENCY_UNITS` maps unit symbols such as ``"Hz"``, ``"kHz"``, ``"MHz"``,
``"GHz"``, and ``"THz"`` to their constructors.
It is intended for boundary code that receives units from configuration files,
protocols, or other external sources.

See Also
--------
~kuchka.quantities.Frequency
    Quantity type representing frequency.
~kuchka.quantities.Time
    Time intervals and periods, which are reciprocal to frequency.
~kuchka.quantities.SampleRate
    Sampling rate, which has the same physical dimension but a distinct meaning.
~kuchka.quantities.BaudRate
    Symbol rate, which has the same physical dimension but a distinct meaning.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Frequency

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HERTZ_NAME = "hertz"
HERTZ_SYMBOL = "Hz"

HERTZ = prefixed_unit(prefixes.UNIT, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
KILOHERTZ = prefixed_unit(prefixes.KILO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MEGAHERTZ = prefixed_unit(prefixes.MEGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
GIGAHERTZ = prefixed_unit(prefixes.GIGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
TERAHERTZ = prefixed_unit(prefixes.TERA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
PETAHERTZ = prefixed_unit(prefixes.PETA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)


Frequency._canonical_unit = HERTZ  # noqa: SLF001 -- this module owns Frequency's canonical unit


def Hertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in hertz."""
    return Frequency(to_exact(value) * HERTZ.scale, HERTZ)


def Kilohertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in kilohertz."""
    return Frequency(to_exact(value) * KILOHERTZ.scale, KILOHERTZ)


def Megahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in megahertz."""
    return Frequency(to_exact(value) * MEGAHERTZ.scale, MEGAHERTZ)


def Gigahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in gigahertz."""
    return Frequency(to_exact(value) * GIGAHERTZ.scale, GIGAHERTZ)


def Terahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in terahertz."""
    return Frequency(to_exact(value) * TERAHERTZ.scale, TERAHERTZ)


def Petahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in petahertz."""
    return Frequency(to_exact(value) * PETAHERTZ.scale, PETAHERTZ)


FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = unit_table(
    "FREQUENCY_UNITS",
    {
        HERTZ: Hertz,
        KILOHERTZ: Kilohertz,
        MEGAHERTZ: Megahertz,
        GIGAHERTZ: Gigahertz,
        TERAHERTZ: Terahertz,
        PETAHERTZ: Petahertz,
    },
)

__all__ = [
    "FREQUENCY_UNITS",
    "GIGAHERTZ",
    "HERTZ",
    "KILOHERTZ",
    "MEGAHERTZ",
    "PETAHERTZ",
    "TERAHERTZ",
    "Gigahertz",
    "Hertz",
    "Kilohertz",
    "Megahertz",
    "Petahertz",
    "Terahertz",
]
