"""Density unit constructors for scientific, engineering, and laboratory calculations.

    from kuchka import KilogramPerCubicMetre, GramPerCubicCentimetre

    steel = KilogramPerCubicMetre(7850)
    water = GramPerCubicCentimetre(1)

`Density` represents mass per unit volume.
`KilogramPerCubicMetre` is the canonical SI unit.
The module also provides:
- `GramPerCubicCentimetre`, `GramPerMillilitre`, and `KilogramPerLitre`, which are
    common in materials science, chemistry, and laboratory work,
- `GramPerLitre` for low-density materials,
- `PoundPerCubicFoot` for customary engineering literature.

Some of these units have numerically identical scales but belong to different naming
traditions.
In particular:

``1 g/cm³ = 1 g/mL = 1 kg/L = 1000 kg/m³``

They remain distinct `UnitDef`s because the unit chosen by an engineer or scientist
carries useful domain context even when the underlying scale is the same.

Examples
--------
Density becomes useful when it participates in an actual physical calculation.

A metal sample has a measured mass of 7.85 kg and occupies exactly one litre.
Its density identifies it immediately as a material in the familiar steel range:

>>> from kuchka import Kilogram
>>> from kuchka import Litre
>>> sample_mass = Kilogram(7.85)
>>> sample_volume = Litre(1)
>>> density = sample_mass / sample_volume
>>> density
7850 kg/m³

The same material can be expressed in the customary materials-science scale:

>>> density.to(GRAM_PER_CUBIC_CENTIMETRE)
7.85 g/cm³

Density also turns a volume into a mass.
A 12 m³ tank filled with a liquid having a density of 820 kg/m³ contains:

>>> from kuchka import CubicMetre
>>> fuel_volume = CubicMetre(12)
>>> fuel_density = KilogramPerCubicMetre(820)
>>> fuel_mass = fuel_density * fuel_volume
>>> fuel_mass
9840 kg

Laboratory work often uses the millilitre scale.
A 250 mL sample with a density of 1.08 g/mL has a mass of:

>>> from kuchka import Millilitre
>>> sample_volume = Millilitre(250)
>>> sample_density = GramPerMillilitre(1.08)
>>> sample_mass = sample_density * sample_volume
>>> sample_mass
0.27 kg

Very low-density materials are often more naturally described in grams per litre.
One cubic metre of a gas with a density of 1.2 g/L therefore contains exactly 1.2 kg
of material:

>>> gas_density = GramPerLitre(1.2)
>>> gas_volume = CubicMetre(1)
>>> gas_density * gas_volume
1.2 kg

Notes
-----
Density is mass divided by volume:

``density = mass / volume``

and therefore:

``mass = density * volume``
``volume = mass / density``

The canonical SI unit is:

``1 kg/m³``

Several common density units are exact scale-equivalent representations:

``1 g/cm³ = 1000 kg/m³``
``1 g/mL  = 1000 kg/m³``
``1 kg/L  = 1000 kg/m³``
``1 g/L   = 1 kg/m³``

`GramPerCubicCentimetre` and `GramPerMillilitre` therefore have the same physical
scale, just as `GramPerCubicCentimetre` and `KilogramPerLitre` do.
They remain separate units because they arise naturally in different kinds of
scientific and engineering literature.

`PoundPerCubicFoot` is retained as a customary engineering unit for density,
particularly where material properties are reported in US customary units.

`DENSITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.

See Also
--------
~kuchka.quantities.Density
Quantity type representing mass per unit volume.
~kuchka.quantities.Mass
Mass that combines with volume to form density.
~kuchka.quantities.Volume
Volume that combines with mass to form density.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import DENSITY
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Density
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


KILOGRAM_PER_CUBIC_METRE = UnitDef(
    "kilogram_per_cubic_metre",
    f"kg/m{symbols.SUPERSCRIPT_THREE}",
    Decimal(1),
    DENSITY,
)
GRAM_PER_CUBIC_CENTIMETRE = UnitDef(
    "gram_per_cubic_centimetre",
    f"g/cm{symbols.SUPERSCRIPT_THREE}",
    Decimal(1000),
    DENSITY,
)

KILOGRAM_PER_CUBIC_METER = KILOGRAM_PER_CUBIC_METRE
GRAM_PER_CUBIC_CENTIMETER = GRAM_PER_CUBIC_CENTIMETRE

Density._canonical_unit = KILOGRAM_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns Density's canonical unit


def KilogramPerCubicMetre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in kilograms per cubic metre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in kilograms per cubic metre.

    Returns
    -------
    Density
        Density represented in kilograms per cubic metre.

    Examples
    --------
    A 12 m³ tank holds a liquid with a density of 820 kg/m³:

    >>> from kuchka import CubicMetre
    >>> density = KilogramPerCubicMetre(820)
    >>> density * CubicMetre(12)
    9840 kg

    """
    return Density(
        to_exact(value) * KILOGRAM_PER_CUBIC_METRE.scale,
        KILOGRAM_PER_CUBIC_METRE,
    )


def GramPerCubicCentimetre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in grams per cubic centimetre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in grams per cubic centimetre.

    Returns
    -------
    Density
        Density represented in grams per cubic centimetre.

    Examples
    --------
    A 250 cm³ metal sample with a density of 7.85 g/cm³ has a mass of:

    >>> from kuchka import CubicCentimetre
    >>> density = GramPerCubicCentimetre(7.85)
    >>> density * CubicCentimetre(250)
    1.9625 kg

    """
    return Density(
        to_exact(value) * GRAM_PER_CUBIC_CENTIMETRE.scale,
        GRAM_PER_CUBIC_CENTIMETRE,
    )


KilogramPerCubicMeter = KilogramPerCubicMetre
GramPerCubicCentimeter = GramPerCubicCentimetre


# Litres.


GRAM_PER_LITRE = UnitDef("gram_per_litre", "g/L", Decimal(1), DENSITY)
GRAM_PER_MILLILITRE = UnitDef("gram_per_millilitre", "g/mL", Decimal(1000), DENSITY)
MILLIGRAM_PER_LITRE = UnitDef(
    "milligram_per_litre",
    "mg/L",
    Decimal("0.001"),
    DENSITY,
    aliases=("mg/l",),
    words=("milligram per liter", "milligram per litre"),
)
MICROGRAM_PER_LITRE = UnitDef(
    "microgram_per_litre",
    f"{symbols.MICRO}g/L",
    Decimal("0.000001"),
    DENSITY,
    aliases=("ug/L", "ug/l", f"{symbols.MICRO}g/l"),
    words=("microgram per liter", "microgram per litre"),
)
KILOGRAM_PER_LITRE = UnitDef("kilogram_per_litre", "kg/L", Decimal(1000), DENSITY)

GRAM_PER_LITER = GRAM_PER_LITRE
GRAM_PER_MILLILITER = GRAM_PER_MILLILITRE
KILOGRAM_PER_LITER = KILOGRAM_PER_LITRE


def GramPerLitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in grams per litre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in grams per litre.

    Returns
    -------
    Density
        Density represented in grams per litre.

    Examples
    --------
    A one-cubic-metre gas sample has a density of 1.2 g/L.
    That cubic metre therefore contains exactly 1.2 kg of gas:

    >>> from kuchka import CubicMetre
    >>> density = GramPerLitre(1.2)
    >>> density * CubicMetre(1)
    1.2 kg

    """
    return Density(
        to_exact(value) * GRAM_PER_LITRE.scale,
        GRAM_PER_LITRE,
    )


def GramPerMillilitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in grams per millilitre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in grams per millilitre.

    Returns
    -------
    Density
        Density represented in grams per millilitre.

    Examples
    --------
    A laboratory sample occupies 250 mL and has a density of 1.08 g/mL:

    >>> from kuchka import Millilitre
    >>> density = GramPerMillilitre(1.08)
    >>> density * Millilitre(250)
    0.27 kg

    """
    return Density(
        to_exact(value) * GRAM_PER_MILLILITRE.scale,
        GRAM_PER_MILLILITRE,
    )


def KilogramPerLitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in kilograms per litre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in kilograms per litre.

    Returns
    -------
    Density
        Density represented in kilograms per litre.

    Examples
    --------
    A cryogenic storage vessel contains 18 L of a liquid with a density of 0.81 kg/L:

    >>> from kuchka import Litre
    >>> density = KilogramPerLitre(0.81)
    >>> density * Litre(18)
    14.58 kg

    """
    return Density(
        to_exact(value) * KILOGRAM_PER_LITRE.scale,
        KILOGRAM_PER_LITRE,
    )


def MilligramPerLitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in milligrams per litre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in milligrams per litre.

    Returns
    -------
    Density
        Density represented in milligrams per litre.

    Examples
    --------
    The mass concentration of a solute is a density: a river with 8 mg/L of dissolved
    oxygen holds 4 mg of it in 0.5 L:

    >>> from kuchka import Litre
    >>> MilligramPerLitre(8) * Litre(0.5)
    0.000004 kg

    """
    return Density(to_exact(value) * MILLIGRAM_PER_LITRE.scale, MILLIGRAM_PER_LITRE)


def MicrogramPerLitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in micrograms per litre.

    Parameters
    ----------
    value : Numeric
        Density magnitude in micrograms per litre.

    Returns
    -------
    Density
        Density represented in micrograms per litre.

    Examples
    --------
    >>> MicrogramPerLitre(500).to(MILLIGRAM_PER_LITRE)
    0.5 mg/L

    """
    return Density(to_exact(value) * MICROGRAM_PER_LITRE.scale, MICROGRAM_PER_LITRE)


GramPerLiter = GramPerLitre
MilligramPerLiter = MilligramPerLitre
MicrogramPerLiter = MicrogramPerLitre
GramPerMilliliter = GramPerMillilitre
KilogramPerLiter = KilogramPerLitre


DENSITY_UNITS: Mapping[str, Callable[[Numeric], Density]] = unit_table(
    "DENSITY_UNITS",
    {
        KILOGRAM_PER_CUBIC_METRE: KilogramPerCubicMetre,
        GRAM_PER_CUBIC_CENTIMETRE: GramPerCubicCentimetre,
        KILOGRAM_PER_LITRE: KilogramPerLitre,
        GRAM_PER_LITRE: GramPerLitre,
        GRAM_PER_MILLILITRE: GramPerMillilitre,
        MILLIGRAM_PER_LITRE: MilligramPerLitre,
        MICROGRAM_PER_LITRE: MicrogramPerLitre,
    },
)

__all__ = [
    "DENSITY_UNITS",
    "GRAM_PER_CUBIC_CENTIMETER",
    "GRAM_PER_CUBIC_CENTIMETRE",
    "GRAM_PER_LITER",
    "GRAM_PER_LITRE",
    "GRAM_PER_MILLILITER",
    "GRAM_PER_MILLILITRE",
    "KILOGRAM_PER_CUBIC_METER",
    "KILOGRAM_PER_CUBIC_METRE",
    "KILOGRAM_PER_LITER",
    "KILOGRAM_PER_LITRE",
    "MICROGRAM_PER_LITRE",
    "MILLIGRAM_PER_LITRE",
    "GramPerCubicCentimeter",
    "GramPerCubicCentimetre",
    "GramPerLiter",
    "GramPerLitre",
    "GramPerMilliliter",
    "GramPerMillilitre",
    "KilogramPerCubicMeter",
    "KilogramPerCubicMetre",
    "KilogramPerLiter",
    "KilogramPerLitre",
    "MicrogramPerLiter",
    "MicrogramPerLitre",
    "MilligramPerLiter",
    "MilligramPerLitre",
]
