"""Specific energy constructors: joules, watt-hours, and kilocalories per mass.

    from kuchka import MegajoulePerKilogram
    from kuchka import WattHourPerKilogram

    diesel = MegajoulePerKilogram(43)
    battery_cell = WattHourPerKilogram(250)

`WattHourPerKilogram` is the unit gravimetric battery capacity is quoted in, and
`KilocaloriePerKilogram` the unit of food energy per mass.
Their scales come from the exact scales of the energy units, so one watt-hour per
kilogram is exactly `3600` J/kg and one kilocalorie per kilogram exactly `4184` J/kg.

`SPECIFIC_ENERGY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificEnergy
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.energy import KILOCALORIE
from kuchka.units.mechanics.energy import KILOWATT_HOUR
from kuchka.units.mechanics.energy import WATT_HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

JOULE_PER_KILOGRAM = UnitDef(
    "joule_per_kilogram",
    "J/kg",
    Decimal(1),
    SPECIFIC_ENERGY,
    words=("joules per kilogram",),
)
KILOJOULE_PER_KILOGRAM = UnitDef(
    "kilojoule_per_kilogram",
    "kJ/kg",
    Decimal(1000),
    SPECIFIC_ENERGY,
    words=("kilojoules per kilogram",),
)
MEGAJOULE_PER_KILOGRAM = UnitDef(
    "megajoule_per_kilogram",
    "MJ/kg",
    Decimal(1_000_000),
    SPECIFIC_ENERGY,
    words=("megajoules per kilogram",),
)
JOULE_PER_GRAM = UnitDef(
    "joule_per_gram",
    "J/g",
    Decimal(1000),
    SPECIFIC_ENERGY,
    words=("joules per gram",),
)
WATT_HOUR_PER_KILOGRAM = UnitDef(
    "watt_hour_per_kilogram",
    "Wh/kg",
    WATT_HOUR.scale,
    SPECIFIC_ENERGY,
    aliases=("wh/kg",),
    words=("watt-hours per kilogram",),
)
KILOWATT_HOUR_PER_KILOGRAM = UnitDef(
    "kilowatt_hour_per_kilogram",
    "kWh/kg",
    KILOWATT_HOUR.scale,
    SPECIFIC_ENERGY,
    aliases=("kwh/kg",),
    words=("kilowatt-hours per kilogram",),
)
KILOCALORIE_PER_KILOGRAM = UnitDef(
    "kilocalorie_per_kilogram",
    "kcal/kg",
    KILOCALORIE.scale,
    SPECIFIC_ENERGY,
    aliases=("Cal/kg",),
    words=("kilocalories per kilogram",),
)

SpecificEnergy._canonical_unit = JOULE_PER_KILOGRAM  # noqa: SLF001 -- this module owns SpecificEnergy's canonical unit


def JoulePerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in joules per kilogram."""
    return SpecificEnergy(
        to_exact(value) * JOULE_PER_KILOGRAM.scale, JOULE_PER_KILOGRAM
    )


def KilojoulePerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in kilojoules per kilogram."""
    return SpecificEnergy(
        to_exact(value) * KILOJOULE_PER_KILOGRAM.scale, KILOJOULE_PER_KILOGRAM
    )


def MegajoulePerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in megajoules per kilogram."""
    return SpecificEnergy(
        to_exact(value) * MEGAJOULE_PER_KILOGRAM.scale, MEGAJOULE_PER_KILOGRAM
    )


def JoulePerGram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in joules per gram."""
    return SpecificEnergy(to_exact(value) * JOULE_PER_GRAM.scale, JOULE_PER_GRAM)


def WattHourPerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in watt-hours per kilogram."""
    return SpecificEnergy(
        to_exact(value) * WATT_HOUR_PER_KILOGRAM.scale, WATT_HOUR_PER_KILOGRAM
    )


def KilowattHourPerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in kilowatt-hours per kilogram."""
    return SpecificEnergy(
        to_exact(value) * KILOWATT_HOUR_PER_KILOGRAM.scale, KILOWATT_HOUR_PER_KILOGRAM
    )


def KilocaloriePerKilogram(value: Numeric) -> SpecificEnergy:
    """Construct a SpecificEnergy from a magnitude in kilocalories per kilogram."""
    return SpecificEnergy(
        to_exact(value) * KILOCALORIE_PER_KILOGRAM.scale, KILOCALORIE_PER_KILOGRAM
    )


SPECIFIC_ENERGY_UNITS: Mapping[str, Callable[[Numeric], SpecificEnergy]] = unit_table(
    "SPECIFIC_ENERGY_UNITS",
    {
        JOULE_PER_KILOGRAM: JoulePerKilogram,
        KILOJOULE_PER_KILOGRAM: KilojoulePerKilogram,
        MEGAJOULE_PER_KILOGRAM: MegajoulePerKilogram,
        JOULE_PER_GRAM: JoulePerGram,
        WATT_HOUR_PER_KILOGRAM: WattHourPerKilogram,
        KILOWATT_HOUR_PER_KILOGRAM: KilowattHourPerKilogram,
        KILOCALORIE_PER_KILOGRAM: KilocaloriePerKilogram,
    },
)

SPECIFIC_ENERGY_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        JOULE_PER_KILOGRAM,
        KILOJOULE_PER_KILOGRAM,
        MEGAJOULE_PER_KILOGRAM,
    ),
    (
        WATT_HOUR_PER_KILOGRAM,
        KILOWATT_HOUR_PER_KILOGRAM,
    ),
)
"""The runs of units `auto_scale` moves a specific energy along.

There is one run for each family of prefixed units, smallest first.
"""

__all__ = [
    "JOULE_PER_GRAM",
    "JOULE_PER_KILOGRAM",
    "KILOCALORIE_PER_KILOGRAM",
    "KILOJOULE_PER_KILOGRAM",
    "KILOWATT_HOUR_PER_KILOGRAM",
    "MEGAJOULE_PER_KILOGRAM",
    "SPECIFIC_ENERGY_LADDERS",
    "SPECIFIC_ENERGY_UNITS",
    "WATT_HOUR_PER_KILOGRAM",
    "JoulePerGram",
    "JoulePerKilogram",
    "KilocaloriePerKilogram",
    "KilojoulePerKilogram",
    "KilowattHourPerKilogram",
    "MegajoulePerKilogram",
    "WattHourPerKilogram",
]
