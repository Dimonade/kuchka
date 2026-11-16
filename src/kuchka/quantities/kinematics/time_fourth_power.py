"""TimeFourthPower: a duration to the fourth power."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import TIME_FOURTH_POWER
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.snap import Snap
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class TimeFourthPower(LinearQuantity):
    """A duration to the fourth power, in seconds to the fourth power.

        Second(2) * Second(2) * Second(2) * Second(2)   # 16 s⁴

    It is the fourth power the constant-snap formulas are written with, `s * t⁴ / 24`:
    `Snap * TimeFourthPower` is a `Length`, and `Length / TimeFourthPower` is a `Snap`.
    A power of a `Time` is a `TimeFourthPower` for the exponent 4.
    """

    dimension: ClassVar[Dimension] = TIME_FOURTH_POWER
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> TimeCubed: ...
    @overload
    def __mul__(self, other: Proportion) -> TimeFourthPower: ...
    @overload
    def __mul__(self, other: Snap) -> Length: ...
    @overload
    def __mul__(self, other: Numeric) -> TimeFourthPower: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> TimeFourthPower: ...
    @overload
    def __truediv__(self, other: Time) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> Time: ...
    @overload
    def __truediv__(self, other: TimeFourthPower) -> Proportion: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: Numeric) -> TimeFourthPower: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(TIME_FOURTH_POWER, TimeFourthPower)

__all__ = ["TimeFourthPower"]
