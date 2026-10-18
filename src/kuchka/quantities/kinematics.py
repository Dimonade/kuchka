"""Velocity, Acceleration, and Force: rates and interactions of mechanical motion.

A number of related relationships defined as:

- `Length / Time -> Velocity`, and its inverse, `Velocity * Time -> Length`.
- `Velocity / Time -> Acceleration`, and its inverse,
    `Acceleration * Time -> Velocity` -- the rate of change of a rate of change.
- `Mass * Acceleration -> Force`, Newton's second law, and its two inverses,
  `Force / Mass -> Acceleration` and `Force / Acceleration -> Mass`.

`Force` also carries the other overload half of `Force / Area -> Pressure` and its
two inverses, `Pressure * Area -> Force` and `Force / Pressure -> Area` (see
`Pressure`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ACCELERATION
from kuchka.dimensions import FORCE
from kuchka.dimensions import VELOCITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.area import Area
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.energy_density import EnergyDensity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.pressure import Pressure
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Velocity(LinearQuantity):
    """A rate of change of position: distance covered per unit time."""

    dimension: ClassVar[Dimension] = VELOCITY
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> Length: ...
    @overload
    def __mul__(self, other: Force) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Acceleration: ...
    @overload
    def __mul__(self, other: Proportion) -> Velocity: ...
    @overload
    def __mul__(self, other: Numeric) -> Velocity: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Length: ...
    @overload
    def __truediv__(self, other: Time) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Acceleration) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Frequency: ...
    @overload
    def __truediv__(self, other: Velocity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Velocity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Velocity: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


class Acceleration(LinearQuantity):
    """A rate of change of velocity: how quickly speed or direction changes."""

    dimension: ClassVar[Dimension] = ACCELERATION
    __slots__ = ()

    @overload
    def __mul__(self, other: Time) -> Velocity: ...
    @overload
    def __mul__(self, other: Mass) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __mul__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Frequency) -> Velocity: ...
    @overload
    def __truediv__(self, other: Velocity) -> Frequency: ...
    @overload
    def __truediv__(self, other: Acceleration) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Numeric) -> Acceleration: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


class Force(LinearQuantity):
    """A push or a pull: the interaction that changes a mass's motion."""

    dimension: ClassVar[Dimension] = FORCE
    __slots__ = ()

    @overload
    def __mul__(self, other: Velocity) -> Power: ...
    @overload
    def __mul__(self, other: Length) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Force: ...
    @overload
    def __mul__(self, other: Numeric) -> Force: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Mass) -> Acceleration: ...
    @overload
    def __truediv__(self, other: Acceleration) -> Mass: ...
    @overload
    def __truediv__(self, other: Area) -> Pressure: ...
    @overload
    def __truediv__(self, other: Pressure) -> Area: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Force) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Force: ...
    @overload
    def __truediv__(self, other: Numeric) -> Force: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(VELOCITY, Velocity)
_register(ACCELERATION, Acceleration)
_register(FORCE, Force)

__all__ = ["Acceleration", "Force", "Velocity"]
