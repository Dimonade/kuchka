"""Quantity types for motion, whatever causes it."""

from __future__ import annotations

from kuchka.quantities.kinematics import acceleration
from kuchka.quantities.kinematics import angular_acceleration
from kuchka.quantities.kinematics import angular_jerk
from kuchka.quantities.kinematics import angular_velocity
from kuchka.quantities.kinematics import angular_velocity_squared
from kuchka.quantities.kinematics import jerk
from kuchka.quantities.kinematics import snap
from kuchka.quantities.kinematics import time_cubed
from kuchka.quantities.kinematics import time_fourth_power
from kuchka.quantities.kinematics import time_squared
from kuchka.quantities.kinematics import velocity
from kuchka.quantities.kinematics.acceleration import *
from kuchka.quantities.kinematics.angular_acceleration import *
from kuchka.quantities.kinematics.angular_jerk import *
from kuchka.quantities.kinematics.angular_velocity import *
from kuchka.quantities.kinematics.angular_velocity_squared import *
from kuchka.quantities.kinematics.jerk import *
from kuchka.quantities.kinematics.snap import *
from kuchka.quantities.kinematics.time_cubed import *
from kuchka.quantities.kinematics.time_fourth_power import *
from kuchka.quantities.kinematics.time_squared import *
from kuchka.quantities.kinematics.velocity import *

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
