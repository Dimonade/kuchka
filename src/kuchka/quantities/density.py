"""Density: mass per unit volume.

Defined alongside its one relationship to `Mass` and `Volume` (`Mass / Volume ->
Density`, and its two inverses, `Density * Volume -> Mass` and `Mass / Density ->
Volume`), whose other overload halves live on `Mass` and `Volume` themselves.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.volume import Volume


class Density(LinearQuantity):
    """Mass per unit volume: how tightly packed a material's mass is."""

    dimension: ClassVar[Dimension] = DENSITY
    __slots__ = ()

    @overload
    def __mul__(self, other: Volume) -> Mass: ...
    @overload
    def __mul__(self, other: Numeric) -> Density: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Density: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DENSITY, Density)

__all__ = ["Density"]
