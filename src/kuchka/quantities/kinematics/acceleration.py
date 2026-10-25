"""Acceleration: a rate of change of velocity.

- `Velocity / Time -> Acceleration`, and its inverse, `Acceleration * Time -> Velocity`.
- `Mass * Acceleration -> Force`, Newton's second law, and its inverse,
  `Force / Acceleration -> Mass`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ACCELERATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Acceleration(LinearQuantity):
    """A rate of change of velocity: how quickly speed or direction changes."""

    dimension: ClassVar[Dimension] = ACCELERATION
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> Velocity: ...
    @overload
    def __mul__(self, other: Mass) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __mul__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Velocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Frequency: ...
    @overload
    def __truediv__(self, other: Acceleration) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ACCELERATION, Acceleration)

__all__ = ["Acceleration"]
