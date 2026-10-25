"""Velocity: a rate of change of position.

- `Length / Time -> Velocity`, and its inverse, `Velocity * Time -> Length`.
- `Velocity / Time -> Acceleration`, and `Velocity / Acceleration -> Time`.
- `Force * Velocity -> Power` and `Power / Force -> Velocity`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VELOCITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Velocity(LinearQuantity):
    """A rate of change of position: distance covered per unit time."""

    dimension: ClassVar[Dimension] = VELOCITY
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> Length: ...
    @overload
    def __mul__(self, other: Force) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Acceleration: ...
    @overload
    def __mul__(self, other: Proportion) -> Velocity: ...
    @overload
    def __mul__(self, other: Numeric) -> Velocity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Length: ...
    @overload
    def __truediv__(self, other: Time) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Acceleration) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Frequency: ...
    @overload
    def __truediv__(self, other: Velocity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Velocity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Velocity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(VELOCITY, Velocity)

__all__ = ["Velocity"]
