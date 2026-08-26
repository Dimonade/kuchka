"""kuchka -- a small pile of physically-typed units for engineering code.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current   # -> Power, computed and typed automatically

Everything below is the entire intended public surface.
Internal modules (``quantities``, ``dimensions``, ``numeric``, ...) are implementation
details and are not part of the supported API.
"""

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import MeasurementError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.quantities import BaudRate
from kuchka.quantities import ConvertibleToFrequency
from kuchka.quantities import Current
from kuchka.quantities import Frequency
from kuchka.quantities import Length
from kuchka.quantities import Power
from kuchka.quantities import Resistance
from kuchka.quantities import SampleRate
from kuchka.quantities import SamplingPeriod
from kuchka.quantities import TemperatureDelta
from kuchka.quantities import Time
from kuchka.quantities import Voltage
from kuchka.temperature import Celsius
from kuchka.temperature import DeltaCelsius
from kuchka.temperature import DeltaKelvin
from kuchka.temperature import Kelvin
from kuchka.temperature import Temperature
from kuchka.units import Ampere
from kuchka.units import Baud
from kuchka.units import Hertz
from kuchka.units import Inch
from kuchka.units import Kiloampere
from kuchka.units import Kilobaud
from kuchka.units import Kilohertz
from kuchka.units import Kilometer
from kuchka.units import Kiloohm
from kuchka.units import KilosamplesPerSecond
from kuchka.units import Kilovolt
from kuchka.units import Kilowatt
from kuchka.units import Megahertz
from kuchka.units import Megaohm
from kuchka.units import MegasamplesPerSecond
from kuchka.units import Meter
from kuchka.units import Microampere
from kuchka.units import Micrometer
from kuchka.units import Microsecond
from kuchka.units import MicrosecondSamplingPeriod
from kuchka.units import Microvolt
from kuchka.units import Milliampere
from kuchka.units import Millimeter
from kuchka.units import Millisecond
from kuchka.units import MillisecondSamplingPeriod
from kuchka.units import Milliohm
from kuchka.units import Millivolt
from kuchka.units import Milliwatt
from kuchka.units import Nanometer
from kuchka.units import Ohm
from kuchka.units import SamplesPerSecond
from kuchka.units import Second
from kuchka.units import SecondSamplingPeriod
from kuchka.units import Volt
from kuchka.units import Watt

__all__: list[str] = [
    "Ampere",
    "Baud",
    "BaudRate",
    "Celsius",
    "ConvertibleToFrequency",
    "Current",
    "DeltaCelsius",
    "DeltaKelvin",
    "Frequency",
    "Hertz",
    "Inch",
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "Kelvin",
    "Kiloampere",
    "Kilobaud",
    "Kilohertz",
    "Kilometer",
    "Kiloohm",
    "KilosamplesPerSecond",
    "Kilovolt",
    "Kilowatt",
    "Length",
    "MeasurementError",
    "Megahertz",
    "Megaohm",
    "MegasamplesPerSecond",
    "Meter",
    "Microampere",
    "Micrometer",
    "Microsecond",
    "MicrosecondSamplingPeriod",
    "Microvolt",
    "Milliampere",
    "Millimeter",
    "Milliohm",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Millivolt",
    "Milliwatt",
    "Nanometer",
    "Ohm",
    "PlannedDimensionError",
    "Power",
    "Resistance",
    "SampleRate",
    "SamplesPerSecond",
    "SamplingPeriod",
    "Second",
    "SecondSamplingPeriod",
    "Temperature",
    "TemperatureDelta",
    "Time",
    "UnrepresentableDimensionError",
    "Volt",
    "Voltage",
    "Watt",
]
