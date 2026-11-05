"""Acceleration: a rate of change of velocity."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ACCELERATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Acceleration(LinearQuantity):
    """A rate of change of velocity: how quickly speed or direction changes."""

    dimension: ClassVar[Dimension] = ACCELERATION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: FirstMomentOfMass) -> Energy: ...
    @overload
    def __mul__(self, other: Impulse) -> Power: ...
    @overload
    def __mul__(self, other: Length) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: Mass) -> Force: ...
    @overload
    def __mul__(self, other: Momentum) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __mul__(self, other: Time) -> Velocity: ...
    @overload
    def __mul__(self, other: Velocity) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Proportion: ...
    @overload
    def __truediv__(self, other: AngularAcceleration) -> Length: ...
    @overload
    def __truediv__(self, other: Frequency) -> Velocity: ...
    @overload
    def __truediv__(self, other: Impulse) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: Momentum) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Velocity) -> Frequency: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ACCELERATION, Acceleration)

__all__ = ["Acceleration"]
