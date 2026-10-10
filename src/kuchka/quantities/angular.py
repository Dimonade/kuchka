"""Angle: a plane angle -- a bearing, a phase, a joint rotation.

Turn is the canonical unit.
See `kuchka.units.angular` for how Radian relates to it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import ANGLE
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Angle(ModularQuantity):
    """A plane angle: a bearing, a phase, a joint rotation."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()


_register(ANGLE, Angle)

__all__ = ["Angle"]
