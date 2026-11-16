"""Specific power: power per unit mass."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class SpecificPower(LinearQuantity):
    """Power per unit mass, in watts per kilogram.

        engine = KilowattPerKilogram(2.5)
        absorbed = engine * Kilogram(80)   # a Power

    It is the quotient `Power / Mass`, and `SpecificPower * Mass` is a `Power`.
    `SpecificPower * Time` is a `SpecificEnergy`, and `SpecificEnergy / Time` is a
    `SpecificPower`.
    `Velocity * Acceleration` is one too: the power that acceleration delivers to each
    kilogram moving at that velocity.
    `AbsorbedDoseRate` is a role of it, and so is the dose rate of each radiation.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_POWER
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Mass) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Time) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: TimeCubed) -> Area: ...
    @overload
    def __mul__(self, other: TimeSquared) -> KinematicViscosity: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificPower: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Velocity: ...
    @overload
    def __truediv__(self, other: Energy) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: HeatingRate) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: Jerk) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Jerk: ...
    @overload
    def __truediv__(self, other: Proportion) -> SpecificPower: ...
    @overload
    def __truediv__(self, other: SpecificActivity) -> Energy: ...
    @overload
    def __truediv__(self, other: SpecificCurrent) -> Voltage: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> Frequency: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> HeatingRate: ...
    @overload
    def __truediv__(self, other: SpecificPower) -> Proportion: ...
    @overload
    def __truediv__(self, other: Velocity) -> Acceleration: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> Frequency: ...
    @overload
    def __truediv__(self, other: Voltage) -> SpecificCurrent: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificPower: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_POWER, SpecificPower)
_rule(SpecificPower, "*", Time, SpecificEnergy)

__all__ = ["SpecificPower"]
