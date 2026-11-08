"""Energy: the capacity to do work, e.g. a laser pulse's delivered energy."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ENERGY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.angular_velocity_squared import (
        AngularVelocitySquared,
    )
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class Energy(LinearQuantity):
    """The capacity to do work: a delivered or dissipated quantity of energy."""

    dimension: ClassVar[Dimension] = ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Frequency) -> Power: ...
    @overload
    def __mul__(self, other: LuminousEfficacy) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: Proportion) -> Energy: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> SpecificPower: ...
    @overload
    def __mul__(self, other: SurfaceActivity) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Numeric) -> Energy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> MolarEnergy: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Torque: ...
    @overload
    def __truediv__(self, other: AngularMomentum) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: AngularVelocity) -> AngularMomentum: ...
    @overload
    def __truediv__(self, other: AngularVelocitySquared) -> MomentOfInertia: ...
    @overload
    def __truediv__(self, other: Charge) -> Voltage: ...
    @overload
    def __truediv__(self, other: Current) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: Energy) -> Proportion: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Volume: ...
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Force) -> Length: ...
    @overload
    def __truediv__(self, other: HeatCapacity) -> TemperatureDelta: ...
    @overload
    def __truediv__(self, other: Impulse) -> Velocity: ...
    @overload
    def __truediv__(self, other: Length) -> Force: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> Current: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificEnergy: ...
    @overload
    def __truediv__(self, other: MolarEnergy) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: MomentOfInertia) -> AngularVelocitySquared: ...
    @overload
    def __truediv__(self, other: Momentum) -> Velocity: ...
    @overload
    def __truediv__(self, other: Power) -> Time: ...
    @overload
    def __truediv__(self, other: Pressure) -> Volume: ...
    @overload
    def __truediv__(self, other: Proportion) -> Energy: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> Mass: ...
    @overload
    def __truediv__(self, other: TemperatureDelta) -> HeatCapacity: ...
    @overload
    def __truediv__(self, other: Time) -> Power: ...
    @overload
    def __truediv__(self, other: Torque) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> Mass: ...
    @overload
    def __truediv__(self, other: Voltage) -> Charge: ...
    @overload
    def __truediv__(self, other: Volume) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Energy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ENERGY, Energy)

__all__ = ["Energy"]
