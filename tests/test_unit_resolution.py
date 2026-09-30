"""The `*_UNITS` symbol resolution tables `kuchka` maintains for boundary code.

Each table maps the symbol an engineer would write in a config file (e.g. `"mV"`)
to the constructor that symbol means (`Millivolt`), closed to one physical dimension.

These are not the primary construction path -- `Volt(5)` remains that -- they exist
specifically for the one place a unit is expected to arrive as a string:
an I/O boundary such as a config file, CSV header, or hardware descriptor.
"""

import pytest

from kuchka import Acre
from kuchka import Ampere
from kuchka import AmpereHour
from kuchka import AmpereSecond
from kuchka import Baud
from kuchka import Bel
from kuchka import Calorie
from kuchka import Candela
from kuchka import Celsius
from kuchka import Centimeter
from kuchka import Coulomb
from kuchka import CubicCentimetre
from kuchka import CubicMetre
from kuchka import CubicMillimetre
from kuchka import Dalton
from kuchka import Decibel
from kuchka import Decimeter
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import EarthMass
from kuchka import Electronvolt
from kuchka import Erg
from kuchka import Foot
from kuchka import Gigaelectronvolt
from kuchka import Gigahertz
from kuchka import Gigajoule
from kuchka import Grain
from kuchka import Gram
from kuchka import Hectare
from kuchka import Hertz
from kuchka import Hour
from kuchka import Inch
from kuchka import Joule
from kuchka import Kelvin
from kuchka import Kiloampere
from kuchka import Kilobaud
from kuchka import Kiloelectronvolt
from kuchka import Kilogram
from kuchka import Kilohertz
from kuchka import Kilojoule
from kuchka import Kilolitre
from kuchka import Kilometer
from kuchka import Kiloohm
from kuchka import KilosamplesPerSecond
from kuchka import Kilosiemens
from kuchka import Kilovolt
from kuchka import Kilowatt
from kuchka import Litre
from kuchka import Megaelectronvolt
from kuchka import Megagram
from kuchka import Megahertz
from kuchka import Megajoule
from kuchka import Megaohm
from kuchka import MegasamplesPerSecond
from kuchka import Megavolt
from kuchka import Meter
from kuchka import Microampere
from kuchka import Microcoulomb
from kuchka import Microelectronvolt
from kuchka import Microgram
from kuchka import Microjoule
from kuchka import Microlitre
from kuchka import Micrometer
from kuchka import Micromole
from kuchka import Microsecond
from kuchka import Microsiemens
from kuchka import Microvolt
from kuchka import Microwatt
from kuchka import Mile
from kuchka import Milliampere
from kuchka import MilliampereHour
from kuchka import MilliampereSecond
from kuchka import Millicoulomb
from kuchka import Millielectronvolt
from kuchka import Milligram
from kuchka import Millijoule
from kuchka import Millilitre
from kuchka import Millimeter
from kuchka import Millimole
from kuchka import Milliohm
from kuchka import Millisecond
from kuchka import Millisiemens
from kuchka import Millivolt
from kuchka import Milliwatt
from kuchka import MilliwattHour
from kuchka import Minute
from kuchka import Mole
from kuchka import Nanocoulomb
from kuchka import Nanogram
from kuchka import Nanojoule
from kuchka import Nanometer
from kuchka import Nanovolt
from kuchka import NauticalMile
from kuchka import Ohm
from kuchka import Ounce
from kuchka import Percent
from kuchka import Petaelectronvolt
from kuchka import Petahertz
from kuchka import Petavolt
from kuchka import Picocoulomb
from kuchka import Picogram
from kuchka import Picojoule
from kuchka import Picometer
from kuchka import Pound
from kuchka import Ratio
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import Siemens
from kuchka import SolarMass
from kuchka import SquareCentimetre
from kuchka import SquareInch
from kuchka import SquareKilometre
from kuchka import SquareMetre
from kuchka import SquareMillimetre
from kuchka import Teraelectronvolt
from kuchka import Terahertz
from kuchka import Terajoule
from kuchka import ThermochemicalCalorie
from kuchka import Tonne
from kuchka import Volt
from kuchka import Watt
from kuchka import WattHour
from kuchka import Yard
from kuchka.internal import symbols
from kuchka.units import AMOUNT_OF_SUBSTANCE_UNITS
from kuchka.units import AREA_UNITS
from kuchka.units import BAUD_RATE_UNITS
from kuchka.units import CHARGE_UNITS
from kuchka.units import CONDUCTANCE_UNITS
from kuchka.units import CURRENT_UNITS
from kuchka.units import ENERGY_UNITS
from kuchka.units import FREQUENCY_UNITS
from kuchka.units import LENGTH_UNITS
from kuchka.units import LOGARITHMIC_RATIO_UNITS
from kuchka.units import LUMINOUS_INTENSITY_UNITS
from kuchka.units import MASS_UNITS
from kuchka.units import POWER_UNITS
from kuchka.units import PROPORTION_UNITS
from kuchka.units import RESISTANCE_UNITS
from kuchka.units import SAMPLE_RATE_UNITS
from kuchka.units import TEMPERATURE_DELTA_UNITS
from kuchka.units import TEMPERATURE_UNITS
from kuchka.units import TIME_UNITS
from kuchka.units import VOLTAGE_UNITS
from kuchka.units import VOLUME_UNITS

# (table, {expected symbol: expected constructor})
TABLE_CASES = [
    (
        VOLTAGE_UNITS,
        {
            "nV": Nanovolt,
            f"{symbols.MICRO}V": Microvolt,
            "mV": Millivolt,
            "V": Volt,
            "kV": Kilovolt,
            "MV": Megavolt,
            "PV": Petavolt,
        },
    ),
    (
        CURRENT_UNITS,
        {
            f"{symbols.MICRO}A": Microampere,
            "mA": Milliampere,
            "A": Ampere,
            "kA": Kiloampere,
        },
    ),
    (
        RESISTANCE_UNITS,
        {
            f"m{symbols.OMEGA}": Milliohm,
            symbols.OMEGA: Ohm,
            f"k{symbols.OMEGA}": Kiloohm,
            f"M{symbols.OMEGA}": Megaohm,
        },
    ),
    (
        POWER_UNITS,
        {f"{symbols.MICRO}W": Microwatt, "mW": Milliwatt, "W": Watt, "kW": Kilowatt},
    ),
    (TEMPERATURE_UNITS, {"K": Kelvin, "C": Celsius}),
    (TEMPERATURE_DELTA_UNITS, {"dK": DeltaKelvin, "dC": DeltaCelsius}),
    (
        TIME_UNITS,
        {
            f"{symbols.MICRO}s": Microsecond,
            "ms": Millisecond,
            "s": Second,
            "min": Minute,
            "h": Hour,
        },
    ),
    (
        FREQUENCY_UNITS,
        {
            "Hz": Hertz,
            "kHz": Kilohertz,
            "MHz": Megahertz,
            "GHz": Gigahertz,
            "THz": Terahertz,
            "PHz": Petahertz,
        },
    ),
    (
        SAMPLE_RATE_UNITS,
        {
            "Sa/s": SamplesPerSecond,
            "kSa/s": KilosamplesPerSecond,
            "MSa/s": MegasamplesPerSecond,
        },
    ),
    (BAUD_RATE_UNITS, {"Bd": Baud, "kBd": Kilobaud}),
    (
        LENGTH_UNITS,
        {
            "pm": Picometer,
            "nm": Nanometer,
            f"{symbols.MICRO}m": Micrometer,
            "mm": Millimeter,
            "cm": Centimeter,
            "dm": Decimeter,
            "m": Meter,
            "km": Kilometer,
            "in": Inch,
            "ft": Foot,
            "yd": Yard,
            "mi": Mile,
            "M": NauticalMile,
        },
    ),
    (PROPORTION_UNITS, {"1": Ratio, "%": Percent}),
    (
        MASS_UNITS,
        {
            "pg": Picogram,
            "ng": Nanogram,
            f"{symbols.MICRO}g": Microgram,
            "mg": Milligram,
            "g": Gram,
            "kg": Kilogram,
            "Mg": Megagram,
            "t": Tonne,
            "Da": Dalton,
            "gr": Grain,
            "lb": Pound,
            "oz": Ounce,
            "M☉": SolarMass,
            "M♁": EarthMass,
        },
    ),
    (
        AMOUNT_OF_SUBSTANCE_UNITS,
        {f"{symbols.MICRO}mol": Micromole, "mmol": Millimole, "mol": Mole},
    ),
    (LUMINOUS_INTENSITY_UNITS, {"cd": Candela}),
    (
        CHARGE_UNITS,
        {
            "pC": Picocoulomb,
            "nC": Nanocoulomb,
            f"{symbols.MICRO}C": Microcoulomb,
            "mC": Millicoulomb,
            "C": Coulomb,
            "As": AmpereSecond,
            "mAs": MilliampereSecond,
            "mAh": MilliampereHour,
            "Ah": AmpereHour,
        },
    ),
    (
        ENERGY_UNITS,
        {
            "pJ": Picojoule,
            "nJ": Nanojoule,
            f"{symbols.MICRO}J": Microjoule,
            "mJ": Millijoule,
            "J": Joule,
            "kJ": Kilojoule,
            "MJ": Megajoule,
            "GJ": Gigajoule,
            "TJ": Terajoule,
            f"{symbols.MICRO}eV": Microelectronvolt,
            "meV": Millielectronvolt,
            "eV": Electronvolt,
            "keV": Kiloelectronvolt,
            "MeV": Megaelectronvolt,
            "GeV": Gigaelectronvolt,
            "TeV": Teraelectronvolt,
            "PeV": Petaelectronvolt,
            "mWh": MilliwattHour,
            "Wh": WattHour,
            "erg": Erg,
            f"cal{symbols.SUBSCRIPT_T}{symbols.SUBSCRIPT_H}": ThermochemicalCalorie,
            "kcal": Calorie,
        },
    ),
    (
        AREA_UNITS,
        {
            f"mm{symbols.SUPERSCRIPT_TWO}": SquareMillimetre,
            f"cm{symbols.SUPERSCRIPT_TWO}": SquareCentimetre,
            f"m{symbols.SUPERSCRIPT_TWO}": SquareMetre,
            f"km{symbols.SUPERSCRIPT_TWO}": SquareKilometre,
            "ha": Hectare,
            "ac": Acre,
            f"in{symbols.SUPERSCRIPT_TWO}": SquareInch,
        },
    ),
    (
        VOLUME_UNITS,
        {
            f"mm{symbols.SUPERSCRIPT_THREE}": CubicMillimetre,
            f"cm{symbols.SUPERSCRIPT_THREE}": CubicCentimetre,
            f"m{symbols.SUPERSCRIPT_THREE}": CubicMetre,
            f"{symbols.MICRO}L": Microlitre,
            "mL": Millilitre,
            "L": Litre,
            "kL": Kilolitre,
        },
    ),
    (
        CONDUCTANCE_UNITS,
        {
            "nS": Nanosiemens,
            f"{symbols.MICRO}S": Microsiemens,
            "mS": Millisiemens,
            "S": Siemens,
            "kS": Kilosiemens,
        },
    ),
    (LOGARITHMIC_RATIO_UNITS, {"dB": Decibel, "B": Bel}),
]

TABLE_CASE_IDS = [
    "voltage",
    "current",
    "resistance",
    "power",
    "temperature",
    "temperature_delta",
    "time",
    "frequency",
    "sample_rate",
    "baud_rate",
    "length",
    "proportion",
    "mass",
    "amount_of_substance",
    "luminous_intensity",
    "charge",
    "energy",
    "area",
    "volume",
    "conductance",
    "logarithmic_ratio",
]


@pytest.mark.parametrize(("table", "expected"), TABLE_CASES, ids=TABLE_CASE_IDS)
def test_table_resolves_every_symbol_to_the_matching_constructor(table, expected):
    assert dict(table) == expected


@pytest.mark.parametrize(("table", "expected"), TABLE_CASES, ids=TABLE_CASE_IDS)
def test_table_constructors_agree_with_calling_them_directly(table, expected):
    for symbol, constructor in expected.items():
        assert table[symbol](5) == constructor(5)


@pytest.mark.parametrize(("table", "expected"), TABLE_CASES, ids=TABLE_CASE_IDS)
def test_table_is_closed_to_symbols_from_other_dimensions(table, expected):
    foreign_symbols = {"mA", "V", "Hz", "Bd", "m", "C"} - set(expected)
    for symbol in foreign_symbols:
        assert symbol not in table


@pytest.mark.parametrize(("table", "expected"), TABLE_CASES, ids=TABLE_CASE_IDS)
def test_table_is_immutable(table, expected):
    # `table` and `expected` are untyped (parametrized), so mypy sees
    # them as `Any` and raises no static error here to suppress; only
    # the runtime immutability of `MappingProxyType` rejects the write.
    any_symbol = next(iter(expected))
    with pytest.raises(TypeError):
        table[any_symbol] = expected[any_symbol]
