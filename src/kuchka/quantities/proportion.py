"""Proportion: a dimensionless quantity, expressed as a ratio or a percentage.

Reachable only by explicit construction (`Percent(5)`, `Ratio(0.05)`), the same way
`SampleRate` and `BaudRate` are:
this module never calls `_register`, so generic arithmetic between two same-dimension
quantities never silently hands back a `Proportion`.

NOTE: This is also structural, not just a choice -- `_promote` already returns a bare
`Fraction` for any dimensionless result before it consults the registry
(see its docstring), so a registration here would be dead code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import LinearQuantity

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()


__all__ = ["Proportion"]
