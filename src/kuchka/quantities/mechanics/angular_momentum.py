"""AngularMomentum: a moment of inertia times its angular velocity.

`AngularMomentum` is M L² angle⁻¹ T⁻¹.
A torque applied for a time changes it, so `Torque * Time` is an `AngularMomentum`, and
`AngularMomentum * AngularVelocity` is an `Energy`.
Turn is the canonical angle, so the canonical unit is the joule second per turn, and
arithmetic results display in the kilogram square metre per second.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ANGULAR_MOMENTUM
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class AngularMomentum(LinearQuantity):
    """A moment of inertia times its angular velocity: the spin a torque changes.

        spin = KilogramSquareMetre(0.04) * RadianPerSecond(300)   # 12 kg·m²/s

    `MomentOfInertia * AngularVelocity` and `Torque * Time` are an `AngularMomentum`.
    `Momentum * Length` has the dimension without the angle and is also the action of
    quantum mechanics, so the angular momentum of a point mass is
    `MomentOfInertia * AngularVelocity`.
    """

    dimension: ClassVar[Dimension] = ANGULAR_MOMENTUM
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularAcceleration) -> Power: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> Torque: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularMomentum) -> Proportion: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> MomentOfInertia: ...
    @overload
    def __truediv__(self, other: MomentOfInertia) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularMomentum: ...
    @overload
    def __truediv__(self, other: Time) -> Torque: ...
    @overload
    def __truediv__(self, other: Torque) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularMomentum: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ANGULAR_MOMENTUM, AngularMomentum)

__all__ = ["AngularMomentum"]
