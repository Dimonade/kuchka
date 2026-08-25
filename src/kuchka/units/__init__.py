"""Engineer-facing unit constructors, one module per physical dimension.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current

Each quantity's canonical unit (the one arithmetic results come back in,
e.g. ``Voltage * Current`` yields a result expressed in ``Watt``) is
assigned onto the corresponding domain class from ``kuchka.quantities``
at the bottom of the module that owns that dimension.
"""

from __future__ import annotations

from kuchka.units.current import AMPERE
from kuchka.units.current import Ampere
from kuchka.units.current import KILOAMPERE
from kuchka.units.current import Kiloampere
from kuchka.units.current import MICROAMPERE
from kuchka.units.current import Microampere
from kuchka.units.current import MILLIAMPERE
from kuchka.units.current import Milliampere
from kuchka.units.power import KILOWATT
from kuchka.units.power import Kilowatt
from kuchka.units.power import MILLIWATT
from kuchka.units.power import Milliwatt
from kuchka.units.power import WATT
from kuchka.units.power import Watt
from kuchka.units.resistance import KILOOHM
from kuchka.units.resistance import Kiloohm
from kuchka.units.resistance import MEGAOHM
from kuchka.units.resistance import Megaohm
from kuchka.units.resistance import MILLIOHM
from kuchka.units.resistance import Milliohm
from kuchka.units.resistance import OHM
from kuchka.units.resistance import Ohm
from kuchka.units.temporal import BAUD
from kuchka.units.temporal import Baud
from kuchka.units.temporal import HERTZ
from kuchka.units.temporal import Hertz
from kuchka.units.temporal import KILOBAUD
from kuchka.units.temporal import Kilobaud
from kuchka.units.temporal import KILOHERTZ
from kuchka.units.temporal import Kilohertz
from kuchka.units.temporal import KILOSAMPLE_PER_SECOND
from kuchka.units.temporal import KilosamplesPerSecond
from kuchka.units.temporal import MEGAHERTZ
from kuchka.units.temporal import Megahertz
from kuchka.units.temporal import MEGASAMPLE_PER_SECOND
from kuchka.units.temporal import MegasamplesPerSecond
from kuchka.units.temporal import MICROSECOND
from kuchka.units.temporal import Microsecond
from kuchka.units.temporal import MicrosecondSamplingPeriod
from kuchka.units.temporal import MILLISECOND
from kuchka.units.temporal import Millisecond
from kuchka.units.temporal import MillisecondSamplingPeriod
from kuchka.units.temporal import SAMPLE_PER_SECOND
from kuchka.units.temporal import SamplesPerSecond
from kuchka.units.temporal import SAMPLING_PERIOD_MICROSECOND
from kuchka.units.temporal import SAMPLING_PERIOD_MILLISECOND
from kuchka.units.temporal import SAMPLING_PERIOD_SECOND
from kuchka.units.temporal import SECOND
from kuchka.units.temporal import Second
from kuchka.units.temporal import SecondSamplingPeriod
from kuchka.units.voltage import KILOVOLT
from kuchka.units.voltage import Kilovolt
from kuchka.units.voltage import MICROVOLT
from kuchka.units.voltage import Microvolt
from kuchka.units.voltage import MILLIVOLT
from kuchka.units.voltage import Millivolt
from kuchka.units.voltage import VOLT
from kuchka.units.voltage import Volt

__all__: list[str] = [
    "AMPERE",
    "BAUD",
    "HERTZ",
    "KILOAMPERE",
    "KILOBAUD",
    "KILOHERTZ",
    "KILOOHM",
    "KILOSAMPLE_PER_SECOND",
    "KILOVOLT",
    "KILOWATT",
    "MEGAHERTZ",
    "MEGAOHM",
    "MEGASAMPLE_PER_SECOND",
    "MICROAMPERE",
    "MICROSECOND",
    "MICROVOLT",
    "MILLIAMPERE",
    "MILLIOHM",
    "MILLISECOND",
    "MILLIVOLT",
    "MILLIWATT",
    "OHM",
    "SAMPLE_PER_SECOND",
    "SAMPLING_PERIOD_MICROSECOND",
    "SAMPLING_PERIOD_MILLISECOND",
    "SAMPLING_PERIOD_SECOND",
    "SECOND",
    "VOLT",
    "WATT",
    "Ampere",
    "Baud",
    "Hertz",
    "Kiloampere",
    "Kilobaud",
    "Kilohertz",
    "Kiloohm",
    "KilosamplesPerSecond",
    "Kilovolt",
    "Kilowatt",
    "Megahertz",
    "Megaohm",
    "MegasamplesPerSecond",
    "Microampere",
    "Microsecond",
    "MicrosecondSamplingPeriod",
    "Microvolt",
    "Milliampere",
    "Milliohm",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Millivolt",
    "Milliwatt",
    "Ohm",
    "SamplesPerSecond",
    "Second",
    "SecondSamplingPeriod",
    "Volt",
    "Watt",
]
