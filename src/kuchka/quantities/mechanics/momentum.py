"""Momentum: the mass of a moving body times its velocity."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOMENTUM
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
from kuchka.quantities.kinematics.velocity import Velocity
from kuchka.quantities.mass import Mass
from kuchka.quantities.mechanics.force import Force

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Momentum(LinearQuantity):
    """The momentum of a moving body: its mass times its velocity.

        cart = Kilogram(2) * MetrePerSecond(3)   # 6 kg·m/s
        energy = Kilogram(2) * speed * speed / 2

    `Mass * Velocity` is a `Momentum`, and `Momentum * Velocity` an `Energy`, so a
    kinetic energy is written without brackets.
    `Momentum / Mass` is a `Velocity` and `Momentum / Time` a `Force`.
    A body turning at an angular velocity needs the centripetal force
    `AngularVelocity * Momentum`.
    The impulse that gives a body its momentum is an `Impulse`, which shares the
    dimension: see `Impulse.from_momentum`.
    """

    dimension: ClassVar[Dimension] = MOMENTUM
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Power: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> Force: ...
    @overload
    def __mul__(self, other: Frequency) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Momentum: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> Acceleration: ...
    @overload
    def __mul__(self, other: Time) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Velocity) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Momentum: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularVelocity) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: Area) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: DynamicViscosity) -> Area: ...
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> Frequency: ...
    @overload
    def __truediv__(self, other: Force) -> Time: ...
    @overload
    def __truediv__(self, other: Frequency) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: Impulse) -> Proportion: ...
    @overload
    def __truediv__(self, other: Length) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: Mass) -> Velocity: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Length: ...
    @overload
    def __truediv__(self, other: Momentum) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Momentum: ...
    @overload
    def __truediv__(self, other: Time) -> Force: ...
    @overload
    def __truediv__(self, other: Velocity) -> Mass: ...
    @overload
    def __truediv__(self, other: Numeric) -> Momentum: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MOMENTUM, Momentum)
_rule(Mass, "*", Velocity, Momentum)
_bridge(AngularVelocity, "*", Momentum, Force)
_bridge(Force, "/", AngularVelocity, Momentum)

__all__ = ["Momentum"]
