"""AngularVelocitySquared: an angular velocity times an angular velocity."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ANGULAR_VELOCITY_SQUARED
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
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.proportion import Proportion


class AngularVelocitySquared(LinearQuantity):
    """An angular velocity times an angular velocity, in rad²/s².

        spin = RadianPerSecond(300)
        centripetal = spin * spin * Metre(0.2)   # an Acceleration of 18000 m/s²

    It is the square that a centripetal acceleration `omega² * r` and a rotational
    kinetic energy `I * omega² / 2` are written with, and the product `theta * alpha`
    of an angular displacement and an angular acceleration.
    Times the radius it acts at, it is the centripetal `Acceleration`, and times a
    `MomentOfInertia` it is an `Energy`.
    """

    dimension: ClassVar[Dimension] = ANGULAR_VELOCITY_SQUARED
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Acceleration: ...
    @overload
    def __mul__(self, other: MomentOfInertia) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularVelocitySquared: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularVelocitySquared: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularAcceleration) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> AngularAcceleration: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: AngularVelocitySquared) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularVelocitySquared: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularVelocitySquared: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ANGULAR_VELOCITY_SQUARED, AngularVelocitySquared)
_bridge(AngularVelocitySquared, "*", Length, Acceleration)
_bridge(Acceleration, "/", AngularVelocitySquared, Length)

__all__ = ["AngularVelocitySquared"]
