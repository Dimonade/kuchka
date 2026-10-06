"""The `*_UNITS` symbol resolution tables `kuchka` maintains for boundary code.

Each table maps the symbol an engineer would write in a config file (e.g. `"mV"`)
to the constructor that symbol means (`Millivolt`), closed to one physical dimension.
Iterating a table yields the display symbols pinned here; the other notations a table
accepts (`C` for `°C`, `t` for `Mg`) are pinned in `test_unit_spellings`.

These are not the primary construction path -- `Volt(5)` remains that -- they exist
specifically for the one place a unit is expected to arrive as a string:
an I/O boundary such as a config file, CSV header, or hardware descriptor.
"""

import pytest

from kuchka.internal import symbols
from kuchka.units import acceleration
from kuchka.units import amount
from kuchka.units import area
from kuchka.units import baud_rate
from kuchka.units import charge
from kuchka.units import conductance
from kuchka.units import current
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import logarithmic
from kuchka.units import luminous_intensity
from kuchka.units import mass
from kuchka.units import power
from kuchka.units import proportion
from kuchka.units import resistance
from kuchka.units import sample_rate
from kuchka.units import thermal
from kuchka.units import time
from kuchka.units import velocity
from kuchka.units import voltage
from kuchka.units import volume

# (table, {expected symbol: expected constructor})
TABLE_CASES = [
    (
        acceleration.ACCELERATION_UNITS,
        {
            f"m/s{symbols.SUPERSCRIPT_TWO}": acceleration.MetrePerSecondSquared,
            "Gal": acceleration.Gal,
            "mGal": acceleration.Milligal,
            f"{symbols.MICRO}Gal": acceleration.Microgal,
        },
    ),
    (
        voltage.VOLTAGE_UNITS,
        {
            "nV": voltage.Nanovolt,
            f"{symbols.MICRO}V": voltage.Microvolt,
            "mV": voltage.Millivolt,
            "V": voltage.Volt,
            "kV": voltage.Kilovolt,
            "MV": voltage.Megavolt,
            "PV": voltage.Petavolt,
        },
    ),
    (
        current.CURRENT_UNITS,
        {
            "pA": current.Picoampere,
            "nA": current.Nanoampere,
            f"{symbols.MICRO}A": current.Microampere,
            "mA": current.Milliampere,
            "A": current.Ampere,
            "kA": current.Kiloampere,
            "MA": current.Megaampere,
        },
    ),
    (
        resistance.RESISTANCE_UNITS,
        {
            f"{symbols.MICRO}{symbols.OMEGA}": resistance.Microohm,
            f"m{symbols.OMEGA}": resistance.Milliohm,
            symbols.OMEGA: resistance.Ohm,
            f"k{symbols.OMEGA}": resistance.Kiloohm,
            f"M{symbols.OMEGA}": resistance.Megaohm,
            f"G{symbols.OMEGA}": resistance.Gigaohm,
        },
    ),
    (
        power.POWER_UNITS,
        {
            "pW": power.Picowatt,
            "nW": power.Nanowatt,
            f"{symbols.MICRO}W": power.Microwatt,
            "mW": power.Milliwatt,
            "W": power.Watt,
            "kW": power.Kilowatt,
            "MW": power.Megawatt,
            "GW": power.Gigawatt,
            "TW": power.Terawatt,
            "PW": power.Petawatt,
            "hp": power.Horsepower,
            "PS": power.MetricHorsepower,
        },
    ),
    (
        thermal.TEMPERATURE_UNITS,
        {
            "K": thermal.Kelvin,
            f"{symbols.DEGREE}C": thermal.Celsius,
            f"{symbols.DEGREE}F": thermal.Fahrenheit,
        },
    ),
    (
        thermal.TEMPERATURE_DELTA_UNITS,
        {
            f"{symbols.DELTA}K": thermal.DeltaKelvin,
            f"{symbols.DELTA}{symbols.DEGREE}C": thermal.DeltaCelsius,
            f"{symbols.DELTA}{symbols.DEGREE}F": thermal.DeltaFahrenheit,
        },
    ),
    (
        time.TIME_UNITS,
        {
            "fs": time.Femtosecond,
            "ps": time.Picosecond,
            "ns": time.Nanosecond,
            f"{symbols.MICRO}s": time.Microsecond,
            "ms": time.Millisecond,
            "s": time.Second,
            "min": time.Minute,
            "h": time.Hour,
            "d": time.Day,
            "wk": time.Week,
            "fortnight": time.Fortnight,
            "a": time.JulianYear,
            "jiffy": time.Jiffy,
        },
    ),
    (
        frequency.FREQUENCY_UNITS,
        {
            "nHz": frequency.Nanohertz,
            f"{symbols.MICRO}Hz": frequency.Microhertz,
            "mHz": frequency.Millihertz,
            "Hz": frequency.Hertz,
            "kHz": frequency.Kilohertz,
            "MHz": frequency.Megahertz,
            "GHz": frequency.Gigahertz,
            "THz": frequency.Terahertz,
            "PHz": frequency.Petahertz,
        },
    ),
    (
        sample_rate.SAMPLE_RATE_UNITS,
        {
            "Sa/s": sample_rate.SamplesPerSecond,
            "kSa/s": sample_rate.KilosamplesPerSecond,
            "MSa/s": sample_rate.MegasamplesPerSecond,
        },
    ),
    (
        baud_rate.BAUD_RATE_UNITS,
        {
            "Bd": baud_rate.Baud,
            "kBd": baud_rate.Kilobaud,
        },
    ),
    (
        length.LENGTH_UNITS,
        {
            "pm": length.Picometer,
            "nm": length.Nanometer,
            f"{symbols.MICRO}m": length.Micrometer,
            "mm": length.Millimeter,
            "cm": length.Centimeter,
            "dm": length.Decimeter,
            "m": length.Meter,
            "km": length.Kilometer,
            "in": length.Inch,
            "ft": length.Foot,
            "yd": length.Yard,
            "mi": length.Mile,
            "M": length.NauticalMile,
            "au": length.AstronomicalUnit,
            "ly": length.LightYear,
        },
    ),
    (
        proportion.PROPORTION_UNITS,
        {
            "1": proportion.Ratio,
            "%": proportion.Percent,
        },
    ),
    (
        mass.MASS_UNITS,
        {
            "pg": mass.Picogram,
            "ng": mass.Nanogram,
            f"{symbols.MICRO}g": mass.Microgram,
            "mg": mass.Milligram,
            "g": mass.Gram,
            "kg": mass.Kilogram,
            "Mg": mass.Megagram,
            "Da": mass.Dalton,
            "gr": mass.Grain,
            "lb": mass.Pound,
            "oz": mass.Ounce,
            "M☉": mass.SolarMass,
            "M♁": mass.EarthMass,
        },
    ),
    (
        amount.AMOUNT_OF_SUBSTANCE_UNITS,
        {
            f"{symbols.MICRO}mol": amount.Micromole,
            "mmol": amount.Millimole,
            "mol": amount.Mole,
        },
    ),
    (
        luminous_intensity.LUMINOUS_INTENSITY_UNITS,
        {
            "cd": luminous_intensity.Candela,
        },
    ),
    (
        charge.CHARGE_UNITS,
        {
            "pC": charge.Picocoulomb,
            "nC": charge.Nanocoulomb,
            f"{symbols.MICRO}C": charge.Microcoulomb,
            "mC": charge.Millicoulomb,
            "C": charge.Coulomb,
            "mAs": charge.MilliampereSecond,
            "mAh": charge.MilliampereHour,
            "Ah": charge.AmpereHour,
        },
    ),
    (
        energy.ENERGY_UNITS,
        {
            "pJ": energy.Picojoule,
            "nJ": energy.Nanojoule,
            f"{symbols.MICRO}J": energy.Microjoule,
            "mJ": energy.Millijoule,
            "J": energy.Joule,
            "kJ": energy.Kilojoule,
            "MJ": energy.Megajoule,
            "GJ": energy.Gigajoule,
            "TJ": energy.Terajoule,
            "PJ": energy.Petajoule,
            f"{symbols.MICRO}eV": energy.Microelectronvolt,
            "meV": energy.Millielectronvolt,
            "eV": energy.Electronvolt,
            "keV": energy.Kiloelectronvolt,
            "MeV": energy.Megaelectronvolt,
            "GeV": energy.Gigaelectronvolt,
            "TeV": energy.Teraelectronvolt,
            "PeV": energy.Petaelectronvolt,
            "mWh": energy.MilliwattHour,
            "Wh": energy.WattHour,
            "kWh": energy.KilowattHour,
            "erg": energy.Erg,
            f"cal{symbols.SUBSCRIPT_T}{symbols.SUBSCRIPT_H}": energy.ThermochemicalCalorie,  # noqa: E501
            "kcal": energy.Calorie,
            "tTNT": energy.TonneOfTNT,
            "ktTNT": energy.KilotonneOfTNT,
            "MtTNT": energy.MegatonneOfTNT,
        },
    ),
    (
        area.AREA_UNITS,
        {
            f"mm{symbols.SUPERSCRIPT_TWO}": area.SquareMillimetre,
            f"cm{symbols.SUPERSCRIPT_TWO}": area.SquareCentimetre,
            f"m{symbols.SUPERSCRIPT_TWO}": area.SquareMetre,
            f"km{symbols.SUPERSCRIPT_TWO}": area.SquareKilometre,
            "ha": area.Hectare,
            "ac": area.Acre,
            f"in{symbols.SUPERSCRIPT_TWO}": area.SquareInch,
        },
    ),
    (
        volume.VOLUME_UNITS,
        {
            f"mm{symbols.SUPERSCRIPT_THREE}": volume.CubicMillimetre,
            f"cm{symbols.SUPERSCRIPT_THREE}": volume.CubicCentimetre,
            f"m{symbols.SUPERSCRIPT_THREE}": volume.CubicMetre,
            f"{symbols.MICRO}L": volume.Microlitre,
            "mL": volume.Millilitre,
            "L": volume.Litre,
            "kL": volume.Kilolitre,
        },
    ),
    (
        conductance.CONDUCTANCE_UNITS,
        {
            "nS": conductance.Nanosiemens,
            f"{symbols.MICRO}S": conductance.Microsiemens,
            "mS": conductance.Millisiemens,
            "S": conductance.Siemens,
            "kS": conductance.Kilosiemens,
        },
    ),
    (
        logarithmic.LOGARITHMIC_RATIO_UNITS,
        {
            "dB": logarithmic.Decibel,
            "B": logarithmic.Bel,
        },
    ),
    (
        force.FORCE_UNITS,
        {
            f"{symbols.MICRO}N": force.Micronewton,
            "mN": force.Millinewton,
            "N": force.Newton,
            "kN": force.Kilonewton,
            "MN": force.Meganewton,
            "dyn": force.Dyne,
            "lbf": force.PoundForce,
            "kgf": force.KilogramForce,
        },
    ),
    (
        velocity.VELOCITY_UNITS,
        {
            "m/s": velocity.MetrePerSecond,
            "km/h": velocity.KilometrePerHour,
            "mph": velocity.MilePerHour,
            "kn": velocity.Knot,
        },
    ),
]

TABLE_CASE_IDS = [
    "acceleration",
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
    "force",
    "velocity",
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
    foreign_symbols = {"mA", "V", "Hz", "Bd", "m", "kg", "Wb"} - set(expected)
    for symbol in foreign_symbols:
        assert symbol not in table


@pytest.mark.parametrize(("table", "expected"), TABLE_CASES, ids=TABLE_CASE_IDS)
def test_table_is_immutable(table, expected):
    # `table` and `expected` are untyped (parametrized), so mypy sees
    # them as `Any` and raises no static error here to suppress; only
    # the runtime read-only `UnitTable` rejects the write.
    any_symbol = next(iter(expected))
    with pytest.raises(TypeError):
        table[any_symbol] = expected[any_symbol]
