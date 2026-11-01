"""Molar flow rate: the amount of substance that passes a section per unit of time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.current import Current
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class MolarFlowRate(LinearQuantity):
    """The amount of substance that passes a section per unit of time."""

    dimension: ClassVar[Dimension] = MOLAR_FLOW_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> Frequency: ...
    @overload
    def __mul__(self, other: MolarCharge) -> Current: ...
    @overload
    def __mul__(self, other: MolarEnergy) -> Power: ...
    @overload
    def __mul__(self, other: MolarMass) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: MolarVolume) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: Time) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> Frequency: ...
    @overload
    def __truediv__(self, other: Frequency) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Molality: ...
    @overload
    def __truediv__(self, other: Molality) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: MolarConcentration) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> MolarConcentration: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarFlowRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MOLAR_FLOW_RATE, MolarFlowRate)

__all__ = ["MolarFlowRate"]
