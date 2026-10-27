"""Magnetic flux density: the strength of a magnetic field."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MAGNETIC_FLUX_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.proportion import Proportion


class MagneticFluxDensity(LinearQuantity):
    """The strength of a magnetic field: the flux per unit area through a surface."""

    dimension: ClassVar[Dimension] = MAGNETIC_FLUX_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Numeric) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MAGNETIC_FLUX_DENSITY, MagneticFluxDensity)

__all__ = ["MagneticFluxDensity"]
