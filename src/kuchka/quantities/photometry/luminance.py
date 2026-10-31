"""Luminance: the luminous intensity of a surface per unit of its area."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.solid_angle import SolidAngle


class Luminance(LinearQuantity):
    """The luminous intensity of a surface per unit area: how bright it looks."""

    dimension: ClassVar[Dimension] = LUMINANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: Proportion) -> Luminance: ...
    @overload
    def __mul__(self, other: SolidAngle) -> Illuminance: ...
    @overload
    def __mul__(self, other: Numeric) -> Luminance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Luminance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Luminance: ...
    @overload
    def __truediv__(self, other: Numeric) -> Luminance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINANCE, Luminance)

__all__ = ["Luminance"]
