"""Heating rate: how fast a temperature changes."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import HEATING_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class HeatingRate(LinearQuantity):
    """How fast a temperature changes, in kelvin or degrees per second, minute, or hour.

        ramp = CelsiusPerMinute(5)
        warmed = ramp * Minute(12)   # a TemperatureDelta of 60 K

    It is the quotient `TemperatureDelta / Time`, and `HeatingRate * Time` is a
    `TemperatureDelta`.
    A temperature that falls has a negative heating rate.
    """

    dimension: ClassVar[Dimension] = HEATING_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: HeatCapacity) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> HeatingRate: ...
    @overload
    def __mul__(self, other: SpecificHeatCapacity) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Time) -> TemperatureDelta: ...
    @overload
    def __mul__(self, other: Numeric) -> HeatingRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Frequency) -> TemperatureDelta: ...
    @overload
    def __truediv__(self, other: HeatingRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> HeatingRate: ...
    @overload
    def __truediv__(self, other: TemperatureDelta) -> Frequency: ...
    @overload
    def __truediv__(self, other: Numeric) -> HeatingRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(HEATING_RATE, HeatingRate)

__all__ = ["HeatingRate"]
