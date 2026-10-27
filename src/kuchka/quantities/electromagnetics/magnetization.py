"""Magnetization: the magnetising field, in current per length."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MAGNETIZATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion


class Magnetization(LinearQuantity):
    """The magnetising field applied to a medium: current per length."""

    dimension: ClassVar[Dimension] = MAGNETIZATION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Current: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> Force: ...
    @overload
    def __mul__(self, other: Permeability) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> Magnetization: ...
    @overload
    def __mul__(self, other: Numeric) -> Magnetization: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Magnetization) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Magnetization: ...
    @overload
    def __truediv__(self, other: Numeric) -> Magnetization: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MAGNETIZATION, Magnetization)

__all__ = ["Magnetization"]
