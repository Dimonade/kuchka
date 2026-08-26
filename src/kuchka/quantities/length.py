"""Length: the one L^1 quantity in the vocabulary so far.

Nothing else here is dimensionally coupled to `Length` yet, unlike
`Voltage`/`Current`/`Power`/`Resistance` (coupled by Ohm's law and the
power triangle) or `Time`/`Frequency` (coupled by being reciprocals).
That is why `Length` lives alone in its own module rather than being
folded into an existing one: the file boundary in this package follows
which types are statically coupled through `@overload` tables, not which
types happen to share a dimension family.

`Length / Time -> Velocity` is a real, named, physically obvious relation,
and is deliberately not implemented yet. Dividing a `Length` by a `Time`
today raises `PlannedDimensionError`, a more specific
`UnrepresentableDimensionError`, rather than a generic scope-boundary
message, precisely because this is not an accident of scope the way
`Resistance * Resistance` is -- it is the nearest planned extension to
this module, tracked in `_PLANNED_DIMENSIONS` in `base.py`.
"""

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
