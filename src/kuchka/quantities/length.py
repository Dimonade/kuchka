"""Length: a distance or a physical extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LENGTH
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.kinematics import Velocity
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.volume import Volume


class Length(LinearQuantity):
    """A distance or a physical extent: how far apart, how long, how wide, how far."""

    dimension: ClassVar[Dimension] = LENGTH
    __slots__ = ()

    @overload
    def __mul__(self, other: Length) -> Area: ...
    @overload
    def __mul__(self, other: Area) -> Volume: ...
    @overload
    def __mul__(self, other: Frequency) -> Velocity: ...
    @overload
    def __mul__(self, other: Force) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Length: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> Velocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Length: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LENGTH, Length)

__all__ = ["Length"]
