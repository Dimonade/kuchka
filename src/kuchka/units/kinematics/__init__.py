"""Unit constructors for motion, whatever causes it.

from kuchka import MetrePerSecond, MetrePerSecondSquared, RevolutionPerMinute

speed = MetrePerSecond(3)
rate_of_change = MetrePerSecondSquared(9.81)
spin = RevolutionPerMinute(3000)
"""

from __future__ import annotations

from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import angular_acceleration
from kuchka.units.kinematics import angular_jerk
from kuchka.units.kinematics import angular_velocity
from kuchka.units.kinematics import angular_velocity_squared
from kuchka.units.kinematics import jerk
from kuchka.units.kinematics import snap
from kuchka.units.kinematics import time_cubed
from kuchka.units.kinematics import time_fourth_power
from kuchka.units.kinematics import time_squared
from kuchka.units.kinematics import velocity
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.angular_acceleration import *
from kuchka.units.kinematics.angular_jerk import *
from kuchka.units.kinematics.angular_velocity import *
from kuchka.units.kinematics.angular_velocity_squared import *
from kuchka.units.kinematics.jerk import *
from kuchka.units.kinematics.snap import *
from kuchka.units.kinematics.time_cubed import *
from kuchka.units.kinematics.time_fourth_power import *
from kuchka.units.kinematics.time_squared import *
from kuchka.units.kinematics.velocity import *

__all__: list[str] = []
__all__ += acceleration.__all__
__all__ += angular_acceleration.__all__
__all__ += angular_jerk.__all__
__all__ += angular_velocity.__all__
__all__ += angular_velocity_squared.__all__
__all__ += jerk.__all__
__all__ += snap.__all__
__all__ += time_cubed.__all__
__all__ += time_fourth_power.__all__
__all__ += time_squared.__all__
__all__ += velocity.__all__
