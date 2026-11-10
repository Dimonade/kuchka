"""Angular velocity squared constructors: turns, radians, and degrees squared.

`AngularVelocitySquared` is an angular velocity times an angular velocity, the square
that a centripetal acceleration `omega² * r` and a rotational kinetic energy
`I * omega² / 2` are written with.
The turn squared per second squared is the canonical unit, because a turn is the
canonical angle, and arithmetic results display in the radian squared per second
squared.
A degree is a plain rational fraction of a turn, so `DegreeSquaredPerSecondSquared` is
exact, and `RadianSquaredPerSecondSquared` carries pi squared as exactly as `Radian`
carries pi.

Examples
--------
A rotor turns at 300 rad/s, so a point on its rim at 0.2 m has a centripetal
acceleration of 18000 m/s², whichever way the factors are grouped:

>>> from kuchka import Metre, RadianPerSecond
>>> omega = RadianPerSecond(300)
>>> omega * omega
90000 rad²/s²
>>> omega * omega * Metre(0.2)
18000 m/s²
>>> Metre(0.2) * omega**2
18000 m/s²

`ANGULAR_VELOCITY_SQUARED_UNITS` maps symbols such as ``"rad²/s²"`` and ``"tr²/s²"`` to
their constructors, for boundary code that reads a unit as a string.

See Also
--------
~kuchka.quantities.AngularVelocity
    The angular velocity an angular velocity squared is the square of.
~kuchka.quantities.MomentOfInertia
    A moment of inertia times an angular velocity squared is an energy.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGULAR_VELOCITY_SQUARED
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AngularVelocitySquared
from kuchka.quantities import UnitDef
from kuchka.units.angular import DEGREE
from kuchka.units.angular import RADIAN
from kuchka.units.angular import TURN

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_TWO = symbols.SUPERSCRIPT_TWO

TURN_SQUARED_PER_SECOND_SQUARED = UnitDef(
    "turn_squared_per_second_squared",
    f"tr{_TWO}/s{_TWO}",
    TURN.scale**2,
    ANGULAR_VELOCITY_SQUARED,
    aliases=("tr^2/s^2", "tr**2/s**2", "rev^2/s^2", "rev**2/s**2"),
    words=("turn squared per second squared", "revolution squared per second squared"),
)
RADIAN_SQUARED_PER_SECOND_SQUARED = UnitDef(
    "radian_squared_per_second_squared",
    f"rad{_TWO}/s{_TWO}",
    RADIAN.scale**2,
    ANGULAR_VELOCITY_SQUARED,
    aliases=("rad^2/s^2", "rad**2/s**2"),
    words=("radian squared per second squared",),
)
DEGREE_SQUARED_PER_SECOND_SQUARED = UnitDef(
    "degree_squared_per_second_squared",
    f"{symbols.DEGREE}{_TWO}/s{_TWO}",
    DEGREE.scale**2,
    ANGULAR_VELOCITY_SQUARED,
    aliases=(
        "deg^2/s^2",
        "deg**2/s**2",
        f"{symbols.DEGREE}^2/s^2",
        f"{symbols.DEGREE}**2/s**2",
    ),
    words=("degree squared per second squared",),
)

AngularVelocitySquared._canonical_unit = TURN_SQUARED_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns AngularVelocitySquared's canonical unit
AngularVelocitySquared._result_unit = RADIAN_SQUARED_PER_SECOND_SQUARED  # noqa: SLF001 -- and the unit its arithmetic results display in


def TurnSquaredPerSecondSquared(value: Numeric) -> AngularVelocitySquared:
    """Construct an angular velocity squared from turns squared per second squared.

    Parameters
    ----------
    value : Numeric
        Angular velocity squared in tr²/s².

    Returns
    -------
    AngularVelocitySquared
        Angular velocity squared represented in turns squared per second squared.

    Examples
    --------
    A shaft at one turn per second has an angular velocity squared of 1 tr²/s²:

    >>> from kuchka import TurnPerSecond
    >>> TurnPerSecond(1) * TurnPerSecond(1) == TurnSquaredPerSecondSquared(1)
    True

    """
    return AngularVelocitySquared(
        to_exact(value) * TURN_SQUARED_PER_SECOND_SQUARED.scale,
        TURN_SQUARED_PER_SECOND_SQUARED,
    )


def RadianSquaredPerSecondSquared(value: Numeric) -> AngularVelocitySquared:
    """Construct an angular velocity squared from radians squared per second squared.

    Parameters
    ----------
    value : Numeric
        Angular velocity squared in rad²/s².

    Returns
    -------
    AngularVelocitySquared
        Angular velocity squared represented in radians squared per second squared.

    Examples
    --------
    A point at 0.5 m on a rotor with 400 rad²/s² feels a centripetal acceleration of
    200 m/s²:

    >>> from kuchka import Metre
    >>> RadianSquaredPerSecondSquared(400) * Metre(0.5)
    200 m/s²

    """
    return AngularVelocitySquared(
        to_exact(value) * RADIAN_SQUARED_PER_SECOND_SQUARED.scale,
        RADIAN_SQUARED_PER_SECOND_SQUARED,
    )


def DegreeSquaredPerSecondSquared(value: Numeric) -> AngularVelocitySquared:
    """Construct an angular velocity squared from degrees squared per second squared.

    Parameters
    ----------
    value : Numeric
        Angular velocity squared in °²/s².

    Returns
    -------
    AngularVelocitySquared
        Angular velocity squared represented in degrees squared per second squared.

    Examples
    --------
    A gimbal at 360 °/s turns once per second, so its square is one turn squared per
    second squared:

    >>> DegreeSquaredPerSecondSquared(129_600) == TurnSquaredPerSecondSquared(1)
    True

    """
    return AngularVelocitySquared(
        to_exact(value) * DEGREE_SQUARED_PER_SECOND_SQUARED.scale,
        DEGREE_SQUARED_PER_SECOND_SQUARED,
    )


ANGULAR_VELOCITY_SQUARED_UNITS: Mapping[
    str, Callable[[Numeric], AngularVelocitySquared]
] = unit_table(
    "ANGULAR_VELOCITY_SQUARED_UNITS",
    {
        TURN_SQUARED_PER_SECOND_SQUARED: TurnSquaredPerSecondSquared,
        RADIAN_SQUARED_PER_SECOND_SQUARED: RadianSquaredPerSecondSquared,
        DEGREE_SQUARED_PER_SECOND_SQUARED: DegreeSquaredPerSecondSquared,
    },
)

__all__ = [
    "ANGULAR_VELOCITY_SQUARED_UNITS",
    "DEGREE_SQUARED_PER_SECOND_SQUARED",
    "RADIAN_SQUARED_PER_SECOND_SQUARED",
    "TURN_SQUARED_PER_SECOND_SQUARED",
    "DegreeSquaredPerSecondSquared",
    "RadianSquaredPerSecondSquared",
    "TurnSquaredPerSecondSquared",
]
