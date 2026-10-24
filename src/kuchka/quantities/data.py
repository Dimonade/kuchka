"""Data and DataRate: an amount of information, and how fast it moves.

`Data` is a count of bits.
`DataRate` is data per time, so `Data / Time` is a `DataRate` and `DataRate * Time` is
`Data`, the way `Current * Time` is a `Charge`.
Both have a dimension of their own (the information axis), so a bit rate is never
mistaken for a `Frequency`, a `SampleRate`, or a `BaudRate`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DATA
from kuchka.dimensions import DATA_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Data(LinearQuantity):
    """An amount of information: how many bits, or bytes, something holds."""

    dimension: ClassVar[Dimension] = DATA
    __slots__ = ()

    @overload
    def __mul__(self, other: Frequency) -> DataRate: ...
    @overload
    def __mul__(self, other: Proportion) -> Data: ...
    @overload
    def __mul__(self, other: Numeric) -> Data: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> DataRate: ...
    @overload
    def __truediv__(self, other: DataRate) -> Time: ...
    @overload
    def __truediv__(self, other: Data) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Data: ...
    @overload
    def __truediv__(self, other: Numeric) -> Data: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


class DataRate(LinearQuantity):
    """How fast information moves: bits, or bytes, per second."""

    dimension: ClassVar[Dimension] = DATA_RATE
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> Data: ...
    @overload
    def __mul__(self, other: Proportion) -> DataRate: ...
    @overload
    def __mul__(self, other: Numeric) -> DataRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Data: ...
    @overload
    def __truediv__(self, other: Data) -> Frequency: ...
    @overload
    def __truediv__(self, other: DataRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> DataRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> DataRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DATA, Data)
_register(DATA_RATE, DataRate)

__all__ = ["Data", "DataRate"]
