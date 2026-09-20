"""Energy: the capacity to do work, e.g. a laser pulse's delivered energy.

Defined alongside two relationships:
- `Power * Time -> Energy`, and its two inverses, `Energy / Time -> Power` and
  `Energy / Power -> Time`.
- `Pressure * Volume -> Energy`, the P-V work relationship, and its two inverses,
  `Energy / Pressure -> Volume` and `Energy / Volume -> Pressure`, whose other
  overload halves live on `Pressure` and `Volume` themselves.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from typing_extensions import override

from kuchka.dimensions import ENERGY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.pressure import Pressure
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.volume import Volume


class Energy(LinearQuantity):
    """The capacity to do work: a delivered or dissipated quantity of energy."""

    dimension: ClassVar[Dimension] = ENERGY

    @overload
    def __truediv__(self, other: Time) -> Power: ...
    @overload
    def __truediv__(self, other: Power) -> Time: ...
    @overload
    def __truediv__(self, other: Pressure) -> Volume: ...
    @overload
    def __truediv__(self, other: Volume) -> Pressure: ...
    @overload
    def __truediv__(self, other: Numeric) -> Energy: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


register(ENERGY, Energy)

__all__ = ["Energy"]
