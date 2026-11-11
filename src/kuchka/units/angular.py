"""Angle and angular-displacement constructors: turns, radians, degrees, and more.

    from kuchka import Degree
    from kuchka import Radian

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

`AngularDisplacement` is the angle swept, which does not wrap, and it uses the same
units under constructors that end in `Displacement`: `DegreeDisplacement(370)` is 370
degrees of rotation, where `Degree(370)` is the position 10 degrees.
`ANGULAR_DISPLACEMENT_UNITS` maps each symbol to its constructor.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.internal import symbols
from kuchka.internal.constants import PI
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Angle
from kuchka.quantities import AngularDisplacement
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric


TURN = UnitDef(
    "turn", "tr", Fraction(1), ANGLE, aliases=("rev",), words=("revolution",)
)
DEGREE = UnitDef("degree", symbols.DEGREE, Fraction(1, 360), ANGLE, aliases=("deg",))
GRADIAN = UnitDef("gradian", "gon", Fraction(1, 400), ANGLE, aliases=("grad",))
ARCMINUTE = UnitDef(
    "arcminute",
    symbols.PRIME,
    Fraction(1, 21600),
    ANGLE,
    aliases=("'", "arcmin"),
    words=("arc minute", "minute of arc"),
)
ARCSECOND = UnitDef(
    "arcsecond",
    symbols.DOUBLE_PRIME,
    Fraction(1, 1296000),
    ANGLE,
    aliases=('"', "''", f"{symbols.PRIME}{symbols.PRIME}", "arcsec"),
    words=("arc second", "second of arc"),
)
RADIAN = UnitDef("radian", "rad", 1 / (2 * PI), ANGLE)

Angle._canonical_unit = TURN  # noqa: SLF001 -- this module owns Angle's canonical unit
Angle._period = TURN.scale  # noqa: SLF001 -- this module owns Angle's period, one turn in the canonical unit
AngularDisplacement._canonical_unit = TURN  # noqa: SLF001 -- this module owns AngularDisplacement's canonical unit
AngularDisplacement._result_unit = RADIAN  # noqa: SLF001 -- and the unit its arithmetic results display in


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


def TurnDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in turns."""
    return AngularDisplacement(to_exact(value), TURN)


def DegreeDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in degrees."""
    return AngularDisplacement(to_exact(value) * DEGREE.scale, DEGREE)


def RadianDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in radians."""
    return AngularDisplacement(to_exact(value) * RADIAN.scale, RADIAN)


def GradianDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in gradians."""
    return AngularDisplacement(to_exact(value) * GRADIAN.scale, GRADIAN)


def ArcMinuteDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in arcminutes."""
    return AngularDisplacement(to_exact(value) * ARCMINUTE.scale, ARCMINUTE)


def ArcSecondDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in arcseconds."""
    return AngularDisplacement(to_exact(value) * ARCSECOND.scale, ARCSECOND)


ANGLE_UNITS: Mapping[str, Callable[[Numeric], Angle]] = unit_table(
    "ANGLE_UNITS",
    {
        TURN: Turn,
        DEGREE: Degree,
        RADIAN: Radian,
        GRADIAN: Gradian,
        ARCMINUTE: ArcMinute,
        ARCSECOND: ArcSecond,
    },
)

ANGULAR_DISPLACEMENT_UNITS: Mapping[str, Callable[[Numeric], AngularDisplacement]] = (
    unit_table(
        "ANGULAR_DISPLACEMENT_UNITS",
        {
            TURN: TurnDisplacement,
            DEGREE: DegreeDisplacement,
            RADIAN: RadianDisplacement,
            GRADIAN: GradianDisplacement,
            ARCMINUTE: ArcMinuteDisplacement,
            ARCSECOND: ArcSecondDisplacement,
        },
    )
)

__all__ = [
    "ANGLE_UNITS",
    "ANGULAR_DISPLACEMENT_UNITS",
    "ARCMINUTE",
    "ARCSECOND",
    "DEGREE",
    "GRADIAN",
    "RADIAN",
    "TURN",
    "ArcMinute",
    "ArcMinuteDisplacement",
    "ArcSecond",
    "ArcSecondDisplacement",
    "Degree",
    "DegreeDisplacement",
    "Gradian",
    "GradianDisplacement",
    "Radian",
    "RadianDisplacement",
    "Turn",
    "TurnDisplacement",
]
