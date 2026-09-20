"""kuchka -- a small pile of physically-typed units for engineering code.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current   # -> Power, computed and typed automatically

Two-tier export policy:
  - kuchka (this package): unit constructors (Volt, Tonne, ...) and semantic quantity
  types (Voltage, Temperature, ...) only.
  - kuchka.units / kuchka.quantities: the complete surface, including raw `UnitDef`
  constants (VOLT, KILOVOLT, ...) and `*_UNITS` boundary tables.
  _see docs/examples/config_migration for why those exist and who needs them._

This file is hand-maintained on purpose.
`tests/test_public_api_surface.py` checks it against
`kuchka.units.__all__` / `kuchka.quantities.__all__` mechanically, so a new dimension
can't quietly go unpromoted, and a UnitDef/table can't quietly leak up a level.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from kuchka.constants import codata_2022
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import MeasurementError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.quantities import Acceleration
from kuchka.quantities import AmountOfSubstance
from kuchka.quantities import Angle
from kuchka.quantities import Area
from kuchka.quantities import BaudRate
from kuchka.quantities import Charge
from kuchka.quantities import Conductance
from kuchka.quantities import ConvertibleToFrequency
from kuchka.quantities import Current
from kuchka.quantities import Density
from kuchka.quantities import Energy
from kuchka.quantities import Force
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
from kuchka.quantities import Time
from kuchka.quantities import Velocity
from kuchka.quantities import Voltage
from kuchka.quantities import Volume
from kuchka.units import Acre
from kuchka.units import Ampere
from kuchka.units import AmpereHour
from kuchka.units import AmpereSecond
from kuchka.units import ArcMinute
from kuchka.units import ArcSecond
from kuchka.units import Baud
from kuchka.units import Candela
from kuchka.units import Celsius
from kuchka.units import Centimeter
from kuchka.units import Centimetre
from kuchka.units import Coulomb
from kuchka.units import CubicCentimeter
from kuchka.units import CubicCentimetre
from kuchka.units import CubicMeter
from kuchka.units import CubicMetre
from kuchka.units import CubicMillimeter
from kuchka.units import CubicMillimetre
from kuchka.units import Decimeter
from kuchka.units import Decimetre
from kuchka.units import Degree
from kuchka.units import DeltaCelsius
from kuchka.units import DeltaKelvin
from kuchka.units import Dyne
from kuchka.units import Gradian
from kuchka.units import Gram
from kuchka.units import GramPerCubicCentimetre
from kuchka.units import Hectare
from kuchka.units import Hertz
from kuchka.units import Hour
from kuchka.units import Inch
from kuchka.units import Joule
from kuchka.units import Kelvin
from kuchka.units import Kiloampere
from kuchka.units import Kilobaud
from kuchka.units import Kilogram
from kuchka.units import KilogramPerCubicMetre
from kuchka.units import KilogramPerLitre
from kuchka.units import Kilohertz
from kuchka.units import Kilojoule
from kuchka.units import Kiloliter
from kuchka.units import Kilolitre
from kuchka.units import Kilometer
from kuchka.units import KilometerPerHour
from kuchka.units import Kilometre
from kuchka.units import KilometrePerHour
from kuchka.units import Kilonewton
from kuchka.units import Kiloohm
from kuchka.units import KilosamplesPerSecond
from kuchka.units import Kilosiemens
from kuchka.units import Kilovolt
from kuchka.units import Kilowatt
from kuchka.units import Liter
from kuchka.units import Litre
from kuchka.units import Megagram
from kuchka.units import Megahertz
from kuchka.units import Megajoule
from kuchka.units import Megaohm
from kuchka.units import MegasamplesPerSecond
from kuchka.units import Meter
from kuchka.units import MeterPerSecond
from kuchka.units import MeterPerSecondSquared
from kuchka.units import Metre
from kuchka.units import MetrePerSecond
from kuchka.units import MetrePerSecondSquared
from kuchka.units import Microampere
from kuchka.units import Microcoulomb
from kuchka.units import Microgram
from kuchka.units import Microjoule
from kuchka.units import Microliter
from kuchka.units import Microlitre
from kuchka.units import Micrometer
from kuchka.units import Micrometre
from kuchka.units import Micromole
from kuchka.units import Microsecond
from kuchka.units import MicrosecondSamplingPeriod
from kuchka.units import Microsiemens
from kuchka.units import Microvolt
from kuchka.units import Microwatt
from kuchka.units import MilePerHour
from kuchka.units import Milliampere
from kuchka.units import MilliampereHour
from kuchka.units import MilliampereSecond
from kuchka.units import Millicoulomb
from kuchka.units import Milligram
from kuchka.units import Millijoule
from kuchka.units import Milliliter
from kuchka.units import Millilitre
from kuchka.units import Millimeter
from kuchka.units import Millimetre
from kuchka.units import Millimole
from kuchka.units import Millinewton
from kuchka.units import Milliohm
from kuchka.units import Millisecond
from kuchka.units import MillisecondSamplingPeriod
from kuchka.units import Millisiemens
from kuchka.units import Millivolt
from kuchka.units import Milliwatt
from kuchka.units import MilliwattHour
from kuchka.units import Minute
from kuchka.units import Mole
from kuchka.units import Nanocoulomb
from kuchka.units import Nanogram
from kuchka.units import Nanojoule
from kuchka.units import Nanometer
from kuchka.units import Nanometre
from kuchka.units import Newton
from kuchka.units import Ohm
from kuchka.units import Percent
from kuchka.units import Picocoulomb
from kuchka.units import Picogram
from kuchka.units import Picojoule
from kuchka.units import PoundForce
from kuchka.units import Radian
from kuchka.units import Ratio
from kuchka.units import SamplesPerSecond
from kuchka.units import Second
from kuchka.units import SecondSamplingPeriod
from kuchka.units import Siemens
from kuchka.units import SquareCentimeter
from kuchka.units import SquareCentimetre
from kuchka.units import SquareInch
from kuchka.units import SquareKilometer
from kuchka.units import SquareKilometre
from kuchka.units import SquareMeter
from kuchka.units import SquareMetre
from kuchka.units import SquareMillimeter
from kuchka.units import SquareMillimetre
from kuchka.units import Tonne
from kuchka.units import Turn
from kuchka.units import Volt
from kuchka.units import Watt
from kuchka.units import WattHour

try:
    __version__ = version("kuchka")
except PackageNotFoundError:  # pragma: no cover -- running from an uninstalled checkout
    __version__ = "0.0.0+unknown"

__all__: list[str] = [
    "Acceleration",
    "Acre",
    "AmountOfSubstance",
    "Ampere",
    "AmpereHour",
    "AmpereSecond",
    "Angle",
    "ArcMinute",
    "ArcSecond",
    "Area",
    "Baud",
    "BaudRate",
    "Candela",
    "Celsius",
    "Centimeter",
    "Centimetre",
    "Charge",
    "Conductance",
    "ConvertibleToFrequency",
    "Coulomb",
    "CubicCentimeter",
    "CubicCentimetre",
    "CubicMeter",
    "CubicMetre",
    "CubicMillimeter",
    "CubicMillimetre",
    "Current",
    "Decimeter",
    "Decimetre",
    "Degree",
    "DeltaCelsius",
    "DeltaKelvin",
    "Density",
    "Dyne",
    "Energy",
    "Force",
    "Frequency",
    "Gradian",
    "Gram",
    "GramPerCubicCentimetre",
    "Hectare",
    "Hertz",
    "Hour",
    "Inch",
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "Joule",
    "Kelvin",
    "Kiloampere",
    "Kilobaud",
    "Kilogram",
    "KilogramPerCubicMetre",
    "KilogramPerLitre",
    "Kilohertz",
    "Kilojoule",
    "Kiloliter",
    "Kilolitre",
    "Kilometer",
    "KilometerPerHour",
    "Kilometre",
    "KilometrePerHour",
    "Kilonewton",
    "Kiloohm",
    "KilosamplesPerSecond",
    "Kilosiemens",
    "Kilovolt",
    "Kilowatt",
    "Length",
    "Liter",
    "Litre",
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
    "MeterPerSecondSquared",
    "Metre",
    "MetrePerSecond",
    "MetrePerSecondSquared",
    "Microampere",
    "Microcoulomb",
    "Microgram",
    "Microjoule",
    "Microliter",
    "Microlitre",
    "Micrometer",
    "Micrometre",
    "Micromole",
    "Microsecond",
    "MicrosecondSamplingPeriod",
    "Microsiemens",
    "Microvolt",
    "Microwatt",
    "MilePerHour",
    "Milliampere",
    "MilliampereHour",
    "MilliampereSecond",
    "Millicoulomb",
    "Milligram",
    "Millijoule",
    "Milliliter",
    "Millilitre",
    "Millimeter",
    "Millimetre",
    "Millimole",
    "Millinewton",
    "Milliohm",
    "Millisecond",
    "MillisecondSamplingPeriod",
    "Millisiemens",
    "Millivolt",
    "Milliwatt",
    "MilliwattHour",
    "Minute",
    "Mole",
    "Nanocoulomb",
    "Nanogram",
    "Nanojoule",
    "Nanometer",
    "Nanometre",
    "Newton",
    "Ohm",
    "Percent",
    "Picocoulomb",
    "Picogram",
    "Picojoule",
    "PlannedDimensionError",
    "PoundForce",
    "Power",
    "Proportion",
    "Radian",
    "Ratio",
    "Resistance",
    "SampleRate",
    "SamplesPerSecond",
    "SamplingPeriod",
    "Second",
    "SecondSamplingPeriod",
    "Siemens",
    "SquareCentimeter",
    "SquareCentimetre",
    "SquareInch",
    "SquareKilometer",
    "SquareKilometre",
    "SquareMeter",
    "SquareMetre",
    "SquareMillimeter",
    "SquareMillimetre",
    "Temperature",
    "TemperatureDelta",
    "Time",
    "Tonne",
    "Turn",
    "UnrepresentableDimensionError",
    "Velocity",
    "Volt",
    "Voltage",
    "Volume",
    "Watt",
    "WattHour",
    "__version__",
    "codata_2022",
]
