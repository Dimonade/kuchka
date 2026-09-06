"""kuchka -- a small pile of physically-typed units for engineering code.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current   # -> Power, computed and typed automatically

Everything below is the entire intended public surface.
Internal modules (``quantities``, ``dimensions``, ``numeric``, ...) are implementation
details and are not part of the supported API.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from kuchka.constants import ELECTRON_MASS
from kuchka.constants import ELEMENTARY_CHARGE
from kuchka.constants import NEUTRON_MASS
from kuchka.constants import PROTON_MASS
from kuchka.constants import SPEED_OF_LIGHT
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import MeasurementError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.quantities import AmountOfSubstance
from kuchka.quantities import BaudRate
from kuchka.quantities import Charge
from kuchka.quantities import ConvertibleToFrequency
from kuchka.quantities import Current
from kuchka.quantities import Energy
from kuchka.quantities import Frequency
from kuchka.quantities import Length
from kuchka.quantities import LuminousIntensity
from kuchka.quantities import Mass
from kuchka.quantities import Power
from kuchka.quantities import Proportion
from kuchka.quantities import Resistance
from kuchka.quantities import SampleRate
from kuchka.quantities import SamplingPeriod
from kuchka.quantities import Temperature
from kuchka.quantities import TemperatureDelta
from kuchka.quantities import Velocity
from kuchka.quantities import Time
from kuchka.quantities import Voltage
from kuchka.quantities.thermal import Celsius
from kuchka.quantities.thermal import DeltaCelsius
from kuchka.quantities.thermal import DeltaKelvin
from kuchka.quantities.thermal import Kelvin
from kuchka.units import Ampere
from kuchka.units import COULOMB
from kuchka.units import Coulomb
from kuchka.units import ENERGY_UNITS
from kuchka.units import JOULE
from kuchka.units import Joule
from kuchka.units import KILOJOULE
from kuchka.units import KILOMETRE
from kuchka.units import Kilojoule
from kuchka.units import Kilometre
from kuchka.units import MEGAJOULE
from kuchka.units import METRE
from kuchka.units import Megajoule
from kuchka.units import Metre
from kuchka.units import METRE_PER_SECOND
from kuchka.units import MeterPerSecond
from kuchka.units import MetrePerSecond
from kuchka.units import MICROCOULOMB
from kuchka.units import MICROJOULE
from kuchka.units import MICROMETRE
from kuchka.units import Microcoulomb
from kuchka.units import Microjoule
from kuchka.units import Micrometre
from kuchka.units import MILLICOULOMB
from kuchka.units import MILLIJOULE
from kuchka.units import MILLIMETRE
from kuchka.units import Millicoulomb
from kuchka.units import Millijoule
from kuchka.units import Millimetre
from kuchka.units import NANOJOULE
from kuchka.units import NANOMETRE
from kuchka.units import Nanojoule
from kuchka.units import Nanometre
from kuchka.units import PICOJOULE
from kuchka.units import Picojoule
from kuchka.units import Baud
from kuchka.units import Candela
from kuchka.units import Gram
from kuchka.units import Hertz
from kuchka.units import Inch
from kuchka.units import Kiloampere
from kuchka.units import Kilobaud
from kuchka.units import Kilogram
from kuchka.units import Kilohertz
from kuchka.units import Kilometer
from kuchka.units import Kiloohm
from kuchka.units import KilosamplesPerSecond
from kuchka.units import Kilovolt
from kuchka.units import Kilowatt
from kuchka.units import Megagram
from kuchka.units import Megahertz
from kuchka.units import Megaohm
from kuchka.units import MegasamplesPerSecond
from kuchka.units import Meter
from kuchka.units import Microampere
from kuchka.units import Microgram
from kuchka.units import Micrometer
from kuchka.units import Micromole
from kuchka.units import Microsecond
from kuchka.units import MicrosecondSamplingPeriod
from kuchka.units import Microvolt
from kuchka.units import Microwatt
from kuchka.units import Milliampere
from kuchka.units import Milligram
from kuchka.units import Millimeter
from kuchka.units import Millimole
from kuchka.units import Milliohm
from kuchka.units import Millisecond
from kuchka.units import MillisecondSamplingPeriod
from kuchka.units import Millivolt
from kuchka.units import Milliwatt
from kuchka.units import Mole
from kuchka.units import Nanogram
from kuchka.units import Nanometer
from kuchka.units import Ohm
from kuchka.units import Percent
from kuchka.units import Ratio
from kuchka.units import SamplesPerSecond
from kuchka.units import Second
from kuchka.units import SecondSamplingPeriod
from kuchka.units import Tonne
from kuchka.units import Volt
from kuchka.units import Watt

try:
    __version__ = version("kuchka")
except PackageNotFoundError:  # pragma: no cover -- running from an uninstalled checkout
    __version__ = "0.0.0+unknown"

__all__: list[str] = [
    "COULOMB",
    "ELECTRON_MASS",
    "ELEMENTARY_CHARGE",
    "ENERGY_UNITS",
    "JOULE",
    "KILOJOULE",
    "KILOMETRE",
    "MEGAJOULE",
    "METRE",
    "METRE_PER_SECOND",
    "MICROCOULOMB",
    "MICROJOULE",
    "MICROMETRE",
    "MILLICOULOMB",
    "MILLIJOULE",
    "MILLIMETRE",
    "NANOJOULE",
    "NANOMETRE",
    "NEUTRON_MASS",
    "PICOJOULE",
    "PROTON_MASS",
    "SPEED_OF_LIGHT",
    "AmountOfSubstance",
    "Ampere",
    "Baud",
    "BaudRate",
    "Candela",
    "Celsius",
    "Charge",
    "ConvertibleToFrequency",
    "Coulomb",
    "Current",
    "DeltaCelsius",
    "DeltaKelvin",
    "Energy",
    "Frequency",
    "Gram",
    "Hertz",
    "Inch",
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "Joule",
    "Kelvin",
    "Kiloampere",
    "Kilobaud",
    "Kilogram",
    "Kilohertz",
    "Kilojoule",
    "Kilometer",
    "Kilometre",
    "Kiloohm",
    "KilosamplesPerSecond",
    "Kilovolt",
    "Kilowatt",
    "Length",
    "LuminousIntensity",
    "Mass",
    "MeasurementError",
    "Megagram",
    "Megahertz",
    "Megajoule",
    "Megaohm",
    "MegasamplesPerSecond",
    "Meter",
    "MeterPerSecond",
    "Metre",
    "MetrePerSecond",
    "Microampere",
    "Microcoulomb",
    "Microgram",
    "Microjoule",
    "Micrometer",
    "Micrometre",
    "Micromole",
    "Microsecond",
    "MicrosecondSamplingPeriod",
    "Microvolt",
    "Microwatt",
    "Milliampere",
    "Millicoulomb",
    "Milligram",
    "Millijoule",
    "Millimeter",
    "Millimetre",
    "Millimole",
    "Milliohm",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Millivolt",
    "Milliwatt",
    "Mole",
    "Nanogram",
    "Nanojoule",
    "Nanometer",
    "Nanometre",
    "Ohm",
    "Percent",
    "Picojoule",
    "PlannedDimensionError",
    "Power",
    "Proportion",
    "Ratio",
    "Resistance",
    "SampleRate",
    "SamplesPerSecond",
    "SamplingPeriod",
    "Second",
    "SecondSamplingPeriod",
    "Temperature",
    "TemperatureDelta",
    "Time",
    "Tonne",
    "UnrepresentableDimensionError",
    "Velocity",
    "Volt",
    "Voltage",
    "Watt",
    "__version__",
]
