"""Unit constructors for Angle: Radian, Degree, Turn, Gradian, ArcMinute, ArcSecond.

    from kuchka import Radian, Degree

    heading = Degree(90) + Degree(45)
    sensor_reading = Radian(1.5707963)

Radian is the canonical unit: the SI-coherent unit for plane angle, and the unit every
other constructor here is scaled relative to.
`Radian(value)` is an ordinary unit constructor, exactly like `Degree(value)` or
`Volt(value)`:
a sensor or config value already expressed in radians is stored exactly, with no
approximation step at the boundary.

One full turn is two pi radians, which is an irrational number.
kuchka defines its own fixed, deterministic, finite rational representation of pi,
`_PI` below, and uses it to define Degree/Turn/Gradian/ArcMinute/ArcSecond's scales
relative to Radian.
The approximation is confined entirely to those five scale definitions, chosen once
here.

Angle's arithmetic is exact relative to kuchka's own `_PI`, not to the true,
irrational, transcendental pi.
Two angles built entirely from Degree, Turn, Gradian, ArcMinute, and ArcSecond compare
exactly as their true rational relationship dictates: `_PI` cancels out of every such
comparison (`Degree(180) / Turn(1) == Fraction(1, 2)` exactly, regardless of `_PI`'s
value).
A `Radian`-built value compares exactly to kuchka's own `_PI`, and to nothing more or
less precise than that.

Concretely: `Radian(math.pi) == Degree(180)` is `False`.
Python's `math.pi` is a binary-float approximation of pi at roughly 17 significant
digits.
kuchka's `_PI` is a separately chosen decimal value at 15.
The two numbers are close but not identical, and exact `Fraction` equality reports
exactly that.
This is correct behavior under this design, not a bug: to build a `Radian` value that
is guaranteed to compare equal to a `Degree`-family value, construct it from
`kuchka.units.angular._PI` itself, not from an independently sourced pi.

`ANGLE_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.internal import symbols
from kuchka.internal.constants import _PI
from kuchka.numeric import to_exact
from kuchka.quantities import Angle
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric


RADIAN = UnitDef("radian", "rad", Fraction(1), ANGLE)
DEGREE = UnitDef("degree", symbols.DEGREE, _PI / 180, ANGLE)
GRADIAN = UnitDef("gradian", "gon", _PI / 200, ANGLE)
ARCMINUTE = UnitDef("arcminute", symbols.PRIME, _PI / 10800, ANGLE)
ARCSECOND = UnitDef("arcsecond", symbols.DOUBLE_PRIME, _PI / 648000, ANGLE)
TURN = UnitDef("turn", "tr", 2 * _PI, ANGLE)

Angle._canonical_unit = RADIAN  # noqa: SLF001 -- this module owns Angle's canonical unit
Angle._period = TURN.scale  # noqa: SLF001 -- this module owns Angle's period, tied to its canonical unit choice


def Radian(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in radians."""
    return Angle(to_exact(value), RADIAN)


def Degree(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in degrees."""
    return Angle(to_exact(value) * DEGREE.scale, DEGREE)


def Turn(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in turns."""
    return Angle(to_exact(value) * TURN.scale, TURN)


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
        RADIAN.symbol: Radian,
        DEGREE.symbol: Degree,
        TURN.symbol: Turn,
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
