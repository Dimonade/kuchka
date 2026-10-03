"""Unit constructors for Angle: Turn, Degree, Radian, Gradian, ArcMinute, ArcSecond.

    from kuchka import Radian, Degree

    heading = Degree(90) + Degree(45)
    sensor_reading = Radian(1.5707963)

Turn is the canonical unit: one full circle.
Degree, Gradian, ArcMinute, and ArcSecond are plain rational fractions of a turn
(a degree is 1/360, a gradian 1/400, an arcminute 1/21600, an arcsecond 1/1296000),
so every conversion and comparison among them and `Turn` is exact, and pi appears
nowhere in them.

Radian is the one unit tied to a turn by an irrational number: a turn is two pi
radians.
kuchka converts it with pi held as an exact rational to 100 decimal places
(`kuchka.internal.constants.PI`), which puts the error of a conversion to or from
radians below one part in 1E+100, far past the digits any display shows.
A value built in radians returns exactly what was given from `value_in(RADIAN)`.

A radian value that comes out of floating-point arithmetic is a rounded approximation
of the angle, and it is not exactly equal to the same angle written in degrees:
`Radian(math.pi / 2) == Degree(90)` is `False`, in the way `0.1 + 0.2 == 0.3` is.
`Angle.is_close(other, tolerance=...)` asks the question that is meant, with the
tolerance written down as an angle.

`ANGLE_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.numeric import to_exact
from kuchka.quantities import Angle
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric


TURN = UnitDef("turn", "tr", Fraction(1), ANGLE)
DEGREE = UnitDef("degree", symbols.DEGREE, Fraction(1, 360), ANGLE)
GRADIAN = UnitDef("gradian", "gon", Fraction(1, 400), ANGLE)
ARCMINUTE = UnitDef("arcminute", symbols.PRIME, Fraction(1, 21600), ANGLE)
ARCSECOND = UnitDef("arcsecond", symbols.DOUBLE_PRIME, Fraction(1, 1296000), ANGLE)
RADIAN = UnitDef("radian", "rad", 1 / (2 * PI), ANGLE)

Angle._canonical_unit = TURN  # noqa: SLF001 -- this module owns Angle's canonical unit
Angle._period = TURN.scale  # noqa: SLF001 -- this module owns Angle's period, one turn in the canonical unit


def Radian(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in radians."""
    return Angle(to_exact(value) * RADIAN.scale, RADIAN)


def Degree(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in degrees."""
    return Angle(to_exact(value) * DEGREE.scale, DEGREE)


def Turn(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in turns."""
    return Angle(to_exact(value), TURN)


def Gradian(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in gradians."""
    return Angle(to_exact(value) * GRADIAN.scale, GRADIAN)


def ArcMinute(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcminutes."""
    return Angle(to_exact(value) * ARCMINUTE.scale, ARCMINUTE)


def ArcSecond(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcseconds."""
    return Angle(to_exact(value) * ARCSECOND.scale, ARCSECOND)


ANGLE_UNITS: Mapping[str, Callable[[Numeric], Angle]] = MappingProxyType(
    {
        TURN.symbol: Turn,
        DEGREE.symbol: Degree,
        RADIAN.symbol: Radian,
        GRADIAN.symbol: Gradian,
        ARCMINUTE.symbol: ArcMinute,
        ARCSECOND.symbol: ArcSecond,
    }
)

__all__ = [
    "ANGLE_UNITS",
    "ARCMINUTE",
    "ARCSECOND",
    "DEGREE",
    "GRADIAN",
    "RADIAN",
    "TURN",
    "ArcMinute",
    "ArcSecond",
    "Degree",
    "Gradian",
    "Radian",
    "Turn",
]
