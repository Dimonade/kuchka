"""Velocity: a rate of change of position."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VELOCITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Velocity(LinearQuantity):
    """A rate of change of position: distance covered per unit time."""

    dimension: ClassVar[Dimension] = VELOCITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Area) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Force) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Acceleration: ...
    @overload
    def __mul__(self, other: Impulse) -> Energy: ...
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
    def __mul__(self, other: Proportion) -> Velocity: ...
    @overload
    def __mul__(self, other: Time) -> Length: ...
    @overload
    def __mul__(self, other: Velocity) -> VelocitySquared: ...
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
    def __truediv__(self, other: Frequency) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Frequency: ...
    @overload
    def __truediv__(self, other: Proportion) -> Velocity: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> Volume: ...
    @overload
    def __truediv__(self, other: Time) -> Acceleration: ...
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


_register(VELOCITY, Velocity)

__all__ = ["Velocity"]
