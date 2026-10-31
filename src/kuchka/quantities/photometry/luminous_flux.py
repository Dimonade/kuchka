"""Luminous flux: the light a source emits in all directions, as the eye sees it."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINOUS_FLUX
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.solid_angle import SolidAngle
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class LuminousFlux(LinearQuantity):
    """The light a source emits as the eye sees it: intensity times solid angle."""

    dimension: ClassVar[Dimension] = LUMINOUS_FLUX
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Time) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Illuminance: ...
    @overload
    def __truediv__(self, other: Frequency) -> LuminousEnergy: ...
    @overload
    def __truediv__(self, other: Illuminance) -> Area: ...
    @overload
    def __truediv__(self, other: LuminousEfficacy) -> Power: ...
    @overload
    def __truediv__(self, other: LuminousEnergy) -> Frequency: ...
    @overload
    def __truediv__(self, other: LuminousFlux) -> Proportion: ...
    @overload
    def __truediv__(self, other: LuminousIntensity) -> SolidAngle: ...
    @overload
    def __truediv__(self, other: Power) -> LuminousEfficacy: ...
    @overload
    def __truediv__(self, other: Proportion) -> LuminousFlux: ...
    @overload
    def __truediv__(self, other: SolidAngle) -> LuminousIntensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> LuminousFlux: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINOUS_FLUX, LuminousFlux)

__all__ = ["LuminousFlux"]
