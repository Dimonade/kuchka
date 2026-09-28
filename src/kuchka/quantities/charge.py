"""Charge: an accumulated flow of electric current over time.

Defined alongside its one relationship to `Current` and `Time`
(`Current * Time -> Charge`, and its two inverses, `Charge / Time -> Current` and
`Charge / Current -> Time`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CHARGE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electrical import Current
    from kuchka.quantities.temporal import Time


class Charge(LinearQuantity):
    """An accumulated flow of electric current: how much charge has moved."""

    dimension: ClassVar[Dimension] = CHARGE

    @overload
    def __truediv__(self, other: Time) -> Current: ...
    @overload
    def __truediv__(self, other: Current) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Charge: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


register(CHARGE, Charge)

__all__ = ["Charge"]
