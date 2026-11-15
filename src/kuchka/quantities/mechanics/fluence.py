"""Fluence: the energy that arrives on each square metre of a surface."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SURFACE_TENSION
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.geometry.area import Area
from kuchka.quantities.mechanics.energy import Energy
from kuchka.quantities.mechanics.surface_tension import SurfaceTension
from kuchka.quantities.temporal import Time
from kuchka.quantities.thermodynamics.heat_flux import HeatFlux

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class Fluence(LinearQuantity):
    """The energy delivered to a surface, per area, in joules per square metre.

        pulse = JoulePerSquareCentimetre(2)
        day = KilowattHourPerSquareMetre(5)

    A laser fluence, a UV dose, and a daily insolation are all read this way, and a
    radiant exposure is a `Fluence`.
    `Energy / Area` is a `Fluence`, `Fluence * Area` is an `Energy`, and the flux that
    delivers it is a `HeatFlux`: `HeatFlux * Time` is a `Fluence` and `Fluence / Time`
    is a `HeatFlux`.
    It adds and subtracts with another `Fluence`, scales by a plain number or a
    `Proportion`, and divides by another `Fluence` into a `Proportion`.
    `to_surface_tension()` takes it as a `SurfaceTension` for any other arithmetic,
    and `from_surface_tension` goes the other way.
    """

    dimension: ClassVar[Dimension] = SURFACE_TENSION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Fluence: ...
    @overload
    def __mul__(self, other: Numeric) -> Fluence: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Fluence) -> Proportion: ...
    @overload
    def __truediv__(self, other: HeatFlux) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> Fluence: ...
    @overload
    def __truediv__(self, other: Time) -> HeatFlux: ...
    @overload
    def __truediv__(self, other: Numeric) -> Fluence: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_surface_tension(cls, surface_tension: SurfaceTension) -> Self:
        """Return the fluence of a `SurfaceTension` read as energy per area.

            Fluence.from_surface_tension(NewtonPerMetre(3)) == JoulePerSquareMetre(3)

        One newton per metre is one joule per square metre, and the value is carried
        over unchanged.
        """
        if not isinstance(surface_tension, SurfaceTension):
            raise IncompatibleDimensionError(
                "build a fluence from", surface_tension, surface_tension
            )
        return cls(surface_tension._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_surface_tension(self) -> SurfaceTension:
        """View this fluence as a `SurfaceTension`, in newtons per metre.

            JoulePerSquareMetre(3).to_surface_tension() * Metre(2) == Newton(6)

        One joule per square metre is one newton per metre, and the value is carried
        over unchanged.
        """
        return SurfaceTension(self._magnitude, SurfaceTension._canonical_unit)  # noqa: SLF001 -- SurfaceTension's own canonical unit


_register(SURFACE_TENSION, Fluence, specialisation_of=SurfaceTension)
_rule(Energy, "/", Area, Fluence)
_rule(Fluence, "*", Area, Energy)
_rule(Energy, "/", Fluence, Area)
_rule(HeatFlux, "*", Time, Fluence)
_rule(Fluence, "/", Time, HeatFlux)
_rule(Fluence, "/", HeatFlux, Time)

__all__ = ["Fluence"]
