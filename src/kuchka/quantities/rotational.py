"""AngularVelocity and Torque: how fast an angle is swept, and the effort behind it.

`AngularVelocity` is angle per time (angle T^-1), and `Torque` is energy per angle
(M L^2 T^-2 angle^-1).
Counting the angle axis tells them apart from `Frequency` and `Energy`: one hertz is a
cycle per second, not an angular velocity, and a newton-metre of torque is not a joule.
Turn is the canonical angle, so the canonical units are the turn per second and the
joule per turn, and a radian enters only as the exact factor `1 / (2 pi)`.

The relationships:

- `AngularVelocity * Time -> AngularDisplacement` and its inverses,
  `AngularDisplacement / Time -> AngularVelocity` and
  `AngularDisplacement / AngularVelocity -> Time`;
- `Torque * AngularDisplacement -> Energy` and its inverses (see `AngularDisplacement`);
- `Torque * AngularVelocity -> Power` and its inverses,
  `Power / AngularVelocity -> Torque` and `Power / Torque -> AngularVelocity`;
- `AngularVelocity / Frequency -> AngularDisplacement`.

The other overload halves live on `AngularDisplacement`, `Time`, `Energy`, `Power`, and
`Frequency`.
`Torque.from_force(force, lever_arm)` builds a torque from a force at a distance, and
`Frequency.to_angular_velocity()` and `AngularVelocity.to_frequency()` move between a
rate of cycles and a rate of angle.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.dimensions import TORQUE
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.constants import PI
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.kinematics import Force
from kuchka.quantities.length import Length

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class AngularVelocity(LinearQuantity):
    """Angle swept per unit time: a shaft speed, a turn rate."""

    dimension: ClassVar[Dimension] = ANGULAR_VELOCITY
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Torque) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_frequency(self) -> Frequency:
        """View this rate of angle as the cycles per second of the rotation.

            shaft_speed = RevolutionPerMinute(3000).to_frequency()

        One turn per second is one hertz.
        """
        from kuchka.quantities.temporal import Frequency  # noqa: PLC0415 -- temporal imports this module at its own import time

        return Frequency(self._magnitude, Frequency._canonical_unit)  # noqa: SLF001 -- Frequency's own canonical unit


class Torque(LinearQuantity):
    """Energy per angle: the turning effort of a force at a distance from an axis."""

    dimension: ClassVar[Dimension] = TORQUE
    __slots__ = ()

    @overload
    def __mul__(self, other: AngularDisplacement) -> Energy: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Torque: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Torque: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_force(cls, force: Force, lever_arm: Length) -> Self:
        """Return the torque of a force applied at a distance from the axis.

            Torque.from_force(Newton(50), Metre(0.2)) == NewtonMetre(10)

        The force is perpendicular to the lever arm, so the torque is their product.
        `Force * Length` alone is an `Energy`, because a newton-metre of work and a
        newton-metre of torque differ by the angle the force turns through.
        """
        if not isinstance(force, Force) or not isinstance(lever_arm, Length):
            raise IncompatibleDimensionError("build a torque from", force, lever_arm)
        joules_per_radian = force._magnitude * lever_arm._magnitude  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes
        return cls(joules_per_radian * 2 * PI, cls._result_unit)


_register(ANGULAR_VELOCITY, AngularVelocity)
_register(TORQUE, Torque)

__all__ = ["AngularVelocity", "Torque"]
