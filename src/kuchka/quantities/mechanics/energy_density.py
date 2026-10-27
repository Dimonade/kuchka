"""Energy density: energy per unit volume.

Shares its dimension with `Pressure` (both are M L⁻¹ T⁻²), and is a different
concept: a pressure is a force on an area, and an energy density is how much energy a
volume holds.
Neither is the general kind of the dimension, so `EnergyDensity` and `Pressure` are
contested, and the operand kinds decide the result.
Any other operation that produces this dimension raises `AmbiguousKindError`, and a
`Pressure` or an `EnergyDensity` is then constructed explicitly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ENERGY_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.geometry.volume import Volume
from kuchka.quantities.mechanics.energy import Energy
from kuchka.quantities.mechanics.pressure import Pressure

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.magnetization import Magnetization
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion


class EnergyDensity(LinearQuantity):
    """Energy per unit volume: how much energy a volume of a material or store holds."""

    dimension: ClassVar[Dimension] = ENERGY_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Volume) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EnergyDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Magnetization) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Magnetization: ...
    @overload
    def __truediv__(self, other: Pressure) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> EnergyDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ENERGY_DENSITY, EnergyDensity, contested_with=Pressure)
_rule(Energy, "/", Volume, EnergyDensity)

__all__ = ["EnergyDensity"]
