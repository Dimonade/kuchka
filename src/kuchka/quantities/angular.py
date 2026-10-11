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
from typing import overload

from kuchka.dimensions import ANGLE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.rotational import AngularVelocity
    from kuchka.quantities.rotational import Torque
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Angle(ModularQuantity):
    """A plane angle: a bearing, a phase, a joint rotation."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()

    def to_angular_displacement(self) -> AngularDisplacement:
        """View this position as the angle swept from zero to reach it.

            quarter_turn = Degree(90).to_angular_displacement()

        A position is within one turn, so `Degree(370)`, the position 10 degrees, gives
        a displacement of 10 degrees.
        """
        wrapped = self._wrap(self._magnitude)
        return AngularDisplacement(wrapped, self._display_unit)


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
    def __mul__(self, other: Numeric) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
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
