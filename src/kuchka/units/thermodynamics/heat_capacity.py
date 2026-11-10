"""Heat capacity constructors: joules, kilojoules, and calories per kelvin.

    from kuchka import JoulePerKelvin, KilojoulePerKelvin

    kettle = KilojoulePerKelvin(1.2)
    block = JoulePerKelvin(385)

`HeatCapacity` is the energy that changes a body's temperature by one degree,
`Energy / TemperatureDelta`.
Its canonical unit is the joule per kelvin (`J/K`), which is also the unit of `Entropy`.
The calorie and kilocalorie per kelvin are the thermochemical ones, as a calorimeter is
rated in.
A degree Celsius in the denominator is a difference, so `J/°C` is the same unit.

Examples
--------
A kettle with a heat capacity of 1.2 kJ/K, in joules per kelvin:

>>> KilojoulePerKelvin(1.2).to(JOULE_PER_KELVIN)
1200 J/K

The heat to warm it by 80 K is a heat capacity times a temperature difference:

>>> from kuchka import DeltaKelvin
>>> from kuchka.units.mechanics.energy import KILOJOULE
>>> (KilojoulePerKelvin(1.2) * DeltaKelvin(80)).to(KILOJOULE)
96 kJ

`HEAT_CAPACITY_UNITS` maps symbols such as ``"J/K"``, ``"kJ/K"``, and ``"J/degC"`` to
their constructors for boundary code that reads unit labels from external data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import HEAT_CAPACITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import HeatCapacity
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.energy import JOULE
from kuchka.units.mechanics.energy import KILOCALORIE
from kuchka.units.mechanics.energy import KILOJOULE
from kuchka.units.mechanics.energy import THERMOCHEMICAL_CALORIE

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric

JOULE_PER_KELVIN = UnitDef(
    "joule_per_kelvin",
    "J/K",
    JOULE.scale,
    HEAT_CAPACITY,
    aliases=("J/°C", "J/degC", "J/C"),
    words=("joules per kelvin", "joule per kelvin"),
)
KILOJOULE_PER_KELVIN = UnitDef(
    "kilojoule_per_kelvin",
    "kJ/K",
    KILOJOULE.scale,
    HEAT_CAPACITY,
    aliases=("kJ/°C", "kJ/degC", "kJ/C"),
    words=("kilojoules per kelvin", "kilojoule per kelvin"),
)

HeatCapacity._canonical_unit = JOULE_PER_KELVIN  # noqa: SLF001 -- this module owns HeatCapacity's canonical unit

THERMOCHEMICAL_CALORIE_PER_KELVIN = UnitDef(
    "thermochemical_calorie_per_kelvin",
    "cal/K",
    THERMOCHEMICAL_CALORIE.scale,
    HEAT_CAPACITY,
    aliases=("cal/\u00b0C", "cal/degC", "cal/C"),
    words=("calories per kelvin", "calorie per kelvin"),
)
KILOCALORIE_PER_KELVIN = UnitDef(
    "kilocalorie_per_kelvin",
    "kcal/K",
    KILOCALORIE.scale,
    HEAT_CAPACITY,
    aliases=("kcal/\u00b0C", "kcal/degC", "kcal/C"),
    words=("kilocalories per kelvin", "kilocalorie per kelvin"),
)


def JoulePerKelvin(value: Numeric) -> HeatCapacity:
    """Construct a HeatCapacity from a magnitude in joules per kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in joules per kelvin.

    Returns
    -------
    HeatCapacity
        HeatCapacity represented in joules per kelvin.

    """
    return HeatCapacity(to_exact(value) * JOULE_PER_KELVIN.scale, JOULE_PER_KELVIN)


def KilojoulePerKelvin(value: Numeric) -> HeatCapacity:
    """Construct a HeatCapacity from a magnitude in kilojoules per kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilojoules per kelvin.

    Returns
    -------
    HeatCapacity
        HeatCapacity represented in kilojoules per kelvin.

    """
    return HeatCapacity(
        to_exact(value) * KILOJOULE_PER_KELVIN.scale, KILOJOULE_PER_KELVIN
    )


def ThermochemicalCaloriePerKelvin(value: Numeric) -> HeatCapacity:
    """Construct a HeatCapacity from a magnitude in thermochemical calories per kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in thermochemical calories per kelvin.

    Returns
    -------
    HeatCapacity
        HeatCapacity represented in thermochemical calories per kelvin.

    """
    return HeatCapacity(
        to_exact(value) * THERMOCHEMICAL_CALORIE_PER_KELVIN.scale,
        THERMOCHEMICAL_CALORIE_PER_KELVIN,
    )


def KilocaloriePerKelvin(value: Numeric) -> HeatCapacity:
    """Construct a HeatCapacity from a magnitude in kilocalories per kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilocalories per kelvin.

    Returns
    -------
    HeatCapacity
        HeatCapacity represented in kilocalories per kelvin.

    """
    return HeatCapacity(
        to_exact(value) * KILOCALORIE_PER_KELVIN.scale, KILOCALORIE_PER_KELVIN
    )


HEAT_CAPACITY_UNITS: UnitTable[HeatCapacity] = unit_table(
    "HEAT_CAPACITY_UNITS",
    {
        JOULE_PER_KELVIN: JoulePerKelvin,
        KILOJOULE_PER_KELVIN: KilojoulePerKelvin,
        THERMOCHEMICAL_CALORIE_PER_KELVIN: ThermochemicalCaloriePerKelvin,
        KILOCALORIE_PER_KELVIN: KilocaloriePerKelvin,
    },
)

__all__ = [
    "HEAT_CAPACITY_UNITS",
    "JOULE_PER_KELVIN",
    "KILOCALORIE_PER_KELVIN",
    "KILOJOULE_PER_KELVIN",
    "THERMOCHEMICAL_CALORIE_PER_KELVIN",
    "JoulePerKelvin",
    "KilocaloriePerKelvin",
    "KilojoulePerKelvin",
    "ThermochemicalCaloriePerKelvin",
]
