"""Luminous efficacy: the luminous flux a source gives per watt it consumes."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import LUMINOUS_EFFICACY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class LuminousEfficacy(LinearQuantity):
    """The luminous flux a source gives per watt: lumens per watt."""

    dimension: ClassVar[Dimension] = LUMINOUS_EFFICACY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Energy) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: HeatFlux) -> Illuminance: ...
    @overload
    def __mul__(self, other: Power) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> LuminousEfficacy: ...
    @overload
    def __mul__(self, other: Numeric) -> LuminousEfficacy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: LuminousEfficacy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> LuminousEfficacy: ...
    @overload
    def __truediv__(self, other: Numeric) -> LuminousEfficacy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(LUMINOUS_EFFICACY, LuminousEfficacy)

__all__ = ["LuminousEfficacy"]
