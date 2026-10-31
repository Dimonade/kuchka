"""Luminous energy: the luminous flux of a source accumulated over time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINOUS_ENERGY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class LuminousEnergy(LinearQuantity):
    """The luminous flux of a source accumulated over time: flux times time."""

    dimension: ClassVar[Dimension] = LUMINOUS_ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> LuminousExposure: ...
    @overload
    def __truediv__(self, other: Energy) -> LuminousEfficacy: ...
    @overload
    def __truediv__(self, other: LuminousEfficacy) -> Energy: ...
    @overload
    def __truediv__(self, other: LuminousEnergy) -> Proportion: ...
    @overload
    def __truediv__(self, other: LuminousExposure) -> Area: ...
    @overload
    def __truediv__(self, other: LuminousFlux) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> LuminousEnergy: ...
    @overload
    def __truediv__(self, other: Time) -> LuminousFlux: ...
    @overload
    def __truediv__(self, other: Numeric) -> LuminousEnergy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINOUS_ENERGY, LuminousEnergy)

__all__ = ["LuminousEnergy"]
