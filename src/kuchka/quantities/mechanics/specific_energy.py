"""Specific energy: energy per unit mass."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.proportion import Proportion


class SpecificEnergy(LinearQuantity):
    """Energy per unit mass: what a kilogram of fuel, battery cell, or material holds.

        pack = WattHourPerKilogram(250)
        fuel = MegajoulePerKilogram(43)

    It is the quotient `Energy / Mass`, and `SpecificEnergy * Mass` is an `Energy`.
    The same dimension is the quotient `Pressure / Density` and the product
    `Acceleration * Length`, the potential energy per mass of a height.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Mass) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Proportion) -> SpecificEnergy: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Velocity) -> Velocity: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificEnergy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_ENERGY, SpecificEnergy)

__all__ = ["SpecificEnergy"]
