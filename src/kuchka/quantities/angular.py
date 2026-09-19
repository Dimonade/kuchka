"""Angle: a plane angle -- a bearing, a phase, a joint rotation.

Radian is the canonical unit: the SI-coherent unit for plane angle.
See `kuchka.units.angular` for how kuchka represents pi and what that means for
comparing a `Radian`-built value against the rest of the family.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import ANGLE
from kuchka.quantities.base import ModularQuantity

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Angle(ModularQuantity):
    """A plane angle: a bearing, a phase, a joint rotation."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()


__all__ = ["Angle"]
