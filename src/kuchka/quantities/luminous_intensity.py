"""Luminous Intensity.

The power a light source emits in a given direction, per solid angle.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import LUMINOUS_INTENSITY
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class LuminousIntensity(LinearQuantity):
    """The power a light source emits in a given direction, per solid angle."""

    dimension: ClassVar[Dimension] = LUMINOUS_INTENSITY
    __slots__ = ()


_register(LUMINOUS_INTENSITY, LuminousIntensity)

__all__ = ["LuminousIntensity"]
