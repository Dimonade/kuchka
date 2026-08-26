"""Length: a distance or a physical extent."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from kuchka.dimensions import LENGTH
from kuchka.quantities.base import LinearQuantity, register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Length(LinearQuantity):
    """A distance or a physical extent: how far apart, how long, how wide."""

    dimension: ClassVar[Dimension] = LENGTH


register(LENGTH, Length)
