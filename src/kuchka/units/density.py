"""Density unit constructors, one per naming tradition it commonly appears in.

    from kuchka import KilogramPerCubicMetre, GramPerCubicCentimetre

    steel = KilogramPerCubicMetre(7850)
    water = GramPerCubicCentimetre(1)

`GramPerCubicCentimetre` and `KilogramPerLitre` share the same scale relative to
the canonical unit (`1000`), the same coincidence `Millilitre`/`CubicCentimetre`
have in `volume.py`.
These are two different naming traditions -- materials-science and
liquid-measure -- they agree numerically, kept as separate `UnitDef`s.

`DENSITY_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import DENSITY
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Density
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

KILOGRAM_PER_CUBIC_METRE = UnitDef(
    "kilogram_per_cubic_metre",
    "kg/m\u00b3",
    Decimal(1),
    DENSITY,
)
GRAM_PER_CUBIC_CENTIMETRE = UnitDef(
    "gram_per_cubic_centimetre",
    "g/cm\u00b3",
    Decimal(1000),
    DENSITY,
)

KILOGRAM_PER_CUBIC_METER = KILOGRAM_PER_CUBIC_METRE
GRAM_PER_CUBIC_CENTIMETER = GRAM_PER_CUBIC_CENTIMETRE

Density._canonical_unit = KILOGRAM_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns Density's canonical unit

KILOGRAM_PER_LITRE = UnitDef("kilogram_per_litre", "kg/L", Decimal(1000), DENSITY)


def KilogramPerCubicMetre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in kilograms per cubic metre."""
    return Density(
        to_exact(value) * KILOGRAM_PER_CUBIC_METRE.scale,
        KILOGRAM_PER_CUBIC_METRE,
    )


def GramPerCubicCentimetre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in grams per cubic centimetre."""
    return Density(
        to_exact(value) * GRAM_PER_CUBIC_CENTIMETRE.scale,
        GRAM_PER_CUBIC_CENTIMETRE,
    )


def KilogramPerLitre(value: Numeric) -> Density:
    """Construct a Density from a magnitude expressed in kilograms per litre."""
    return Density(to_exact(value) * KILOGRAM_PER_LITRE.scale, KILOGRAM_PER_LITRE)


KilogramPerCubicMeter = KilogramPerCubicMetre
GramPerCubicCentimeter = GramPerCubicCentimetre


DENSITY_UNITS: Mapping[str, Callable[[Numeric], Density]] = MappingProxyType(
    {
        KILOGRAM_PER_CUBIC_METRE.symbol: KilogramPerCubicMetre,
        GRAM_PER_CUBIC_CENTIMETRE.symbol: GramPerCubicCentimetre,
        KILOGRAM_PER_LITRE.symbol: KilogramPerLitre,
    }
)

__all__ = [
    "DENSITY_UNITS",
    "GRAM_PER_CUBIC_CENTIMETER",
    "GRAM_PER_CUBIC_CENTIMETRE",
    "KILOGRAM_PER_CUBIC_METER",
    "KILOGRAM_PER_CUBIC_METRE",
    "KILOGRAM_PER_LITRE",
    "GramPerCubicCentimeter",
    "GramPerCubicCentimetre",
    "KilogramPerCubicMeter",
    "KilogramPerCubicMetre",
    "KilogramPerLitre",
]
