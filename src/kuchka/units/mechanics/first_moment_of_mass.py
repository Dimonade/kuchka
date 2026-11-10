"""First moment of mass constructors: kilogram-metres and their relatives.

A first moment of mass is a mass times its distance from an axis.
On a rotor it is the unbalance, specified and measured in gram-millimetres: a 2 g
correction weight 15 mm from the axis corrects 30 g·mm.
The kilogram metre is the canonical unit.

Examples
--------
A balancing machine reports 30 g·mm of residual unbalance on a 1.5 kg rotor.
Its centre of mass sits 20 µm off the axis:

>>> from kuchka import Kilogram
>>> from kuchka.units import MICROMETRE
>>> (GramMillimetre(30) / Kilogram(1.5)).to(MICROMETRE)
20 µm

`FIRST_MOMENT_OF_MASS_UNITS` maps symbols such as ``"g·mm"`` and ``"oz·in"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.MomentOfInertia
    A first moment of mass times a further length.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import FIRST_MOMENT_OF_MASS
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import FirstMomentOfMass
from kuchka.quantities import UnitDef
from kuchka.units.length import INCH
from kuchka.units.mass import OUNCE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

KILOGRAM_METRE = UnitDef(
    "kilogram_metre",
    f"kg{symbols.MIDDLE_DOT}m",
    1,
    FIRST_MOMENT_OF_MASS,
    aliases=("kg*m", "kg m"),
    words=("kilogram metre", "kilogram meter"),
)
GRAM_CENTIMETRE = UnitDef(
    "gram_centimetre",
    f"g{symbols.MIDDLE_DOT}cm",
    Fraction(1, 100_000),
    FIRST_MOMENT_OF_MASS,
    aliases=("g*cm", "g cm"),
    words=("gram centimetre", "gram centimeter"),
)
GRAM_MILLIMETRE = UnitDef(
    "gram_millimetre",
    f"g{symbols.MIDDLE_DOT}mm",
    Fraction(1, 1_000_000),
    FIRST_MOMENT_OF_MASS,
    aliases=("g*mm", "g mm", "gmm"),
    words=("gram millimetre", "gram millimeter"),
)
OUNCE_INCH = UnitDef(
    "ounce_inch",
    f"oz{symbols.MIDDLE_DOT}in",
    OUNCE.scale * INCH.scale,
    FIRST_MOMENT_OF_MASS,
    aliases=("oz*in", "oz in", "oz-in"),
    words=("ounce inch",),
)

KILOGRAM_METER = KILOGRAM_METRE
GRAM_CENTIMETER = GRAM_CENTIMETRE
GRAM_MILLIMETER = GRAM_MILLIMETRE

FirstMomentOfMass._canonical_unit = KILOGRAM_METRE  # noqa: SLF001 -- this module owns FirstMomentOfMass's canonical unit


def KilogramMetre(value: Numeric) -> FirstMomentOfMass:
    """Construct a first moment of mass from kilogram metres.

    Parameters
    ----------
    value : Numeric
        First moment of mass in kg·m.

    Returns
    -------
    FirstMomentOfMass
        First moment of mass represented in kilogram metres.

    Examples
    --------
    >>> from kuchka import Kilogram, Metre
    >>> Kilogram(2) * Metre(0.5) == KilogramMetre(1)
    True

    """
    return FirstMomentOfMass(to_exact(value) * KILOGRAM_METRE.scale, KILOGRAM_METRE)


def GramCentimetre(value: Numeric) -> FirstMomentOfMass:
    """Construct a first moment of mass from gram centimetres.

    Parameters
    ----------
    value : Numeric
        First moment of mass in g·cm.

    Returns
    -------
    FirstMomentOfMass
        First moment of mass represented in gram centimetres.

    Examples
    --------
    >>> GramCentimetre(3) == GramMillimetre(30)
    True

    """
    return FirstMomentOfMass(to_exact(value) * GRAM_CENTIMETRE.scale, GRAM_CENTIMETRE)


def GramMillimetre(value: Numeric) -> FirstMomentOfMass:
    """Construct a first moment of mass from gram millimetres.

    Parameters
    ----------
    value : Numeric
        First moment of mass in g·mm, the unit of rotor unbalance.

    Returns
    -------
    FirstMomentOfMass
        First moment of mass represented in gram millimetres.

    Examples
    --------
    A 2 g correction weight placed 15 mm from the axis:

    >>> from kuchka import Gram, Millimetre
    >>> Gram(2) * Millimetre(15) == GramMillimetre(30)
    True

    """
    return FirstMomentOfMass(to_exact(value) * GRAM_MILLIMETRE.scale, GRAM_MILLIMETRE)


def OunceInch(value: Numeric) -> FirstMomentOfMass:
    """Construct a first moment of mass from ounce inches.

    Parameters
    ----------
    value : Numeric
        First moment of mass in oz·in.

    Returns
    -------
    FirstMomentOfMass
        First moment of mass represented in ounce inches.

    Examples
    --------
    >>> f"{OunceInch(1).to(GRAM_MILLIMETRE):.1f}"
    '720.1 g·mm'

    """
    return FirstMomentOfMass(to_exact(value) * OUNCE_INCH.scale, OUNCE_INCH)


KilogramMeter = KilogramMetre
GramCentimeter = GramCentimetre
GramMillimeter = GramMillimetre


FIRST_MOMENT_OF_MASS_UNITS: Mapping[str, Callable[[Numeric], FirstMomentOfMass]] = (
    unit_table(
        "FIRST_MOMENT_OF_MASS_UNITS",
        {
            KILOGRAM_METRE: KilogramMetre,
            GRAM_CENTIMETRE: GramCentimetre,
            GRAM_MILLIMETRE: GramMillimetre,
            OUNCE_INCH: OunceInch,
        },
    )
)

__all__ = [
    "FIRST_MOMENT_OF_MASS_UNITS",
    "GRAM_CENTIMETER",
    "GRAM_CENTIMETRE",
    "GRAM_MILLIMETER",
    "GRAM_MILLIMETRE",
    "KILOGRAM_METER",
    "KILOGRAM_METRE",
    "OUNCE_INCH",
    "GramCentimeter",
    "GramCentimetre",
    "GramMillimeter",
    "GramMillimetre",
    "KilogramMeter",
    "KilogramMetre",
    "OunceInch",
]
