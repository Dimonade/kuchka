"""Power: energy per time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import POWER
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Power(LinearQuantity):
    """The rate at which electrical energy is transferred or dissipated."""

    dimension: ClassVar[Dimension] = POWER
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: LuminousEfficacy) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> Power: ...
    @overload
    def __mul__(self, other: Time) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Power: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularVelocity) -> Torque: ...
    @overload
    def __truediv__(self, other: Current) -> Voltage: ...
    @overload
    def __truediv__(self, other: Energy) -> Frequency: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Force) -> Velocity: ...
    @overload
    def __truediv__(self, other: Frequency) -> Energy: ...
    @overload
    def __truediv__(self, other: Impulse) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Momentum) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Power) -> Proportion: ...
    @overload
    def __truediv__(self, other: Pressure) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Proportion) -> Power: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: Torque) -> AngularVelocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Force: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: Voltage) -> Current: ...
    @overload
    def __truediv__(self, other: Numeric) -> Power: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(POWER, Power)

__all__ = ["Power"]
