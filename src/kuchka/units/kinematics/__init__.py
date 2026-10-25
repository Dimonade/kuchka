"""Unit constructors for Velocity, Acceleration, and AngularVelocity.

    from kuchka import MetrePerSecond, MetrePerSecondSquared, RevolutionPerMinute

    speed = MetrePerSecond(3)
    rate_of_change = MetrePerSecondSquared(9.81)
    spin = RevolutionPerMinute(3000)

`VELOCITY_UNITS`, `ACCELERATION_UNITS`, and `ANGULAR_VELOCITY_UNITS` each map a symbol
to its constructor, for boundary code that reads a unit as a string from outside the
application.
These quantities describe motion, whatever causes it.
"""

from __future__ import annotations

from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import angular_velocity
from kuchka.units.kinematics import velocity
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.angular_velocity import *
from kuchka.units.kinematics.velocity import *

__all__: list[str] = []
__all__ += acceleration.__all__
__all__ += angular_velocity.__all__
__all__ += velocity.__all__
