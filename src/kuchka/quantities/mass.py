"""Mass: how much matter something contains.

Defined alongside its one relationship to `Acceleration` and `Force`
(`Mass * Acceleration -> Force`, Newton's second law).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from typing_extensions import override

from kuchka.dimensions import MASS
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics import Acceleration
    from kuchka.quantities.kinematics import Force


class Mass(LinearQuantity):
    """How much matter something contains."""

    dimension: ClassVar[Dimension] = MASS

    @overload
    def __mul__(self, other: Acceleration) -> Force: ...
    @overload
    def __mul__(self, other: Numeric) -> Mass: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)


register(MASS, Mass)

__all__ = ["Mass"]
