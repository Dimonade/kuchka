"""Volume: a three-dimensional extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLUME
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Volume(LinearQuantity):
    """A three-dimensional extent: how much space something occupies or holds."""

    dimension: ClassVar[Dimension] = VOLUME
    __slots__ = ()

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Area: ...
    @overload
    def __truediv__(self, other: Proportion) -> Volume: ...
    @overload
    def __truediv__(self, other: Time) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Volume) -> Proportion: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Volume: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Density) -> Mass: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Pressure) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Volume: ...
    @overload
    def __mul__(self, other: Numeric) -> Volume: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)


_register(VOLUME, Volume)

__all__ = ["Volume"]
