"""FirstMomentOfMass: a mass times its distance from an axis, a rotor's unbalance."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import FIRST_MOMENT_OF_MASS
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
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Time


class FirstMomentOfMass(LinearQuantity):
    """A mass times its distance from an axis: the unbalance of a rotor, in g·mm.

        unbalance = Gram(2) * Millimetre(15)   # 30 g·mm

    `Mass * Length` is a `FirstMomentOfMass`, and times a further length it is a
    `MomentOfInertia`, so `m * r * r` reads in the order Python evaluates it.
    """

    dimension: ClassVar[Dimension] = FIRST_MOMENT_OF_MASS
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Energy: ...
    @overload
    def __mul__(self, other: Length) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: Proportion) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> Velocity: ...
    @overload
    def __mul__(self, other: Numeric) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> Proportion: ...
    @overload
    def __truediv__(self, other: Impulse) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Mass: ...
    @overload
    def __truediv__(self, other: Mass) -> Length: ...
    @overload
    def __truediv__(self, other: Momentum) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: Numeric) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(FIRST_MOMENT_OF_MASS, FirstMomentOfMass)

__all__ = ["FirstMomentOfMass"]
