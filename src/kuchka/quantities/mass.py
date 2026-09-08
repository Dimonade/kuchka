"""Mass: how much matter something contains."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import MASS
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Mass(LinearQuantity):
    """How much matter something contains."""

    dimension: ClassVar[Dimension] = MASS


register(MASS, Mass)

__all__ = ["Mass"]
