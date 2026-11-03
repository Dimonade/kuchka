"""Specific heat capacity: the energy per mass for one degree of temperature change."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_HEAT_CAPACITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate


class SpecificHeatCapacity(LinearQuantity):
    """The energy per unit mass that changes a temperature by one degree, in J/(kg K).

        water = KilojoulePerKilogramKelvin(4.184)
        heat = water * Kilogram(2) * DeltaKelvin(30)   # an Energy

    `SpecificHeatCapacity * Mass` is a `HeatCapacity`, and `SpecificHeatCapacity *
    TemperatureDelta` is a `SpecificEnergy`.
    `SpecificEnergy / TemperatureDelta` and `HeatCapacity / Mass` are specific heat
    capacities, and `SpecificEnergy / SpecificHeatCapacity` is a `TemperatureDelta`.
    So the heat `Q = m * c * dT` comes out as an `Energy` however it is grouped.
    A joule per kilogram degree Celsius is a joule per kilogram kelvin, because a
    Celsius degree is a difference.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: HeatingRate) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Mass) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_HEAT_CAPACITY, SpecificHeatCapacity)

__all__ = ["SpecificHeatCapacity"]
