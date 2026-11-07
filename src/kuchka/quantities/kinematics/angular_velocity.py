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
from typing import Literal
from typing import Self
from typing import overload

from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.constants import PI
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.kinematics.acceleration import Acceleration
from kuchka.quantities.kinematics.velocity import Velocity
from kuchka.quantities.length import Length
from kuchka.quantities.temporal import Frequency

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_jerk import AngularJerk
    from kuchka.quantities.kinematics.angular_velocity_squared import (
        AngularVelocitySquared,
    )
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Time


class AngularVelocity(LinearQuantity):
    """Angle swept per unit time: a shaft speed, a turn rate.

        rim = RadianPerSecond(300) * Metre(0.2)   # 60 m/s

    Times the radius a point turns at, it is the tangential `Velocity`, and a
    tangential velocity over an angular velocity is that radius.
    Times that tangential velocity, it is the centripetal `Acceleration`.
    `AngularVelocity.from_tangential(velocity, radius)` reads the rate back.
    """

    dimension: ClassVar[Dimension] = ANGULAR_VELOCITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularMomentum) -> Energy: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> AngularVelocitySquared: ...
    @overload
    def __mul__(self, other: FirstMomentOfMass) -> Momentum: ...
    @overload
    def __mul__(self, other: Frequency) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: Length) -> Velocity: ...
    @overload
    def __mul__(self, other: MomentOfInertia) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: Momentum) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Time) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Torque) -> Power: ...
    @overload
    def __mul__(self, other: Velocity) -> Acceleration: ...
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
    def __truediv__(self, other: AngularJerk) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: Time) -> AngularAcceleration: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> AngularJerk: ...
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

    @classmethod
    def from_tangential(cls, velocity: Velocity, radius: Length) -> Self:
        """Return the angular velocity of a point moving at a speed around a radius.

            AngularVelocity.from_tangential(MetrePerSecond(60), Metre(0.2))  # 300 rad/s

        The angle swept is the arc travelled over the radius, in radians.
        `Velocity / Length` alone is a `Frequency`, because a speed over a wavelength
        is the cycles per second of a wave.
        """
        if not isinstance(velocity, Velocity) or not isinstance(radius, Length):
            raise IncompatibleDimensionError(
                "build an angular velocity from", velocity, radius
            )
        radians_per_second = (velocity / radius)._magnitude  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes
        return cls(radians_per_second / (2 * PI), cls._result_unit)

    # BEGIN GENERATED __pow__
    @overload
    def __pow__(self, exponent: Literal[2]) -> AngularVelocitySquared: ...
    @overload
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction:
        return super().__pow__(exponent)


_register(ANGULAR_VELOCITY, AngularVelocity)
_bridge(AngularVelocity, "*", Length, Velocity)
_bridge(Velocity, "/", AngularVelocity, Length)
_bridge(AngularVelocity, "*", Velocity, Acceleration)
_bridge(Acceleration, "/", AngularVelocity, Velocity)

__all__ = ["AngularVelocity"]
