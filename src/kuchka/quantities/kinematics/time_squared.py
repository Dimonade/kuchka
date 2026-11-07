"""TimeSquared: a duration times a duration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import TIME_SQUARED
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class TimeSquared(LinearQuantity):
    """A duration times a duration, in seconds squared.

        fall = MetrePerSecondSquared(9.81) * Second(2) * Second(2)   # 39.24 m

    It is the square the constant-acceleration formulas are written with:
    `Acceleration * TimeSquared` is a `Length`, `Length / TimeSquared` an
    `Acceleration`, and `AngularAcceleration * TimeSquared` an `AngularDisplacement`.
    A power of a `Time` is a `TimeSquared` for the exponent 2.
    """

    dimension: ClassVar[Dimension] = TIME_SQUARED
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Length: ...
    @overload
    def __mul__(self, other: AngularAcceleration) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Force) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Frequency) -> Time: ...
    @overload
    def __mul__(self, other: Jerk) -> Velocity: ...
    @overload
    def __mul__(self, other: Proportion) -> TimeSquared: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> Area: ...
    @overload
    def __mul__(self, other: Time) -> TimeCubed: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> Area: ...
    @overload
    def __mul__(self, other: Numeric) -> TimeSquared: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Capacitance) -> Inductance: ...
    @overload
    def __truediv__(self, other: Frequency) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: Inductance) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Proportion) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: Time) -> Time: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> Frequency: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> TimeSquared: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(TIME_SQUARED, TimeSquared)

__all__ = ["TimeSquared"]
