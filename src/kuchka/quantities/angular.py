"""Angle: a plane angle -- a bearing, a phase, a joint rotation.

Radian is the SI-coherent unit for plane angle.
Internal storage uses turns as the exact rational frame: one full turn is
`Fraction(1)`.
`Degree`, `Turn`, `Gradian`, `ArcMinute`, and `ArcSecond` are each an exact rational
fraction of a turn, so every one of them is exact end to end, including `.to()` between
any pair of them.

`Radian` needs pi, which has no exact rational representation.
There is no `UnitDef` for it: a `UnitDef.scale` is always an exact `Fraction`, and no
`Fraction` equals pi.
NOTE: `kuchka.units.angular.Radian` currently raises `PlannedDimensionError`
unconditionally.

`to_lossy()` is the one approximate operation on `Angle`.
It materializes the exact turn-count into a `Decimal` count of radians.
Every other operation on `Angle`, including `.to()`, stays exact.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import ANGLE
from kuchka.numeric import to_decimal
from kuchka.quantities.base import ModularQuantity

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

_TWO_PI = Decimal("6.283185307179586")
"""Two pi to 15 significant digits.

Used only by `Angle.to_lossy`.
"""


class Angle(ModularQuantity):
    """A plane angle: a bearing, a phase, a joint rotation."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()

    def to_lossy(self) -> Decimal:
        """Materialize this angle as an approximate Decimal count of radians.

        Multiplies the exact turn-count by a fixed 15-digit approximation of two pi.
        Not exact: pi has no exact rational representation.
        The one approximate operation on `Angle`.
        """
        return to_decimal(self._magnitude) * _TWO_PI


__all__ = ["Angle"]
