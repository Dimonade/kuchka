"""Unit constructors for Angle: Degree, Turn, Gradian, ArcMinute, ArcSecond, Radian.

    from kuchka import Degree, Turn

    heading = Degree(90) + Degree(45)
    full_circle = Turn(1)

Turn is the canonical unit: one full turn is `Fraction(1)`.
Every other working unit here is an exact rational fraction of a turn:
- `1 degree = 1/360 turn`,
- `1 gradian = 1/400 turn`,
- `1 arcminute = 1/21600 turn`,
- `1 arcsecond = 1/1296000 turn`.

Thus, construction, arithmetic, and `.to()` between any pair of them are all exact.

`Radian` needs pi, which has no exact rational representation, so it raises
`PlannedDimensionError` unconditionally.
`Angle.to_lossy()` is the explicit approximate escape hatch for reading an angle as a
`Decimal` count of radians.

`ANGLE_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
`"rad"` maps to `Radian`, so a config field naming radians fails with a clear
`PlannedDimensionError`.
"""

from __future__ import annotations

from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.errors import PlannedDimensionError
from kuchka.numeric import to_exact
from kuchka.quantities import Angle
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

TURN = UnitDef("turn", "tr", Fraction(1), ANGLE)
DEGREE = UnitDef("degree", "\u00b0", Fraction(1, 360), ANGLE)
GRADIAN = UnitDef("gradian", "gon", Fraction(1, 400), ANGLE)
ARCMINUTE = UnitDef("arcminute", "\u2032", Fraction(1, 21600), ANGLE)
ARCSECOND = UnitDef("arcsecond", "\u2033", Fraction(1, 1296000), ANGLE)

Angle._period = Fraction(1)  # noqa: SLF001 -- this module owns Angle's period, tied to its canonical unit choice
Angle._canonical_unit = TURN  # noqa: SLF001 -- this module owns Angle's canonical unit


def Turn(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in turns."""
    return Angle(to_exact(value) * TURN.scale, TURN)


def Degree(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in degrees."""
    return Angle(to_exact(value) * DEGREE.scale, DEGREE)


def Gradian(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in gradians."""
    return Angle(to_exact(value) * GRADIAN.scale, GRADIAN)


def ArcMinute(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcminutes."""
    return Angle(to_exact(value) * ARCMINUTE.scale, ARCMINUTE)


def ArcSecond(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcseconds."""
    return Angle(to_exact(value) * ARCSECOND.scale, ARCSECOND)


_PLANNED_NAME = "Angle"


def Radian(value: Numeric) -> Angle:  # noqa: ARG001 -- signature kept stable for when this is implemented.
    """Raise `PlannedDimensionError` unconditionally. Not implemented.

    Blocked on an exact representation for pi: `Angle.to_lossy()` is the
    approximate escape hatch for reading an angle as a `Decimal` count of
    radians.
    """
    raise PlannedDimensionError(ANGLE, _PLANNED_NAME)


ANGLE_UNITS: Mapping[str, Callable[[Numeric], Angle]] = MappingProxyType(
    {
        TURN.symbol: Turn,
        DEGREE.symbol: Degree,
        GRADIAN.symbol: Gradian,
        ARCMINUTE.symbol: ArcMinute,
        ARCSECOND.symbol: ArcSecond,
        "rad": Radian,
    }
)

__all__ = [
    "ANGLE_UNITS",
    "ARCMINUTE",
    "ARCSECOND",
    "DEGREE",
    "GRADIAN",
    "TURN",
    "ArcMinute",
    "ArcSecond",
    "Degree",
    "Gradian",
    "Radian",
    "Turn",
]
