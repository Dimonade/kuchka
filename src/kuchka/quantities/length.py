"""Length: a distance or a physical extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LENGTH
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from decimal import Decimal

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.kinematics import Velocity
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.volume import Volume


class Length(LinearQuantity):
    """A distance or a physical extent: how far apart, how long, how wide, how far."""

    dimension: ClassVar[Dimension] = LENGTH

    @overload
    def __mul__(self, other: Length) -> Area: ...
    @overload
    def __mul__(self, other: Area) -> Volume: ...
    @overload
    def __mul__(self, other: Numeric) -> Length: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> Velocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Length: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


register(LENGTH, Length)

__all__ = ["Length"]
