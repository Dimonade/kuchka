"""Length: a distance or a physical extent."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Literal
from typing import overload

from kuchka.dimensions import LENGTH
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity_concentration import ActivityConcentration
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Length(LinearQuantity):
    """A distance or a physical extent: how far apart, how long, how wide, how far."""

    dimension: ClassVar[Dimension] = LENGTH
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: ActivityConcentration) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: Area) -> Volume: ...
    @overload
    def __mul__(self, other: Force) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> Velocity: ...
    @overload
    def __mul__(self, other: Length) -> Area: ...
    @overload
    def __mul__(self, other: MagneticFieldStrength) -> Current: ...
    @overload
    def __mul__(self, other: Permeability) -> Inductance: ...
    @overload
    def __mul__(self, other: Permittivity) -> Capacitance: ...
    @overload
    def __mul__(self, other: Proportion) -> Length: ...
    @overload
    def __mul__(self, other: Numeric) -> Length: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Length) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Length: ...
    @overload
    def __truediv__(self, other: Time) -> Velocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Time: ...
    @overload
    def __truediv__(self, other: Numeric) -> Length: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __pow__
    @overload
    def __pow__(self, exponent: Literal[2]) -> Area: ...
    @overload
    def __pow__(self, exponent: Literal[3]) -> Volume: ...
    @overload
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction:
        return super().__pow__(exponent)


_register(LENGTH, Length)

__all__ = ["Length"]
