"""Molar mass: the mass of one mole of a substance."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_MASS
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
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.proportion import Proportion


class MolarMass(LinearQuantity):
    """The mass of one mole of a substance: kilograms per mole."""

    dimension: ClassVar[Dimension] = MOLAR_MASS
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Mass: ...
    @overload
    def __mul__(self, other: Molality) -> Fraction: ...
    @overload
    def __mul__(self, other: MolarConcentration) -> Density: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarMass: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> MolarCharge: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarMass: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> MolarVolume: ...
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Mass: ...
    @overload
    def __truediv__(self, other: Mass) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: MolarMass) -> Proportion: ...
    @overload
    def __truediv__(self, other: MolarVolume) -> Density: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarMass: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarMass: ...
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
    def __rtruediv__(self, other: Numeric) -> Molality: ...
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


_register(MOLAR_MASS, MolarMass)

__all__ = ["MolarMass"]
