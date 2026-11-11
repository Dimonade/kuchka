"""Specific heat capacity constructors: joules and calories per kilogram kelvin.

    from kuchka import KilojoulePerKilogramKelvin

    water = KilojoulePerKilogramKelvin(4.184)

`SpecificHeatCapacity` is the energy per unit mass that changes a temperature by one
degree, `SpecificEnergy / TemperatureDelta`.
Its canonical unit is the joule per kilogram kelvin (`J/(kg·K)`).
The calorie per gram kelvin is the thermochemical calorie, so it is exactly
4184 J/(kg·K), and water's famous 1 cal/(g·K) is 4.184 kJ/(kg·K).
A degree Celsius in the denominator is a difference, so `J/(kg·°C)` is the same unit.

Examples
--------
Water, in the calorie unit:

>>> KilojoulePerKilogramKelvin(4.184).to(THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN)
1 cal/(g·K)

The heat to warm 2 kg of water by 30 K, grouped either way:

>>> from kuchka import DeltaKelvin
>>> from kuchka import Kilogram
>>> from kuchka.units import KILOJOULE
>>> water = KilojoulePerKilogramKelvin(4.184)
>>> (water * Kilogram(2) * DeltaKelvin(30)).to(KILOJOULE)
251.04 kJ
>>> (water * DeltaKelvin(30) * Kilogram(2)).to(KILOJOULE)
251.04 kJ

`SPECIFIC_HEAT_CAPACITY_UNITS` maps symbols such as ``"J/(kg K)"``, ``"kJ/kg/K"``, and
``"cal/(g K)"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_HEAT_CAPACITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificHeatCapacity
from kuchka.quantities import UnitDef
from kuchka.units.mass import GRAM
from kuchka.units.mass import KILOGRAM
from kuchka.units.mechanics.energy import JOULE
from kuchka.units.mechanics.energy import KILOJOULE
from kuchka.units.mechanics.energy import THERMOCHEMICAL_CALORIE

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric

JOULE_PER_KILOGRAM_KELVIN = UnitDef(
    "joule_per_kilogram_kelvin",
    "J/(kg·K)",
    JOULE.scale / KILOGRAM.scale,
    SPECIFIC_HEAT_CAPACITY,
    aliases=(
        "J/(kg K)",
        "J/(kg*K)",
        "J/kg/K",
        "J/(kg·°C)",
        "J/(kg °C)",
        "J/(kg*°C)",
        "J/kg/°C",
        "J/(kg degC)",
        "J/(kg·degC)",
    ),
    words=("joules per kilogram kelvin", "joule per kilogram kelvin"),
)
KILOJOULE_PER_KILOGRAM_KELVIN = UnitDef(
    "kilojoule_per_kilogram_kelvin",
    "kJ/(kg·K)",
    KILOJOULE.scale / KILOGRAM.scale,
    SPECIFIC_HEAT_CAPACITY,
    aliases=(
        "kJ/(kg K)",
        "kJ/(kg*K)",
        "kJ/kg/K",
        "kJ/(kg·°C)",
        "kJ/(kg °C)",
        "kJ/(kg*°C)",
        "kJ/kg/°C",
        "kJ/(kg degC)",
        "kJ/(kg·degC)",
    ),
    words=("kilojoules per kilogram kelvin", "kilojoule per kilogram kelvin"),
)
THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN = UnitDef(
    "thermochemical_calorie_per_gram_kelvin",
    "cal/(g·K)",
    THERMOCHEMICAL_CALORIE.scale / GRAM.scale,
    SPECIFIC_HEAT_CAPACITY,
    aliases=(
        "cal/(g K)",
        "cal/(g*K)",
        "cal/g/K",
        "cal/(g·°C)",
        "cal/(g °C)",
        "cal/(g*°C)",
        "cal/g/°C",
        "cal/(g degC)",
        "cal/(g·degC)",
    ),
    words=("calories per gram kelvin", "calorie per gram kelvin"),
)

SpecificHeatCapacity._canonical_unit = JOULE_PER_KILOGRAM_KELVIN  # noqa: SLF001 -- this module owns SpecificHeatCapacity's canonical unit


def JoulePerKilogramKelvin(value: Numeric) -> SpecificHeatCapacity:
    """Construct a SpecificHeatCapacity from a magnitude in joules per kilogram kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in joules per kilogram kelvin.

    Returns
    -------
    SpecificHeatCapacity
        SpecificHeatCapacity represented in joules per kilogram kelvin.

    """
    return SpecificHeatCapacity(
        to_exact(value) * JOULE_PER_KILOGRAM_KELVIN.scale, JOULE_PER_KILOGRAM_KELVIN
    )


def KilojoulePerKilogramKelvin(value: Numeric) -> SpecificHeatCapacity:
    """Construct a SpecificHeatCapacity in kilojoules per kilogram kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilojoules per kilogram kelvin.

    Returns
    -------
    SpecificHeatCapacity
        SpecificHeatCapacity represented in kilojoules per kilogram kelvin.

    """
    return SpecificHeatCapacity(
        to_exact(value) * KILOJOULE_PER_KILOGRAM_KELVIN.scale,
        KILOJOULE_PER_KILOGRAM_KELVIN,
    )


def ThermochemicalCaloriePerGramKelvin(value: Numeric) -> SpecificHeatCapacity:
    """Construct a SpecificHeatCapacity in thermochemical calories per gram kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in thermochemical calories per gram kelvin.

    Returns
    -------
    SpecificHeatCapacity
        SpecificHeatCapacity represented in thermochemical calories per gram kelvin.

    """
    return SpecificHeatCapacity(
        to_exact(value) * THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN.scale,
        THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN,
    )


SPECIFIC_HEAT_CAPACITY_UNITS: UnitTable[SpecificHeatCapacity] = unit_table(
    "SPECIFIC_HEAT_CAPACITY_UNITS",
    {
        JOULE_PER_KILOGRAM_KELVIN: JoulePerKilogramKelvin,
        KILOJOULE_PER_KILOGRAM_KELVIN: KilojoulePerKilogramKelvin,
        THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN: ThermochemicalCaloriePerGramKelvin,
    },
)

__all__ = [
    "JOULE_PER_KILOGRAM_KELVIN",
    "KILOJOULE_PER_KILOGRAM_KELVIN",
    "SPECIFIC_HEAT_CAPACITY_UNITS",
    "THERMOCHEMICAL_CALORIE_PER_GRAM_KELVIN",
    "JoulePerKilogramKelvin",
    "KilojoulePerKilogramKelvin",
    "ThermochemicalCaloriePerGramKelvin",
]
