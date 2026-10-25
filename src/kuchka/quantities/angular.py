"""Angle and AngularDisplacement: a position on a circle, and the angle swept.

`Angle` is a position on a circle, a bearing or a joint position: 370 degrees is 10
degrees, so it wraps and takes no part in arithmetic.
`AngularDisplacement` is the total angle swept, which does not wrap: 370 degrees of
rotation do different work than 10 degrees, and a torque multiplies the swept angle.
Both measure the same dimension in the same units, and `Angle.to_angular_displacement()`
and `AngularDisplacement.to_angle()` move between them.

Turn is the canonical unit.
See `kuchka.units.angular` for how Radian relates to it.

The relationships that involve an angular displacement:

- `AngularDisplacement / Time -> AngularVelocity` and its inverses,
  `AngularVelocity * Time -> AngularDisplacement` and
  `AngularDisplacement / AngularVelocity -> Time`;
- `Torque * AngularDisplacement -> Energy` and its inverses,
  `Energy / AngularDisplacement -> Torque` and `Energy / Torque -> AngularDisplacement`;
- `AngularDisplacement * Frequency -> AngularVelocity`, the angle swept per cycle times
  the cycles per second.

The other overload halves live on `Time`, `Energy`, `Frequency`, `AngularVelocity`,
and `Torque`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import ANGLE
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.storage import _ScalarStorage

if TYPE_CHECKING:
    from fractions import Fraction
    from typing import Any
    from typing import Never

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Angle(ModularQuantity):
    """A plane angle: a bearing, a phase, a joint rotation."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()

    @override
    def __mul__(self, other: Numeric) -> Self:
        """Scale by a plain number; refuse a quantity, pointing at the angle swept."""
        _refuse_a_quantity("multiply", self, other)
        return super().__mul__(other)

    @override
    def __rmul__(self, other: Numeric) -> Self:
        """Scale by a plain number; refuse a quantity, pointing at the angle swept."""
        _refuse_a_quantity("multiply", other, self)
        return super().__rmul__(other)

    @override
    def __truediv__(self, other: Numeric) -> Self:
        """Divide by a plain number; refuse a quantity, pointing at the angle swept."""
        _refuse_a_quantity("divide", self, other)
        return super().__truediv__(other)

    def __rtruediv__(self, other: Never) -> Any:  # noqa: ANN401 -- only ever raises or declines
        """Refuse to be the divisor of a quantity, pointing at the angle swept."""
        _refuse_a_quantity("divide", other, self)
        return NotImplemented

    def to_angular_displacement(self) -> AngularDisplacement:
        """View this position as the angle swept from zero to reach it.

            quarter_turn = Degree(90).to_angular_displacement()

        A position is within one turn, so `Degree(370)`, the position 10 degrees, gives
        a displacement of 10 degrees.
        """
        wrapped = self._wrap(self._magnitude)
        return AngularDisplacement(wrapped, self._display_unit)


def _refuse_a_quantity(operation: str, left: object, right: object) -> None:
    """Raise if either operand of a product or quotient is a quantity, not a number."""
    if isinstance(left, _ScalarStorage) and isinstance(right, _ScalarStorage):
        raise IncompatibleDimensionError(
            operation,
            left,
            right,
            hint=(
                "An `Angle` is a position on a circle and wraps, so it does not "
                f"{operation} quantities. Use `angle.to_angular_displacement()` for "
                "the angle swept, which does."
            ),
        )


class AngularDisplacement(LinearQuantity):
    """The total angle swept: a rotation that keeps counting past one turn.

    Unlike `Angle` it does not wrap, so 370 degrees of rotation stay 370 degrees, and it
    multiplies and divides like any linear quantity:
    `Torque * AngularDisplacement` is the work done, and `AngularDisplacement / Time` is
    an angular velocity.
    """

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()

    @overload
    def __mul__(self, other: Torque) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Proportion) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Numeric) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Time: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularDisplacement: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_angle(self) -> Angle:
        """Wrap this displacement into the position on the circle it ends at.

            DegreeDisplacement(370).to_angle() == Degree(10)

        The full turns it swept are dropped.
        """
        return Angle(self._magnitude, self._display_unit).normalize()


_register(ANGLE, Angle)
_register(ANGLE, AngularDisplacement)

__all__ = ["Angle", "AngularDisplacement"]
