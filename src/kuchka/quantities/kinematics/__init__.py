"""Quantity types for motion: Velocity, Acceleration, and AngularVelocity.

    from kuchka import Acceleration, AngularVelocity, Velocity

These describe motion, whatever causes it.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package composes its own ``__all__`` from theirs, and `kuchka.quantities` composes
its own from this one's.
A new leaf module needs three lines here: its module import, its wildcard import, and
its ``__all__ +=``.
"""

from __future__ import annotations

from kuchka.quantities.kinematics import acceleration
from kuchka.quantities.kinematics import angular_velocity
from kuchka.quantities.kinematics import velocity
from kuchka.quantities.kinematics.acceleration import *
from kuchka.quantities.kinematics.angular_velocity import *
from kuchka.quantities.kinematics.velocity import *

__all__: list[str] = []
__all__ += acceleration.__all__
__all__ += angular_velocity.__all__
__all__ += velocity.__all__
