"""Density: mass per unit volume."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion


class Density(LinearQuantity):
    """Mass per unit volume: how tightly packed a material's mass is."""

    dimension: ClassVar[Dimension] = DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Density: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> Pressure: ...
    @overload
    def __mul__(self, other: Volume) -> Mass: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Numeric) -> Density: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Density: ...
    @overload
    def __truediv__(self, other: Numeric) -> Density: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DENSITY, Density)

__all__ = ["Density"]
