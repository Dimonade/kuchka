"""Luminous Intensity.

The power a light source emits in a given direction, per solid angle.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINOUS_INTENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.photometry.luminance import Luminance
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.solid_angle import SolidAngle


class LuminousIntensity(LinearQuantity):
    """The power a light source emits in a given direction, per solid angle."""

    dimension: ClassVar[Dimension] = LUMINOUS_INTENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: SolidAngle) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Numeric) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Luminance: ...
    @overload
    def __truediv__(self, other: Luminance) -> Area: ...
    @overload
    def __truediv__(self, other: LuminousIntensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> LuminousIntensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> LuminousIntensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINOUS_INTENSITY, LuminousIntensity)

__all__ = ["LuminousIntensity"]
