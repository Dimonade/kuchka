"""SolidAngle: the extent of a cone of directions, measured in steradians.

`SolidAngle` has an axis of its own, so a steradian is neither a plain number nor the
square of a plane angle.
SI writes it as a square metre per square metre, which cancels: in `kuchka`,
`Area / Area` is a `Proportion`, and a solid angle comes from a constructor or from
`SolidAngle.from_area(area, radius)`, which names the sphere the area lies on.

The steradian is the canonical unit.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import AREA
from kuchka.dimensions import LENGTH
from kuchka.dimensions import SOLID_ANGLE
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.length import Length
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.proportion import Proportion


class SolidAngle(LinearQuantity):
    """The extent of a cone of directions: the area it cuts from a sphere over r²."""

    dimension: ClassVar[Dimension] = SOLID_ANGLE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: LuminousIntensity) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: Proportion) -> SolidAngle: ...
    @overload
    def __mul__(self, other: Numeric) -> SolidAngle: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SolidAngle: ...
    @overload
    def __truediv__(self, other: SolidAngle) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SolidAngle: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_area(cls, area: Area, radius: Length) -> Self:
        """Return the solid angle an area on a sphere of a given radius subtends.

            SolidAngle.from_area(SquareMetre(2), Metre(2)) == Steradian(0.5)

        The area is measured on the surface of the sphere, and the radius is the
        distance from the sphere's centre to that surface.

        Raises
        ------
        IncompatibleDimensionError
            If `area` is not an area or `radius` is not a length.
        InvalidMeasurementError
            If the radius is not positive.

        """
        if getattr(area, "dimension", None) != AREA:
            raise IncompatibleDimensionError("build a solid angle from", area, radius)
        if getattr(radius, "dimension", None) != LENGTH:
            raise IncompatibleDimensionError("build a solid angle from", area, radius)
        if radius._magnitude <= 0:  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes
            msg = f"a sphere has a positive radius, got {radius}"
            raise InvalidMeasurementError(msg)
        return cls(area._magnitude / radius._magnitude**2, cls._canonical_unit)  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes


_register(SOLID_ANGLE, SolidAngle)

__all__ = ["SolidAngle"]
