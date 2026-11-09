"""Unit constructors for AngularVelocity: turns, radians, degrees per second, and rpm.

    from kuchka import RadianPerSecond, RevolutionPerMinute
    from kuchka.units import RADIAN_PER_SECOND, TURN_PER_SECOND

    spindle = RevolutionPerMinute(3000)
    motor = RadianPerSecond(100)

`AngularVelocity` describes the rate of change of angular displacement.
Its SI-coherent unit is the radian per second (rad/s).
`kuchka` uses the turn per second (tr/s) as its canonical unit, following `TURN` as the
canonical unit of angle.
Arithmetic results display in radians per second.

The available units cover several areas of rotational mechanics:

* degrees per second (°/s) describe slewing rates, robotic joint motion, gimbal
    movement, and other angular positioning systems;
* radians per second (rad/s) are used in rotational dynamics, control systems,
    mechanical engineering, and physics;
* turns per second (tr/s) express rotation rates directly as complete revolutions per
    unit time, useful for rotating machinery and rotor characterization;
* revolutions per minute (rpm) are widely used for motors, spindles, turbines, pumps,
    fans, and other rotating machinery.

Examples
--------
A two-pole synchronous motor operating from a 50 Hz supply completes 50 mechanical
revolutions per second.
Convert its electrical frequency to angular velocity:

>>> from kuchka import Hertz
>>> supply_frequency = Hertz(50)
>>> shaft_speed = supply_frequency.to_angular_velocity()
>>> shaft_speed.to(TURN_PER_SECOND)
50 tr/s

The quantities have different meanings, even though their magnitudes match when angular
velocity is expressed in turns per second.
The corresponding frequency can be recovered explicitly:

>>> shaft_speed.to_frequency()
50 Hz

A robotic arm joint rotates at 4 rad/s.
A point 0.5 m from the joint axis has a tangential speed of 2 m/s:

>>> from kuchka import Metre
>>> joint_rate = RadianPerSecond(4)
>>> arm_radius = Metre(0.5)
>>> joint_rate * arm_radius
2 m/s

A motion controller exports a slew rate using the alternative spelling ``"deg/s"``.
Read the complete measurement:

>>> from kuchka import AngularVelocity, DegreePerSecond, parse
>>> parse("90 deg/s", AngularVelocity) == DegreePerSecond(90)
True

Notes
-----
Angular velocity, denoted by ω, is the rate of change of angular displacement, denoted
by θ:

``ω = dθ/dt``

Its coherent SI unit is the radian per second:

``rad/s``

One complete turn corresponds to an angular displacement of 2π radians:

``1 tr = 360° = 2π rad``

Consequently:

``1 tr/s = 2π rad/s``

Angular velocity and cyclic frequency are related by:

``ω = 2π f``

where f counts complete cycles per second and ω measures angular displacement per
second.
A frequency of 1 Hz corresponds to an angular velocity of 1 tr/s, or 2π rad/s.

`Frequency.to_angular_velocity()` and `AngularVelocity.to_frequency()` provide
explicit conversions between these distinct quantities.

The turn and degree are rationally related:

``1° = 1/360 tr``

Their conversions are exact.
The revolution per minute is also an exact unit definition because one minute is
exactly 60 seconds:

``1 rpm = 1/60 tr/s``

The radian uses the same π-based scale as `Radian` in the angular unit module.
`RadianPerSecond` therefore inherits the same numerical representation of π.

Angular velocity and length form a useful mechanical relationship.
Multiplying angular velocity by a radius gives the tangential velocity of a point
rotating at that radius:

``v = ωr``

The library provides this as an explicit concept bridge.
The inverse relationship, tangential velocity divided by angular velocity, gives the
radius:

``r = v/ω``

`parse` reads complete measurements such as ``"2 tr/s"``, ``"100 rad/s"``,
``"90 deg/s"``, and ``"3000 rpm"``.
Alternative spellings registered by the unit definitions are accepted.

`ANGULAR_VELOCITY_UNITS` maps supported symbols such as ``"tr/s"``, ``"rev/s"``,
``"rad/s"``, ``"rad/sec"``, ``"°/s"``, ``"deg/s"``, ``"rpm"``, and ``"rev/min"`` to
their constructors.
It is useful for boundary code that receives a numeric magnitude and a separate unit
symbol.

For the SI treatment of plane angle and the radian, see the
BIPM International System of Units:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.AngularVelocity
    Quantity type representing angular velocity.

~kuchka.quantities.AngularDisplacement
    Angular displacement accumulated over an interval.

~kuchka.quantities.AngularAcceleration
    Rate of change of angular velocity.

~kuchka.quantities.Frequency
    Cyclic frequency, which converts explicitly to angular velocity.

~kuchka.quantities.Angle
    Plane angle, whose canonical unit is the turn.

~kuchka.quantities.Velocity
    Linear velocity, obtainable from angular velocity and a radius.

~kuchka.quantities.Length
    Radius or lever distance used in rotational mechanics.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AngularVelocity
from kuchka.quantities import UnitDef
from kuchka.units.angular import DEGREE
from kuchka.units.angular import RADIAN
from kuchka.units.angular import TURN
from kuchka.units.temporal.time import MINUTE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TURN_PER_SECOND = UnitDef(
    "turn_per_second",
    "tr/s",
    TURN.scale,
    ANGULAR_VELOCITY,
    aliases=("rev/s",),
    words=("revolution per second",),
)
RADIAN_PER_SECOND = UnitDef(
    "radian_per_second", "rad/s", RADIAN.scale, ANGULAR_VELOCITY, aliases=("rad/sec",)
)
DEGREE_PER_SECOND = UnitDef(
    "degree_per_second",
    f"{symbols.DEGREE}/s",
    DEGREE.scale,
    ANGULAR_VELOCITY,
    aliases=("deg/s",),
)
REVOLUTION_PER_MINUTE = UnitDef(
    "revolution_per_minute",
    "rpm",
    TURN.scale / MINUTE.scale,
    ANGULAR_VELOCITY,
    aliases=("rev/min", "RPM"),
    words=("revolution per minute",),
)

AngularVelocity._canonical_unit = TURN_PER_SECOND  # noqa: SLF001 -- this module owns AngularVelocity's canonical unit
AngularVelocity._result_unit = RADIAN_PER_SECOND  # noqa: SLF001 -- and the unit its arithmetic results display in


def TurnPerSecond(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude in turns per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in tr/s.

    Returns
    -------
    AngularVelocity
        Angular velocity represented in turns per second.

    Examples
    --------
    A high-speed centrifuge rotor completes 60 revolutions per second:

    >>> rotor = TurnPerSecond(60)
    >>> rotor
    60 tr/s

    Express the same rotational speed in revolutions per minute:

    >>> from kuchka.units import REVOLUTION_PER_MINUTE
    >>> rotor.to(REVOLUTION_PER_MINUTE)
    3600 rpm

    """
    return AngularVelocity(to_exact(value) * TURN_PER_SECOND.scale, TURN_PER_SECOND)


def RadianPerSecond(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude in radians per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in rad/s.

    Returns
    -------
    AngularVelocity
        Angular velocity represented in radians per second.

    Examples
    --------
    A servo-driven robotic joint changes its angular position at 1.5 rad/s:

    >>> joint_rate = RadianPerSecond(1.5)
    >>> joint_rate
    1.5 rad/s

    A point on a rotating shaft lies 0.25 m from its axis.
    At an angular velocity of 12 rad/s, its tangential speed is:

    >>> from kuchka import Metre
    >>> shaft_rate = RadianPerSecond(12)
    >>> shaft_radius = Metre(0.25)
    >>> shaft_rate * shaft_radius
    3 m/s

    """
    return AngularVelocity(to_exact(value) * RADIAN_PER_SECOND.scale, RADIAN_PER_SECOND)


def DegreePerSecond(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude in degrees per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in °/s.

    Returns
    -------
    AngularVelocity
        Angular velocity represented in degrees per second.

    Examples
    --------
    A camera gimbal slews its positioning axis at 30 degrees per second:

    >>> slew_rate = DegreePerSecond(30)
    >>> slew_rate
    30 °/s

    A mechanism rotating at 180 degrees per second completes half a turn each second:

    >>> DegreePerSecond(180).to(TURN_PER_SECOND)
    0.5 tr/s

    """
    return AngularVelocity(to_exact(value) * DEGREE_PER_SECOND.scale, DEGREE_PER_SECOND)


def RevolutionPerMinute(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude in revolutions per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in rpm.

    Returns
    -------
    AngularVelocity
        Angular velocity represented in revolutions per minute.

    Examples
    --------
    A lathe spindle operates at 3000 revolutions per minute:

    >>> spindle = RevolutionPerMinute(3000)
    >>> spindle
    3000 rpm

    The spindle completes 50 revolutions per second.
    Express its rotational frequency in hertz:

    >>> spindle.to_frequency()
    50 Hz

    """
    return AngularVelocity(
        to_exact(value) * REVOLUTION_PER_MINUTE.scale, REVOLUTION_PER_MINUTE
    )


ANGULAR_VELOCITY_UNITS: Mapping[str, Callable[[Numeric], AngularVelocity]] = unit_table(
    "ANGULAR_VELOCITY_UNITS",
    {
        TURN_PER_SECOND: TurnPerSecond,
        RADIAN_PER_SECOND: RadianPerSecond,
        DEGREE_PER_SECOND: DegreePerSecond,
        REVOLUTION_PER_MINUTE: RevolutionPerMinute,
    },
)

__all__ = [
    "ANGULAR_VELOCITY_UNITS",
    "DEGREE_PER_SECOND",
    "RADIAN_PER_SECOND",
    "REVOLUTION_PER_MINUTE",
    "TURN_PER_SECOND",
    "DegreePerSecond",
    "RadianPerSecond",
    "RevolutionPerMinute",
    "TurnPerSecond",
]
