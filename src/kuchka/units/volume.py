"""Volume unit constructors: cubic-metric prefixes, alongside Litre and its prefixes.

    from kuchka import Litre, Millilitre

    reagent = Millilitre(500) + Litre(Decimal("0.25"))

`CubicMetre` is the SI-coherent canonical unit (`scale = Decimal(1)`).
A `Litre` is exactly one cubic decimetre (`Decimal("0.001")` m^3), but as it is the
unit that actually shows up in lab and process-engineering work, so it gets its own
full set of prefixes and first grade support.

NOTE: Two pairs below have the exact same scale by coincidence:
- `CubicCentimetre` and `Millilitre` are both `Decimal("0.000001")` m^3, and,
- `CubicMillimetre` and `Microlitre` are both `Decimal("0.000000001")` m^3.

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
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import VOLUME
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import Volume

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

CUBIC_METRE_NAME = "cubic_metre"
CUBIC_METRE_SYMBOL = f"m{symbols.SUPERSCRIPT_THREE}"

# NOTE: same reasoning as kuchka.units.area -- a cubed unit needs the linear prefix's
# scale applied three times, not once, so `prefixed_unit()`'s constructor is not
# flexible enough for it as defined now.
CUBIC_MILLIMETRE = UnitDef(
    "cubic_millimetre",
    f"mm{symbols.SUPERSCRIPT_THREE}",
    prefixes.MILLI.factor * prefixes.MILLI.factor * prefixes.MILLI.factor,
    VOLUME,
)
CUBIC_CENTIMETRE = UnitDef(
    "cubic_centimetre", f"cm{symbols.SUPERSCRIPT_THREE}", Decimal("0.000001"), VOLUME
)
CUBIC_METRE = prefixed_unit(prefixes.UNIT, CUBIC_METRE_NAME, CUBIC_METRE_SYMBOL, VOLUME)

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

MICROLITRE = prefixed_unit(
    prefixes.MICRO, LITRE_NAME, LITRE_SYMBOL, VOLUME, coherent_offset=-3
)
MILLILITRE = prefixed_unit(
    prefixes.MILLI, LITRE_NAME, LITRE_SYMBOL, VOLUME, coherent_offset=-3
)
LITRE = prefixed_unit(
    prefixes.UNIT, LITRE_NAME, LITRE_SYMBOL, VOLUME, coherent_offset=-3
)
KILOLITRE = prefixed_unit(
    prefixes.KILO, LITRE_NAME, LITRE_SYMBOL, VOLUME, coherent_offset=-3
)


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

VOLUME_UNITS: Mapping[str, Callable[[Numeric], Volume]] = MappingProxyType(
    {
        CUBIC_MILLIMETRE.symbol: CubicMillimetre,
        CUBIC_CENTIMETRE.symbol: CubicCentimetre,
        CUBIC_METRE.symbol: CubicMetre,
        MICROLITRE.symbol: Microlitre,
        MILLILITRE.symbol: Millilitre,
        LITRE.symbol: Litre,
        KILOLITRE.symbol: Kilolitre,
    }
)

__all__ = [
    "CUBIC_CENTIMETER",
    "CUBIC_CENTIMETRE",
    "CUBIC_METER",
    "CUBIC_METRE",
    "CUBIC_MILLIMETER",
    "CUBIC_MILLIMETRE",
    "KILOLITRE",
    "LITRE",
    "MICROLITRE",
    "MILLILITRE",
    "VOLUME_UNITS",
    "CubicCentimeter",
    "CubicCentimetre",
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
]
