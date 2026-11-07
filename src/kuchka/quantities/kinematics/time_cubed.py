"""TimeCubed: a duration times a duration times a duration."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import TIME_CUBED
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class TimeCubed(LinearQuantity):
    """A duration cubed, in seconds cubed.

        MetrePerSecondCubed(50) * Second(2) * Second(2) * Second(2)   # 400 m

    It is the cube the constant-jerk formulas are written with, `j * t³ / 6`:
    `Jerk * TimeCubed` is a `Length`, and `Length / TimeCubed` and
    `Velocity / TimeSquared` are a `Jerk`.
    A power of a `Time` is a `TimeCubed` for the exponent 3.
    """

    dimension: ClassVar[Dimension] = TIME_CUBED
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> TimeSquared: ...
    @overload
    def __mul__(self, other: Jerk) -> Length: ...
    @overload
    def __mul__(self, other: Proportion) -> TimeCubed: ...
    @overload
    def __mul__(self, other: SpecificPower) -> Area: ...
    @overload
    def __mul__(self, other: Numeric) -> TimeCubed: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> TimeCubed: ...
    @overload
    def __truediv__(self, other: Time) -> TimeSquared: ...
    @overload
    def __truediv__(self, other: TimeCubed) -> Proportion: ...
    @overload
    def __truediv__(self, other: TimeSquared) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> TimeCubed: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(TIME_CUBED, TimeCubed)

__all__ = ["TimeCubed"]
