"""Area quantities and constructors for metric and selected non-SI units.

`Area` represents two-dimensional extent.
The square metre is the canonical SI unit, while the constructors in this module
provide convenient entry points from metric scales and a small set of exact non-SI
units.

`Metre` is the canonical spelling used by `Length`, and the area constructors follow
the same convention:
`SquareMetre` is canonical, while `SquareMeter` is a true alias of the same object.
The same applies to all prefixed metre constructors.

Metric area prefixes are applied to both dimensions.
Consequently, a millimetre-based area is scaled by `10^-6` relative to the square
metre, while a kilometre-based area is scaled by `10^6`.

`Hectare` is an exact non-SI unit equal to 10,000 m².
It is especially useful for land and forestry, where square metres quickly become
cumbersome.

`Acre` and `SquareInch` are exact international units.
An acre is exactly 4,046.8564224 m², while a square inch is exactly 645.16 mm².
These conversions carry the same exact-arithmetic guarantees as the metric units.

Examples
--------
Area becomes much easier to reason about when attached to physical spaces.

A modest building footprint might cover 120 m²:

>>> house_footprint = SquareMetre(120)
>>> house_footprint
120 m²

A garden can be described by the same quantity.
A 20 m by 25 m garden has an area of 500 m²:

>>> garden = SquareMetre(500)
>>> garden
500 m²

A two-hectare parcel contains exactly 20,000 m²:

>>> parcel = Hectare(2)
>>> parcel
2 ha

>>> parcel == SquareMetre(20_000)
True

This makes hectares useful once land areas become inconvenient to express in square
metres.
A 2 ha parcel containing a 120 m² building and a 500 m² garden still has 19,380 m² of
remaining area:

>>> house_footprint = SquareMetre(120)
>>> garden = SquareMetre(500)
>>> parcel = Hectare(2)
>>> remaining = parcel - house_footprint - garden
>>> remaining
19380 m²

A hectare also has a memorable geometric interpretation:
it is exactly the area of a 100 m by 100 m square.

>>> field = SquareMetre(10_000)
>>> field == Hectare(1)
True

Smaller areas are useful in engineering as well.
A 100 mm by 50 mm component panel covers 5,000 mm²:

>>> panel = SquareMillimetre(5000)
>>> panel
5000 mm²

which is exactly 50 cm²:

>>> panel == SquareCentimetre(50)
True

Square inches are still encountered in engineering drawings and component dimensions.
A surface measuring 4 by 2 inches has exactly 8 square inches:

>>> mounting_plate = SquareInch(8)
>>> mounting_plate
8 in²

The conversion to metric area is exact:

>>> mounting_plate == SquareCentimetre(51.6128)
True

Acre is useful when the scale is that of agricultural or rural land rather than a
building footprint.
One acre is exactly 4,046.8564224 m²:

>>> one_acre = Acre(1)
>>> one_acre
1 ac

>>> one_acre == SquareMetre(4046.8564224)
True

Two acres can be combined with a metric parcel without losing their common meaning:

>>> total_land = Acre(2) + SquareMetre(500)
>>> total_land
8593.7128448 m²

Area is therefore a single quantity spanning the scale of a small component surface, a
house, a garden, a field, and a rural property.

Notes
-----
Area scales quadratically with length.

If a length is multiplied by a factor `k`, the corresponding area is multiplied by
`k²`.
This is why

`1 mm² = 0.000001 m²`

rather than `0.001 m²`.

The same rule applies to larger metric units:

`1 km² = 1,000,000 m²`.

Metric conversions are exact powers of ten, and the non-SI units implemented here are
exact by definition.
Consequently, conversions such as

>>> SquareMillimetre(1_000_000) == SquareMetre(1)
True

and

>>> SquareKilometre(1) == SquareMetre(1_000_000)
True

hold exactly.

`Hectare` is exactly 10,000 m².

`Acre` is exactly 4,046.8564224 m².
The value follows from the international acre definition of 4,840 square yards together
with the exact international yard definition of 0.9144 m.

`SquareInch` is exactly 0.00064516 m² because one inch is exactly 0.0254 m.

`AREA_UNITS` maps symbols such as ``"mm²"``, ``"cm²"``, ``"m²"``, ``"km²"``, ``"ha"``,
and ``"in²"`` to their constructors.
This is intended for boundary code that receives units as external data, such as
configuration files.

See Also
--------
~kuchka.quantities.Length
    One-dimensional distance from which area is conceptually derived.
~kuchka.quantities.Volume
    Three-dimensional extent derived from length.
~kuchka.units.length
    Metric and selected non-SI length constructors.

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
# A squared unit like `mm²` needs the *linear* millimetre's scale applied twice
# (mm² relative to m² is `(10⁻³)²`, not `10⁻³`), so these `UnitDefs`` are built
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
    """Construct an Area from a magnitude expressed in square millimetres.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square millimetres.

    Returns
    -------
    Area
        Area represented in square millimetres.

    Examples
    --------
    A 100 mm by 50 mm panel covers exactly 5,000 mm²:

    >>> panel = SquareMillimetre(5000)
    >>> panel
    5000 mm²

    The same surface is exactly 50 cm²:

    >>> SquareMillimetre(5000) == SquareCentimetre(50)
    True

    """
    return Area(to_exact(value) * SQUARE_MILLIMETRE.scale, SQUARE_MILLIMETRE)


def SquareCentimetre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square centimetres.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square centimetres.

    Returns
    -------
    Area
        Area represented in square centimetres.

    Examples
    --------
    A 20 cm by 25 cm work surface covers exactly 500 cm²:

    >>> work_surface = SquareCentimetre(500)
    >>> work_surface
    500 cm²

    One hundred square centimetres make exactly one square metre:

    >>> SquareCentimetre(10_000) == SquareMetre(1)
    True

    """
    return Area(to_exact(value) * SQUARE_CENTIMETRE.scale, SQUARE_CENTIMETRE)


def SquareMetre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square metres.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square metres.

    Returns
    -------
    Area
        Area represented in square metres.

    Examples
    --------
    A 120 m² building footprint is naturally represented in square metres:

    >>> footprint = SquareMetre(120)
    >>> footprint
    120 m²

    A 100 m by 100 m square covers exactly one hectare:

    >>> SquareMetre(10_000) == Hectare(1)
    True

    """
    return Area(to_exact(value) * SQUARE_METRE.scale, SQUARE_METRE)


def SquareKilometre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square kilometres.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square kilometres.

    Returns
    -------
    Area
        Area represented in square kilometres.

    Examples
    --------
    A one-square-kilometre area contains exactly one million square metres:

    >>> district = SquareKilometre(1)
    >>> district
    1 km²

    >>> district == SquareMetre(1_000_000)
    True

    """
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
    """Construct an Area from a magnitude expressed in hectares.

    Parameters
    ----------
    value : Numeric
        Area magnitude in hectares.

    Returns
    -------
    Area
        Area represented in hectares.

    Examples
    --------
    A two-hectare field contains exactly 20,000 m²:

    >>> field = Hectare(2)
    >>> field
    2 ha

    >>> field == SquareMetre(20_000)
    True

    """
    return Area(to_exact(value) * HECTARE.scale, HECTARE)


def Acre(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in acres.

    Parameters
    ----------
    value : Numeric
        Area magnitude in acres.

    Returns
    -------
    Area
        Area represented in acres.

    Notes
    -----
    An acre is exactly 4,046.8564224 m².
    It is derived from 4,840 square international yards and the exact international
    yard definition.

    Examples
    --------
    One acre is slightly larger than 4,000 m²:

    >>> property_area = Acre(1)
    >>> property_area > SquareMeter(4_000)
    True

    The conversion is exact:

    >>> Acre(1) == SquareMetre(4046.8564224)
    True

    """
    return Area(to_exact(value) * ACRE.scale, ACRE)


def SquareInch(value: Numeric) -> Area:
    """Construct an Area from a magnitude expressed in square inches.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square inches.

    Returns
    -------
    Area
        Area represented in square inches.

    Notes
    -----
    One square inch is exactly 645.16 mm² because one international inch is exactly
    25.4 mm.

    Examples
    --------
    A 4 by 2 inch engineering surface has an area of exactly 8 in²:

    >>> mounting_plate = SquareInch(8)
    >>> mounting_plate
    8 in²

    The metric equivalent is exact:

    >>> SquareInch(8) == SquareCentimetre(51.6128)
    True

    """
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
