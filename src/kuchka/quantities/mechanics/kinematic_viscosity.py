"""KinematicViscosity: a fluid's viscosity per density."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import KINEMATIC_VISCOSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class KinematicViscosity(LinearQuantity):
    """A fluid's viscosity per density, in square metres per second.

    `DynamicViscosity / Density` is a `KinematicViscosity`, and so is
    `Velocity * Length`, so the Reynolds number `v * L / nu` is a `Proportion`.
    A thermal diffusivity and a diffusion coefficient are measured in the same square
    metres per second, and read as a `KinematicViscosity` too.
    """

    dimension: ClassVar[Dimension] = KINEMATIC_VISCOSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Density) -> DynamicViscosity: ...
    @overload
    def __mul__(self, other: DynamicViscosity) -> Force: ...
    @overload
    def __mul__(self, other: Length) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: LuminousExposure) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> Voltage: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: SurfaceChargeDensity) -> Current: ...
    @overload
    def __mul__(self, other: SurfaceTension) -> Power: ...
    @overload
    def __mul__(self, other: Time) -> Area: ...
    @overload
    def __mul__(self, other: VolumeChargeDensity) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Numeric) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Frequency: ...
    @overload
    def __truediv__(self, other: Frequency) -> Area: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Length) -> Velocity: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: Proportion) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> Time: ...
    @overload
    def __truediv__(self, other: SpecificPower) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> SpecificPower: ...
    @overload
    def __truediv__(self, other: Velocity) -> Length: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> KinematicViscosity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(KINEMATIC_VISCOSITY, KinematicViscosity)

__all__ = ["KinematicViscosity"]
