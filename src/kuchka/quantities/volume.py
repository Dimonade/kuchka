"""Volume: a three-dimensional extent.

Defined as:
- `Volume / Length -> Area` and,
- `Volume / Area -> Length`, are the two inverses of
- `Length * Area -> Volume` (spelled out on `Length`), and,
-  `Area * Length -> Volume`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLUME
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from decimal import Decimal

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.length import Length


class Volume(LinearQuantity):
    """A three-dimensional extent: how much space something occupies or holds."""

    dimension: ClassVar[Dimension] = VOLUME

    @overload
    def __truediv__(self, other: Length) -> Area: ...
    @overload
    def __truediv__(self, other: Area) -> Length: ...
    @overload
    def __truediv__(self, other: Numeric) -> Volume: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Decimal: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)

    @overload
    def __mul__(self, other: Numeric) -> Volume: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Decimal: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)


register(VOLUME, Volume)

__all__ = ["Volume"]
