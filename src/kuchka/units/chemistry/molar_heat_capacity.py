"""Molar heat capacity constructors: joules and calories per mole kelvin.

    from kuchka import JoulePerMoleKelvin, KilojoulePerMoleKelvin

    helium = JoulePerMoleKelvin(12.47)
    water = JoulePerMoleKelvin(75.3)

`MolarHeatCapacity` is the energy that changes the temperature of one mole by one
degree, `HeatCapacity / AmountOfSubstance`.
Its canonical unit is the joule per mole kelvin (`J/(mol·K)`), which is also the unit of
`MolarEntropy`.
The calorie per mole kelvin is the thermochemical calorie, so it is exactly
4.184 J/(mol·K), and it is the classical "entropy unit" of chemistry tables.
A degree Celsius in the denominator is a difference, so `J/(mol·°C)` is the same unit.

Examples
--------
A monatomic ideal gas has a heat capacity of 3/2 R at constant volume.
In calories per mole kelvin:

>>> JoulePerMoleKelvin(12.47).to(THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN)
2.980401529636711281070745698 cal/(mol·K)

The heat to warm 2 mol by 10 K, grouped either way:

>>> from kuchka import AmountOfSubstance, DeltaKelvin
>>> from kuchka.units import JOULE
>>> from kuchka.units import Mole
>>> (JoulePerMoleKelvin(12.5) * Mole(2) * DeltaKelvin(10)).to(JOULE)
250 J

`MOLAR_HEAT_CAPACITY_UNITS` maps symbols such as ``"J/(mol K)"``, ``"kJ/mol/K"``, and
``"cal/(mol K)"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_HEAT_CAPACITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarHeatCapacity
from kuchka.quantities import UnitDef
from kuchka.units.amount import MOLE
from kuchka.units.mechanics.energy import JOULE
from kuchka.units.mechanics.energy import KILOJOULE
from kuchka.units.mechanics.energy import THERMOCHEMICAL_CALORIE

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric

JOULE_PER_MOLE_KELVIN = UnitDef(
    "joule_per_mole_kelvin",
    "J/(mol·K)",
    JOULE.scale / MOLE.scale,
    MOLAR_HEAT_CAPACITY,
    aliases=(
        "J/(mol K)",
        "J/(mol*K)",
        "J/mol/K",
        "J/(mol·°C)",
        "J/(mol °C)",
        "J/(mol*°C)",
        "J/mol/°C",
        "J/(mol degC)",
        "J/(mol·degC)",
    ),
    words=("joules per mole kelvin", "joule per mole kelvin"),
)
KILOJOULE_PER_MOLE_KELVIN = UnitDef(
    "kilojoule_per_mole_kelvin",
    "kJ/(mol·K)",
    KILOJOULE.scale / MOLE.scale,
    MOLAR_HEAT_CAPACITY,
    aliases=(
        "kJ/(mol K)",
        "kJ/(mol*K)",
        "kJ/mol/K",
        "kJ/(mol·°C)",
        "kJ/(mol °C)",
        "kJ/(mol*°C)",
        "kJ/mol/°C",
        "kJ/(mol degC)",
        "kJ/(mol·degC)",
    ),
    words=("kilojoules per mole kelvin", "kilojoule per mole kelvin"),
)
THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN = UnitDef(
    "thermochemical_calorie_per_mole_kelvin",
    "cal/(mol·K)",
    THERMOCHEMICAL_CALORIE.scale / MOLE.scale,
    MOLAR_HEAT_CAPACITY,
    aliases=(
        "cal/(mol K)",
        "cal/(mol*K)",
        "cal/mol/K",
        "cal/(mol·°C)",
        "cal/(mol °C)",
        "cal/(mol*°C)",
        "cal/mol/°C",
        "cal/(mol degC)",
        "cal/(mol·degC)",
    ),
    words=("calories per mole kelvin", "calorie per mole kelvin"),
)

MolarHeatCapacity._canonical_unit = JOULE_PER_MOLE_KELVIN  # noqa: SLF001 -- this module owns MolarHeatCapacity's canonical unit


def JoulePerMoleKelvin(value: Numeric) -> MolarHeatCapacity:
    """Construct a MolarHeatCapacity from a magnitude in joules per mole kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in joules per mole kelvin.

    Returns
    -------
    MolarHeatCapacity
        MolarHeatCapacity represented in joules per mole kelvin.

    """
    return MolarHeatCapacity(
        to_exact(value) * JOULE_PER_MOLE_KELVIN.scale, JOULE_PER_MOLE_KELVIN
    )


def KilojoulePerMoleKelvin(value: Numeric) -> MolarHeatCapacity:
    """Construct a MolarHeatCapacity from a magnitude in kilojoules per mole kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilojoules per mole kelvin.

    Returns
    -------
    MolarHeatCapacity
        MolarHeatCapacity represented in kilojoules per mole kelvin.

    """
    return MolarHeatCapacity(
        to_exact(value) * KILOJOULE_PER_MOLE_KELVIN.scale, KILOJOULE_PER_MOLE_KELVIN
    )


def ThermochemicalCaloriePerMoleKelvin(value: Numeric) -> MolarHeatCapacity:
    """Construct a MolarHeatCapacity in thermochemical calories per mole kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in thermochemical calories per mole kelvin.

    Returns
    -------
    MolarHeatCapacity
        MolarHeatCapacity represented in thermochemical calories per mole kelvin.

    """
    return MolarHeatCapacity(
        to_exact(value) * THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN.scale,
        THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN,
    )


MOLAR_HEAT_CAPACITY_UNITS: UnitTable[MolarHeatCapacity] = unit_table(
    "MOLAR_HEAT_CAPACITY_UNITS",
    {
        JOULE_PER_MOLE_KELVIN: JoulePerMoleKelvin,
        KILOJOULE_PER_MOLE_KELVIN: KilojoulePerMoleKelvin,
        THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN: ThermochemicalCaloriePerMoleKelvin,
    },
)

__all__ = [
    "JOULE_PER_MOLE_KELVIN",
    "KILOJOULE_PER_MOLE_KELVIN",
    "MOLAR_HEAT_CAPACITY_UNITS",
    "THERMOCHEMICAL_CALORIE_PER_MOLE_KELVIN",
    "JoulePerMoleKelvin",
    "KilojoulePerMoleKelvin",
    "ThermochemicalCaloriePerMoleKelvin",
]
