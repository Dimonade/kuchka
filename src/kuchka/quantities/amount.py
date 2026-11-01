"""Amount Of Substance: a count of elementary entities, expressed in moles."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import AMOUNT_OF_SUBSTANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class AmountOfSubstance(LinearQuantity):
    """A count of elementary entities, expressed in moles."""

    dimension: ClassVar[Dimension] = AMOUNT_OF_SUBSTANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> Fraction: ...
    @overload
    def __mul__(self, other: Frequency) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: MolarCharge) -> Charge: ...
    @overload
    def __mul__(self, other: MolarEnergy) -> Energy: ...
    @overload
    def __mul__(self, other: MolarMass) -> Mass: ...
    @overload
    def __mul__(self, other: MolarVolume) -> Volume: ...
    @overload
    def __mul__(self, other: Proportion) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: Numeric) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Mass) -> Molality: ...
    @overload
    def __truediv__(self, other: Molality) -> Mass: ...
    @overload
    def __truediv__(self, other: MolarConcentration) -> Volume: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Time) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: Volume) -> MolarConcentration: ...
    @overload
    def __truediv__(self, other: Numeric) -> AmountOfSubstance: ...
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
    def __rtruediv__(self, other: Numeric) -> EntitiesPerAmount: ...
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


_register(AMOUNT_OF_SUBSTANCE, AmountOfSubstance)

__all__ = ["AmountOfSubstance"]
