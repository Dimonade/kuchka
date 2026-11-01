"""Molar mass constructors: KilogramPerMole, GramPerMole, and KilogramPerKilomole.

Molar mass is the mass of one mole of a substance: `1 kg/mol` is the canonical unit.
Chemists write it in `g/mol`, and a molecule's molar mass in `g/mol` has the same number
as its mass in daltons, which is a mass and not a molar mass: no spelling of the dalton
(`Da`, `u`) is a molar mass unit.
Process engineers write `kg/kmol`, which has the same value as `g/mol`.

`MOLAR_MASS_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_MASS
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarMass
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

KILOGRAM_PER_MOLE = UnitDef(
    "kilogram_per_mole",
    "kg/mol",
    1,
    MOLAR_MASS,
    words=("kilogram per mole", "kilograms per mole"),
)
GRAM_PER_MOLE = UnitDef(
    "gram_per_mole",
    "g/mol",
    Fraction(1, 1000),
    MOLAR_MASS,
    words=("gram per mole", "grams per mole"),
)
KILOGRAM_PER_KILOMOLE = UnitDef(
    "kilogram_per_kilomole",
    "kg/kmol",
    Fraction(1, 1000),
    MOLAR_MASS,
    words=("kilogram per kilomole", "kilograms per kilomole"),
)

MolarMass._canonical_unit = KILOGRAM_PER_MOLE  # noqa: SLF001 -- this module owns MolarMass's canonical unit


def KilogramPerMole(value: Numeric) -> MolarMass:
    """Construct a molar mass from a magnitude in kilograms per mole.

    Parameters
    ----------
    value : Numeric
        Molar mass magnitude in kg/mol.

    Returns
    -------
    MolarMass
        Molar mass represented in kilograms per mole.

    """
    return MolarMass(to_exact(value) * KILOGRAM_PER_MOLE.scale, KILOGRAM_PER_MOLE)


def GramPerMole(value: Numeric) -> MolarMass:
    """Construct a molar mass from a magnitude in grams per mole.

    Parameters
    ----------
    value : Numeric
        Molar mass magnitude in g/mol.

    Returns
    -------
    MolarMass
        Molar mass represented in grams per mole.

    Examples
    --------
    Water has a molar mass of 18.015 g/mol, so 90.075 g of it is 5 mol:

    >>> from kuchka import Gram
    >>> Gram(90.075) / GramPerMole(18.015)
    5 mol

    """
    return MolarMass(to_exact(value) * GRAM_PER_MOLE.scale, GRAM_PER_MOLE)


def KilogramPerKilomole(value: Numeric) -> MolarMass:
    """Construct a molar mass from a magnitude in kilograms per kilomole.

    Parameters
    ----------
    value : Numeric
        Molar mass magnitude in kg/kmol.

    Returns
    -------
    MolarMass
        Molar mass represented in kilograms per kilomole.

    Examples
    --------
    >>> KilogramPerKilomole(44).to(GRAM_PER_MOLE)
    44 g/mol

    """
    return MolarMass(
        to_exact(value) * KILOGRAM_PER_KILOMOLE.scale, KILOGRAM_PER_KILOMOLE
    )


MOLAR_MASS_UNITS: Mapping[str, Callable[[Numeric], MolarMass]] = unit_table(
    "MOLAR_MASS_UNITS",
    {
        KILOGRAM_PER_MOLE: KilogramPerMole,
        GRAM_PER_MOLE: GramPerMole,
        KILOGRAM_PER_KILOMOLE: KilogramPerKilomole,
    },
)

__all__ = [
    "GRAM_PER_MOLE",
    "KILOGRAM_PER_KILOMOLE",
    "KILOGRAM_PER_MOLE",
    "MOLAR_MASS_UNITS",
    "GramPerMole",
    "KilogramPerKilomole",
    "KilogramPerMole",
]
