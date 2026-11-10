"""Kinematic viscosity constructors: square metres per second and the stokes.

    from kuchka import Centistokes, SquareMetrePerSecond

    water = Centistokes(1)
    engine_oil = SquareMetrePerSecond(0.0001)

`KinematicViscosity` is a fluid's viscosity per density, `DynamicViscosity / Density`.
Its canonical unit is the square metre per second (`m²/s`).
The stokes (`St`) is exactly 1 cm²/s, or 0.0001 m²/s, and the centistokes is exactly
1 mm²/s, the unit oils are graded in.
A thermal diffusivity and a diffusion coefficient read as a `KinematicViscosity` too, in
the same units.

Examples
--------
Water at room temperature is about one centistokes, which is one square millimetre per
second:

>>> Centistokes(1) == SquareMillimetrePerSecond(1)
True

The Reynolds number of water at 2 m/s in a 5 cm pipe is one hundred thousand:

>>> from kuchka import Metre, MetrePerSecond
>>> MetrePerSecond(2) * Metre(0.05) / Centistokes(1)
100000 1

A diffusion coefficient quoted in cm²/s, converted:

>>> SquareCentimetrePerSecond(0.2).to(SQUARE_MICROMETRE_PER_SECOND)
20000000 µm²/s

`KINEMATIC_VISCOSITY_UNITS` maps symbols such as ``"m2/s"``, ``"St"``, and ``"cSt"`` to
their constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import KINEMATIC_VISCOSITY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import KinematicViscosity
from kuchka.quantities import UnitDef
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.geometry.area import SQUARE_MILLIMETRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

SQUARE_METRE_PER_SECOND = UnitDef(
    "square_metre_per_second",
    "m²/s",
    1,
    KINEMATIC_VISCOSITY,
    aliases=("m2/s", "m^2/s", "m**2/s"),
    words=(
        "square metre per second",
        "square meter per second",
        "square metres per second",
        "square meters per second",
    ),
)
SQUARE_CENTIMETRE_PER_SECOND = UnitDef(
    "square_centimetre_per_second",
    "cm²/s",
    SQUARE_CENTIMETRE.scale,
    KINEMATIC_VISCOSITY,
    aliases=("cm2/s", "cm^2/s", "cm**2/s"),
    words=(
        "square centimetre per second",
        "square centimeter per second",
        "square centimetres per second",
        "square centimeters per second",
    ),
)
SQUARE_MILLIMETRE_PER_SECOND = UnitDef(
    "square_millimetre_per_second",
    "mm²/s",
    SQUARE_MILLIMETRE.scale,
    KINEMATIC_VISCOSITY,
    aliases=("mm2/s", "mm^2/s", "mm**2/s"),
    words=(
        "square millimetre per second",
        "square millimeter per second",
        "square millimetres per second",
        "square millimeters per second",
    ),
)
SQUARE_MICROMETRE_PER_SECOND = UnitDef(
    "square_micrometre_per_second",
    f"{symbols.MICRO}m²/s",
    Decimal("0.000000000001"),
    KINEMATIC_VISCOSITY,
    aliases=("um2/s", "um^2/s", "um**2/s", f"{symbols.MICRO}m2/s"),
    words=(
        "square micrometre per second",
        "square micrometer per second",
        "square micrometres per second",
        "square micrometers per second",
    ),
)
STOKES = UnitDef(
    "stokes",
    "St",
    SQUARE_CENTIMETRE.scale,
    KINEMATIC_VISCOSITY,
    words=("stokes",),
)
CENTISTOKES = with_prefix(prefixes.CENTI, STOKES)

KinematicViscosity._canonical_unit = SQUARE_METRE_PER_SECOND  # noqa: SLF001 -- this module owns KinematicViscosity's canonical unit


def SquareMetrePerSecond(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from square metres per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in square metres per second.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in square metres per second.

    """
    return KinematicViscosity(
        to_exact(value) * SQUARE_METRE_PER_SECOND.scale, SQUARE_METRE_PER_SECOND
    )


def SquareCentimetrePerSecond(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from square centimetres per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in square centimetres per second.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in square centimetres per second.

    """
    return KinematicViscosity(
        to_exact(value) * SQUARE_CENTIMETRE_PER_SECOND.scale,
        SQUARE_CENTIMETRE_PER_SECOND,
    )


def SquareMillimetrePerSecond(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from square millimetres per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in square millimetres per second.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in square millimetres per second.

    """
    return KinematicViscosity(
        to_exact(value) * SQUARE_MILLIMETRE_PER_SECOND.scale,
        SQUARE_MILLIMETRE_PER_SECOND,
    )


def SquareMicrometrePerSecond(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from square micrometres per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in square micrometres per second.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in square micrometres per second.

    """
    return KinematicViscosity(
        to_exact(value) * SQUARE_MICROMETRE_PER_SECOND.scale,
        SQUARE_MICROMETRE_PER_SECOND,
    )


def Stokes(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from stokes.

    Parameters
    ----------
    value : Numeric
        Magnitude in stokes.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in stokes.

    """
    return KinematicViscosity(to_exact(value) * STOKES.scale, STOKES)


def Centistokes(value: Numeric) -> KinematicViscosity:
    """Construct a KinematicViscosity from centistokes.

    Parameters
    ----------
    value : Numeric
        Magnitude in centistokes.

    Returns
    -------
    KinematicViscosity
        KinematicViscosity represented in centistokes.

    """
    return KinematicViscosity(to_exact(value) * CENTISTOKES.scale, CENTISTOKES)


KINEMATIC_VISCOSITY_UNITS: Mapping[str, Callable[[Numeric], KinematicViscosity]] = (
    unit_table(
        "KINEMATIC_VISCOSITY_UNITS",
        {
            SQUARE_METRE_PER_SECOND: SquareMetrePerSecond,
            SQUARE_CENTIMETRE_PER_SECOND: SquareCentimetrePerSecond,
            SQUARE_MILLIMETRE_PER_SECOND: SquareMillimetrePerSecond,
            SQUARE_MICROMETRE_PER_SECOND: SquareMicrometrePerSecond,
            STOKES: Stokes,
            CENTISTOKES: Centistokes,
        },
    )
)

__all__ = [
    "CENTISTOKES",
    "KINEMATIC_VISCOSITY_UNITS",
    "SQUARE_CENTIMETRE_PER_SECOND",
    "SQUARE_METRE_PER_SECOND",
    "SQUARE_MICROMETRE_PER_SECOND",
    "SQUARE_MILLIMETRE_PER_SECOND",
    "STOKES",
    "Centistokes",
    "SquareCentimetrePerSecond",
    "SquareMetrePerSecond",
    "SquareMicrometrePerSecond",
    "SquareMillimetrePerSecond",
    "Stokes",
]
