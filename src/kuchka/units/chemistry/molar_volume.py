"""Molar volume constructors: CubicMetrePerMole, LitrePerMole, and more.

Molar volume is the volume that one mole of a substance occupies: `1 m³/mol` is the
canonical unit, and `L/mol` (the same as `dm³/mol`) and `cm³/mol` are the scales that
gases and liquids are written in.
It is the reciprocal of the molar concentration: `1 / MolarConcentration` is a
`MolarVolume`.

`MOLAR_VOLUME_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_VOLUME
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarVolume
from kuchka.quantities import UnitDef
from kuchka.units.geometry.volume import LITRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

CUBIC_METRE_PER_MOLE = UnitDef(
    "cubic_metre_per_mole",
    "m\u00b3/mol",
    1,
    MOLAR_VOLUME,
    aliases=("m^3/mol", "m**3/mol"),
    words=("cubic metre per mole", "cubic meter per mole"),
)
LITRE_PER_MOLE = UnitDef(
    "litre_per_mole",
    "L/mol",
    LITRE.scale,
    MOLAR_VOLUME,
    aliases=("l/mol", "dm3/mol", "dm^3/mol", "dm**3/mol"),
    words=("liter per mole", "litre per mole", "liters per mole", "litres per mole"),
)
CUBIC_CENTIMETRE_PER_MOLE = UnitDef(
    "cubic_centimetre_per_mole",
    "cm\u00b3/mol",
    Fraction(1, 1_000_000),
    MOLAR_VOLUME,
    aliases=("cm^3/mol", "cm**3/mol", "cc/mol"),
    words=("cubic centimetre per mole", "cubic centimeter per mole"),
)

MolarVolume._canonical_unit = CUBIC_METRE_PER_MOLE  # noqa: SLF001 -- this module owns MolarVolume's canonical unit


def CubicMetrePerMole(value: Numeric) -> MolarVolume:
    """Construct a molar volume from a magnitude in cubic metres per mole.

    Parameters
    ----------
    value : Numeric
        Molar volume magnitude in m³/mol.

    Returns
    -------
    MolarVolume
        Molar volume represented in cubic metres per mole.

    """
    return MolarVolume(
        to_exact(value) * CUBIC_METRE_PER_MOLE.scale, CUBIC_METRE_PER_MOLE
    )


def LitrePerMole(value: Numeric) -> MolarVolume:
    """Construct a molar volume from a magnitude in litres per mole.

    Parameters
    ----------
    value : Numeric
        Molar volume magnitude in L/mol.

    Returns
    -------
    MolarVolume
        Molar volume represented in litres per mole.

    Examples
    --------
    An ideal gas at 0 °C and 1 bar takes up about 22.711 L/mol, so 2 mol of it fills:

    >>> from kuchka import Mole
    >>> (LitrePerMole(22.711) * Mole(2)).to(LITRE)
    45.422 L

    """
    return MolarVolume(to_exact(value) * LITRE_PER_MOLE.scale, LITRE_PER_MOLE)


def CubicCentimetrePerMole(value: Numeric) -> MolarVolume:
    """Construct a molar volume from a magnitude in cubic centimetres per mole.

    Parameters
    ----------
    value : Numeric
        Molar volume magnitude in cm³/mol.

    Returns
    -------
    MolarVolume
        Molar volume represented in cubic centimetres per mole.

    Examples
    --------
    Liquid water takes up about 18.07 cm³/mol:

    >>> CubicCentimetrePerMole(18.07).to(LITRE_PER_MOLE)
    0.01807 L/mol

    """
    return MolarVolume(
        to_exact(value) * CUBIC_CENTIMETRE_PER_MOLE.scale, CUBIC_CENTIMETRE_PER_MOLE
    )


CubicMeterPerMole = CubicMetrePerMole
LiterPerMole = LitrePerMole
CubicCentimeterPerMole = CubicCentimetrePerMole


MOLAR_VOLUME_UNITS: Mapping[str, Callable[[Numeric], MolarVolume]] = unit_table(
    "MOLAR_VOLUME_UNITS",
    {
        CUBIC_CENTIMETRE_PER_MOLE: CubicCentimetrePerMole,
        LITRE_PER_MOLE: LitrePerMole,
        CUBIC_METRE_PER_MOLE: CubicMetrePerMole,
    },
)

__all__ = [
    "CUBIC_CENTIMETRE_PER_MOLE",
    "CUBIC_METRE_PER_MOLE",
    "LITRE_PER_MOLE",
    "MOLAR_VOLUME_UNITS",
    "CubicCentimeterPerMole",
    "CubicCentimetrePerMole",
    "CubicMeterPerMole",
    "CubicMetrePerMole",
    "LiterPerMole",
    "LitrePerMole",
]
