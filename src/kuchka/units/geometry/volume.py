"""Volume constructors: cubic units, the litre and its prefixes, and the US gallon.

    from kuchka import Litre
    from kuchka import Millilitre

    reagent = Millilitre(500) + Litre(Decimal("0.25"))

`CubicMetre` is the SI-coherent canonical unit (`scale = Decimal(1)`).
A `Litre` is exactly one cubic decimetre (`Decimal("0.001")` m³), but as it is the
unit that actually shows up in lab and process-engineering work, so it gets its own
full set of prefixes and first grade support.

NOTE: Two pairs below have the exact same scale by coincidence:
- `CubicCentimetre` and `Millilitre` are both `Decimal("0.000001")` m³, and,
- `CubicMillimetre` and `Microlitre` are both `Decimal("0.000000001")` m³.

A cubic centimetre and a millilitre are the same physical quantity;
they are kept as separate `UnitDef`s (the way `Tonne` aliases `Megagram`) because they
come from genuinely different naming traditions -- geometric length-cubed versus the
metric volume unit -- that happen to coincide numerically.
They are not two names for one coherent SI unit.

`VOLUME_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
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
    """Construct a Volume from a magnitude expressed in cubic millimetres."""
    return Volume(to_exact(value) * CUBIC_MILLIMETRE.scale, CUBIC_MILLIMETRE)


def CubicCentimetre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic centimetres."""
    return Volume(to_exact(value) * CUBIC_CENTIMETRE.scale, CUBIC_CENTIMETRE)


def CubicMetre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in cubic metres."""
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
    """Construct a Volume from a magnitude expressed in cubic feet."""
    return Volume(to_exact(value) * CUBIC_FOOT.scale, CUBIC_FOOT)


def UsGallon(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in US liquid gallons."""
    return Volume(to_exact(value) * US_GALLON.scale, US_GALLON)


def Microlitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in microlitres."""
    return Volume(to_exact(value) * MICROLITRE.scale, MICROLITRE)


def Millilitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in millilitres."""
    return Volume(to_exact(value) * MILLILITRE.scale, MILLILITRE)


def Litre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in litres."""
    return Volume(to_exact(value) * LITRE.scale, LITRE)


def Kilolitre(value: Numeric) -> Volume:
    """Construct a Volume from a magnitude expressed in kilolitres."""
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
