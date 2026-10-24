"""Angular velocity unit constructors: TurnPerSecond, RadianPerSecond, and the rpm.

    from kuchka import RadianPerSecond, RevolutionPerMinute

    spindle = RevolutionPerMinute(3000)
    motor = RadianPerSecond(314.16)

The turn per second is the canonical unit, because a turn is the canonical angle.
A degree and a revolution are plain rational fractions of a turn, so
`DegreePerSecond` and `RevolutionPerMinute` are exact, and `RadianPerSecond` carries pi
as exactly as `Radian` does (see `kuchka.units.angular`).
One turn per second equals one hertz in magnitude, and the two are different kinds:
`Frequency.to_angular_velocity()` and `AngularVelocity.to_frequency()` convert.

`ANGULAR_VELOCITY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
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
    """Construct an AngularVelocity from a magnitude expressed in turns per second."""
    return AngularVelocity(to_exact(value) * TURN_PER_SECOND.scale, TURN_PER_SECOND)


def RadianPerSecond(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude expressed in radians per second."""
    return AngularVelocity(to_exact(value) * RADIAN_PER_SECOND.scale, RADIAN_PER_SECOND)


def DegreePerSecond(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude expressed in degrees per second."""
    return AngularVelocity(to_exact(value) * DEGREE_PER_SECOND.scale, DEGREE_PER_SECOND)


def RevolutionPerMinute(value: Numeric) -> AngularVelocity:
    """Construct an AngularVelocity from a magnitude in revolutions per minute."""
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
