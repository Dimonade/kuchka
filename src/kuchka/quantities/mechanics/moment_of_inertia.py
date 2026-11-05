"""MomentOfInertia: how a body resists angular acceleration about an axis.

`MomentOfInertia` is M L² angle⁻², the torque per angular acceleration, so `I * alpha`
is a `Torque`, `I * omega` an `AngularMomentum`, and `I * omega * omega` an `Energy`.
A kilogram square metre is a kilogram square metre per square radian, the way a
newton-metre of torque is a joule per radian.
Turn is the canonical angle, so the canonical unit is the kilogram square metre per
square turn, and arithmetic results display in the kilogram square metre.

`Mass * Area` is a `MomentOfInertia` by a bridge, the one place a mass and the square
of a length meet: the moment of inertia of a point mass at that radius.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOMENT_OF_INERTIA
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _bridge
from kuchka.quantities.base.registry import _register
from kuchka.quantities.geometry.area import Area
from kuchka.quantities.length import Length
from kuchka.quantities.mass import Mass
from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion


class MomentOfInertia(LinearQuantity):
    """How a body resists angular acceleration about an axis, in kg·m².

        rotor = KilogramSquareCentimetre(30)
        disc = 0.5 * Kilogram(2) * Metre(0.2) * Metre(0.2)   # 0.04 kg·m²

    A mass times the square of its radius is a `MomentOfInertia`, so a point mass, a
    thin ring, and a disc are written as their formulas.
    Divided by a mass it is the square of the radius of gyration, an `Area`.
    """

    dimension: ClassVar[Dimension] = MOMENT_OF_INERTIA
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AngularAcceleration) -> Torque: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: Proportion) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: Numeric) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Mass: ...
    @overload
    def __truediv__(self, other: FirstMomentOfMass) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> FirstMomentOfMass: ...
    @overload
    def __truediv__(self, other: Mass) -> Area: ...
    @overload
    def __truediv__(self, other: MomentOfInertia) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MomentOfInertia: ...
    @overload
    def __truediv__(self, other: Numeric) -> MomentOfInertia: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MOMENT_OF_INERTIA, MomentOfInertia)
_bridge(Mass, "*", Area, MomentOfInertia)
_bridge(FirstMomentOfMass, "*", Length, MomentOfInertia)
_bridge(MomentOfInertia, "/", Mass, Area)
_bridge(MomentOfInertia, "/", Area, Mass)
_bridge(MomentOfInertia, "/", Length, FirstMomentOfMass)
_bridge(MomentOfInertia, "/", FirstMomentOfMass, Length)

__all__ = ["MomentOfInertia"]
