"""The `*_UNITS` symbol resolution tables `kuchka` maintains for boundary code.

Each table maps the symbol an engineer would write in a config file (e.g. `"mV"`)
to the constructor that symbol means (`Millivolt`), closed to one physical dimension.

These are not the primary construction path -- `Volt(5)` remains that -- they exist
specifically for the one place a unit is expected to arrive as a string:
an I/O boundary such as a config file, CSV header, or hardware descriptor.
"""

from kuchka.units.power import Microwatt

from kuchka.units.mass import Picogram

import pytest
from kuchka import Ampere
from kuchka import Baud
from kuchka import Celsius
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import Hertz
from kuchka import Inch
from kuchka import Kelvin
from kuchka import Kiloampere
from kuchka import Kilobaud
from kuchka import Kilohertz
from kuchka import Kilometer
from kuchka import Kiloohm
from kuchka import KilosamplesPerSecond
from kuchka import Kilovolt
from kuchka import Kilowatt
from kuchka import Megahertz
from kuchka import Megaohm
from kuchka import MegasamplesPerSecond
from kuchka import Meter
from kuchka import Microampere
from kuchka import Micrometer
from kuchka import Microsecond
from kuchka import MicrosecondSamplingPeriod
from kuchka import Microvolt
from kuchka import Milliampere
from kuchka import Millimeter
from kuchka import Millisecond
from kuchka import MillisecondSamplingPeriod
from kuchka import Milliohm
from kuchka import Millivolt
from kuchka import Milliwatt
from kuchka import Nanometer
from kuchka import Ohm
from kuchka import Percent
from kuchka import Ratio
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import SecondSamplingPeriod
from kuchka import Volt
from kuchka import Watt
from kuchka.units import BAUD_RATE_UNITS
from kuchka.units import CURRENT_UNITS
from kuchka.units import FREQUENCY_UNITS
from kuchka.units import LENGTH_UNITS
from kuchka.units import POWER_UNITS
from kuchka.units import PROPORTION_UNITS
from kuchka.units import RESISTANCE_UNITS
from kuchka.units import SAMPLE_RATE_UNITS
from kuchka.units import SAMPLING_PERIOD_UNITS
from kuchka.units import TEMPERATURE_DELTA_UNITS
from kuchka.units import TEMPERATURE_UNITS
from kuchka.units import TIME_UNITS
from kuchka.units import VOLTAGE_UNITS
from kuchka import Candela
from kuchka import Gram
from kuchka import Kilogram
from kuchka import Megagram
from kuchka import Microgram
from kuchka import Micromole
from kuchka import Milligram
from kuchka import Millimole
from kuchka import Mole
from kuchka import Nanogram
from kuchka import Tonne
from kuchka.units import AMOUNT_OF_SUBSTANCE_UNITS
from kuchka.units import LUMINOUS_INTENSITY_UNITS
from kuchka.units import MASS_UNITS

# (table, {expected symbol: expected constructor})
TABLE_CASES = [
    (VOLTAGE_UNITS, {"\u00b5V": Microvolt, "mV": Millivolt, "V": Volt, "kV": Kilovolt}),
    (
        CURRENT_UNITS,
        {"\u00b5A": Microampere, "mA": Milliampere, "A": Ampere, "kA": Kiloampere},
    ),
    (
        RESISTANCE_UNITS,
        {"m\u03a9": Milliohm, "\u03a9": Ohm, "k\u03a9": Kiloohm, "M\u03a9": Megaohm},
    ),
    (POWER_UNITS, {"\u00b5W": Microwatt, "mW": Milliwatt, "W": Watt, "kW": Kilowatt}),
    (TEMPERATURE_UNITS, {"K": Kelvin, "C": Celsius}),
    (TEMPERATURE_DELTA_UNITS, {"dK": DeltaKelvin, "dC": DeltaCelsius}),
    (TIME_UNITS, {"\u00b5s": Microsecond, "ms": Millisecond, "s": Second}),
    (FREQUENCY_UNITS, {"Hz": Hertz, "kHz": Kilohertz, "MHz": Megahertz}),
    (
        SAMPLING_PERIOD_UNITS,
        {
            "\u00b5s": MicrosecondSamplingPeriod,
            "ms": MillisecondSamplingPeriod,
            "s": SecondSamplingPeriod,
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
            "nm": Nanometer,
            "\u00b5m": Micrometer,
            "mm": Millimeter,
            "m": Meter,
            "km": Kilometer,
            "in": Inch,
        },
    ),
    (PROPORTION_UNITS, {"1": Ratio, "%": Percent}),
    (
        MASS_UNITS,
        {
            "pg": Picogram,
            "ng": Nanogram,
            "\u00b5g": Microgram,
            "mg": Milligram,
            "g": Gram,
            "kg": Kilogram,
            "Mg": Megagram,
            "t": Tonne,
        },
    ),
    (
        AMOUNT_OF_SUBSTANCE_UNITS,
        {"\u00b5mol": Micromole, "mmol": Millimole, "mol": Mole},
    ),
    (LUMINOUS_INTENSITY_UNITS, {"cd": Candela}),
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
    "sampling_period",
    "sample_rate",
    "baud_rate",
    "length",
    "proportion",
    "mass",
    "amount_of_substance",
    "luminous_intensity",
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
