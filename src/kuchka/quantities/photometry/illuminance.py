"""Illuminance: the luminous flux that falls on a surface, per unit area."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ILLUMINANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.photometry.luminance import Luminance
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.solid_angle import SolidAngle
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class Illuminance(LinearQuantity):
    """The luminous flux that falls on a surface, per unit area."""

    dimension: ClassVar[Dimension] = ILLUMINANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> Illuminance: ...
    @overload
    def __mul__(self, other: Time) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: Numeric) -> Illuminance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Frequency) -> LuminousExposure: ...
    @overload
    def __truediv__(self, other: HeatFlux) -> LuminousEfficacy: ...
    @overload
    def __truediv__(self, other: Illuminance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Luminance) -> SolidAngle: ...
    @overload
    def __truediv__(self, other: LuminousEfficacy) -> HeatFlux: ...
    @overload
    def __truediv__(self, other: LuminousEnergy) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: LuminousExposure) -> Frequency: ...
    @overload
    def __truediv__(self, other: Proportion) -> Illuminance: ...
    @overload
    def __truediv__(self, other: SolidAngle) -> Luminance: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> LuminousEnergy: ...
    @overload
    def __truediv__(self, other: Numeric) -> Illuminance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ILLUMINANCE, Illuminance)

__all__ = ["Illuminance"]
