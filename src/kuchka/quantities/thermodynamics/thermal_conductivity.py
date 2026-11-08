"""ThermalConductivity: how readily a material conducts heat."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import THERMAL_CONDUCTIVITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class ThermalConductivity(LinearQuantity):
    """How readily a material conducts heat: power per length per kelvin.

    A degree Celsius in the denominator is a kelvin, so `W/(m·°C)` is the same unit.
    """

    dimension: ClassVar[Dimension] = THERMAL_CONDUCTIVITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> ThermalConductivity: ...
    @overload
    def __mul__(self, other: Numeric) -> ThermalConductivity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: DynamicViscosity) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: Proportion) -> ThermalConductivity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: ThermalConductivity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> ThermalConductivity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(THERMAL_CONDUCTIVITY, ThermalConductivity)

__all__ = ["ThermalConductivity"]
