"""Area: a two-dimensional extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import AREA
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        ElectricFluxDensity,
    )
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.fluence import Fluence
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminance import Luminance
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity import Activity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class Area(LinearQuantity):
    """A two-dimensional extent: how much surface something covers."""

    dimension: ClassVar[Dimension] = AREA
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: CurrentDensity) -> Current: ...
    @overload
    def __mul__(self, other: ElectricFluxDensity) -> Charge: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> Force: ...
    @overload
    def __mul__(self, other: Fluence) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: HeatFlux) -> Power: ...
    @overload
    def __mul__(self, other: Illuminance) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Length) -> Volume: ...
    @overload
    def __mul__(self, other: Luminance) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: LuminousExposure) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Mass) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: Pressure) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Area: ...
    @overload
    def __mul__(self, other: SurfaceActivity) -> Activity: ...
    @overload
    def __mul__(self, other: SurfaceChargeDensity) -> Charge: ...
    @overload
    def __mul__(self, other: SurfaceTension) -> Energy: ...
    @overload
    def __mul__(self, other: Velocity) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: VolumeChargeDensity) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> Area: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Proportion: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Length: ...
    @overload
    def __truediv__(self, other: Proportion) -> Area: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: SpecificPower) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: Time) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> SpecificPower: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: Numeric) -> Area: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(AREA, Area)

__all__ = ["Area"]
