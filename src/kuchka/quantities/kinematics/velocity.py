"""Velocity: a rate of change of position."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Literal
from typing import overload

from kuchka.dimensions import VELOCITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
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
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.snap import Snap
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class Velocity(LinearQuantity):
    """A rate of change of position: distance covered per unit time."""

    dimension: ClassVar[Dimension] = VELOCITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> SpecificPower: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Acceleration: ...
    @overload
    def __mul__(self, other: Area) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: DynamicViscosity) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Force) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Acceleration: ...
    @overload
    def __mul__(self, other: Impulse) -> Energy: ...
    @overload
    def __mul__(self, other: Length) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: LinearChargeDensity) -> Current: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> ElectricFieldStrength: ...
    @overload
    def __mul__(self, other: Mass) -> Momentum: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> Force: ...
    @overload
    def __mul__(self, other: Momentum) -> Energy: ...
    @overload
    def __mul__(self, other: Permeability) -> Resistance: ...
    @overload
    def __mul__(self, other: Permittivity) -> Conductance: ...
    @overload
    def __mul__(self, other: Pressure) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> Velocity: ...
    @overload
    def __mul__(self, other: SurfaceChargeDensity) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: Time) -> Length: ...
    @overload
    def __mul__(self, other: Velocity) -> VelocitySquared: ...
    @overload
    def __mul__(self, other: VolumeChargeDensity) -> CurrentDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> Velocity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Time: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Length: ...
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: Frequency) -> Length: ...
    @overload
    def __truediv__(self, other: Jerk) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: Length) -> Frequency: ...
    @overload
    def __truediv__(self, other: Proportion) -> Velocity: ...
    @overload
    def __truediv__(self, other: Snap) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: SpecificActivity) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> Volume: ...
    @overload
    def __truediv__(self, other: Time) -> Acceleration: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> Snap: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> Jerk: ...
    @overload
    def __truediv__(self, other: Velocity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Volume) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Velocity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __pow__
    @overload
    def __pow__(self, exponent: Literal[2]) -> VelocitySquared: ...
    @overload
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction:
        return super().__pow__(exponent)


_register(VELOCITY, Velocity)

__all__ = ["Velocity"]
