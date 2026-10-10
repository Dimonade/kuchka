"""Proportion: a dimensionless quantity, expressed as a ratio or a percentage.

Reachable only by explicit construction (`Percent(5)`, `Ratio(0.05)`):
generic arithmetic that cancels every dimension returns a plain `Fraction`, so
`Proportion` is registered as a kind of the dimensionless dimension and is never an
arithmetic result.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()


_register(DIMENSIONLESS, Proportion)

__all__ = ["Proportion"]
