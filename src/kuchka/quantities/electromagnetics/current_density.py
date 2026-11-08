"""CurrentDensity: electric current through an area."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CURRENT_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class CurrentDensity(LinearQuantity):
    """The electric current through a unit area, J: current per area.

    `CurrentDensity * Area` is a `Current`, and `VolumeChargeDensity * Velocity` is a
    `CurrentDensity`, the convective current `J = rho * v`.
    `MagneticFieldStrength / Length` is a `CurrentDensity`, the circulation of
    Ampère's law per area.
    """

    dimension: ClassVar[Dimension] = CURRENT_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Current: ...
    @overload
    def __mul__(self, other: Inductance) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Length) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Proportion) -> CurrentDensity: ...
    @overload
    def __mul__(self, other: Time) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: Voltage) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Numeric) -> CurrentDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Charge) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: CurrentDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: Proportion) -> CurrentDensity: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> Charge: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Frequency: ...
    @overload
    def __truediv__(self, other: Velocity) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> Velocity: ...
    @overload
    def __truediv__(self, other: Numeric) -> CurrentDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CURRENT_DENSITY, CurrentDensity)

__all__ = ["CurrentDensity"]
