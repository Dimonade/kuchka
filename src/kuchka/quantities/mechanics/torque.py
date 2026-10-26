"""Torque: energy per angle, the turning effort of a force at a distance from an axis.

`Torque` is M L² T⁻² angle⁻¹.
Counting the angle axis tells it apart from `Energy`: a newton-metre of torque is not a
joule.
Turn is the canonical angle, so the canonical unit is the joule per turn.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import TORQUE
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import _register_hint
from kuchka.internal.constants import PI
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.length import Length
from kuchka.quantities.mechanics.energy import Energy
from kuchka.quantities.mechanics.force import Force

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion


class Torque(LinearQuantity):
    """Energy per angle: the turning effort of a force at a distance from an axis."""

    dimension: ClassVar[Dimension] = TORQUE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularDisplacement) -> Energy: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> Torque: ...
    @overload
    def __mul__(self, other: Numeric) -> Torque: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> Torque: ...
    @overload
    def __truediv__(self, other: Torque) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Torque: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
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


_register(TORQUE, Torque)
_register_hint(
    Energy,
    Torque,
    "A newton-metre of work is an `Energy`, and a `Torque` is energy per angle: "
    "divide an energy by an `AngularDisplacement` for a torque, multiply a torque by "
    "one for an energy, or build a torque with `Torque.from_force(force, lever_arm)`.",
)

__all__ = ["Torque"]
