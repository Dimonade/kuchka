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
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electrical import Current
    from kuchka.quantities.electrical import Voltage
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Charge(LinearQuantity):
    """An accumulated flow of electric current: how much charge has moved."""

    dimension: ClassVar[Dimension] = CHARGE
    __slots__ = ()

    @overload
    def __mul__(self, other: Frequency) -> Current: ...
    @overload
    def __mul__(self, other: Voltage) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Charge: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> Current: ...
    @overload
    def __truediv__(self, other: Current) -> Time: ...
    @overload
    def __truediv__(self, other: Charge) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Charge: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CHARGE, Charge)

__all__ = ["Charge"]
