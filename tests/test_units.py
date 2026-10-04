"""Unit prefixes: every constructor must scale into its canonical unit correctly.

Tests parametrize over `PrefixCase`, which provides a comfortable interface to add
new units and quantities to.

`PrefixCase.prefixed_unit` and `.canonical_unit` are the actual `UnitDef` instances
each constructor carries (`MILLIVOLT`, `VOLT`, ...), imported directly from
`kuchka.units`.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest
from hypothesis import given

from kuchka.units import acceleration
from kuchka.units import area
from kuchka.units import charge
from kuchka.units import conductance
from kuchka.units import current
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import mass
from kuchka.units import power
from kuchka.units import resistance
from kuchka.units import sample_rate
from kuchka.units import time
from kuchka.units import voltage
from kuchka.units import volume
from tests.quantity_families import FINITE_DECIMALS

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric
    from kuchka.quantities import LinearQuantity
    from kuchka.quantities.base import UnitDef


@dataclass(frozen=True)
class PrefixCase:
    """One prefix constructor paired with its canonical constructor and both units."""

    id: str
    prefixed: Callable[[Numeric], LinearQuantity]
    canonical: Callable[[Numeric], LinearQuantity]
    scale: Decimal
    prefixed_unit: UnitDef
    canonical_unit: UnitDef


PREFIX_CASES: list[PrefixCase] = [
    PrefixCase(
        "Milligal",
        acceleration.Milligal,
        acceleration.MetrePerSecondSquared,
        Decimal("0.00001"),
        acceleration.MILLIGAL,
        acceleration.METRE_PER_SECOND_SQUARED,
    ),
    PrefixCase(
        "Microgal",
        acceleration.Microgal,
        acceleration.MetrePerSecondSquared,
        Decimal("0.00000001"),
        acceleration.MICROGAL,
        acceleration.METRE_PER_SECOND_SQUARED,
    ),
    PrefixCase(
        "Nanovolt",
        voltage.Nanovolt,
        voltage.Volt,
        Decimal("0.000000001"),
        voltage.NANOVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Microvolt",
        voltage.Microvolt,
        voltage.Volt,
        Decimal("0.000001"),
        voltage.MICROVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Millivolt",
        voltage.Millivolt,
        voltage.Volt,
        Decimal("0.001"),
        voltage.MILLIVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Kilovolt",
        voltage.Kilovolt,
        voltage.Volt,
        Decimal(1000),
        voltage.KILOVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Megavolt",
        voltage.Megavolt,
        voltage.Volt,
        Decimal(1_000_000),
        voltage.MEGAVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Petavolt",
        voltage.Petavolt,
        voltage.Volt,
        Decimal("1e15"),
        voltage.PETAVOLT,
        voltage.VOLT,
    ),
    PrefixCase(
        "Picoampere",
        current.Picoampere,
        current.Ampere,
        Decimal("0.000000000001"),
        current.PICOAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Nanoampere",
        current.Nanoampere,
        current.Ampere,
        Decimal("0.000000001"),
        current.NANOAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Microampere",
        current.Microampere,
        current.Ampere,
        Decimal("0.000001"),
        current.MICROAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Milliampere",
        current.Milliampere,
        current.Ampere,
        Decimal("0.001"),
        current.MILLIAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Kiloampere",
        current.Kiloampere,
        current.Ampere,
        Decimal(1000),
        current.KILOAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Megaampere",
        current.Megaampere,
        current.Ampere,
        Decimal(1_000_000),
        current.MEGAAMPERE,
        current.AMPERE,
    ),
    PrefixCase(
        "Microohm",
        resistance.Microohm,
        resistance.Ohm,
        Decimal("0.000001"),
        resistance.MICROOHM,
        resistance.OHM,
    ),
    PrefixCase(
        "Milliohm",
        resistance.Milliohm,
        resistance.Ohm,
        Decimal("0.001"),
        resistance.MILLIOHM,
        resistance.OHM,
    ),
    PrefixCase(
        "Kiloohm",
        resistance.Kiloohm,
        resistance.Ohm,
        Decimal(1000),
        resistance.KILOOHM,
        resistance.OHM,
    ),
    PrefixCase(
        "Megaohm",
        resistance.Megaohm,
        resistance.Ohm,
        Decimal(1_000_000),
        resistance.MEGAOHM,
        resistance.OHM,
    ),
    PrefixCase(
        "Gigaohm",
        resistance.Gigaohm,
        resistance.Ohm,
        Decimal("1e9"),
        resistance.GIGAOHM,
        resistance.OHM,
    ),
    PrefixCase(
        "Milliwatt",
        power.Milliwatt,
        power.Watt,
        Decimal("0.001"),
        power.MILLIWATT,
        power.WATT,
    ),
    PrefixCase(
        "Kilowatt",
        power.Kilowatt,
        power.Watt,
        Decimal(1000),
        power.KILOWATT,
        power.WATT,
    ),
    PrefixCase(
        "Femtosecond",
        time.Femtosecond,
        time.Second,
        Decimal("0.000000000000001"),
        time.FEMTOSECOND,
        time.SECOND,
    ),
    PrefixCase(
        "Picosecond",
        time.Picosecond,
        time.Second,
        Decimal("0.000000000001"),
        time.PICOSECOND,
        time.SECOND,
    ),
    PrefixCase(
        "Nanosecond",
        time.Nanosecond,
        time.Second,
        Decimal("0.000000001"),
        time.NANOSECOND,
        time.SECOND,
    ),
    PrefixCase(
        "Microsecond",
        time.Microsecond,
        time.Second,
        Decimal("0.000001"),
        time.MICROSECOND,
        time.SECOND,
    ),
    PrefixCase(
        "Millisecond",
        time.Millisecond,
        time.Second,
        Decimal("0.001"),
        time.MILLISECOND,
        time.SECOND,
    ),
    PrefixCase(
        "Kilohertz",
        frequency.Kilohertz,
        frequency.Hertz,
        Decimal(1_000),
        frequency.KILOHERTZ,
        frequency.HERTZ,
    ),
    PrefixCase(
        "Megahertz",
        frequency.Megahertz,
        frequency.Hertz,
        Decimal(1_000_000),
        frequency.MEGAHERTZ,
        frequency.HERTZ,
    ),
    PrefixCase(
        "Gigahertz",
        frequency.Gigahertz,
        frequency.Hertz,
        Decimal("1e9"),
        frequency.GIGAHERTZ,
        frequency.HERTZ,
    ),
    PrefixCase(
        "Terahertz",
        frequency.Terahertz,
        frequency.Hertz,
        Decimal("1e12"),
        frequency.TERAHERTZ,
        frequency.HERTZ,
    ),
    PrefixCase(
        "Petahertz",
        frequency.Petahertz,
        frequency.Hertz,
        Decimal("1e15"),
        frequency.PETAHERTZ,
        frequency.HERTZ,
    ),
    PrefixCase(
        "KilosamplesPerSecond",
        sample_rate.KilosamplesPerSecond,
        sample_rate.SamplesPerSecond,
        Decimal(1000),
        sample_rate.KILOSAMPLES_PER_SECOND,
        sample_rate.SAMPLES_PER_SECOND,
    ),
    PrefixCase(
        "MegasamplesPerSecond",
        sample_rate.MegasamplesPerSecond,
        sample_rate.SamplesPerSecond,
        Decimal(1_000_000),
        sample_rate.MEGASAMPLES_PER_SECOND,
        sample_rate.SAMPLES_PER_SECOND,
    ),
    PrefixCase(
        "Picometer",
        length.Picometer,
        length.Meter,
        Decimal("0.000000000001"),
        length.PICOMETER,
        length.METER,
    ),
    PrefixCase(
        "Nanometer",
        length.Nanometer,
        length.Meter,
        Decimal("0.000000001"),
        length.NANOMETER,
        length.METER,
    ),
    PrefixCase(
        "Micrometer",
        length.Micrometer,
        length.Meter,
        Decimal("0.000001"),
        length.MICROMETER,
        length.METER,
    ),
    PrefixCase(
        "Millimeter",
        length.Millimeter,
        length.Meter,
        Decimal("0.001"),
        length.MILLIMETER,
        length.METER,
    ),
    PrefixCase(
        "Centimeter",
        length.Centimeter,
        length.Meter,
        Decimal("0.01"),
        length.CENTIMETER,
        length.METER,
    ),
    PrefixCase(
        "Decimeter",
        length.Decimeter,
        length.Meter,
        Decimal("0.1"),
        length.DECIMETER,
        length.METER,
    ),
    PrefixCase(
        "Kilometer",
        length.Kilometer,
        length.Meter,
        Decimal(1000),
        length.KILOMETER,
        length.METER,
    ),
    PrefixCase(
        "Inch",
        length.Inch,
        length.Meter,
        Decimal("0.0254"),
        length.INCH,
        length.METER,
    ),
    PrefixCase(
        "Foot",
        length.Foot,
        length.Meter,
        Decimal("0.3048"),
        length.FOOT,
        length.METER,
    ),
    PrefixCase(
        "Yard",
        length.Yard,
        length.Meter,
        Decimal("0.9144"),
        length.YARD,
        length.METER,
    ),
    PrefixCase(
        "Mile",
        length.Mile,
        length.Meter,
        Decimal("1_609.344"),
        length.MILE,
        length.METER,
    ),
    PrefixCase(
        "Nautical Mile",
        length.NauticalMile,
        length.Meter,
        Decimal(1_852),
        length.NAUTICAL_MILE,
        length.METER,
    ),
    PrefixCase(
        "Picogram",
        mass.Picogram,
        mass.Kilogram,
        Decimal("0.000000000000001"),
        mass.PICOGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Nanogram",
        mass.Nanogram,
        mass.Kilogram,
        Decimal("0.000000000001"),
        mass.NANOGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Microgram",
        mass.Microgram,
        mass.Kilogram,
        Decimal("0.000000001"),
        mass.MICROGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Milligram",
        mass.Milligram,
        mass.Kilogram,
        Decimal("0.000001"),
        mass.MILLIGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Gram",
        mass.Gram,
        mass.Kilogram,
        Decimal("0.001"),
        mass.GRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Megagram",
        mass.Megagram,
        mass.Kilogram,
        Decimal(1000),
        mass.MEGAGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Tonne",
        mass.Tonne,
        mass.Kilogram,
        Decimal(1000),
        mass.MEGAGRAM,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Grain",
        mass.Grain,
        mass.Kilogram,
        Decimal("0.00006479891"),
        mass.GRAIN,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Pound",
        mass.Pound,
        mass.Kilogram,
        Decimal("0.45359237"),
        mass.POUND,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Ounce",
        mass.Ounce,
        mass.Kilogram,
        Decimal("0.028349523125"),
        mass.OUNCE,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Dalton",
        mass.Dalton,
        mass.Kilogram,
        Decimal("1.66053906892e-27"),
        mass.DALTON,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "SolarMass",
        mass.SolarMass,
        mass.Kilogram,
        Decimal("1.988416e30"),
        mass.SOLAR_MASS,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "EarthMass",
        mass.EarthMass,
        mass.Kilogram,
        Decimal("5.972168e24"),
        mass.EARTH_MASS,
        mass.KILOGRAM,
    ),
    PrefixCase(
        "Minute",
        time.Minute,
        time.Second,
        Decimal(60),
        time.MINUTE,
        time.SECOND,
    ),
    PrefixCase(
        "Hour",
        time.Hour,
        time.Second,
        Decimal(3600),
        time.HOUR,
        time.SECOND,
    ),
    PrefixCase(
        "WattHour",
        energy.WattHour,
        energy.Joule,
        Decimal(3600),
        energy.WATT_HOUR,
        energy.JOULE,
    ),
    PrefixCase(
        "MilliwattHour",
        energy.MilliwattHour,
        energy.Joule,
        Decimal("3.6"),
        energy.MILLIWATT_HOUR,
        energy.JOULE,
    ),
    PrefixCase(
        "MilliampereSecond",
        charge.MilliampereSecond,
        charge.Coulomb,
        Decimal("0.001"),
        charge.MILLIAMPERE_SECOND,
        charge.COULOMB,
    ),
    PrefixCase(
        "MilliampereHour",
        charge.MilliampereHour,
        charge.Coulomb,
        Decimal("3.6"),
        charge.MILLIAMPERE_HOUR,
        charge.COULOMB,
    ),
    PrefixCase(
        "AmpereHour",
        charge.AmpereHour,
        charge.Coulomb,
        Decimal(3600),
        charge.AMPERE_HOUR,
        charge.COULOMB,
    ),
    PrefixCase(
        "SquareMillimetre",
        area.SquareMillimetre,
        area.SquareMetre,
        Decimal("0.000001"),
        area.SQUARE_MILLIMETRE,
        area.SQUARE_METRE,
    ),
    PrefixCase(
        "SquareCentimetre",
        area.SquareCentimetre,
        area.SquareMetre,
        Decimal("0.0001"),
        area.SQUARE_CENTIMETRE,
        area.SQUARE_METRE,
    ),
    PrefixCase(
        "SquareKilometre",
        area.SquareKilometre,
        area.SquareMetre,
        Decimal(1_000_000),
        area.SQUARE_KILOMETRE,
        area.SQUARE_METRE,
    ),
    PrefixCase(
        "Hectare",
        area.Hectare,
        area.SquareMetre,
        Decimal(10_000),
        area.HECTARE,
        area.SQUARE_METRE,
    ),
    PrefixCase(
        "Acre",
        area.Acre,
        area.SquareMetre,
        Decimal("4046.8564224"),
        area.ACRE,
        area.SQUARE_METRE,
    ),
    PrefixCase(
        "CubicMillimetre",
        volume.CubicMillimetre,
        volume.CubicMetre,
        Decimal("0.000000001"),
        volume.CUBIC_MILLIMETRE,
        volume.CUBIC_METRE,
    ),
    PrefixCase(
        "CubicCentimetre",
        volume.CubicCentimetre,
        volume.CubicMetre,
        Decimal("0.000001"),
        volume.CUBIC_CENTIMETRE,
        volume.CUBIC_METRE,
    ),
    PrefixCase(
        "Microlitre",
        volume.Microlitre,
        volume.Litre,
        Decimal("0.000001"),
        volume.MICROLITRE,
        volume.LITRE,
    ),
    PrefixCase(
        "Millilitre",
        volume.Millilitre,
        volume.Litre,
        Decimal("0.001"),
        volume.MILLILITRE,
        volume.LITRE,
    ),
    PrefixCase(
        "Kilolitre",
        volume.Kilolitre,
        volume.Litre,
        Decimal(1000),
        volume.KILOLITRE,
        volume.LITRE,
    ),
    PrefixCase(
        "Nanosiemens",
        conductance.Nanosiemens,
        conductance.Siemens,
        Decimal("0.000000001"),
        conductance.NANOSIEMENS,
        conductance.SIEMENS,
    ),
    PrefixCase(
        "Microsiemens",
        conductance.Microsiemens,
        conductance.Siemens,
        Decimal("0.000001"),
        conductance.MICROSIEMENS,
        conductance.SIEMENS,
    ),
    PrefixCase(
        "Millisiemens",
        conductance.Millisiemens,
        conductance.Siemens,
        Decimal("0.001"),
        conductance.MILLISIEMENS,
        conductance.SIEMENS,
    ),
    PrefixCase(
        "Kilosiemens",
        conductance.Kilosiemens,
        conductance.Siemens,
        Decimal(1000),
        conductance.KILOSIEMENS,
        conductance.SIEMENS,
    ),
    PrefixCase(
        "Gigajoule",
        energy.Gigajoule,
        energy.Joule,
        Decimal(1_000_000_000),
        energy.GIGAJOULE,
        energy.JOULE,
    ),
    PrefixCase(
        "Terajoule",
        energy.Terajoule,
        energy.Joule,
        Decimal(1_000_000_000_000),
        energy.TERAJOULE,
        energy.JOULE,
    ),
    PrefixCase(
        "Petajoule",
        energy.Petajoule,
        energy.Joule,
        Decimal(1_000_000_000_000_000),
        energy.PETAJOULE,
        energy.JOULE,
    ),
    PrefixCase(
        "Microelectronvolt",
        energy.Microelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-25"),
        energy.MICROELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Millielectronvolt",
        energy.Millielectronvolt,
        energy.Joule,
        Decimal("1.602176634e-22"),
        energy.MILLIELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Electronvolt",
        energy.Electronvolt,
        energy.Joule,
        Decimal("1.602176634e-19"),
        energy.ELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Kiloelectronvolt",
        energy.Kiloelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-16"),
        energy.KILOELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Megaelectronvolt",
        energy.Megaelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-13"),
        energy.MEGAELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Gigaelectronvolt",
        energy.Gigaelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-10"),
        energy.GIGAELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Teraelectronvolt",
        energy.Teraelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-7"),
        energy.TERAELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Petaelectronvolt",
        energy.Petaelectronvolt,
        energy.Joule,
        Decimal("1.602176634e-4"),
        energy.PETAELECTRONVOLT,
        energy.JOULE,
    ),
    PrefixCase(
        "Erg",
        energy.Erg,
        energy.Joule,
        Decimal("1E-7"),
        energy.ERG,
        energy.JOULE,
    ),
    PrefixCase(
        "Calorie",
        energy.Calorie,
        energy.Joule,
        Decimal(4184),
        energy.KILOCALORIE,
        energy.JOULE,
    ),
    PrefixCase(
        "ThermochemicalCalorie",
        energy.ThermochemicalCalorie,
        energy.Joule,
        Decimal("4.184"),
        energy.THERMOCHEMICAL_CALORIE,
        energy.JOULE,
    ),
    PrefixCase(
        "Micronewton",
        force.Micronewton,
        force.Newton,
        Decimal("0.000001"),
        force.MICRONEWTON,
        force.NEWTON,
    ),
    PrefixCase(
        "Millinewton",
        force.Millinewton,
        force.Newton,
        Decimal("0.001"),
        force.MILLINEWTON,
        force.NEWTON,
    ),
    PrefixCase(
        "Kilonewton",
        force.Kilonewton,
        force.Newton,
        Decimal(1000),
        force.KILONEWTON,
        force.NEWTON,
    ),
    PrefixCase(
        "Meganewton",
        force.Meganewton,
        force.Newton,
        Decimal(1_000_000),
        force.MEGANEWTON,
        force.NEWTON,
    ),
]

PREFIX_CASE_IDS: list[str] = [case.id for case in PREFIX_CASES]


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
def test_prefix_scales_into_the_canonical_unit(case: PrefixCase) -> None:
    assert case.prefixed(1) == case.canonical(case.scale)
    assert case.prefixed(1).unit is case.prefixed_unit
    assert case.canonical(1).unit is case.canonical_unit


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
@given(magnitude=FINITE_DECIMALS)
def test_prefix_scale_is_exact_across_a_range_of_magnitudes(
    case: PrefixCase,
    magnitude: Decimal,
) -> None:
    assert case.prefixed(magnitude) == case.canonical(
        Fraction(magnitude) * Fraction(case.scale)
    )


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
def test_round_trip_conversion_through_to(case: PrefixCase) -> None:
    """Converting a canonical-unit value down and back up preserves the value."""
    original = case.canonical(1)
    converted = original.to(case.prefixed_unit)
    assert converted == original
    assert converted.unit is case.prefixed_unit
    assert converted.value_in(case.prefixed_unit) == 1 / Fraction(case.scale)
    assert converted.to(case.canonical_unit) == original


def test_unit_def_repr_shows_name_and_symbol() -> None:
    assert repr(voltage.Volt(1).unit) == "UnitDef('volt', 'V')"
