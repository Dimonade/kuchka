"""Molar concentration constructors: moles per cubic metre and per litre.

Molar concentration is the amount of a solute per volume of solution, which chemists
call molarity: `1 mol/m³` is the canonical unit, and `1 mol/L` is written `M`.
The prefixed forms are the laboratory scales: `mM` (millimolar), `µM` (micromolar), and
`nM` (nanomolar).
The symbol `M` is read in this table only, and a bare `MM` is not a spelling.

A mass concentration (`mg/L`) is a `Density`: a molar concentration times a `MolarMass`
is one, and a `Density` over a `MolarMass` is a molar concentration.

`MOLAR_CONCENTRATION_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_CONCENTRATION
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarConcentration
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

MOLE_PER_CUBIC_METRE = UnitDef(
    "mole_per_cubic_metre",
    "mol/m\u00b3",
    1,
    MOLAR_CONCENTRATION,
    aliases=("mol/m^3", "mol/m**3"),
    words=("mole per cubic metre", "mole per cubic meter"),
)
MOLE_PER_LITRE = UnitDef(
    "mole_per_litre",
    "mol/L",
    1000,
    MOLAR_CONCENTRATION,
    aliases=("mol/l", "M"),
    words=("molar", "mole per litre", "mole per liter"),
)
MILLIMOLE_PER_LITRE = with_prefix(prefixes.MILLI, MOLE_PER_LITRE)
MICROMOLE_PER_LITRE = with_prefix(prefixes.MICRO, MOLE_PER_LITRE)
NANOMOLE_PER_LITRE = with_prefix(prefixes.NANO, MOLE_PER_LITRE)

MolarConcentration._canonical_unit = MOLE_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns MolarConcentration's canonical unit


def MolePerCubicMetre(value: Numeric) -> MolarConcentration:
    """Construct a molar concentration from a magnitude in moles per cubic metre.

    Parameters
    ----------
    value : Numeric
        Molar concentration magnitude in mol/m³.

    Returns
    -------
    MolarConcentration
        Molar concentration represented in moles per cubic metre.

    """
    return MolarConcentration(
        to_exact(value) * MOLE_PER_CUBIC_METRE.scale, MOLE_PER_CUBIC_METRE
    )


def MolePerLitre(value: Numeric) -> MolarConcentration:
    """Construct a molar concentration from a magnitude in moles per litre.

    Parameters
    ----------
    value : Numeric
        Molar concentration magnitude in mol/L.

    Returns
    -------
    MolarConcentration
        Molar concentration represented in moles per litre.

    Examples
    --------
    A 0.5 L flask of a 2 M solution holds 1 mol of solute, which is 58.44 g of sodium
    chloride:

    >>> from kuchka import GramPerMole
    >>> from kuchka import Litre
    >>> from kuchka.units import GRAM
    >>> amount = MolePerLitre(2) * Litre(0.5)
    >>> amount
    1 mol
    >>> (amount * GramPerMole(58.44)).to(GRAM)
    58.44 g

    """
    return MolarConcentration(to_exact(value) * MOLE_PER_LITRE.scale, MOLE_PER_LITRE)


def MillimolePerLitre(value: Numeric) -> MolarConcentration:
    """Construct a molar concentration from a magnitude in millimoles per litre.

    Parameters
    ----------
    value : Numeric
        Molar concentration magnitude in mmol/L.

    Returns
    -------
    MolarConcentration
        Molar concentration represented in millimoles per litre.

    Examples
    --------
    Blood glucose of 5 mmol/L is 5 mM, and times a molar mass of 180.16 g/mol is a mass
    concentration of 0.9008 g/L:

    >>> from kuchka import GramPerMole
    >>> from kuchka.units import GRAM_PER_LITRE
    >>> (MillimolePerLitre(5) * GramPerMole(180.16)).to(GRAM_PER_LITRE)
    0.9008 g/L

    """
    return MolarConcentration(
        to_exact(value) * MILLIMOLE_PER_LITRE.scale, MILLIMOLE_PER_LITRE
    )


def MicromolePerLitre(value: Numeric) -> MolarConcentration:
    """Construct a molar concentration from a magnitude in micromoles per litre.

    Parameters
    ----------
    value : Numeric
        Molar concentration magnitude in µmol/L.

    Returns
    -------
    MolarConcentration
        Molar concentration represented in micromoles per litre.

    Examples
    --------
    >>> MicromolePerLitre(250).to(MILLIMOLE_PER_LITRE)
    0.25 mmol/L

    """
    return MolarConcentration(
        to_exact(value) * MICROMOLE_PER_LITRE.scale, MICROMOLE_PER_LITRE
    )


def NanomolePerLitre(value: Numeric) -> MolarConcentration:
    """Construct a molar concentration from a magnitude in nanomoles per litre.

    Parameters
    ----------
    value : Numeric
        Molar concentration magnitude in nmol/L.

    Returns
    -------
    MolarConcentration
        Molar concentration represented in nanomoles per litre.

    Examples
    --------
    >>> NanomolePerLitre(1500).to(MICROMOLE_PER_LITRE)
    1.5 µmol/L

    """
    return MolarConcentration(
        to_exact(value) * NANOMOLE_PER_LITRE.scale, NANOMOLE_PER_LITRE
    )


MolePerLiter = MolePerLitre
MillimolePerLiter = MillimolePerLitre
MicromolePerLiter = MicromolePerLitre
NanomolePerLiter = NanomolePerLitre
MolePerCubicMeter = MolePerCubicMetre

MOLAR_CONCENTRATION_UNITS: Mapping[str, Callable[[Numeric], MolarConcentration]] = (
    unit_table(
        "MOLAR_CONCENTRATION_UNITS",
        {
            NANOMOLE_PER_LITRE: NanomolePerLitre,
            MICROMOLE_PER_LITRE: MicromolePerLitre,
            MILLIMOLE_PER_LITRE: MillimolePerLitre,
            MOLE_PER_LITRE: MolePerLitre,
            MOLE_PER_CUBIC_METRE: MolePerCubicMetre,
        },
    )
)

__all__ = [
    "MICROMOLE_PER_LITRE",
    "MILLIMOLE_PER_LITRE",
    "MOLAR_CONCENTRATION_UNITS",
    "MOLE_PER_CUBIC_METRE",
    "MOLE_PER_LITRE",
    "NANOMOLE_PER_LITRE",
    "MicromolePerLiter",
    "MicromolePerLitre",
    "MillimolePerLiter",
    "MillimolePerLitre",
    "MolePerCubicMeter",
    "MolePerCubicMetre",
    "MolePerLiter",
    "MolePerLitre",
    "NanomolePerLiter",
    "NanomolePerLitre",
]
