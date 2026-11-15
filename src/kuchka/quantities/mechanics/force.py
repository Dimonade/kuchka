"""Force: a push or a pull, the interaction that changes a mass's motion."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import FORCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
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
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Force(LinearQuantity):
    """A push or a pull: the interaction that changes a mass's motion."""

    dimension: ClassVar[Dimension] = FORCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Force: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> Jerk: ...
    @overload
    def __mul__(self, other: Time) -> Impulse: ...
    @overload
    def __mul__(self, other: TimeSquared) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Velocity) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Force: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Mass: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> Momentum: ...
    @overload
    def __truediv__(self, other: Area) -> Pressure: ...
    @overload
    def __truediv__(self, other: Charge) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: DynamicViscosity) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Charge: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Force) -> Proportion: ...
    @overload
    def __truediv__(self, other: Frequency) -> Impulse: ...
    @overload
    def __truediv__(self, other: Impulse) -> Frequency: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: Length) -> SurfaceTension: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> Voltage: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Mass) -> Acceleration: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Velocity: ...
    @overload
    def __truediv__(self, other: Momentum) -> Frequency: ...
    @overload
    def __truediv__(self, other: Pressure) -> Area: ...
    @overload
    def __truediv__(self, other: Proportion) -> Force: ...
    @overload
    def __truediv__(self, other: SurfaceTension) -> Length: ...
    @overload
    def __truediv__(self, other: Velocity) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: Voltage) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Force: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(FORCE, Force)

__all__ = ["Force"]
