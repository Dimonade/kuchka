"""Molar volume: the volume that one mole of a substance occupies."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_VOLUME
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion


class MolarVolume(LinearQuantity):
    """The volume that one mole of a substance occupies: cubic metres per mole."""

    dimension: ClassVar[Dimension] = MOLAR_VOLUME
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Volume: ...
    @overload
    def __mul__(self, other: Density) -> MolarMass: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: MolarConcentration) -> Fraction: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Pressure) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarVolume: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarVolume: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Volume: ...
    @overload
    def __truediv__(self, other: MolarVolume) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarVolume: ...
    @overload
    def __truediv__(self, other: Volume) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarVolume: ...
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
    def __rtruediv__(self, other: Numeric) -> MolarConcentration: ...
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


_register(MOLAR_VOLUME, MolarVolume)

__all__ = ["MolarVolume"]
