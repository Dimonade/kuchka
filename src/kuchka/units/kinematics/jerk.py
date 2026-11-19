"""Jerk constructors: metres and millimetres per second cubed.

`Jerk` is the rate at which an acceleration changes, also called jolt: the third
derivative of a position, which a motion profile limits to keep a drive smooth.
The metre per second cubed is the canonical unit.

Examples
--------
A drive that ramps its acceleration at 50 m/s³ for 0.2 s reaches 10 m/s²:

>>> from kuchka import Second
>>> MetrePerSecondCubed(50) * Second(0.2)
10 m/s²

An acceleration changing by 3 m/s² over two seconds has a jerk of 1.5 m/s³:

>>> from kuchka import MetrePerSecondSquared
>>> MetrePerSecondSquared(3) / Second(2)
1.5 m/s³

An S-curve at 1 m/s³ takes 2 s to build up an acceleration of 2 m/s²:

>>> MetrePerSecondSquared(2) / MetrePerSecondCubed(1)
2 s

Datasheets of linear stages often give the limit in millimetres:

>>> MillimetrePerSecondCubed(5000) == MetrePerSecondCubed(5)
True

`JERK_UNITS` maps symbols such as ``"m/s³"`` and ``"mm/s³"`` to their constructors,
for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.Acceleration
    The acceleration a jerk changes.
~kuchka.quantities.TimeCubed
    A jerk times a time cubed is a length.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import JERK
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Jerk
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_THREE = symbols.SUPERSCRIPT_THREE

METRE_PER_SECOND_CUBED = UnitDef(
    "metre_per_second_cubed",
    f"m/s{_THREE}",
    Decimal(1),
    JERK,
    aliases=powered("m/s", 3),
    words=(
        "meter per second cubed",
        "meters per second cubed",
        "metres per second cubed",
    ),
)
MILLIMETRE_PER_SECOND_CUBED = UnitDef(
    "millimetre_per_second_cubed",
    f"mm/s{_THREE}",
    Decimal("0.001"),
    JERK,
    aliases=powered("mm/s", 3),
    words=(
        "millimeter per second cubed",
        "millimeters per second cubed",
        "millimetres per second cubed",
    ),
)

METER_PER_SECOND_CUBED = METRE_PER_SECOND_CUBED
MILLIMETER_PER_SECOND_CUBED = MILLIMETRE_PER_SECOND_CUBED

Jerk._canonical_unit = METRE_PER_SECOND_CUBED  # noqa: SLF001 -- this module owns Jerk's canonical unit


def MetrePerSecondCubed(value: Numeric) -> Jerk:
    """Construct a jerk from a magnitude in metres per second cubed.

    Parameters
    ----------
    value : Numeric
        Jerk magnitude in metres per second cubed.

    Returns
    -------
    Jerk
        Jerk represented in metres per second cubed.

    Examples
    --------
    A jerk of 4 m/s³ adds 8 m/s² of acceleration in two seconds:

    >>> from kuchka import Second
    >>> MetrePerSecondCubed(4) * Second(2)
    8 m/s²

    """
    return Jerk(to_exact(value) * METRE_PER_SECOND_CUBED.scale, METRE_PER_SECOND_CUBED)


MeterPerSecondCubed = MetrePerSecondCubed
"""American spelling, aliasing `MetrePerSecondCubed`: the same function object."""


def MillimetrePerSecondCubed(value: Numeric) -> Jerk:
    """Construct a jerk from a magnitude in millimetres per second cubed.

    Parameters
    ----------
    value : Numeric
        Jerk magnitude in millimetres per second cubed.

    Returns
    -------
    Jerk
        Jerk represented in millimetres per second cubed.

    Examples
    --------
    A millimetre per second cubed is a thousandth of a metre per second cubed:

    >>> MillimetrePerSecondCubed(1) == MetrePerSecondCubed(Decimal("0.001"))
    True

    """
    return Jerk(
        to_exact(value) * MILLIMETRE_PER_SECOND_CUBED.scale,
        MILLIMETRE_PER_SECOND_CUBED,
    )


MillimeterPerSecondCubed = MillimetrePerSecondCubed
"""American spelling, aliasing `MillimetrePerSecondCubed`: the same function object."""


JERK_UNITS: Mapping[str, Callable[[Numeric], Jerk]] = unit_table(
    "JERK_UNITS",
    {
        METRE_PER_SECOND_CUBED: MetrePerSecondCubed,
        MILLIMETRE_PER_SECOND_CUBED: MillimetrePerSecondCubed,
    },
)

JERK_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        MILLIMETRE_PER_SECOND_CUBED,
        METRE_PER_SECOND_CUBED,
    ),
)
"""The units `auto_scale` moves a jerk along, smallest first."""

__all__ = [
    "JERK_LADDERS",
    "JERK_UNITS",
    "METER_PER_SECOND_CUBED",
    "METRE_PER_SECOND_CUBED",
    "MILLIMETER_PER_SECOND_CUBED",
    "MILLIMETRE_PER_SECOND_CUBED",
    "MeterPerSecondCubed",
    "MetrePerSecondCubed",
    "MillimeterPerSecondCubed",
    "MillimetrePerSecondCubed",
]
