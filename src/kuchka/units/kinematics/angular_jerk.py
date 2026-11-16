"""Angular jerk constructors: turns, radians, and degrees per second cubed.

`AngularJerk` is the rate at which an angular acceleration changes, the ramp of the
S-curve a servo or a stepper follows.
The turn per second cubed is the canonical unit, because a turn is the canonical
angle, and arithmetic results display in the radian per second cubed.
A degree is a plain rational fraction of a turn, so `DegreePerSecondCubed` is exact,
and `RadianPerSecondCubed` carries pi as exactly as `Radian` does.

Examples
--------
A spindle whose acceleration rises from 0 to 150 rad/s² in half a second ramps at
300 rad/s³:

>>> from kuchka import RadianPerSecondSquared
>>> from kuchka import Second
>>> RadianPerSecondSquared(150) / Second(0.5)
300 rad/s³

At a radius of 0.2 m, that is a tangential jerk of 60 m/s³:

>>> from kuchka import Metre
>>> RadianPerSecondCubed(300) * Metre(0.2)
60 m/s³

An angular jerk of 75 rad/s³ takes two seconds to build up an angular acceleration of
150 rad/s²:

>>> RadianPerSecondSquared(150) / RadianPerSecondCubed(75)
2 s

`ANGULAR_JERK_UNITS` maps symbols such as ``"rad/s³"`` and ``"tr/s³"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.AngularAcceleration
    The angular acceleration an angular jerk changes.
~kuchka.quantities.Jerk
    An angular jerk times the radius it acts at is a jerk.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGULAR_JERK
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AngularJerk
from kuchka.quantities import UnitDef
from kuchka.units.angular import DEGREE
from kuchka.units.angular import RADIAN
from kuchka.units.angular import TURN

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_THREE = symbols.SUPERSCRIPT_THREE

TURN_PER_SECOND_CUBED = UnitDef(
    "turn_per_second_cubed",
    f"tr/s{_THREE}",
    TURN.scale,
    ANGULAR_JERK,
    aliases=(*powered("tr/s", 3), *powered("rev/s", 3)),
    words=("turn per second cubed", "revolution per second cubed"),
)
RADIAN_PER_SECOND_CUBED = UnitDef(
    "radian_per_second_cubed",
    f"rad/s{_THREE}",
    RADIAN.scale,
    ANGULAR_JERK,
    aliases=powered("rad/s", 3),
    words=("radian per second cubed",),
)
DEGREE_PER_SECOND_CUBED = UnitDef(
    "degree_per_second_cubed",
    f"{symbols.DEGREE}/s{_THREE}",
    DEGREE.scale,
    ANGULAR_JERK,
    aliases=(*powered("deg/s", 3), *powered(f"{symbols.DEGREE}/s", 3)),
    words=("degree per second cubed",),
)

AngularJerk._canonical_unit = TURN_PER_SECOND_CUBED  # noqa: SLF001 -- this module owns AngularJerk's canonical unit
AngularJerk._result_unit = RADIAN_PER_SECOND_CUBED  # noqa: SLF001 -- and the unit its arithmetic results display in


def TurnPerSecondCubed(value: Numeric) -> AngularJerk:
    """Construct an angular jerk from turns per second cubed.

    Parameters
    ----------
    value : Numeric
        Angular jerk in tr/s³.

    Returns
    -------
    AngularJerk
        Angular jerk represented in turns per second cubed.

    Examples
    --------
    A turntable whose acceleration gains half a turn per second every second:

    >>> TurnPerSecondCubed(0.5)
    0.5 tr/s³

    """
    return AngularJerk(
        to_exact(value) * TURN_PER_SECOND_CUBED.scale, TURN_PER_SECOND_CUBED
    )


def RadianPerSecondCubed(value: Numeric) -> AngularJerk:
    """Construct an angular jerk from radians per second cubed.

    Parameters
    ----------
    value : Numeric
        Angular jerk in rad/s³.

    Returns
    -------
    AngularJerk
        Angular jerk represented in radians per second cubed.

    Examples
    --------
    A jerk of 40 rad/s³ adds 80 rad/s² of angular acceleration in two seconds:

    >>> from kuchka import Second
    >>> RadianPerSecondCubed(40) * Second(2)
    80 rad/s²

    """
    return AngularJerk(
        to_exact(value) * RADIAN_PER_SECOND_CUBED.scale, RADIAN_PER_SECOND_CUBED
    )


def DegreePerSecondCubed(value: Numeric) -> AngularJerk:
    """Construct an angular jerk from degrees per second cubed.

    Parameters
    ----------
    value : Numeric
        Angular jerk in °/s³.

    Returns
    -------
    AngularJerk
        Angular jerk represented in degrees per second cubed.

    Examples
    --------
    A gimbal limited to 360 °/s³ gains one turn per second squared every second:

    >>> DegreePerSecondCubed(360) == TurnPerSecondCubed(1)
    True

    """
    return AngularJerk(
        to_exact(value) * DEGREE_PER_SECOND_CUBED.scale, DEGREE_PER_SECOND_CUBED
    )


ANGULAR_JERK_UNITS: Mapping[str, Callable[[Numeric], AngularJerk]] = unit_table(
    "ANGULAR_JERK_UNITS",
    {
        TURN_PER_SECOND_CUBED: TurnPerSecondCubed,
        RADIAN_PER_SECOND_CUBED: RadianPerSecondCubed,
        DEGREE_PER_SECOND_CUBED: DegreePerSecondCubed,
    },
)

__all__ = [
    "ANGULAR_JERK_UNITS",
    "DEGREE_PER_SECOND_CUBED",
    "RADIAN_PER_SECOND_CUBED",
    "TURN_PER_SECOND_CUBED",
    "DegreePerSecondCubed",
    "RadianPerSecondCubed",
    "TurnPerSecondCubed",
]
