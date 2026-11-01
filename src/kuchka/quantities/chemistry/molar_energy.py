"""Molar energy: the energy per mole of a substance."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_ENERGY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.proportion import Proportion


class MolarEnergy(LinearQuantity):
    """The energy per mole of a substance, such as a reaction enthalpy."""

    dimension: ClassVar[Dimension] = MOLAR_ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Energy) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Energy: ...
    @overload
    def __truediv__(self, other: MolarEnergy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarEnergy: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> MolarMass: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> MolarMass: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarEnergy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MOLAR_ENERGY, MolarEnergy)

__all__ = ["MolarEnergy"]
