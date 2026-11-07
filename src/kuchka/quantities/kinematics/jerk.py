"""Jerk: a rate of change of acceleration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import JERK
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_jerk import AngularJerk
    from kuchka.quantities.kinematics.snap import Snap
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Jerk(LinearQuantity):
    """A rate of change of acceleration, in metres per second cubed, also called jolt.

        MetrePerSecondCubed(50) * Second(0.2)   # an Acceleration of 10 m/s²

    A motion profile limits it to keep a drive smooth:
    `Acceleration / Time` is a `Jerk`, `Jerk * Time` an `Acceleration`, and
    `Jerk * TimeCubed` the `Length` a constant jerk covers from rest.
    """

    dimension: ClassVar[Dimension] = JERK
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: FirstMomentOfMass) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Snap: ...
    @overload
    def __mul__(self, other: Length) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Proportion) -> Jerk: ...
    @overload
    def __mul__(self, other: Time) -> Acceleration: ...
    @overload
    def __mul__(self, other: TimeCubed) -> Length: ...
    @overload
    def __mul__(self, other: TimeSquared) -> Velocity: ...
    @overload
    def __mul__(self, other: Numeric) -> Jerk: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Frequency: ...
    @overload
    def __truediv__(self, other: AngularJerk) -> Length: ...
    @overload
    def __truediv__(self, other: Force) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: Frequency) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Jerk) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Jerk: ...
    @overload
    def __truediv__(self, other: Snap) -> Time: ...
    @overload
    def __truediv__(self, other: SpecificActivity) -> Force: ...
    @overload
    def __truediv__(self, other: Time) -> Snap: ...
    @overload
    def __truediv__(self, other: Numeric) -> Jerk: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(JERK, Jerk)

__all__ = ["Jerk"]
