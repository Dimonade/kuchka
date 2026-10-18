"""Mass: how much matter something contains.

Defined alongside two relationships:
- `Mass * Acceleration -> Force`, Newton's second law, whose other two overload
  halves live on `Acceleration` and `Force` themselves in `kinematics.py`.
- `Mass / Volume -> Density`, and its inverse `Mass / Density -> Volume`, whose
  other overload half (`Density * Volume -> Mass`) lives on `Density` and `Volume`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MASS
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.density import Density
    from kuchka.quantities.kinematics import Acceleration
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.volume import Volume


class Mass(LinearQuantity):
    """How much matter something contains."""

    dimension: ClassVar[Dimension] = MASS
    __slots__ = ()

    @overload
    def __mul__(self, other: Acceleration) -> Force: ...
    @overload
    def __mul__(self, other: Numeric) -> Mass: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Volume) -> Density: ...
    @overload
    def __truediv__(self, other: Density) -> Volume: ...
    @overload
    def __truediv__(self, other: Mass) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Mass: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MASS, Mass)

__all__ = ["Mass"]
