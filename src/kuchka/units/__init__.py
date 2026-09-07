"""Engineer-facing unit constructors, one module per physical dimension.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current

Each quantity's canonical unit (the one arithmetic results come back in, e.g.
``Voltage * Current`` yields a result expressed in ``Watt``) is assigned onto the
corresponding domain class from ``kuchka.quantities`` at the bottom of the module that
owns that dimension.
"""

from __future__ import annotations

from kuchka.units.voltage import *

from kuchka.units.thermal import CELSIUS
from kuchka.units.thermal import Celsius
from kuchka.units.thermal import DELTA_CELSIUS
from kuchka.units.thermal import DeltaCelsius
from kuchka.units.thermal import DELTA_KELVIN
from kuchka.units.thermal import DeltaKelvin
from kuchka.units.thermal import KELVIN
from kuchka.units.thermal import Kelvin
from kuchka.units.thermal import TEMPERATURE_DELTA_UNITS
from kuchka.units.thermal import TEMPERATURE_UNITS
from kuchka.units.amount import AMOUNT_OF_SUBSTANCE_UNITS
from kuchka.units.charge import CHARGE_UNITS
from kuchka.units.charge import COULOMB
from kuchka.units.charge import Coulomb
from kuchka.units.charge import MICROCOULOMB
from kuchka.units.charge import Microcoulomb
from kuchka.units.charge import MILLICOULOMB
from kuchka.units.charge import Millicoulomb
from kuchka.units.energy import ENERGY_UNITS
from kuchka.units.energy import JOULE
from kuchka.units.energy import Joule
from kuchka.units.energy import KILOJOULE
from kuchka.units.energy import Kilojoule
from kuchka.units.energy import MEGAJOULE
from kuchka.units.energy import Megajoule
from kuchka.units.energy import MICROJOULE
from kuchka.units.energy import Microjoule
from kuchka.units.energy import MILLIJOULE
from kuchka.units.energy import Millijoule
from kuchka.units.energy import NANOJOULE
from kuchka.units.energy import Nanojoule
from kuchka.units.energy import PICOJOULE
from kuchka.units.energy import Picojoule
from kuchka.units.kinematics import METRE_PER_SECOND
from kuchka.units.kinematics import MeterPerSecond
from kuchka.units.kinematics import MetrePerSecond
from kuchka.units.kinematics import VELOCITY_UNITS
from kuchka.units.amount import MICROMOLE
from kuchka.units.amount import Micromole
from kuchka.units.amount import MILLIMOLE
from kuchka.units.amount import Millimole
from kuchka.units.amount import MOLE
from kuchka.units.amount import Mole
from kuchka.units.current import AMPERE
from kuchka.units.current import Ampere
from kuchka.units.current import CURRENT_UNITS
from kuchka.units.current import KILOAMPERE
from kuchka.units.current import Kiloampere
from kuchka.units.current import MICROAMPERE
from kuchka.units.current import Microampere
from kuchka.units.current import MILLIAMPERE
from kuchka.units.current import Milliampere
from kuchka.units.length import INCH
from kuchka.units.length import Inch
from kuchka.units.length import KILOMETER
from kuchka.units.length import KILOMETRE
from kuchka.units.length import Kilometer
from kuchka.units.length import Kilometre
from kuchka.units.length import LENGTH_UNITS
from kuchka.units.length import METER
from kuchka.units.length import METRE
from kuchka.units.length import Meter
from kuchka.units.length import Metre
from kuchka.units.length import MICROMETER
from kuchka.units.length import MICROMETRE
from kuchka.units.length import Micrometer
from kuchka.units.length import Micrometre
from kuchka.units.length import MILLIMETER
from kuchka.units.length import MILLIMETRE
from kuchka.units.length import Millimeter
from kuchka.units.length import Millimetre
from kuchka.units.length import NANOMETER
from kuchka.units.length import NANOMETRE
from kuchka.units.length import Nanometer
from kuchka.units.length import Nanometre
from kuchka.units.luminous_intensity import CANDELA
from kuchka.units.luminous_intensity import Candela
from kuchka.units.luminous_intensity import LUMINOUS_INTENSITY_UNITS
from kuchka.units.mass import GRAM
from kuchka.units.mass import Gram
from kuchka.units.mass import KILOGRAM
from kuchka.units.mass import Kilogram
from kuchka.units.mass import MASS_UNITS
from kuchka.units.mass import MEGAGRAM
from kuchka.units.mass import Megagram
from kuchka.units.mass import MICROGRAM
from kuchka.units.mass import Microgram
from kuchka.units.mass import MILLIGRAM
from kuchka.units.mass import Milligram
from kuchka.units.mass import NANOGRAM
from kuchka.units.mass import Nanogram
from kuchka.units.mass import PICOGRAM
from kuchka.units.mass import Picogram
from kuchka.units.mass import Tonne
from kuchka.units.power import MICROWATT
from kuchka.units.power import Microwatt
from kuchka.units.power import KILOWATT
from kuchka.units.power import Kilowatt
from kuchka.units.power import MILLIWATT
from kuchka.units.power import Milliwatt
from kuchka.units.power import POWER_UNITS
from kuchka.units.power import WATT
from kuchka.units.power import Watt
from kuchka.units.proportion import PERCENT
from kuchka.units.proportion import Percent
from kuchka.units.proportion import PROPORTION_UNITS
from kuchka.units.proportion import RATIO
from kuchka.units.proportion import Ratio
from kuchka.units.resistance import KILOOHM
from kuchka.units.resistance import Kiloohm
from kuchka.units.resistance import MEGAOHM
from kuchka.units.resistance import Megaohm
from kuchka.units.resistance import MILLIOHM
from kuchka.units.resistance import Milliohm
from kuchka.units.resistance import OHM
from kuchka.units.resistance import Ohm
from kuchka.units.resistance import RESISTANCE_UNITS
from kuchka.units.temporal import BAUD
from kuchka.units.temporal import Baud
from kuchka.units.temporal import BAUD_RATE_UNITS
from kuchka.units.temporal import FREQUENCY_UNITS
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
from kuchka.units.temporal import SAMPLE_RATE_UNITS
from kuchka.units.temporal import SamplesPerSecond
from kuchka.units.temporal import SAMPLING_PERIOD_MICROSECOND
from kuchka.units.temporal import SAMPLING_PERIOD_MILLISECOND
from kuchka.units.temporal import SAMPLING_PERIOD_SECOND
from kuchka.units.temporal import SAMPLING_PERIOD_UNITS
from kuchka.units.temporal import SECOND
from kuchka.units.temporal import Second
from kuchka.units.temporal import SecondSamplingPeriod
from kuchka.units.temporal import TIME_UNITS
from kuchka.units.voltage import KILOVOLT
from kuchka.units.voltage import Kilovolt
from kuchka.units.voltage import MICROVOLT
from kuchka.units.voltage import Microvolt
from kuchka.units.voltage import MILLIVOLT
from kuchka.units.voltage import Millivolt
from kuchka.units.voltage import VOLT
from kuchka.units.voltage import Volt
from kuchka.units.voltage import VOLTAGE_UNITS

__all__: list[str] = [
    "AMOUNT_OF_SUBSTANCE_UNITS",
    "AMPERE",
    "BAUD",
    "BAUD_RATE_UNITS",
    "CANDELA",
    "CELSIUS",
    "CHARGE_UNITS",
    "COULOMB",
    "CURRENT_UNITS",
    "DELTA_CELSIUS",
    "DELTA_KELVIN",
    "ENERGY_UNITS",
    "FREQUENCY_UNITS",
    "GRAM",
    "HERTZ",
    "INCH",
    "JOULE",
    "KELVIN",
    "KILOAMPERE",
    "KILOBAUD",
    "KILOGRAM",
    "KILOHERTZ",
    "KILOJOULE",
    "KILOMETER",
    "KILOMETRE",
    "KILOOHM",
    "KILOSAMPLE_PER_SECOND",
    "KILOVOLT",
    "KILOWATT",
    "LENGTH_UNITS",
    "LUMINOUS_INTENSITY_UNITS",
    "MASS_UNITS",
    "MEGAGRAM",
    "MEGAHERTZ",
    "MEGAJOULE",
    "MEGAOHM",
    "MEGASAMPLE_PER_SECOND",
    "METER",
    "METRE",
    "METRE_PER_SECOND",
    "MICROAMPERE",
    "MICROCOULOMB",
    "MICROGRAM",
    "MICROJOULE",
    "MICROMETER",
    "MICROMETRE",
    "MICROMOLE",
    "MICROSECOND",
    "MICROVOLT",
    "MICROWATT",
    "MILLIAMPERE",
    "MILLICOULOMB",
    "MILLIGRAM",
    "MILLIJOULE",
    "MILLIMETER",
    "MILLIMETRE",
    "MILLIMOLE",
    "MILLIOHM",
    "MILLISECOND",
    "MILLIVOLT",
    "MILLIWATT",
    "MOLE",
    "NANOGRAM",
    "NANOJOULE",
    "NANOMETER",
    "NANOMETRE",
    "OHM",
    "PERCENT",
    "PICOGRAM",
    "PICOJOULE",
    "POWER_UNITS",
    "PROPORTION_UNITS",
    "RATIO",
    "RESISTANCE_UNITS",
    "SAMPLE_PER_SECOND",
    "SAMPLE_RATE_UNITS",
    "SAMPLING_PERIOD_MICROSECOND",
    "SAMPLING_PERIOD_MILLISECOND",
    "SAMPLING_PERIOD_SECOND",
    "SAMPLING_PERIOD_UNITS",
    "SECOND",
    "TEMPERATURE_DELTA_UNITS",
    "TEMPERATURE_UNITS",
    "TIME_UNITS",
    "VELOCITY_UNITS",
    "VOLT",
    "VOLTAGE_UNITS",
    "WATT",
    "Ampere",
    "Baud",
    "Candela",
    "Celsius",
    "Coulomb",
    "DeltaCelsius",
    "DeltaKelvin",
    "Gram",
    "Hertz",
    "Inch",
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
    "Picogram",
    "Picojoule",
    "Ratio",
    "SamplesPerSecond",
    "Second",
    "SecondSamplingPeriod",
    "Tonne",
    "Volt",
    "Watt",
]
