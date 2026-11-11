"""Volume constructors: cubic units, the litre and its prefixes, and the US gallon.

`Volume` is the space a body occupies, and the cubic metre (`m³`) is its canonical unit.
The module provides the cubic millimetre, centimetre, and metre, the litre with its
micro, milli, and kilo forms, and the US customary cubic foot and gallon:

>>> from decimal import Decimal
>>> from kuchka import Litre
>>> from kuchka import Millilitre
>>> reagent = Millilitre(500) + Litre(Decimal("0.25"))

The litre is exactly one cubic decimetre, and it is the unit that laboratories and
process plants work in, so it has the full set of prefixes.
Cubic millimetres and microlitres measure a drop, cubic centimetres and millilitres a
dose or an engine cylinder, litres a bottle or a fuel tank, and cubic metres and
kilolitres a room, a tank, or a reservoir.

Examples
--------
A room of 12 m² under a ceiling of 2.5 m holds 30 m³ of air, which is 30 kL:

>>> from kuchka import Metre
>>> from kuchka import SquareMetre
>>> from kuchka.units import KILOLITRE
>>> room = SquareMetre(12) * Metre(2.5)
>>> room
30 m³
>>> room.to(KILOLITRE)
30 kL

A thousand litres poured over 2 m² of flat roof stand half a metre deep, and a volume
over an area is a length:

>>> from kuchka import Litre
>>> Litre(1000) / SquareMetre(2)
0.5 m

A tank that fills at 5 US gallons a minute takes 12 minutes to take 60 gallons, and the
rate in litres per minute is:

>>> from kuchka import Minute
>>> from kuchka import UsGallon
>>> from kuchka.units import LITRE_PER_MINUTE
>>> f"{(UsGallon(5) / Minute(1)).to(LITRE_PER_MINUTE):.1f}"
'18.9 L/min'

A volume and a length are different quantities, so the two refuse to add:

>>> Litre(1) + Metre(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
The litre is exactly 0.001 m³ and the kilolitre exactly one cubic metre.
The US gallon is exactly 231 cubic inches, which is 3.785411784 L, and the cubic foot is
exactly 28.316846592 L, both following from the exact inch and foot.

Two pairs of units have the same scale: `CubicCentimetre` and `Millilitre` (1E-6 m³),
and `CubicMillimetre` and `Microlitre` (1E-9 m³).
They stay separate units because they come from two naming traditions, the cube of a
length and the metric unit of volume, in the way `Tonne` and `Megagram` do, and each
displays under its own name.

`Liter`, `Milliliter`, `Kiloliter`, `Microliter`, and `CubicMeter` are the American
spellings of the same constructors.

`VOLUME_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
It accepts `cc` for the cubic centimetre and the plain spellings of the cubed units.

References
----------
NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

BIPM, The International System of Units (SI Brochure), on the litre accepted for use
with the SI:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Area
    An area times a length is a volume.
~kuchka.quantities.Density
    A mass over a volume.
~kuchka.quantities.VolumetricFlowRate
    A volume over a time.
~kuchka.quantities.MolarConcentration
    An amount of substance over a volume.

"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import VOLUME
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import Volume
from kuchka.units.length import FOOT

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

CUBIC_METRE_NAME = "cubic_metre"
CUBIC_METRE_SYMBOL = f"m{symbols.SUPERSCRIPT_THREE}"

# NOTE: same reasoning as kuchka.units.geometry.area -- a cubed unit needs the linear
# prefix's scale applied three times, not once, so `prefixed_unit()`'s constructor is
# not flexible enough for it as defined now.
CUBIC_MILLIMETRE = UnitDef(
    "cubic_millimetre",
    f"mm{symbols.SUPERSCRIPT_THREE}",
    prefixes.MILLI.factor * prefixes.MILLI.factor * prefixes.MILLI.factor,
    VOLUME,
    aliases=powered("mm", 3),
    words=("cubic millimeter",),
)
CUBIC_CENTIMETRE = UnitDef(
    "cubic_centimetre",
    f"cm{symbols.SUPERSCRIPT_THREE}",
    Decimal("0.000001"),
    VOLUME,
    aliases=(*powered("cm", 3), "cc"),
    words=("cubic centimeter",),
)
CUBIC_METRE = prefixed_unit(
    prefixes.UNIT,
    CUBIC_METRE_NAME,
    CUBIC_METRE_SYMBOL,
    VOLUME,
    aliases=powered("m", 3),
    words=("cubic meter",),
)

CUBIC_MILLIMETER = CUBIC_MILLIMETRE
CUBIC_CENTIMETER = CUBIC_CENTIMETRE
CUBIC_METER = CUBIC_METRE

Volume._canonical_unit = CUBIC_METRE  # noqa: SLF001 -- this module owns Volume's canonical unit


def CubicMillimetre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic millimetres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in cubic millimetres.

    Returns
    -------
    Volume
        Volume represented in cubic millimetres.

    Examples
    --------
    A drop of water from a dropper is about 50 mm³:

    >>> drop = CubicMillimetre(50)
    >>> drop
    50 mm³

    In a laboratory, the same drop is 50 microlitres of the metric unit, and a cubic
    millimetre equals a microlitre exactly:

    >>> from kuchka import Microlitre
    >>> CubicMillimetre(1) == Microlitre(1)
    True

    """
    return Volume(to_exact(value) * CUBIC_MILLIMETRE.scale, CUBIC_MILLIMETRE)


def CubicCentimetre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic centimetres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in cubic centimetres.

    Returns
    -------
    Volume
        Volume represented in cubic centimetres.

    Examples
    --------
    An engine with cylinders that sweep 1600 cm³ in total is sold as a 1.6 L engine:

    >>> engine = CubicCentimetre(1600)
    >>> engine
    1600 cm³
    >>> from kuchka.units import LITRE
    >>> engine.to(LITRE)
    1.6 L

    Brochures write the same unit as `cc`, which `parse` reads:

    >>> from kuchka import Volume
    >>> from kuchka import parse
    >>> parse("1600 cc", Volume) == engine
    True

    """
    return Volume(to_exact(value) * CUBIC_CENTIMETRE.scale, CUBIC_CENTIMETRE)


def CubicMetre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic metres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in cubic metres.

    Returns
    -------
    Volume
        Volume represented in cubic metres.

    Examples
    --------
    A swimming pool that is 25 m long, 10 m wide, and 2 m deep holds 500 m³ of water:

    >>> from kuchka import Metre
    >>> from kuchka import SquareMetre
    >>> pool = SquareMetre(25 * 10) * Metre(2)
    >>> pool
    500 m³

    At the density of water, that volume has a mass of about half a million kilograms:

    >>> from kuchka import KilogramPerCubicMetre
    >>> from kuchka.units import KILOGRAM
    >>> (KilogramPerCubicMetre(1000) * pool).to(KILOGRAM)
    500000 kg

    """
    return Volume(to_exact(value) * CUBIC_METRE.scale, CUBIC_METRE)


CubicMillimeter = CubicMillimetre
CubicCentimeter = CubicCentimetre
CubicMeter = CubicMetre


# Litres -- non-SI, but very frequent.


LITRE_NAME = "litre"
LITRE_SYMBOL = "L"
LITRE_ALIASES = ("l",)
"""The lower-case symbol, which prefixes follow: `ml`."""
LITRE_WORDS = ("liter",)
"""The American spelling, which prefixed names follow: `milliliter`."""

MICROLITRE = prefixed_unit(
    prefixes.MICRO,
    LITRE_NAME,
    LITRE_SYMBOL,
    VOLUME,
    coherent_offset=-3,
    base_aliases=LITRE_ALIASES,
    base_words=LITRE_WORDS,
)
MILLILITRE = prefixed_unit(
    prefixes.MILLI,
    LITRE_NAME,
    LITRE_SYMBOL,
    VOLUME,
    coherent_offset=-3,
    base_aliases=LITRE_ALIASES,
    base_words=LITRE_WORDS,
)
LITRE = prefixed_unit(
    prefixes.UNIT,
    LITRE_NAME,
    LITRE_SYMBOL,
    VOLUME,
    coherent_offset=-3,
    base_aliases=LITRE_ALIASES,
    base_words=LITRE_WORDS,
)
KILOLITRE = prefixed_unit(
    prefixes.KILO,
    LITRE_NAME,
    LITRE_SYMBOL,
    VOLUME,
    coherent_offset=-3,
    base_aliases=LITRE_ALIASES,
    base_words=LITRE_WORDS,
)


# Customary volumes, exact from the foot and the cubic inch.

CUBIC_FOOT = UnitDef(
    "cubic_foot",
    f"ft{symbols.SUPERSCRIPT_THREE}",
    FOOT.scale * FOOT.scale * FOOT.scale,
    VOLUME,
    aliases=powered("ft", 3),
    words=("cubic foot", "cubic feet"),
)
US_GALLON = UnitDef(
    "us_gallon",
    "US gal",
    Fraction(231) * Fraction(254, 10_000) ** 3,
    VOLUME,
    aliases=("gal(US)", "gal (US)", "USgal"),
    words=("us gallon", "us liquid gallon"),
)
"""The US liquid gallon: 231 cubic inches, exactly 3.785411784 litres.

A bare `gal` is not a spelling of it, because the imperial gallon is another unit."""


def CubicFoot(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic feet.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in cubic feet.

    Returns
    -------
    Volume
        Volume represented in cubic feet.

    Notes
    -----
    Exact: the cube of the international foot, 28.316846592 L.

    Examples
    --------
    A household refrigerator is sold with a capacity of 18 ft³:

    >>> fridge = CubicFoot(18)
    >>> fridge
    18 ft³
    >>> from kuchka.units import LITRE
    >>> f"{fridge.to(LITRE):.0f}"
    '510 L'

    A cubic foot of water fills about seven and a half US gallons:

    >>> from kuchka.units import US_GALLON
    >>> f"{CubicFoot(1).to(US_GALLON):.4f}"
    '7.4805 US gal'

    """
    return Volume(to_exact(value) * CUBIC_FOOT.scale, CUBIC_FOOT)


def UsGallon(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in US gallons.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in US gallons.

    Returns
    -------
    Volume
        Volume represented in US gallons.

    Notes
    -----
    Exact: 231 cubic inches, which is 3.785411784 L.

    Examples
    --------
    A pickup truck's fuel tank holds 26 US gallons:

    >>> tank = UsGallon(26)
    >>> tank
    26 US gal
    >>> from kuchka.units import LITRE
    >>> f"{tank.to(LITRE):.1f}"
    '98.4 L'

    The conversion factor to the litre is exact:

    >>> UsGallon(1).to(LITRE)
    3.785411784 L

    """
    return Volume(to_exact(value) * US_GALLON.scale, US_GALLON)


def Microlitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in microlitres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in microlitres.

    Returns
    -------
    Volume
        Volume represented in microlitres.

    Examples
    --------
    A PCR reaction is 20 µL, made of 15 µL of master mix and 5 µL of template:

    >>> reaction = Microlitre(15) + Microlitre(5)
    >>> reaction
    20 µL

    A 96-well plate takes 96 reactions, and the total is in millilitres:

    >>> from kuchka.units import MILLILITRE
    >>> (reaction * 96).to(MILLILITRE)
    1.92 mL

    """
    return Volume(to_exact(value) * MICROLITRE.scale, MICROLITRE)


def Millilitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in millilitres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in millilitres.

    Returns
    -------
    Volume
        Volume represented in millilitres.

    Examples
    --------
    A measuring cup of water holds 250 mL, and at 1000 kg per cubic metre its mass is
    250 g:

    >>> cup = Millilitre(250)
    >>> cup
    250 mL
    >>> from kuchka import KilogramPerCubicMetre
    >>> from kuchka.units import GRAM
    >>> (KilogramPerCubicMetre(1000) * cup).to(GRAM)
    250 g

    A millilitre is the same volume as a cubic centimetre, under the name that medicine
    and kitchens use:

    >>> from kuchka import CubicCentimetre
    >>> Millilitre(1) == CubicCentimetre(1)
    True

    """
    return Volume(to_exact(value) * MILLILITRE.scale, MILLILITRE)


def Litre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in litres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in litres.

    Returns
    -------
    Volume
        Volume represented in litres.

    Examples
    --------
    A laboratory mixes 500 mL of buffer with a further quarter litre:

    >>> from decimal import Decimal
    >>> from kuchka import Millilitre
    >>> mix = Millilitre(500) + Litre(Decimal("0.25"))
    >>> mix
    750 mL

    A one-litre bottle is a thousandth of a cubic metre:

    >>> from kuchka import CubicMetre
    >>> Litre(1) == CubicMetre(Decimal("0.001"))
    True

    A volume that arrives as text, as a recipe or a datasheet writes it, enters through
    `parse`:

    >>> from kuchka import Volume
    >>> from kuchka import parse
    >>> parse("2.5 L", Volume)
    2.5 L

    """
    return Volume(to_exact(value) * LITRE.scale, LITRE)


def Kilolitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in kilolitres.

    Parameters
    ----------
    value : Numeric
        Volume magnitude in kilolitres.

    Returns
    -------
    Volume
        Volume represented in kilolitres.

    Examples
    --------
    A rainwater tank on a farm holds 22.5 kL:

    >>> tank = Kilolitre(22.5)
    >>> tank
    22.5 kL

    A kilolitre is a cubic metre, so a roof of 90 m² that catches a 25 mm shower yields
    2.25 kL:

    >>> from kuchka import Millimetre
    >>> from kuchka import SquareMetre
    >>> from kuchka.units import KILOLITRE
    >>> (SquareMetre(90) * Millimetre(25)).to(KILOLITRE)
    2.25 kL

    """
    return Volume(to_exact(value) * KILOLITRE.scale, KILOLITRE)


Microliter = Microlitre
Milliliter = Millilitre
Liter = Litre
Kiloliter = Kilolitre

VOLUME_UNITS: Mapping[str, Callable[[Numeric], Volume]] = unit_table(
    "VOLUME_UNITS",
    {
        CUBIC_MILLIMETRE: CubicMillimetre,
        CUBIC_CENTIMETRE: CubicCentimetre,
        CUBIC_METRE: CubicMetre,
        CUBIC_FOOT: CubicFoot,
        US_GALLON: UsGallon,
        MICROLITRE: Microlitre,
        MILLILITRE: Millilitre,
        LITRE: Litre,
        KILOLITRE: Kilolitre,
    },
)

__all__ = [
    "CUBIC_CENTIMETER",
    "CUBIC_CENTIMETRE",
    "CUBIC_FOOT",
    "CUBIC_METER",
    "CUBIC_METRE",
    "CUBIC_MILLIMETER",
    "CUBIC_MILLIMETRE",
    "KILOLITRE",
    "LITRE",
    "MICROLITRE",
    "MILLILITRE",
    "US_GALLON",
    "VOLUME_UNITS",
    "CubicCentimeter",
    "CubicCentimetre",
    "CubicFoot",
    "CubicMeter",
    "CubicMetre",
    "CubicMillimeter",
    "CubicMillimetre",
    "Kiloliter",
    "Kilolitre",
    "Liter",
    "Litre",
    "Microliter",
    "Microlitre",
    "Milliliter",
    "Millilitre",
    "UsGallon",
]
