"""Frequency constructors: the hertz, from nanohertz to petahertz.

    from kuchka import Hertz
    from kuchka import Megahertz

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


The millisecond pulsar PSR J1748-2446ad rotates at approximately 716.358 Hz.
At a steady spin rate, a 15-minute observation spans more than 640,000 rotations, while
each rotation takes less than 1.4 milliseconds.

>>> spin_rate = Hertz(716.358)
>>> spin_rate.to(HERTZ)
716.358 Hz
>>> round(716.358 * 15 * 60)
644722
>>> f"{1000 / 716.358:.4f} ms"
'1.3960 ms'


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

Hessels et al., A Radio Pulsar Spinning at 716 Hertz, NRAO
https://www.nrao.edu/pr/2006/mspulsar/

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

    from kuchka.quantities import UnitDef

HERTZ_NAME = "hertz"
HERTZ_SYMBOL = "Hz"

NANOHERTZ = prefixed_unit(prefixes.NANO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MICROHERTZ = prefixed_unit(prefixes.MICRO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MILLIHERTZ = prefixed_unit(prefixes.MILLI, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
HERTZ = prefixed_unit(prefixes.UNIT, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
KILOHERTZ = prefixed_unit(prefixes.KILO, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
MEGAHERTZ = prefixed_unit(prefixes.MEGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
GIGAHERTZ = prefixed_unit(prefixes.GIGA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
TERAHERTZ = prefixed_unit(prefixes.TERA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)
PETAHERTZ = prefixed_unit(prefixes.PETA, HERTZ_NAME, HERTZ_SYMBOL, FREQUENCY)


Frequency._canonical_unit = HERTZ  # noqa: SLF001 -- this module owns Frequency's canonical unit


def Nanohertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in nanohertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in nanohertz.

    Returns
    -------
    Frequency
        Frequency represented in nanohertz.

    Examples
    --------
    A pulsar timing array can probe extraordinarily slow gravitational-wave
    oscillations in the nanohertz range:

    >>> gravitational_wave = Nanohertz(30)
    >>> gravitational_wave
    30 nHz

    A long-period oscillation at 20 nHz repeats once every 50 million seconds:

    >>> oscillation = Nanohertz(20)
    >>> 1 / oscillation
    50000000 s

    """
    return Frequency(to_exact(value) * NANOHERTZ.scale, NANOHERTZ)


def Microhertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in microhertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in microhertz.

    Returns
    -------
    Frequency
        Frequency represented in microhertz.

    Examples
    --------
    A mechanical structure resonating at 250 microhertz completes one
    oscillation every 4000 seconds:

    >>> resonance = Microhertz(250)
    >>> 1 / resonance
    4000 s


    """
    return Frequency(to_exact(value) * MICROHERTZ.scale, MICROHERTZ)


def Millihertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in millihertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in millihertz.

    Returns
    -------
    Frequency
        Frequency represented in millihertz.

    Examples
    --------
    A respiration monitor observes 18 breaths per minute:

    >>> respiratory_rate = Millihertz(300)
    >>> respiratory_rate.to(HERTZ)
    0.3 Hz

    """
    return Frequency(to_exact(value) * MILLIHERTZ.scale, MILLIHERTZ)


def Hertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in hertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in hertz.

    Returns
    -------
    Frequency
        Frequency represented in hertz.

    Examples
    --------
    A cardiac monitor records 72 beats per minute:

    >>> heart_rate = Hertz(1.2)
    >>> heart_rate
    1.2 Hz

    The corresponding period is exactly 5/6 of a second:

    >>> 1 / heart_rate
    0.8333333333333333333333333333 s

    """
    return Frequency(to_exact(value) * HERTZ.scale, HERTZ)


def Kilohertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in kilohertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in kilohertz.

    Returns
    -------
    Frequency
        Frequency represented in kilohertz.

    Examples
    --------
    A switched-mode power converter operates at 250 kHz.
    Increasing the switching frequency by 50 kHz gives a 300 kHz control regime:

    >>> switching = Kilohertz(250)
    >>> increase = Kilohertz(50)
    >>> switching + increase
    300 kHz

    """
    return Frequency(to_exact(value) * KILOHERTZ.scale, KILOHERTZ)


def Megahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in megahertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in megahertz.

    Returns
    -------
    Frequency
        Frequency represented in megahertz.

    Examples
    --------
    A medical ultrasound probe operates at 5 MHz.
    Its third harmonic therefore occurs at 15 MHz:

    >>> fundamental = Megahertz(5)
    >>> third_harmonic = fundamental * 3
    >>> third_harmonic
    15 MHz


    """
    return Frequency(to_exact(value) * MEGAHERTZ.scale, MEGAHERTZ)


def Gigahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in gigahertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in gigahertz.

    Returns
    -------
    Frequency
        Frequency represented in gigahertz.

    Examples
    --------
    A 2.4 GHz radio link and a 915 MHz telemetry beacon occupy distinct frequency
    bands:

    >>> radio = Gigahertz(2.4)
    >>> telemetry = Megahertz(915)
    >>> radio - telemetry
    1.485 GHz

    """
    return Frequency(to_exact(value) * GIGAHERTZ.scale, GIGAHERTZ)


def Terahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in terahertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in terahertz.

    Returns
    -------
    Frequency
        Frequency represented in terahertz.

    Examples
    --------
    A terahertz imaging system sweeps between 0.8 THz and 1.2 THz:

    >>> lower = Terahertz(0.8)
    >>> upper = Terahertz(1.2)
    >>> upper - lower
    0.4 THz

    """
    return Frequency(to_exact(value) * TERAHERTZ.scale, TERAHERTZ)


def Petahertz(value: Numeric) -> Frequency:
    """Construct a Frequency from a magnitude expressed in petahertz.

    Parameters
    ----------
    value : Numeric
        Frequency magnitude in petahertz.

    Returns
    -------
    Frequency
        Frequency represented in petahertz.

    Examples
    --------
    An ultrafast optical system is described at a 2.5 PHz carrier frequency.
    Doubling the carrier reaches the petahertz-scale ultraviolet regime:

    >>> carrier = Petahertz(2.5)
    >>> carrier * 2
    5 PHz

    """
    return Frequency(to_exact(value) * PETAHERTZ.scale, PETAHERTZ)


FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = unit_table(
    "FREQUENCY_UNITS",
    {
        NANOHERTZ: Nanohertz,
        MICROHERTZ: Microhertz,
        MILLIHERTZ: Millihertz,
        HERTZ: Hertz,
        KILOHERTZ: Kilohertz,
        MEGAHERTZ: Megahertz,
        GIGAHERTZ: Gigahertz,
        TERAHERTZ: Terahertz,
        PETAHERTZ: Petahertz,
    },
)

FREQUENCY_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        NANOHERTZ,
        MICROHERTZ,
        MILLIHERTZ,
        HERTZ,
        KILOHERTZ,
        MEGAHERTZ,
        GIGAHERTZ,
        TERAHERTZ,
        PETAHERTZ,
    ),
)
"""The units `auto_scale` moves a frequency along, smallest first."""

__all__ = [
    "FREQUENCY_LADDERS",
    "FREQUENCY_UNITS",
    "GIGAHERTZ",
    "HERTZ",
    "KILOHERTZ",
    "MEGAHERTZ",
    "MICROHERTZ",
    "MILLIHERTZ",
    "NANOHERTZ",
    "PETAHERTZ",
    "TERAHERTZ",
    "Gigahertz",
    "Hertz",
    "Kilohertz",
    "Megahertz",
    "Microhertz",
    "Millihertz",
    "Nanohertz",
    "Petahertz",
    "Terahertz",
]
