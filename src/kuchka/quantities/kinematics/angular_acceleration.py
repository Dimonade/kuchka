"""AngularAcceleration: how fast an angular velocity changes.

`AngularAcceleration` is angle per time squared (angle T⁻²).
Turn is the canonical angle, so the canonical unit is the turn per second squared, and
arithmetic results display in the radian per second squared.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ANGULAR_ACCELERATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.kinematics.acceleration import Acceleration
from kuchka.quantities.length import Length

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.kinematics.angular_jerk import AngularJerk
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.angular_velocity_squared import (
        AngularVelocitySquared,
    )
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class AngularAcceleration(LinearQuantity):
    """Angular velocity gained per unit time: a spindle spinning up, a joint braking.

        spin_up = RadianPerSecond(300) / Second(2)   # 150 rad/s²

    `AngularVelocity / Time` is an `AngularAcceleration`, and a moment of inertia
    times one is a `Torque`.
    Times the radius it acts at, it is the tangential `Acceleration`.
    """

    dimension: ClassVar[Dimension] = ANGULAR_ACCELERATION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularDisplacement) -> AngularVelocitySquared: ...
    @overload
    def __mul__(self, other: AngularMomentum) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> AngularJerk: ...
    @overload
    def __mul__(self, other: Length) -> Acceleration: ...
    @overload
    def __mul__(self, other: MomentOfInertia) -> Torque: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: Time) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: TimeSquared) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularAcceleration) -> Proportion: ...
    @overload
    def __truediv__(self, other: AngularJerk) -> Time: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Frequency: ...
    @overload
    def __truediv__(self, other: Frequency) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularAcceleration: ...
    @overload
    def __truediv__(self, other: Time) -> AngularJerk: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularAcceleration: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ANGULAR_ACCELERATION, AngularAcceleration)
_bridge(AngularAcceleration, "*", Length, Acceleration)
_bridge(Acceleration, "/", AngularAcceleration, Length)

__all__ = ["AngularAcceleration"]
