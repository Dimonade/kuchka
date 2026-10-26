"""Resistance: the opposition a circuit element presents to current flow."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import RESISTANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.proportion import Proportion


class Resistance(LinearQuantity):
    """The opposition a circuit element presents to current flow."""

    dimension: ClassVar[Dimension] = RESISTANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Conductance) -> Fraction: ...
    @overload
    def __mul__(self, other: Current) -> Voltage: ...
    @overload
    def __mul__(self, other: Proportion) -> Resistance: ...
    @overload
    def __mul__(self, other: Numeric) -> Resistance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __rtruediv__
    @overload
    def __rtruediv__(self, other: Numeric) -> Conductance: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        # NOTE: `Resistance` is the registered canonical type for `RESISTANCE`, so the
        # base implementation's canonical-type guard passes and this reaches
        # `Conductance` through ordinary dimension algebra -- no override of the
        # runtime logic needed, only of the static signature (see `Time.__rtruediv__`
        # for the same pattern with Frequency).
        return super().__rtruediv__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> Resistance: ...
    @overload
    def __truediv__(self, other: Resistance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Resistance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(RESISTANCE, Resistance)

__all__ = ["Resistance"]
