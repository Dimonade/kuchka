"""Angular acceleration unit constructors: RadianPerSecondSquared and its relatives.

`AngularAcceleration` is the rate at which an angular velocity changes, the spin-up of
a spindle or the braking of a joint.
The turn per second squared is the canonical unit, because a turn is the canonical
angle, and arithmetic results display in the radian per second squared.
A degree and a revolution are plain rational fractions of a turn, so
`DegreePerSecondSquared` and `RevolutionPerMinutePerSecond` are exact, and
`RadianPerSecondSquared` carries pi as exactly as `Radian` does.

Examples
--------
A spindle reaches 300 rad/s two seconds after it starts:

>>> from kuchka import RadianPerSecond, Second
>>> RadianPerSecond(300) / Second(2)
150 rad/s²

At a radius of 0.2 m, that is a tangential acceleration of 30 m/s²:

>>> from kuchka import Metre
>>> RadianPerSecondSquared(150) * Metre(0.2)
30 m/s²

`ANGULAR_ACCELERATION_UNITS` maps symbols such as ``"rad/s²"`` and ``"rpm/s"`` to their
constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.AngularVelocity
    The angular velocity an angular acceleration changes.
~kuchka.quantities.MomentOfInertia
    A moment of inertia times an angular acceleration is a torque.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGULAR_ACCELERATION
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AngularAcceleration
from kuchka.quantities import UnitDef
from kuchka.units.angular import DEGREE
from kuchka.units.angular import RADIAN
from kuchka.units.angular import TURN
from kuchka.units.temporal.time import MINUTE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TURN_PER_SECOND_SQUARED = UnitDef(
    "turn_per_second_squared",
    f"tr/s{symbols.SUPERSCRIPT_TWO}",
    TURN.scale,
    ANGULAR_ACCELERATION,
    aliases=(*powered("tr/s", 2), *powered("rev/s", 2)),
    words=("turn per second squared", "revolution per second squared"),
)
RADIAN_PER_SECOND_SQUARED = UnitDef(
    "radian_per_second_squared",
    f"rad/s{symbols.SUPERSCRIPT_TWO}",
    RADIAN.scale,
    ANGULAR_ACCELERATION,
    aliases=powered("rad/s", 2),
    words=("radian per second squared",),
)
DEGREE_PER_SECOND_SQUARED = UnitDef(
    "degree_per_second_squared",
    f"{symbols.DEGREE}/s{symbols.SUPERSCRIPT_TWO}",
    DEGREE.scale,
    ANGULAR_ACCELERATION,
    aliases=(*powered("deg/s", 2), *powered(f"{symbols.DEGREE}/s", 2)),
    words=("degree per second squared",),
)
REVOLUTION_PER_MINUTE_PER_SECOND = UnitDef(
    "revolution_per_minute_per_second",
    "rpm/s",
    TURN.scale / MINUTE.scale,
    ANGULAR_ACCELERATION,
    aliases=("rev/min/s", "RPM/s"),
    words=("revolution per minute per second",),
)

AngularAcceleration._canonical_unit = TURN_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns AngularAcceleration's canonical unit
AngularAcceleration._result_unit = RADIAN_PER_SECOND_SQUARED  # noqa: SLF001 -- and the unit its arithmetic results display in


def TurnPerSecondSquared(value: Numeric) -> AngularAcceleration:
    """Construct an angular acceleration from turns per second squared.

    Parameters
    ----------
    value : Numeric
        Angular acceleration in tr/s².

    Returns
    -------
    AngularAcceleration
        Angular acceleration represented in turns per second squared.

    Examples
    --------
    A turntable that gains half a turn per second every second:

    >>> TurnPerSecondSquared(0.5)
    0.5 tr/s²

    """
    return AngularAcceleration(
        to_exact(value) * TURN_PER_SECOND_SQUARED.scale, TURN_PER_SECOND_SQUARED
    )


def RadianPerSecondSquared(value: Numeric) -> AngularAcceleration:
    """Construct an angular acceleration from radians per second squared.

    Parameters
    ----------
    value : Numeric
        Angular acceleration in rad/s².

    Returns
    -------
    AngularAcceleration
        Angular acceleration represented in radians per second squared.

    Examples
    --------
    A joint braking at 40 rad/s² stops a 120 rad/s swing in three seconds:

    >>> from kuchka import RadianPerSecond
    >>> RadianPerSecond(120) / RadianPerSecondSquared(40)
    3 s

    """
    return AngularAcceleration(
        to_exact(value) * RADIAN_PER_SECOND_SQUARED.scale, RADIAN_PER_SECOND_SQUARED
    )


def DegreePerSecondSquared(value: Numeric) -> AngularAcceleration:
    """Construct an angular acceleration from degrees per second squared.

    Parameters
    ----------
    value : Numeric
        Angular acceleration in °/s².

    Returns
    -------
    AngularAcceleration
        Angular acceleration represented in degrees per second squared.

    Examples
    --------
    A gimbal limited to 360 °/s² gains one turn per second each second:

    >>> DegreePerSecondSquared(360) == TurnPerSecondSquared(1)
    True

    """
    return AngularAcceleration(
        to_exact(value) * DEGREE_PER_SECOND_SQUARED.scale, DEGREE_PER_SECOND_SQUARED
    )


def RevolutionPerMinutePerSecond(value: Numeric) -> AngularAcceleration:
    """Construct an angular acceleration from revolutions per minute per second.

    Parameters
    ----------
    value : Numeric
        Angular acceleration in rpm/s.

    Returns
    -------
    AngularAcceleration
        Angular acceleration represented in revolutions per minute per second.

    Examples
    --------
    A drive ramp of 600 rpm/s reaches 3000 rpm in five seconds:

    >>> from kuchka import RevolutionPerMinute
    >>> RevolutionPerMinute(3000) / RevolutionPerMinutePerSecond(600)
    5 s

    """
    return AngularAcceleration(
        to_exact(value) * REVOLUTION_PER_MINUTE_PER_SECOND.scale,
        REVOLUTION_PER_MINUTE_PER_SECOND,
    )


ANGULAR_ACCELERATION_UNITS: Mapping[str, Callable[[Numeric], AngularAcceleration]] = (
    unit_table(
        "ANGULAR_ACCELERATION_UNITS",
        {
            TURN_PER_SECOND_SQUARED: TurnPerSecondSquared,
            RADIAN_PER_SECOND_SQUARED: RadianPerSecondSquared,
            DEGREE_PER_SECOND_SQUARED: DegreePerSecondSquared,
            REVOLUTION_PER_MINUTE_PER_SECOND: RevolutionPerMinutePerSecond,
        },
    )
)

__all__ = [
    "ANGULAR_ACCELERATION_UNITS",
    "DEGREE_PER_SECOND_SQUARED",
    "RADIAN_PER_SECOND_SQUARED",
    "REVOLUTION_PER_MINUTE_PER_SECOND",
    "TURN_PER_SECOND_SQUARED",
    "DegreePerSecondSquared",
    "RadianPerSecondSquared",
    "RevolutionPerMinutePerSecond",
    "TurnPerSecondSquared",
]
