"""VolumeChargeDensity: the electric charge in a volume: charge per volume."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLUME_CHARGE_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion


class VolumeChargeDensity(LinearQuantity):
    """The electric charge in a volume: charge per volume."""

    dimension: ClassVar[Dimension] = VOLUME_CHARGE_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: Length) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: MolarVolume) -> MolarCharge: ...
    @overload
    def __mul__(self, other: Proportion) -> VolumeChargeDensity: ...
    @overload
    def __mul__(self, other: Volume) -> Charge: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> Current: ...
    @overload
    def __mul__(self, other: Numeric) -> VolumeChargeDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: MolarCharge) -> MolarConcentration: ...
    @overload
    def __truediv__(self, other: MolarConcentration) -> MolarCharge: ...
    @overload
    def __truediv__(self, other: Proportion) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> Density: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(VOLUME_CHARGE_DENSITY, VolumeChargeDensity)

__all__ = ["VolumeChargeDensity"]
