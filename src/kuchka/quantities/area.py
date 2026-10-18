"""Area: a two-dimensional extent.

Defined alongside its relationships to `Length` and `Volume`:
- `Length * Length -> Area`, its inverse,
- `Area / Length -> Length`, and
- `Area * Length -> Volume`, and its inverse,
- `Volume / Area -> Length`.

The other halves defined and derived on `Length` and `Volume` accordingly.

Also carries the other overload half of `Area * Pressure -> Force` (see `Pressure`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import AREA
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.energy_density import EnergyDensity
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.length import Length
    from kuchka.quantities.pressure import Pressure
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.volume import Volume


class Area(LinearQuantity):
    """A two-dimensional extent: how much surface something covers."""

    dimension: ClassVar[Dimension] = AREA
    __slots__ = ()

    @overload
    def __mul__(self, other: Length) -> Volume: ...
    @overload
    def __mul__(self, other: Pressure) -> Force: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> Force: ...
    @overload
    def __mul__(self, other: Numeric) -> Area: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Length) -> Length: ...
    @overload
    def __truediv__(self, other: Area) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Area: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(AREA, Area)

__all__ = ["Area"]
