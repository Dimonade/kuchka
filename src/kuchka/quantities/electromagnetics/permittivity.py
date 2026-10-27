"""Permittivity: how a material stores electric field energy."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import PERMITTIVITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion


class Permittivity(LinearQuantity):
    """How a material stores energy in an electric field: capacitance per length."""

    dimension: ClassVar[Dimension] = PERMITTIVITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> Capacitance: ...
    @overload
    def __mul__(self, other: Proportion) -> Permittivity: ...
    @overload
    def __mul__(self, other: Velocity) -> Conductance: ...
    @overload
    def __mul__(self, other: Numeric) -> Permittivity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Permittivity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Permittivity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Permittivity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(PERMITTIVITY, Permittivity)

__all__ = ["Permittivity"]
