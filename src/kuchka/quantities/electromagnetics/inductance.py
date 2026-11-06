"""Inductance: the magnetic flux a circuit links per ampere."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import INDUCTANCE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.length import Length
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Inductance(LinearQuantity):
    """The flux linked per ampere: how a circuit opposes a change of current."""

    dimension: ClassVar[Dimension] = INDUCTANCE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Capacitance) -> TimeSquared: ...
    @overload
    def __mul__(self, other: Conductance) -> Time: ...
    @overload
    def __mul__(self, other: Current) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Frequency) -> Resistance: ...
    @overload
    def __mul__(self, other: Proportion) -> Inductance: ...
    @overload
    def __mul__(self, other: Numeric) -> Inductance: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Inductance) -> Proportion: ...
    @overload
    def __truediv__(self, other: Length) -> Permeability: ...
    @overload
    def __truediv__(self, other: Permeability) -> Length: ...
    @overload
    def __truediv__(self, other: Proportion) -> Inductance: ...
    @overload
    def __truediv__(self, other: Resistance) -> Time: ...
    @overload
    def __truediv__(self, other: Time) -> Resistance: ...
    @overload
    def __truediv__(self, other: Numeric) -> Inductance: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(INDUCTANCE, Inductance)

__all__ = ["Inductance"]
