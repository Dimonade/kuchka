"""Data: an amount of information.

`Data` is a count of bits.
It has a dimension of its own (the information axis), so a bit count is never mistaken
for a `Frequency`, a `SampleRate`, or a `BaudRate`.
`Data / Time` is a `DataRate` and `DataRate * Time` is `Data`, the way `Current * Time`
is a `Charge`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DATA
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.information.data_rate import DataRate
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


_register(DATA, Data)

__all__ = ["Data"]
