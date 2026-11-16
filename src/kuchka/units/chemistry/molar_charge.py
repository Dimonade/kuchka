"""Molar charge constructors: coulombs and kilocoulombs per mole.

Molar charge is the electric charge carried by one mole of a substance: `1 C/mol` is the
canonical unit.
The Faraday constant is the charge of one mole of electrons, about `96.485 kC/mol`, and
turns a charge passed through a cell into an amount of substance.

`MOLAR_CHARGE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_CHARGE
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarCharge
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

COULOMB_PER_MOLE = UnitDef(
    "coulomb_per_mole",
    "C/mol",
    1,
    MOLAR_CHARGE,
    words=("coulomb per mole", "coulombs per mole"),
)
KILOCOULOMB_PER_MOLE = UnitDef(
    "kilocoulomb_per_mole",
    "kC/mol",
    1000,
    MOLAR_CHARGE,
    words=("kilocoulomb per mole", "kilocoulombs per mole"),
)

MolarCharge._canonical_unit = COULOMB_PER_MOLE  # noqa: SLF001 -- this module owns MolarCharge's canonical unit


def CoulombPerMole(value: Numeric) -> MolarCharge:
    """Construct a molar charge from a magnitude in coulombs per mole.

    Parameters
    ----------
    value : Numeric
        Molar charge magnitude in C/mol.

    Returns
    -------
    MolarCharge
        Molar charge represented in coulombs per mole.

    """
    return MolarCharge(to_exact(value) * COULOMB_PER_MOLE.scale, COULOMB_PER_MOLE)


def KilocoulombPerMole(value: Numeric) -> MolarCharge:
    """Construct a molar charge from a magnitude in kilocoulombs per mole.

    Parameters
    ----------
    value : Numeric
        Molar charge magnitude in kC/mol.

    Returns
    -------
    MolarCharge
        Molar charge represented in kilocoulombs per mole.

    Examples
    --------
    Passing 192 970.66 C through a cell moves two moles of electrons, to the precision
    of the charge:

    >>> from kuchka import Coulomb
    >>> from kuchka.constants.codata_2022 import FARADAY_CONSTANT
    >>> moles = Coulomb(192970.66424662) / FARADAY_CONSTANT
    >>> f"{moles:.6f}"
    '2.000000 mol'

    """
    return MolarCharge(
        to_exact(value) * KILOCOULOMB_PER_MOLE.scale, KILOCOULOMB_PER_MOLE
    )


MOLAR_CHARGE_UNITS: Mapping[str, Callable[[Numeric], MolarCharge]] = unit_table(
    "MOLAR_CHARGE_UNITS",
    {
        COULOMB_PER_MOLE: CoulombPerMole,
        KILOCOULOMB_PER_MOLE: KilocoulombPerMole,
    },
)

__all__ = [
    "COULOMB_PER_MOLE",
    "KILOCOULOMB_PER_MOLE",
    "MOLAR_CHARGE_UNITS",
    "CoulombPerMole",
    "KilocoulombPerMole",
]
