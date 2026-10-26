"""Activity: how many nuclei of a radioactive source decay each second."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import FREQUENCY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.temporal import Frequency

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class Activity(LinearQuantity):
    """The decay rate of a radioactive source, in becquerel or curie.

        source = Megabecquerel(37)
        remaining = source * Percent(50)   # after one half-life

    Dimensionally identical to `Frequency`: one becquerel is one decay per second.
    It adds and subtracts with another `Activity`, scales by a plain number or a
    `Proportion`, and divides by another `Activity` into a `Proportion`.
    `to_frequency()` takes it as a `Frequency` for any other arithmetic, such as the
    number of decays over a time.
    """

    dimension: ClassVar[Dimension] = FREQUENCY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Activity: ...
    @overload
    def __mul__(self, other: Numeric) -> Activity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Activity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Activity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Activity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_frequency(self) -> Frequency:
        """View this activity as an ordinary `Frequency`, in events per second.

            Kilobecquerel(3).to_frequency() == Kilohertz(3)

        The becquerel and the hertz are both one per second, and the value is carried
        over unchanged.
        """
        return Frequency(self._magnitude, Frequency._canonical_unit)  # noqa: SLF001 -- Frequency's own canonical unit


_register(FREQUENCY, Activity, specialisation_of=Frequency)

__all__ = ["Activity"]
