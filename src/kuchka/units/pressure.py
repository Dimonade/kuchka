"""Pressure unit constructors, from SI-prefixed pascals to psi.

    from kuchka import Pascal, Bar, PoundPerSquareInch

    tyre_pressure = Bar(2.2)
    tank_rating = PoundPerSquareInch(3000)

`Bar`, `Millibar`, and `Atmosphere` are all exact by definition (`100 000`, `100`,
and `101 325` Pa respectively).
`PoundPerSquareInch` is exact too, but for a different reason:
it is computed directly from `kuchka`'s own already-exact `POUND_FORCE` and
`SQUARE_INCH` scales (`kuchka.units.kinematics.POUND_FORCE`,
`kuchka.units.area.SQUARE_INCH`) rather than a separately hand-typed literal, so
it can never drift out of sync with either.

`Millibar` and `Hectopascal` share the same scale (`100`), the same coincidence
`Litre`/`CubicDecimetre`-style units have elsewhere.
They are two different naming traditions -- meteorology and SI prefixing -- that happen
to agree numerically.

`PRESSURE_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import PRESSURE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Pressure
from kuchka.quantities import UnitDef
from kuchka.units.area import SQUARE_INCH
from kuchka.units.kinematics import POUND_FORCE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

PASCAL_NAME = "pascal"
PASCAL_SYMBOL = "Pa"

PASCAL = prefixed_unit(prefixes.UNIT, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
HECTOPASCAL = prefixed_unit(prefixes.HECTO, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
KILOPASCAL = prefixed_unit(prefixes.KILO, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)
MEGAPASCAL = prefixed_unit(prefixes.MEGA, PASCAL_NAME, PASCAL_SYMBOL, PRESSURE)

Pressure._canonical_unit = PASCAL  # noqa: SLF001 -- this module owns Pressure's canonical unit


def Pascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in pascals."""
    return Pressure(to_exact(value) * PASCAL.scale, PASCAL)


def Hectopascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in hectopascals."""
    return Pressure(to_exact(value) * HECTOPASCAL.scale, HECTOPASCAL)


def Kilopascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in kilopascals."""
    return Pressure(to_exact(value) * KILOPASCAL.scale, KILOPASCAL)


def Megapascal(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in megapascals."""
    return Pressure(to_exact(value) * MEGAPASCAL.scale, MEGAPASCAL)


# Non-SI units.

BAR = UnitDef("bar", "bar", Decimal(100_000), PRESSURE)
MILLIBAR = UnitDef("millibar", "mbar", Decimal(100), PRESSURE)
ATMOSPHERE = UnitDef("atmosphere", "atm", Decimal(101_325), PRESSURE)
POUND_PER_SQUARE_INCH = UnitDef(
    "pound_per_square_inch",
    "psi",
    POUND_FORCE.scale / SQUARE_INCH.scale,
    PRESSURE,
)


def Bar(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in bar.

    Exact: a bar is defined as precisely 100 000 Pa.
    """
    return Pressure(to_exact(value) * BAR.scale, BAR)


def Millibar(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in millibar."""
    return Pressure(to_exact(value) * MILLIBAR.scale, MILLIBAR)


def Atmosphere(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in standard atmospheres.

    Exact: the standard atmosphere is defined as precisely 101 325 Pa.
    """
    return Pressure(to_exact(value) * ATMOSPHERE.scale, ATMOSPHERE)


def PoundPerSquareInch(value: Numeric) -> Pressure:
    """Construct a Pressure from a magnitude expressed in pounds per square inch.

    Exact: see `POUND_PER_SQUARE_INCH`'s own docstring.
    """
    return Pressure(
        to_exact(value) * POUND_PER_SQUARE_INCH.scale,
        POUND_PER_SQUARE_INCH,
    )


PRESSURE_UNITS: Mapping[str, Callable[[Numeric], Pressure]] = unit_table(
    "PRESSURE_UNITS",
    {
        PASCAL: Pascal,
        HECTOPASCAL: Hectopascal,
        KILOPASCAL: Kilopascal,
        MEGAPASCAL: Megapascal,
        BAR: Bar,
        MILLIBAR: Millibar,
        ATMOSPHERE: Atmosphere,
        POUND_PER_SQUARE_INCH: PoundPerSquareInch,
    },
)

__all__ = [
    "ATMOSPHERE",
    "BAR",
    "HECTOPASCAL",
    "KILOPASCAL",
    "MEGAPASCAL",
    "MILLIBAR",
    "PASCAL",
    "POUND_PER_SQUARE_INCH",
    "PRESSURE_UNITS",
    "Atmosphere",
    "Bar",
    "Hectopascal",
    "Kilopascal",
    "Megapascal",
    "Millibar",
    "Pascal",
    "PoundPerSquareInch",
]
