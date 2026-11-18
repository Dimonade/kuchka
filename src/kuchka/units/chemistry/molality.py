"""Molality constructors: moles per kilogram, with milli and micro forms.

Molality is the amount of a solute per mass of solvent: `1 mol/kg` is the canonical
unit.
Unlike a molar concentration it does not change with temperature, because a mass does
not expand, which is why it is used for boiling-point and freezing-point work.
A bare `m` is not a spelling of the molal, since it reads as a metre.

`MOLALITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLALITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Molality
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

MOLE_PER_KILOGRAM = UnitDef(
    "mole_per_kilogram",
    "mol/kg",
    1,
    MOLALITY,
    words=("molal", "mole per kilogram", "moles per kilogram"),
)
MILLIMOLE_PER_KILOGRAM = with_prefix(prefixes.MILLI, MOLE_PER_KILOGRAM)
MICROMOLE_PER_KILOGRAM = with_prefix(prefixes.MICRO, MOLE_PER_KILOGRAM)

Molality._canonical_unit = MOLE_PER_KILOGRAM  # noqa: SLF001 -- this module owns Molality's canonical unit


def MolePerKilogram(value: Numeric) -> Molality:
    """Construct a molality from a magnitude in moles per kilogram.

    Parameters
    ----------
    value : Numeric
        Molality magnitude in mol/kg.

    Returns
    -------
    Molality
        Molality represented in moles per kilogram.

    Examples
    --------
    Dissolving 0.5 mol of sucrose in 250 g of water gives a 2 mol/kg solution:

    >>> from kuchka import Gram
    >>> from kuchka import Mole
    >>> Mole(0.5) / Gram(250)
    2 mol/kg

    """
    return Molality(to_exact(value) * MOLE_PER_KILOGRAM.scale, MOLE_PER_KILOGRAM)


def MillimolePerKilogram(value: Numeric) -> Molality:
    """Construct a molality from a magnitude in millimoles per kilogram.

    Parameters
    ----------
    value : Numeric
        Molality magnitude in mmol/kg.

    Returns
    -------
    Molality
        Molality represented in millimoles per kilogram.

    """
    return Molality(
        to_exact(value) * MILLIMOLE_PER_KILOGRAM.scale, MILLIMOLE_PER_KILOGRAM
    )


def MicromolePerKilogram(value: Numeric) -> Molality:
    """Construct a molality from a magnitude in micromoles per kilogram.

    Parameters
    ----------
    value : Numeric
        Molality magnitude in µmol/kg.

    Returns
    -------
    Molality
        Molality represented in micromoles per kilogram.

    Examples
    --------
    >>> MicromolePerKilogram(2500).to(MILLIMOLE_PER_KILOGRAM)
    2.5 mmol/kg

    """
    return Molality(
        to_exact(value) * MICROMOLE_PER_KILOGRAM.scale, MICROMOLE_PER_KILOGRAM
    )


MOLALITY_UNITS: Mapping[str, Callable[[Numeric], Molality]] = unit_table(
    "MOLALITY_UNITS",
    {
        MICROMOLE_PER_KILOGRAM: MicromolePerKilogram,
        MILLIMOLE_PER_KILOGRAM: MillimolePerKilogram,
        MOLE_PER_KILOGRAM: MolePerKilogram,
    },
)

MOLALITY_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        MICROMOLE_PER_KILOGRAM,
        MILLIMOLE_PER_KILOGRAM,
        MOLE_PER_KILOGRAM,
    ),
)
"""The units `auto_scale` moves a molality along, smallest first."""

__all__ = [
    "MICROMOLE_PER_KILOGRAM",
    "MILLIMOLE_PER_KILOGRAM",
    "MOLALITY_LADDERS",
    "MOLALITY_UNITS",
    "MOLE_PER_KILOGRAM",
    "MicromolePerKilogram",
    "MillimolePerKilogram",
    "MolePerKilogram",
]
