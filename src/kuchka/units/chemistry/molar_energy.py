"""Molar energy constructors: joules, kilojoules, and kilocalories per mole.

Molar energy is the energy per mole of a substance, as a reaction enthalpy or a bond
energy is quoted: `1 J/mol` is the canonical unit.
Chemistry reads it in `kJ/mol` and, in older tables, in `kcal/mol`, the thermochemical
kilocalorie of 4184 joules.

`MOLAR_ENERGY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_ENERGY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarEnergy
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.energy import KILOCALORIE
from kuchka.units.mechanics.energy import KILOJOULE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

JOULE_PER_MOLE = UnitDef(
    "joule_per_mole",
    "J/mol",
    1,
    MOLAR_ENERGY,
    words=("joule per mole", "joules per mole"),
)
KILOJOULE_PER_MOLE = UnitDef(
    "kilojoule_per_mole",
    "kJ/mol",
    KILOJOULE.scale,
    MOLAR_ENERGY,
    words=("kilojoule per mole", "kilojoules per mole"),
)
KILOCALORIE_PER_MOLE = UnitDef(
    "kilocalorie_per_mole",
    "kcal/mol",
    KILOCALORIE.scale,
    MOLAR_ENERGY,
    words=("kilocalorie per mole", "kilocalories per mole"),
)

MolarEnergy._canonical_unit = JOULE_PER_MOLE  # noqa: SLF001 -- this module owns MolarEnergy's canonical unit


def JoulePerMole(value: Numeric) -> MolarEnergy:
    """Construct a molar energy from a magnitude in joules per mole.

    Parameters
    ----------
    value : Numeric
        Molar energy magnitude in J/mol.

    Returns
    -------
    MolarEnergy
        Molar energy represented in joules per mole.

    """
    return MolarEnergy(to_exact(value) * JOULE_PER_MOLE.scale, JOULE_PER_MOLE)


def KilojoulePerMole(value: Numeric) -> MolarEnergy:
    """Construct a molar energy from a magnitude in kilojoules per mole.

    Parameters
    ----------
    value : Numeric
        Molar energy magnitude in kJ/mol.

    Returns
    -------
    MolarEnergy
        Molar energy represented in kilojoules per mole.

    Examples
    --------
    Burning a mole of methane releases 890 kJ, so 2 mol of it releases:

    >>> from kuchka import Mole
    >>> from kuchka.units import KILOJOULE
    >>> (KilojoulePerMole(890) * Mole(2)).to(KILOJOULE)
    1780 kJ

    """
    return MolarEnergy(to_exact(value) * KILOJOULE_PER_MOLE.scale, KILOJOULE_PER_MOLE)


def KilocaloriePerMole(value: Numeric) -> MolarEnergy:
    """Construct a molar energy from a magnitude in kilocalories per mole.

    Parameters
    ----------
    value : Numeric
        Molar energy magnitude in kcal/mol.

    Returns
    -------
    MolarEnergy
        Molar energy represented in kilocalories per mole.

    Examples
    --------
    >>> KilocaloriePerMole(1).to(KILOJOULE_PER_MOLE)
    4.184 kJ/mol

    """
    return MolarEnergy(
        to_exact(value) * KILOCALORIE_PER_MOLE.scale, KILOCALORIE_PER_MOLE
    )


MOLAR_ENERGY_UNITS: Mapping[str, Callable[[Numeric], MolarEnergy]] = unit_table(
    "MOLAR_ENERGY_UNITS",
    {
        JOULE_PER_MOLE: JoulePerMole,
        KILOJOULE_PER_MOLE: KilojoulePerMole,
        KILOCALORIE_PER_MOLE: KilocaloriePerMole,
    },
)

__all__ = [
    "JOULE_PER_MOLE",
    "KILOCALORIE_PER_MOLE",
    "KILOJOULE_PER_MOLE",
    "MOLAR_ENERGY_UNITS",
    "JoulePerMole",
    "KilocaloriePerMole",
    "KilojoulePerMole",
]
