"""Unit constructors for Velocity, Acceleration, and Force.

    from kuchka import MetrePerSecond, MetrePerSecondSquared, Newton

    speed = MetrePerSecond(3)
    rate_of_change = MetrePerSecondSquared(9.81)
    push = Newton(10)


`VELOCITY_UNITS`, `ACCELERATION_UNITS`, and `FORCE_UNITS` each map a symbol to its
constructor, for boundary code that reads a unit as a string from outside the
application.

A number of families share this package, as they all share a recurring theme, and a
number of physical dimensions, making them closely related:

- `velocity.py`,
- `acceleration.py`,
- `force.py`.
"""

from __future__ import annotations

from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import force
from kuchka.units.kinematics import velocity
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.force import *
from kuchka.units.kinematics.velocity import *

__all__: list[str] = []
__all__ += acceleration.__all__
__all__ += force.__all__
__all__ += velocity.__all__
