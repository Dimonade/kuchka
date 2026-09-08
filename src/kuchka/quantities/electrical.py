"""Voltage, Current, Power, and Resistance.

These four types are defined together, in one module, as they are not independent:
their `@overload` tables are the power triangle and Ohm's law, so each type's
multiplication and division signatures name the other three directly.

Runtime arithmetic (`+`, `-`, `*`, `/`) is fully general and lives on `LinearQuantity`:
it derives any product or quotient from `Dimension` exponent-vector algebra, and does
not need to know about "Power" as a concept at all.
Python's type checkers cannot infer "Voltage times Current is Power" from that general
algebra, though -- they only know it because each of the six relationships below is
spelled out as an explicit `@overload`.

Every overload list also ends with a fallback overload matching the signature declared
on `LinearQuantity`, which is what keeps these overrides compatible with the base class
under strict type checking.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CURRENT
from kuchka.dimensions import POWER
from kuchka.dimensions import RESISTANCE
from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from decimal import Decimal

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.charge import Charge
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.temporal import Time


class Voltage(LinearQuantity):
    """An electric potential difference."""

    dimension: ClassVar[Dimension] = VOLTAGE

    @overload
    def __mul__(self, other: Current) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Voltage: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Current) -> Resistance: ...
    @overload
    def __truediv__(self, other: Resistance) -> Current: ...
    @overload
    def __truediv__(self, other: Numeric) -> Voltage: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


class Current(LinearQuantity):
    """An electric current."""

    dimension: ClassVar[Dimension] = CURRENT

    @overload
    def __mul__(self, other: Voltage) -> Power: ...
    @overload
    def __mul__(self, other: Resistance) -> Voltage: ...
    @overload
    def __mul__(self, other: Time) -> Charge: ...
    @overload
    def __mul__(self, other: Numeric) -> Current: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)


class Power(LinearQuantity):
    """The rate at which electrical energy is transferred or dissipated."""

    dimension: ClassVar[Dimension] = POWER

    @overload
    def __mul__(self, other: Time) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Power: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Voltage) -> Current: ...
    @overload
    def __truediv__(self, other: Current) -> Voltage: ...
    @overload
    def __truediv__(self, other: Numeric) -> Power: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


class Resistance(LinearQuantity):
    """The opposition a circuit element presents to current flow."""

    dimension: ClassVar[Dimension] = RESISTANCE

    @overload
    def __mul__(self, other: Current) -> Voltage: ...
    @overload
    def __mul__(self, other: Numeric) -> Resistance: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)


register(VOLTAGE, Voltage)
register(CURRENT, Current)
register(POWER, Power)
register(RESISTANCE, Resistance)

__all__ = ["Current", "Power", "Resistance", "Voltage"]
