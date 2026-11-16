"""Snap: a rate of change of jerk."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SNAP
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_fourth_power import TimeFourthPower
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Snap(LinearQuantity):
    """A rate of change of jerk, in m/s⁴, also called jounce.

        MetrePerSecondFourthPower(20) * Second(0.5)   # a Jerk of 10 m/s³

    It is the fourth derivative of a position:
    `Jerk / Time` is a `Snap`, `Snap * Time` a `Jerk`, and
    `Snap * TimeFourthPower` the `Length` a constant snap covers from rest.
    """

    dimension: ClassVar[Dimension] = SNAP
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Snap: ...
    @overload
    def __mul__(self, other: Time) -> Jerk: ...
    @overload
    def __mul__(self, other: TimeCubed) -> Velocity: ...
    @overload
    def __mul__(self, other: TimeFourthPower) -> Length: ...
    @overload
    def __mul__(self, other: TimeSquared) -> Acceleration: ...
    @overload
    def __mul__(self, other: Numeric) -> Snap: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Frequency) -> Jerk: ...
    @overload
    def __truediv__(self, other: Jerk) -> Frequency: ...
    @overload
    def __truediv__(self, other: Proportion) -> Snap: ...
    @overload
    def __truediv__(self, other: Snap) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Snap: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SNAP, Snap)

__all__ = ["Snap"]
