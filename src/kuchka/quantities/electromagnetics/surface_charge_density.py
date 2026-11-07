"""SurfaceChargeDensity: the electric charge on a surface: charge per area."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SURFACE_CHARGE_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion


class SurfaceChargeDensity(LinearQuantity):
    """The electric charge on a surface: charge per area.

    An electric flux density and a polarization density are measured in the same
    coulombs per square metre.
    """

    dimension: ClassVar[Dimension] = SURFACE_CHARGE_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Charge: ...
    @overload
    def __mul__(self, other: Length) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: Resistance) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Velocity) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Numeric) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Conductance) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Length) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Conductance: ...
    @overload
    def __truediv__(self, other: Proportion) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> Length: ...
    @overload
    def __truediv__(self, other: Numeric) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SURFACE_CHARGE_DENSITY, SurfaceChargeDensity)

__all__ = ["SurfaceChargeDensity"]
