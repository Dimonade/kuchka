"""Molar concentration: the amount of a solute per volume of solution."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_CONCENTRATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion


class MolarConcentration(LinearQuantity):
    """The amount of a solute per volume of solution, called molarity: mol/L."""

    dimension: ClassVar[Dimension] = MOLAR_CONCENTRATION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: MolarMass) -> Density: ...
    @overload
    def __mul__(self, other: MolarVolume) -> Fraction: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarConcentration: ...
    @overload
    def __mul__(self, other: Volume) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarConcentration: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> Molality: ...
    @overload
    def __truediv__(self, other: Molality) -> Density: ...
    @overload
    def __truediv__(self, other: MolarConcentration) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarConcentration: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarConcentration: ...
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
    def __rtruediv__(self, other: Numeric) -> MolarVolume: ...
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


_register(MOLAR_CONCENTRATION, MolarConcentration)

__all__ = ["MolarConcentration"]
