"""Entities per amount: how many atoms or molecules make up an amount of substance."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ENTITIES_PER_AMOUNT
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarEntropy
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarHeatCapacity
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.thermodynamics.heat_capacity import Entropy
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity


class EntitiesPerAmount(LinearQuantity):
    """The number of elementary entities per amount of substance: reciprocal moles."""

    dimension: ClassVar[Dimension] = ENTITIES_PER_AMOUNT
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Fraction: ...
    @overload
    def __mul__(self, other: Charge) -> MolarCharge: ...
    @overload
    def __mul__(self, other: Energy) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Entropy) -> MolarEntropy: ...
    @overload
    def __mul__(self, other: HeatCapacity) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: Mass) -> MolarMass: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> Frequency: ...
    @overload
    def __mul__(self, other: Proportion) -> EntitiesPerAmount: ...
    @overload
    def __mul__(self, other: Volume) -> MolarVolume: ...
    @overload
    def __mul__(self, other: Numeric) -> EntitiesPerAmount: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: Numeric) -> EntitiesPerAmount: ...
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
    def __rtruediv__(self, other: Numeric) -> AmountOfSubstance: ...
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


_register(ENTITIES_PER_AMOUNT, EntitiesPerAmount)

__all__ = ["EntitiesPerAmount"]
