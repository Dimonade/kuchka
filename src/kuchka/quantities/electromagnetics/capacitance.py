"""Capacitance: the charge a component stores per volt."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CAPACITANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Capacitance(LinearQuantity):
    """The charge stored per volt across a component."""

    dimension: ClassVar[Dimension] = CAPACITANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> Conductance: ...
    @overload
    def __mul__(self, other: Proportion) -> Capacitance: ...
    @overload
    def __mul__(self, other: Resistance) -> Time: ...
    @overload
    def __mul__(self, other: Voltage) -> Charge: ...
    @overload
    def __mul__(self, other: Numeric) -> Capacitance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Capacitance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Conductance) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Permittivity: ...
    @overload
    def __truediv__(self, other: Permittivity) -> Length: ...
    @overload
    def __truediv__(self, other: Proportion) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Time) -> Conductance: ...
    @overload
    def __truediv__(self, other: Numeric) -> Capacitance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CAPACITANCE, Capacitance)

__all__ = ["Capacitance"]
