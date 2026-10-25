"""Conductance: how readily a circuit element passes current.

`Conductance` is the reciprocal of `Resistance`.

Ohm's law works from either side of the reciprocal: `Voltage * Conductance -> Current`
alongside `Voltage / Resistance -> Current`, and `Current / Voltage -> Conductance`
alongside `Voltage / Current -> Resistance`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CONDUCTANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.proportion import Proportion


class Conductance(LinearQuantity):
    """How readily a circuit element passes current: the reciprocal of Resistance."""

    dimension: ClassVar[Dimension] = CONDUCTANCE
    __slots__ = ()

    @overload
    def __mul__(self, other: Voltage) -> Current: ...
    @overload
    def __mul__(self, other: Resistance) -> Fraction: ...
    @overload
    def __mul__(self, other: Proportion) -> Conductance: ...
    @overload
    def __mul__(self, other: Numeric) -> Conductance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Conductance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Conductance: ...
    @overload
    def __truediv__(self, other: Numeric) -> Conductance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @overload
    def __rtruediv__(self, other: Numeric) -> Resistance: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        return super().__rtruediv__(other)


_register(CONDUCTANCE, Conductance)

__all__ = ["Conductance"]
