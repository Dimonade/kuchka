"""Molality: the amount of a solute per mass of solvent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLALITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarHeatCapacity
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class Molality(LinearQuantity):
    """The amount of a solute per mass of solvent: moles per kilogram."""

    dimension: ClassVar[Dimension] = MOLALITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Density) -> MolarConcentration: ...
    @overload
    def __mul__(self, other: Mass) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: MolarCharge) -> SpecificCharge: ...
    @overload
    def __mul__(self, other: MolarHeatCapacity) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: MolarMass) -> Fraction: ...
    @overload
    def __mul__(self, other: Proportion) -> Molality: ...
    @overload
    def __mul__(self, other: Numeric) -> Molality: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Molality) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Molality: ...
    @overload
    def __truediv__(self, other: Numeric) -> Molality: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __rtruediv__
    @overload
    def __rtruediv__(self, other: Numeric) -> MolarMass: ...
    @overload
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __rtruediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction:
        return super().__rtruediv__(other)


_register(MOLALITY, Molality)

__all__ = ["Molality"]
