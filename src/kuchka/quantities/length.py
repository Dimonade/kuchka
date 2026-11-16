"""Length: a distance or a physical extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Literal
from typing import overload

from kuchka.dimensions import LENGTH
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_jerk import AngularJerk
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.angular_velocity_squared import (
        AngularVelocitySquared,
    )
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.snap import Snap
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_fourth_power import TimeFourthPower
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity_concentration import ActivityConcentration
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Length(LinearQuantity):
    """A distance or a physical extent: how far apart, how long, how wide, how far."""

    dimension: ClassVar[Dimension] = LENGTH
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: ActivityConcentration) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: AngularAcceleration) -> Acceleration: ...
    @overload
    def __mul__(self, other: AngularDisplacement) -> Length: ...
    @overload
    def __mul__(self, other: AngularJerk) -> Jerk: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Velocity: ...
    @overload
    def __mul__(self, other: AngularVelocitySquared) -> Acceleration: ...
    @overload
    def __mul__(self, other: Area) -> Volume: ...
    @overload
    def __mul__(self, other: CurrentDensity) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: DynamicViscosity) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: ElectricFieldStrength) -> Voltage: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: FirstMomentOfMass) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: Force) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> Velocity: ...
    @overload
    def __mul__(self, other: Jerk) -> SpecificPower: ...
    @overload
    def __mul__(self, other: KinematicViscosity) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Length) -> Area: ...
    @overload
    def __mul__(self, other: LinearChargeDensity) -> Charge: ...
    @overload
    def __mul__(self, other: MagneticFieldStrength) -> Current: ...
    @overload
    def __mul__(self, other: Mass) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Permeability) -> Inductance: ...
    @overload
    def __mul__(self, other: Permittivity) -> Capacitance: ...
    @overload
    def __mul__(self, other: Pressure) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: Proportion) -> Length: ...
    @overload
    def __mul__(self, other: SurfaceChargeDensity) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: SurfaceTension) -> Force: ...
    @overload
    def __mul__(self, other: Velocity) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: VolumeChargeDensity) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> Length: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Length: ...
    @overload
    def __truediv__(self, other: Jerk) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: Length) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Length: ...
    @overload
    def __truediv__(self, other: Snap) -> TimeFourthPower: ...
    @overload
    def __truediv__(self, other: Time) -> Velocity: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> Jerk: ...
    @overload
    def __truediv__(self, other: TimeFourthPower) -> Snap: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Velocity) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Length: ...
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
    def __pow__(self, exponent: Literal[2]) -> Area: ...
    @overload
    def __pow__(self, exponent: Literal[3]) -> Volume: ...
    @overload
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction:
        return super().__pow__(exponent)


_register(LENGTH, Length)

__all__ = ["Length"]
