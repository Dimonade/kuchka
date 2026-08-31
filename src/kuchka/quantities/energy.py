"""Energy: the capacity to do work, e.g. a laser pulse's delivered energy.

Defined alongside its one relationship to `Power` and `Time` (`Power * Time -> Energy`,
and its two inverses, `Energy / Time -> Power` and `Energy / Power -> Time`).
"""

from __future__ import annotations

from typing import ClassVar
from typing import overload
from typing import TYPE_CHECKING

from kuchka.dimensions import ENERGY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from decimal import Decimal
    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.temporal import Time


class Energy(LinearQuantity):
    """The capacity to do work: a delivered or dissipated quantity of energy."""

    dimension: ClassVar[Dimension] = ENERGY

    @overload
    def __truediv__(self, other: Time) -> Power: ...
    @overload
    def __truediv__(self, other: Power) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Energy: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


register(ENERGY, Energy)
