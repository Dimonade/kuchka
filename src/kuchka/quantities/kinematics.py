"""Velocity: a rate of change of position.

Defined alongside its one relationship to `Length` and `Time`
(`Length / Time -> Velocity`, and its inverse, `Velocity * Time -> Length`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VELOCITY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from decimal import Decimal

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.length import Length
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Velocity(LinearQuantity):
    """A rate of change of position: distance covered per unit time."""

    dimension: ClassVar[Dimension] = VELOCITY

    @overload
    def __mul__(self, other: Time) -> Length: ...
    @overload
    def __mul__(self, other: Numeric) -> Velocity: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Length: ...
    @overload
    def __truediv__(self, other: Numeric) -> Velocity: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


register(VELOCITY, Velocity)

__all__ = ["Velocity"]
