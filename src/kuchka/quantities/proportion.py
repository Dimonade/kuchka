"""Proportion: a dimensionless quantity, expressed as a ratio or a percentage.

Reachable only by explicit construction (`Percent(5)`, `Ratio(0.05)`), the same way
`SampleRate` and `BaudRate` are:
this module never calls `register`, so generic arithmetic between two same-dimension
quantities never silently hands back a `Proportion`.

Unlike `SampleRate`/`BaudRate`, this is also structural rather than a choice --
`_promote` already returns a bare `Decimal` for any dimensionless result before it ever
consults the registry (see its docstring), so a registration here would be dead code
regardless.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import LinearQuantity

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
