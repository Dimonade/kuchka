"""Luminous exposure: the illuminance a surface receives accumulated over time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINOUS_EXPOSURE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class LuminousExposure(LinearQuantity):
    """The illuminance a surface receives, accumulated over time."""

    dimension: ClassVar[Dimension] = LUMINOUS_EXPOSURE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: Frequency) -> Illuminance: ...
    @overload
    def __mul__(self, other: KinematicViscosity) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: Numeric) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Illuminance) -> Time: ...
    @overload
    def __truediv__(self, other: LuminousExposure) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> LuminousExposure: ...
    @overload
    def __truediv__(self, other: Time) -> Illuminance: ...
    @overload
    def __truediv__(self, other: Numeric) -> LuminousExposure: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINOUS_EXPOSURE, LuminousExposure)

__all__ = ["LuminousExposure"]
