"""DataRate: how fast information moves.

`DataRate` is data per time.
It has a dimension of its own (the information axis), so a bit rate is never mistaken
for a `Frequency`, a `SampleRate`, or a `BaudRate`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DATA_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.information.data import Data
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class DataRate(LinearQuantity):
    """How fast information moves: bits, or bytes, per second."""

    dimension: ClassVar[Dimension] = DATA_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> DataRate: ...
    @overload
    def __mul__(self, other: Time) -> Data: ...
    @overload
    def __mul__(self, other: Numeric) -> DataRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Data) -> Frequency: ...
    @overload
    def __truediv__(self, other: DataRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> Data: ...
    @overload
    def __truediv__(self, other: Proportion) -> DataRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> DataRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DATA_RATE, DataRate)

__all__ = ["DataRate"]
