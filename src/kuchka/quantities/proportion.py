"""Proportion: a dimensionless quantity, expressed as a ratio or a percentage.

Built by explicit construction (`Percent(5)`, `Ratio(0.05)`) and as the result of a
ratio: the quotient of two quantities of one dimension, and the product or quotient of
two proportions.
`Volt(5) / Volt(2)` is `Ratio(Fraction(5, 2))`, and `Percent(50) * Percent(50)` is
`Ratio(Fraction(1, 4))`.
Other dimensionless results, such as `Hertz(2) * Second(3)`, are plain `Fraction`
values.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DIMENSIONLESS
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _register_ratio

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()

    @overload
    def __mul__(self, other: Proportion) -> Proportion: ...
    @overload
    def __mul__(self, other: Numeric) -> Proportion: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Proportion) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Proportion: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DIMENSIONLESS, Proportion)
_register_ratio(Proportion)

__all__ = ["Proportion"]
