"""Pressure: force per unit area.

Defined alongside two relationships:
- `Force / Area -> Pressure`, and its two inverses, `Pressure * Area -> Force` and
  `Force / Pressure -> Area`, whose other overload halves live on `Force` and
  `Area` themselves.
- `Pressure * Volume -> Energy`, the P-V work relationship, and its two inverses,
  `Energy / Pressure -> Volume` and `Energy / Volume -> Pressure`, whose other
  overload halves live on `Volume` and `Energy` themselves.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import PRESSURE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.volume import Volume


class Pressure(LinearQuantity):
    """Force per unit area: how concentrated a push or pull is over a surface."""

    dimension: ClassVar[Dimension] = PRESSURE
    __slots__ = ()

    @overload
    def __mul__(self, other: Area) -> Force: ...
    @overload
    def __mul__(self, other: Volume) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Pressure: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Pressure: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(PRESSURE, Pressure)

__all__ = ["Pressure"]
