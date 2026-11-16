"""DynamicViscosity: how strongly a fluid resists shearing."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DYNAMIC_VISCOSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mechanics.pressure import Stress
from kuchka.quantities.temporal import Frequency
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
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
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )
    from kuchka.quantities.thermodynamics.thermal_conductivity import (
        ThermalConductivity,
    )


class DynamicViscosity(LinearQuantity):
    """How strongly a fluid resists shearing: pressure times time.

    The shear stress is the viscosity times the shear rate, so
    `DynamicViscosity * Frequency` is a `Stress`, where the shear rate is a velocity
    over a distance, `Velocity / Length`.
    `DynamicViscosity / Density` is a `KinematicViscosity`.
    """

    dimension: ClassVar[Dimension] = DYNAMIC_VISCOSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Frequency) -> Stress: ...
    @overload
    def __mul__(self, other: KinematicViscosity) -> Force: ...
    @overload
    def __mul__(self, other: Length) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> DynamicViscosity: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: SpecificHeatCapacity) -> ThermalConductivity: ...
    @overload
    def __mul__(self, other: Velocity) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> DynamicViscosity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Density) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: DynamicViscosity) -> Proportion: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Time: ...
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> Density: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: Pressure) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: Numeric) -> DynamicViscosity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DYNAMIC_VISCOSITY, DynamicViscosity)

_rule(DynamicViscosity, "*", Frequency, Stress)
_rule(Stress, "/", Frequency, DynamicViscosity)
_rule(Stress, "*", Time, DynamicViscosity)
_rule(Stress, "/", DynamicViscosity, Frequency)

__all__ = ["DynamicViscosity"]
