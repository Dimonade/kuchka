"""Volume: a three-dimensional extent.

Defined as:
- `Volume / Length -> Area` and,
- `Volume / Area -> Length`, are the two inverses of
- `Length * Area -> Volume` (spelled out on `Length`), and,
-  `Area * Length -> Volume`.

Also carries the other overload halves of two relationships defined on their own types:
- `Volume * Density -> Mass` (see `Density`) and
- `Volume * Pressure -> Energy` (see `Pressure`),
the P-V work relationship, alongside its inverse `Energy / Volume -> Pressure`
(see `Energy`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLUME
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.density import Density
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.pressure import Pressure


class Volume(LinearQuantity):
    """A three-dimensional extent: how much space something occupies or holds."""

    dimension: ClassVar[Dimension] = VOLUME
    __slots__ = ()

    @overload
    def __truediv__(self, other: Length) -> Area: ...
    @overload
    def __truediv__(self, other: Area) -> Length: ...
    @overload
    def __truediv__(self, other: Numeric) -> Volume: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @overload
    def __mul__(self, other: Density) -> Mass: ...
    @overload
    def __mul__(self, other: Pressure) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Volume: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)


_register(VOLUME, Volume)

__all__ = ["Volume"]
