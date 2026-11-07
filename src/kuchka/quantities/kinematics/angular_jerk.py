"""AngularJerk: how fast an angular acceleration changes.

`AngularJerk` is angle per time cubed (angle T⁻³).
Turn is the canonical angle, so the canonical unit is the turn per second cubed, and
arithmetic results display in the radian per second cubed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ANGULAR_JERK
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.kinematics.jerk import Jerk
from kuchka.quantities.length import Length

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class AngularJerk(LinearQuantity):
    """Angular acceleration gained per unit time: the ramp of a servo's S-curve.

        ramp = RadianPerSecondSquared(150) / Second(0.5)   # 300 rad/s³

    `AngularAcceleration / Time` is an `AngularJerk`, and `AngularJerk * Time` an
    `AngularAcceleration`.
    Times the radius it acts at, it is the tangential `Jerk`.
    """

    dimension: ClassVar[Dimension] = ANGULAR_JERK
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Jerk: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularJerk: ...
    @overload
    def __mul__(self, other: Time) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: TimeCubed) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: TimeSquared) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularJerk: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularAcceleration) -> Frequency: ...
    @overload
    def __truediv__(self, other: AngularJerk) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> AngularAcceleration: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularJerk: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularJerk: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ANGULAR_JERK, AngularJerk)
_bridge(AngularJerk, "*", Length, Jerk)
_bridge(Jerk, "/", AngularJerk, Length)

__all__ = ["AngularJerk"]
