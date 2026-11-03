"""Heat capacity: the energy a body needs to change its temperature by one degree."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import HEAT_CAPACITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class HeatCapacity(LinearQuantity):
    """The energy that changes a body's temperature by one degree, in joules per kelvin.

        kettle = KilojoulePerKelvin(1.2)
        heat = kettle * DeltaKelvin(80)   # an Energy

    It is the quotient `Energy / TemperatureDelta`.
    `HeatCapacity * TemperatureDelta` is an `Energy`: the heat `Q = C * dT`.
    `Energy / HeatCapacity` is a `TemperatureDelta`, and `Power / HeatCapacity` is a
    `HeatingRate`.
    `HeatCapacity / Mass` is a `SpecificHeatCapacity`, and `SpecificHeatCapacity * Mass`
    is a `HeatCapacity`.
    A joule per degree Celsius is a joule per kelvin, because a Celsius degree is a
    difference.
    """

    dimension: ClassVar[Dimension] = HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: HeatingRate) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: HeatCapacity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: Proportion) -> HeatCapacity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> Mass: ...
    @overload
    def __truediv__(self, other: Numeric) -> HeatCapacity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(HEAT_CAPACITY, HeatCapacity)

__all__ = ["HeatCapacity"]
