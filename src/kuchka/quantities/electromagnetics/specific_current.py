"""Specific current: electric current per unit mass."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class SpecificCurrent(LinearQuantity):
    """Electric current per unit mass, in amperes per kilogram.

        rate = MilliamperePerKilogram(0.2)
        current = rate * Kilogram(5)   # a Current

    It is the quotient `Current / Mass`, and `SpecificCurrent * Mass` is a `Current`.
    It is also the rate of change of a `SpecificCharge`: `SpecificCharge / Time` is a
    `SpecificCurrent`, and `SpecificCurrent * Time` a `SpecificCharge`.
    `ExposureRate` is a role of it: the exposure an X-ray or gamma beam delivers in a
    unit of time.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_CURRENT
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Mass) -> Current: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificCurrent: ...
    @overload
    def __mul__(self, other: Time) -> SpecificCharge: ...
    @overload
    def __mul__(self, other: Voltage) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificCurrent: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Frequency) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: Proportion) -> SpecificCurrent: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> Frequency: ...
    @overload
    def __truediv__(self, other: SpecificCurrent) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificCurrent: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_CURRENT, SpecificCurrent)

__all__ = ["SpecificCurrent"]
