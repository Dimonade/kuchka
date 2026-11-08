"""Surface charge density and electric flux density: two readings of a C/m².

`ElectricFluxDensity` is a role of `SurfaceChargeDensity`: the same dimension, read as
the displacement field D and not as the charge sitting on a surface.
"""

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
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
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
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class SurfaceChargeDensity(LinearQuantity):
    """The electric charge on a surface: charge per area.

    A polarization density reads as a `SurfaceChargeDensity` too.
    `to_electric_flux_density()` reads it as an `ElectricFluxDensity`.
    """

    dimension: ClassVar[Dimension] = SURFACE_CHARGE_DENSITY
    __slots__ = ()

    def to_electric_flux_density(self) -> ElectricFluxDensity:
        """View this surface charge density as an `ElectricFluxDensity`.

        The unit it displays in carries over, and
        `ElectricFluxDensity.to_surface_charge_density()` takes the value back.
        """
        return ElectricFluxDensity(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Charge: ...
    @overload
    def __mul__(self, other: Frequency) -> CurrentDensity: ...
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
    def __truediv__(self, other: CurrentDensity) -> Time: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Permittivity: ...
    @overload
    def __truediv__(self, other: Length) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Conductance: ...
    @overload
    def __truediv__(self, other: Permittivity) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: Proportion) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Time) -> CurrentDensity: ...
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


class ElectricFluxDensity(LinearQuantity):
    """The electric displacement field, D: free charge per area, as `D = εE`.

    `Permittivity * ElectricFieldStrength` is an `ElectricFluxDensity`, and
    `ElectricFluxDensity * Area` is the `Charge` the flux of D encloses.
    `to_surface_charge_density()` takes it as a `SurfaceChargeDensity`, to add it to a
    charge density or to divide it by a time.
    """

    dimension: ClassVar[Dimension] = SURFACE_CHARGE_DENSITY
    __slots__ = ()

    def to_surface_charge_density(self) -> SurfaceChargeDensity:
        """View this electric flux density as a `SurfaceChargeDensity`.

        The unit it displays in carries over, and
        `SurfaceChargeDensity.to_electric_flux_density()` takes the value back.
        """
        return SurfaceChargeDensity(self._magnitude, self._display_unit)

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Charge: ...
    @overload
    def __mul__(self, other: ElectricFieldStrength) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> ElectricFluxDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> ElectricFluxDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Permittivity: ...
    @overload
    def __truediv__(self, other: ElectricFluxDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Permittivity) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: Proportion) -> ElectricFluxDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> ElectricFluxDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SURFACE_CHARGE_DENSITY, SurfaceChargeDensity)
_register(
    SURFACE_CHARGE_DENSITY, ElectricFluxDensity, specialisation_of=SurfaceChargeDensity
)

__all__ = ["ElectricFluxDensity", "SurfaceChargeDensity"]
