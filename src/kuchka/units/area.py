"""Area unit constructors: metric prefixes, and imperial Hectare, Acre, and SquareInch.

    from kuchka import SquareMetre, Hectare

    plot = Hectare(2) + SquareMetre(500)

Area follows the `Length`'s naming convension -- `Metre` is canonical, `Meter` and its
prefixed forms are plain aliases for American English use, the exact same objects,
aliased.

`Hectare` (`10 000 m^2` exactly) and `Acre` are the two non-SI area units that actually
show up in the wild often enough to be worth naming.

`Acre` derives from the same 1959 international yard definition that makes `Inch` and
`SquareInch` exact:
- `1 acre = 4840 yd^2`, and,
- a yard has been exactly `0.9144 m` since 1959,

Therefore,  `Acre`'s scale (`4046.8564224 m^2`) carries no rounding error, following
the same guarantee `Inch` already gives `Length`.

`AREA_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import AREA
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Area
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

SQUARE_METRE_NAME = "square_metre"
SQUARE_METRE_SYMBOL = f"m{symbols.SUPERSCRIPT_TWO}"

# NOTE: `prefixed_unit()` is built for linear dimensions, where a prefix scales the
# coherent unit once.
# A squared unit like `mm^2` needs the *linear* millimetre's scale applied twice
# (mm^2 relative to m^2 is `(10^-3)^2`, not `10^-3`), so these `UnitDefs`` are built
# directly, as `prefixed_unit()` does not supply this construction.
SQUARE_MILLIMETRE = UnitDef(
    "square_millimetre",
    f"mm{symbols.SUPERSCRIPT_TWO}",
    prefixes.MILLI.factor * prefixes.MILLI.factor,
    AREA,
)
SQUARE_CENTIMETRE = UnitDef(
    "square_centimetre",
    f"cm{symbols.SUPERSCRIPT_TWO}",
    prefixes.CENTI.factor * prefixes.CENTI.factor,
    AREA,
)
SQUARE_METRE = prefixed_unit(
    prefixes.UNIT, SQUARE_METRE_NAME, SQUARE_METRE_SYMBOL, AREA
)
SQUARE_KILOMETRE = UnitDef(
    "square_kilometre",
    f"km{symbols.SUPERSCRIPT_TWO}",
    prefixes.KILO.factor * prefixes.KILO.factor,
    AREA,
)

SQUARE_MILLIMETER = SQUARE_MILLIMETRE
SQUARE_CENTIMETER = SQUARE_CENTIMETRE
SQUARE_METER = SQUARE_METRE
SQUARE_KILOMETER = SQUARE_KILOMETRE

Area._canonical_unit = SQUARE_METRE  # noqa: SLF001 -- this module owns Area's canonical unit


def SquareMillimetre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square millimetres."""
    return Area(to_exact(value) * SQUARE_MILLIMETRE.scale, SQUARE_MILLIMETRE)


def SquareCentimetre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square centimetres."""
    return Area(to_exact(value) * SQUARE_CENTIMETRE.scale, SQUARE_CENTIMETRE)


def SquareMetre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square metres."""
    return Area(to_exact(value) * SQUARE_METRE.scale, SQUARE_METRE)


def SquareKilometre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square kilometres."""
    return Area(to_exact(value) * SQUARE_KILOMETRE.scale, SQUARE_KILOMETRE)


SquareMillimeter = SquareMillimetre
SquareCentimeter = SquareCentimetre
SquareMeter = SquareMetre
SquareKilometer = SquareKilometre


# Non-SI units.

HECTARE = UnitDef("hectare", "ha", Decimal(10_000), AREA)
ACRE = UnitDef("acre", "ac", Decimal("4046.8564224"), AREA)
SQUARE_INCH = UnitDef(
    "square_inch", f"in{symbols.SUPERSCRIPT_TWO}", Decimal("0.00064516"), AREA
)


def Hectare(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in hectares."""
    return Area(to_exact(value) * HECTARE.scale, HECTARE)


def Acre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in acres.

    Exact, not approximate: an acre has been precisely `4840` international square
    yards since 1959, the same yard definition that makes `Inch` exact.
    """
    return Area(to_exact(value) * ACRE.scale, ACRE)


def SquareInch(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square inches."""
    return Area(to_exact(value) * SQUARE_INCH.scale, SQUARE_INCH)


AREA_UNITS: Mapping[str, Callable[[Numeric], Area]] = MappingProxyType(
    {
        SQUARE_MILLIMETRE.symbol: SquareMillimetre,
        SQUARE_CENTIMETRE.symbol: SquareCentimetre,
        SQUARE_METRE.symbol: SquareMetre,
        SQUARE_KILOMETRE.symbol: SquareKilometre,
        HECTARE.symbol: Hectare,
        ACRE.symbol: Acre,
        SQUARE_INCH.symbol: SquareInch,
    }
)

__all__ = [
    "ACRE",
    "AREA_UNITS",
    "HECTARE",
    "SQUARE_CENTIMETER",
    "SQUARE_CENTIMETRE",
    "SQUARE_INCH",
    "SQUARE_KILOMETER",
    "SQUARE_KILOMETRE",
    "SQUARE_METER",
    "SQUARE_METRE",
    "SQUARE_MILLIMETER",
    "SQUARE_MILLIMETRE",
    "Acre",
    "Hectare",
    "SquareCentimeter",
    "SquareCentimetre",
    "SquareInch",
    "SquareKilometer",
    "SquareKilometre",
    "SquareMeter",
    "SquareMetre",
    "SquareMillimeter",
    "SquareMillimetre",
]
