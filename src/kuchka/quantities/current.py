"""An electric current: a base quantity, beside `Length` and `Mass`.

`Current` takes part in Ohm's law and the power triangle, whose halves are spelled out
on each type they name:

- `Current * Resistance -> Voltage` and `Current * Voltage -> Power`,
- `Current * Time -> Charge`, and its inverses `Charge / Time -> Current` and
  `Charge / Current -> Time`,
- `Current / Voltage -> Conductance` and `Current / Conductance -> Voltage`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CURRENT
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Current(LinearQuantity):
    """An electric current."""

    dimension: ClassVar[Dimension] = CURRENT
    __slots__ = ()

    @overload
    def __mul__(self, other: Voltage) -> Power: ...
    @overload
    def __mul__(self, other: Resistance) -> Voltage: ...
    @overload
    def __mul__(self, other: Time) -> Charge: ...
    @overload
    def __mul__(self, other: Proportion) -> Current: ...
    @overload
    def __mul__(self, other: Numeric) -> Current: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Voltage) -> Conductance: ...
    @overload
    def __truediv__(self, other: Conductance) -> Voltage: ...
    @overload
    def __truediv__(self, other: Charge) -> Frequency: ...
    @overload
    def __truediv__(self, other: Frequency) -> Charge: ...
    @overload
    def __truediv__(self, other: Current) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Current: ...
    @overload
    def __truediv__(self, other: Numeric) -> Current: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CURRENT, Current)

__all__ = ["Current"]
