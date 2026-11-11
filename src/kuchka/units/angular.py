"""Angle and angular-displacement constructors: turns, radians, degrees, and more.

`Angle` is a position on a circle, and it wraps around the circle.
`AngularDisplacement` is the angle swept, and it keeps counting past a full turn.
Both use the same six units, and the displacement constructors end in `Displacement`:

>>> from kuchka import Degree
>>> from kuchka import DegreeDisplacement
>>> heading = Degree(90) + Degree(45)
>>> spin = DegreeDisplacement(720)

The turn is the canonical unit, one full circle.
The degree, gradian, arcminute, and arcsecond are rational fractions of a turn (a degree
is 1/360, a gradian 1/400, an arcminute 1/21600, an arcsecond 1/1296000), so every
conversion and comparison among them and the turn is exact, with no pi in any of them.
The radian is the one unit tied to a turn by an irrational number, and the library holds
pi as an exact rational to 100 decimal places.

Arcseconds and arcminutes belong to astronomy and surveying, where the Sun is a half
degree wide and a star's parallax is a fraction of an arcsecond.
Degrees suit navigation, machinery, and everyday use, gradians suit European surveying,
radians suit physics and signal processing, and turns count the rotations of a shaft.

Examples
--------
A ship holds a heading of 350 degrees and the next waypoint lies on a bearing of
10 degrees.
Angles wrap, so the turn to make is the short way round, 20 degrees to starboard:

>>> from kuchka import Degree
>>> heading = Degree(350)
>>> bearing = Degree(10)
>>> bearing.difference(heading)
20 °
>>> heading + Degree(20)
10 °

A displacement keeps its turns, so a wheel that turns through 720 degrees in 2 s is
spinning at one revolution per second:

>>> from kuchka import DegreeDisplacement
>>> from kuchka import Second
>>> from kuchka.units import REVOLUTION_PER_MINUTE
>>> (DegreeDisplacement(720) / Second(2)).to(REVOLUTION_PER_MINUTE)
60 rpm

The position of a heading has no rate of its own, and the library refuses to divide it
by a time:

>>> Degree(90) / Second(2)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

An arm of 2 m that swings through half a radian moves its tip along an arc of 1 m,
and an arc over a radius gives the angle back:

>>> from kuchka import AngularDisplacement
>>> from kuchka import Metre
>>> from kuchka import RadianDisplacement
>>> RadianDisplacement(0.5) * Metre(2)
1 m
>>> AngularDisplacement.from_arc(Metre(1), Metre(2))
0.5 rad

The parsec is the distance at which one astronomical unit spans one arcsecond, and the
arc over the radius shows it exactly:

>>> from kuchka import AstronomicalUnit
>>> from kuchka import Parsec
>>> from kuchka.units import ARCSECOND
>>> AngularDisplacement.from_arc(AstronomicalUnit(1), Parsec(1)).to(ARCSECOND)
1 ″

Notes
-----
A value built in radians returns exactly what was given from `value_in(RADIAN)`, and a
conversion to or from radians is accurate to better than one part in 1E+100.
A radian that comes out of floating-point arithmetic is a rounded approximation of the
angle, so it differs from the same angle written in degrees in the way `0.1 + 0.2`
differs from `0.3`.
`Angle.is_close(other, tolerance=...)` compares them with the tolerance written down
as an angle.

`Degree(370)` is the position 10 degrees, and `DegreeDisplacement(370)` is 370 degrees
of rotation.
`Angle.normalize()` gives the position within one turn, and
`Angle.to_angular_displacement()` and `AngularDisplacement.to_angle()` move between
the two.

`ANGLE_UNITS` and `ANGULAR_DISPLACEMENT_UNITS` map each symbol to its constructor, for
boundary code that reads a unit as a string from outside the application.
They accept the plain spellings `deg`, `rev`, `grad`, `arcmin`, and `arcsec`, and the
marks `'` and `"`.

References
----------
BIPM, The International System of Units (SI Brochure), on the radian and on the degree,
arcminute, and arcsecond accepted for use with the SI:
https://www.bipm.org/en/publications/si-brochure

IAU 2015 Resolution B2, which defines the parsec as exactly 648000/pi astronomical
units:
https://arxiv.org/abs/1510.06262

See Also
--------
~kuchka.quantities.AngularVelocity
    An angular displacement over a time.
~kuchka.quantities.Length
    An arc is a displacement times a radius (`AngularDisplacement.from_arc`).
~kuchka.quantities.SolidAngle
    The angle of a cone, measured in steradians.

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
    """Construct an Angle from a magnitude expressed in radians.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in radians.

    Returns
    -------
    Angle
        Angle represented in radians.

    Examples
    --------
    A pendulum swings through an amplitude of 0.1 rad, which is under six degrees:

    >>> from kuchka.units import DEGREE
    >>> amplitude = Radian(0.1)
    >>> f"{amplitude.to(DEGREE):.2f}"
    '5.73 °'

    An angle from floating-point arithmetic is a rounded approximation, so it is
    compared with a tolerance that is written as an angle:

    >>> import math
    >>> from kuchka import ArcSecond
    >>> from kuchka import Degree
    >>> Radian(math.pi / 2) == Degree(90)
    False
    >>> Radian(math.pi / 2).is_close(Degree(90), tolerance=ArcSecond(1))
    True

    """
    return Angle(to_exact(value) * RADIAN.scale, RADIAN)


def Degree(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in degrees.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in degrees.

    Returns
    -------
    Angle
        Angle represented in degrees.

    Examples
    --------
    A compass bearing of 90 degrees, turned a further 45 degrees, points at 135:

    >>> heading = Degree(90) + Degree(45)
    >>> heading
    135 °

    Angles wrap around the circle, so 20 degrees past a heading of 350 is a heading
    of 10, and 370 degrees is the same position as 10:

    >>> Degree(350) + Degree(20)
    10 °
    >>> Degree(370) == Degree(10)
    True

    """
    return Angle(to_exact(value) * DEGREE.scale, DEGREE)


def Turn(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in turns.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in turns.

    Returns
    -------
    Angle
        Angle represented in turns.

    Examples
    --------
    A quarter-turn valve closes through 0.25 turns, which is a right angle:

    >>> valve = Turn(0.25)
    >>> valve
    0.25 tr
    >>> from kuchka import Degree
    >>> valve == Degree(90)
    True

    A datasheet writes the travel of a potentiometer as a number of revolutions, and
    `parse` reads that spelling:

    >>> from kuchka import Angle
    >>> from kuchka import parse
    >>> parse("1.5 rev", Angle)
    1.5 tr

    """
    return Angle(to_exact(value), TURN)


def Gradian(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in gradians.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in gradians.

    Returns
    -------
    Angle
        Angle represented in gradians.

    Examples
    --------
    A surveyor's theodolite reads 50 gon for half a right angle:

    >>> sight = Gradian(50)
    >>> sight
    50 gon

    The gradian divides a right angle into 100, so the two systems agree exactly at the
    right angle:

    >>> from kuchka import Degree
    >>> Gradian(100) == Degree(90)
    True

    """
    return Angle(to_exact(value) * GRADIAN.scale, GRADIAN)


def ArcMinute(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcminutes.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in arcminutes.

    Returns
    -------
    Angle
        Angle represented in arcminutes.

    Examples
    --------
    The Sun and the Moon each span about half a degree of sky, near 32 arcminutes:

    >>> sun = ArcMinute(32)
    >>> from kuchka.units import DEGREE
    >>> f"{sun.to(DEGREE):.2f}"
    '0.53 °'

    A nautical mile was defined as one arcminute of latitude.
    On the mean radius of the Earth (6371 km), the arc of one nautical mile spans one
    arcminute to within an arcsecond:

    >>> from kuchka import AngularDisplacement
    >>> from kuchka import ArcMinuteDisplacement
    >>> from kuchka import ArcSecondDisplacement
    >>> from kuchka import Kilometre
    >>> from kuchka import NauticalMile
    >>> arc = AngularDisplacement.from_arc(NauticalMile(1), Kilometre(6371))
    >>> arc.is_close(ArcMinuteDisplacement(1), tolerance=ArcSecondDisplacement(1))
    True

    """
    return Angle(to_exact(value) * ARCMINUTE.scale, ARCMINUTE)


def ArcSecond(value: Numeric) -> Angle:
    """Construct an Angle from a magnitude expressed in arcseconds.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in arcseconds.

    Returns
    -------
    Angle
        Angle represented in arcseconds.

    Examples
    --------
    The parallax of Proxima Centauri, the nearest star beyond the Sun, is about 0.77
    arcseconds:

    >>> parallax = ArcSecond(0.77)
    >>> parallax
    0.77 ″

    A small angle that arrives as text with the marks of its unit is read exactly, and
    3600 arcseconds make a degree:

    >>> from kuchka import Angle
    >>> from kuchka import Degree
    >>> from kuchka import parse
    >>> parse('3600"', Angle) == Degree(1)
    True

    """
    return Angle(to_exact(value) * ARCSECOND.scale, ARCSECOND)


def TurnDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in turns.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in turns.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in turns.

    Examples
    --------
    A centrifuge rotor makes 30 turns in 10 s:

    >>> from kuchka import Second
    >>> from kuchka.units import REVOLUTION_PER_MINUTE
    >>> rotor = TurnDisplacement(30) / Second(10)
    >>> rotor.to(REVOLUTION_PER_MINUTE)
    180 rpm

    The same rotation rate in radians per second:

    >>> from kuchka.units import RADIAN_PER_SECOND
    >>> f"{rotor.to(RADIAN_PER_SECOND):.2f}"
    '18.85 rad/s'

    """
    return AngularDisplacement(to_exact(value), TURN)


def DegreeDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in degrees.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in degrees.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in degrees.

    Examples
    --------
    A cable drum is turned through 720 degrees, two full turns:

    >>> drum = DegreeDisplacement(720)
    >>> drum
    720 °

    Rotation counts past a full turn, where a position wraps:

    >>> from kuchka import Degree
    >>> from kuchka import DegreeDisplacement
    >>> Degree(370) == Degree(10)
    True
    >>> DegreeDisplacement(370) == DegreeDisplacement(10)
    False

    """
    return AngularDisplacement(to_exact(value) * DEGREE.scale, DEGREE)


def RadianDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in radians.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in radians.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in radians.

    Examples
    --------
    A robot arm of 2 m swings through 0.5 rad, and its tip travels along an arc of 1 m:

    >>> from kuchka import Metre
    >>> swing = RadianDisplacement(0.5)
    >>> swing * Metre(2)
    1 m

    Read the other way, an arc over its radius is the angle:

    >>> from kuchka import AngularDisplacement
    >>> AngularDisplacement.from_arc(Metre(1), Metre(2))
    0.5 rad

    """
    return AngularDisplacement(to_exact(value) * RADIAN.scale, RADIAN)


def GradianDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in gradians.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in gradians.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in gradians.

    Examples
    --------
    A total station turned through 400 gon has made one full circle.
    Two traverse legs of 150 and 250 gon add up to that circle:

    >>> legs = GradianDisplacement(150) + GradianDisplacement(250)
    >>> legs
    400 gon
    >>> from kuchka.units import TURN
    >>> legs.to(TURN)
    1 tr

    """
    return AngularDisplacement(to_exact(value) * GRADIAN.scale, GRADIAN)


def ArcMinuteDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in arcminutes.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in arcminutes.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in arcminutes.

    Examples
    --------
    An equatorial mount tracks the sky through about 900 arcminutes in an hour,
    which is 15 degrees:

    >>> tracking = ArcMinuteDisplacement(900)
    >>> from kuchka.units import DEGREE
    >>> tracking.to(DEGREE)
    15 °

    Spread over the hour, that is the angular rate the mount drives at:

    >>> from kuchka import Hour
    >>> from kuchka.units import RADIAN_PER_SECOND
    >>> f"{(tracking / Hour(1)).to(RADIAN_PER_SECOND):.2e}"
    '7.27e-5 rad/s'

    """
    return AngularDisplacement(to_exact(value) * ARCMINUTE.scale, ARCMINUTE)


def ArcSecondDisplacement(value: Numeric) -> AngularDisplacement:
    """Construct an AngularDisplacement from a magnitude expressed in arcseconds.

    Parameters
    ----------
    value : Numeric
        Angle magnitude in arcseconds.

    Returns
    -------
    AngularDisplacement
        AngularDisplacement represented in arcseconds.

    Examples
    --------
    A telescope's guiding camera corrects a drift of 2 arcseconds:

    >>> drift = ArcSecondDisplacement(2)
    >>> drift
    2 ″

    In degrees, that is a very small fraction:

    >>> from kuchka.units import DEGREE
    >>> f"{drift.to(DEGREE):.5f}"
    '0.00056 °'

    """
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
