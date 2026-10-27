"""Permeability: how a material supports a magnetic field."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import PERMEABILITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion


class Permeability(LinearQuantity):
    """How a material supports a magnetic field: inductance per length."""

    dimension: ClassVar[Dimension] = PERMEABILITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Inductance: ...
    @overload
    def __mul__(self, other: Proportion) -> Permeability: ...
    @overload
    def __mul__(self, other: Velocity) -> Resistance: ...
    @overload
    def __mul__(self, other: Numeric) -> Permeability: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Permeability) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Permeability: ...
    @overload
    def __truediv__(self, other: Numeric) -> Permeability: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(PERMEABILITY, Permeability)

__all__ = ["Permeability"]
