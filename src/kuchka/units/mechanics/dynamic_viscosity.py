"""Dynamic viscosity constructors: the pascal-second, the poise, and their prefixes.

    from kuchka import Centipoise, MillipascalSecond, PascalSecond

    honey = PascalSecond(10)
    water = MillipascalSecond(1)
    oil = Centipoise(50)

`DynamicViscosity` is how strongly a fluid resists shearing, `Pressure * Time`.
Its canonical unit is the pascal-second (`Pa·s`), which is also a `kg/(m·s)` and an
`N·s/m²`.
The poise (`P`) is exactly 0.1 Pa·s, so the centipoise is exactly one
millipascal-second.

Examples
--------
Water is about one centipoise, which is one millipascal-second:

>>> Centipoise(1) == MillipascalSecond(1)
True

A fluid of 2 Pa·s sheared at 50 1/s carries a shear stress of 100 Pa:

>>> from kuchka import Hertz
>>> PascalSecond(2) * Hertz(50)
100 Pa

The kinematic viscosity of that water, at a density of 1000 kg/m³, is one centistokes:

>>> from kuchka import KilogramPerCubicMetre
>>> from kuchka.units import CENTISTOKES
>>> (MillipascalSecond(1) / KilogramPerCubicMetre(1000)).to(CENTISTOKES)
1 cSt

`DYNAMIC_VISCOSITY_UNITS` maps symbols such as ``"Pa*s"``, ``"mPa s"``, and ``"cP"`` to
their constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import DYNAMIC_VISCOSITY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import DynamicViscosity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

PASCAL_SECOND = UnitDef(
    "pascal_second",
    "Pa·s",
    1,
    DYNAMIC_VISCOSITY,
    aliases=(
        "Pa*s",
        "Pa s",
        "N·s/m2",
        "N*s/m2",
        "N s/m2",
        "kg/(m·s)",
        "kg/(m*s)",
        "kg/(m s)",
        "kg/m/s",
    ),
    words=("pascal second", "pascal-second", "pascal seconds", "pascal-seconds"),
)
MILLIPASCAL_SECOND = UnitDef(
    "millipascal_second",
    "mPa·s",
    Decimal("0.001"),
    DYNAMIC_VISCOSITY,
    aliases=("mPa*s", "mPa s"),
    words=("millipascal second", "millipascal-second"),
)
MICROPASCAL_SECOND = UnitDef(
    "micropascal_second",
    f"{symbols.MICRO}Pa·s",
    Decimal("0.000001"),
    DYNAMIC_VISCOSITY,
    aliases=("uPa*s", "uPa s", f"{symbols.MICRO}Pa*s", f"{symbols.MICRO}Pa s"),
    words=("micropascal second", "micropascal-second"),
)
POISE = UnitDef(
    "poise",
    "P",
    Decimal("0.1"),
    DYNAMIC_VISCOSITY,
    words=("poise",),
)
CENTIPOISE = with_prefix(prefixes.CENTI, POISE)

DynamicViscosity._canonical_unit = PASCAL_SECOND  # noqa: SLF001 -- this module owns DynamicViscosity's canonical unit


def PascalSecond(value: Numeric) -> DynamicViscosity:
    """Construct a DynamicViscosity from pascal-seconds.

    Parameters
    ----------
    value : Numeric
        Magnitude in pascal-seconds.

    Returns
    -------
    DynamicViscosity
        DynamicViscosity represented in pascal-seconds.

    """
    return DynamicViscosity(to_exact(value) * PASCAL_SECOND.scale, PASCAL_SECOND)


def MillipascalSecond(value: Numeric) -> DynamicViscosity:
    """Construct a DynamicViscosity from millipascal-seconds.

    Parameters
    ----------
    value : Numeric
        Magnitude in millipascal-seconds.

    Returns
    -------
    DynamicViscosity
        DynamicViscosity represented in millipascal-seconds.

    """
    return DynamicViscosity(
        to_exact(value) * MILLIPASCAL_SECOND.scale, MILLIPASCAL_SECOND
    )


def MicropascalSecond(value: Numeric) -> DynamicViscosity:
    """Construct a DynamicViscosity from micropascal-seconds.

    Parameters
    ----------
    value : Numeric
        Magnitude in micropascal-seconds.

    Returns
    -------
    DynamicViscosity
        DynamicViscosity represented in micropascal-seconds.

    """
    return DynamicViscosity(
        to_exact(value) * MICROPASCAL_SECOND.scale, MICROPASCAL_SECOND
    )


def Poise(value: Numeric) -> DynamicViscosity:
    """Construct a DynamicViscosity from poise.

    Parameters
    ----------
    value : Numeric
        Magnitude in poise.

    Returns
    -------
    DynamicViscosity
        DynamicViscosity represented in poise.

    """
    return DynamicViscosity(to_exact(value) * POISE.scale, POISE)


def Centipoise(value: Numeric) -> DynamicViscosity:
    """Construct a DynamicViscosity from centipoise.

    Parameters
    ----------
    value : Numeric
        Magnitude in centipoise.

    Returns
    -------
    DynamicViscosity
        DynamicViscosity represented in centipoise.

    """
    return DynamicViscosity(to_exact(value) * CENTIPOISE.scale, CENTIPOISE)


DYNAMIC_VISCOSITY_UNITS: Mapping[str, Callable[[Numeric], DynamicViscosity]] = (
    unit_table(
        "DYNAMIC_VISCOSITY_UNITS",
        {
            PASCAL_SECOND: PascalSecond,
            MILLIPASCAL_SECOND: MillipascalSecond,
            MICROPASCAL_SECOND: MicropascalSecond,
            POISE: Poise,
            CENTIPOISE: Centipoise,
        },
    )
)

__all__ = [
    "CENTIPOISE",
    "DYNAMIC_VISCOSITY_UNITS",
    "MICROPASCAL_SECOND",
    "MILLIPASCAL_SECOND",
    "PASCAL_SECOND",
    "POISE",
    "Centipoise",
    "MicropascalSecond",
    "MillipascalSecond",
    "PascalSecond",
    "Poise",
]
