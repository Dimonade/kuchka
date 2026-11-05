"""AngularVelocity: how fast an angle is swept.

`AngularVelocity` is angle per time (angle T⁻¹).
Counting the angle axis tells it apart from `Frequency`: one hertz is a cycle per
second, not an angular velocity.
Turn is the canonical angle, so the canonical unit is the turn per second, and a radian
enters only as the exact factor `1 / (2 pi)`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.kinematics.velocity import Velocity
from kuchka.quantities.length import Length
from kuchka.quantities.temporal import Frequency

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Time


class AngularVelocity(LinearQuantity):
    """Angle swept per unit time: a shaft speed, a turn rate.

        rim = RadianPerSecond(300) * Metre(0.2)   # 60 m/s

    Times the radius a point turns at, it is the tangential `Velocity`, and a
    tangential velocity over an angular velocity is that radius.
    """

    dimension: ClassVar[Dimension] = ANGULAR_VELOCITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularMomentum) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: Length) -> Velocity: ...
    @overload
    def __mul__(self, other: MomentOfInertia) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Time) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Torque) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularAcceleration) -> Time: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Frequency: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: Time) -> AngularAcceleration: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularVelocity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_frequency(self) -> Frequency:
        """View this rate of angle as the cycles per second of the rotation.

            shaft_speed = RevolutionPerMinute(3000).to_frequency()

        One turn per second is one hertz.
        """
        return Frequency(self._magnitude, Frequency._canonical_unit)  # noqa: SLF001 -- Frequency's own canonical unit


_register(ANGULAR_VELOCITY, AngularVelocity)
_bridge(AngularVelocity, "*", Length, Velocity)
_bridge(Velocity, "/", AngularVelocity, Length)

__all__ = ["AngularVelocity"]
