"""Impulse: a force acting over a time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import IMPULSE
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import _register_hint
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mechanics.force import Force
from kuchka.quantities.mechanics.momentum import Momentum
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency


class Impulse(LinearQuantity):
    """A force acting over a time: the push a thruster or a collision delivers.

        burn = Newton(20) * Second(3)   # 60 N·s
        delta_v = burn / Kilogram(12)   # a Velocity: 5 m/s

    An impulse is measured in newton seconds (1 N·s = 1 kg·m/s) or in dyne seconds
    (1 dyn·s = 1 g·cm/s).
    `Force * Time` is an `Impulse`, `Impulse / Time` a `Force`, and `Impulse / Mass`
    the `Velocity` it gives that mass.
    It shares its dimension with `Momentum`, the two are contested, and an impulse
    that brings a body from rest to a momentum is `Impulse.from_momentum(momentum)`.
    """

    dimension: ClassVar[Dimension] = IMPULSE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Power: ...
    @overload
    def __mul__(self, other: Frequency) -> Force: ...
    @overload
    def __mul__(self, other: Proportion) -> Impulse: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> Acceleration: ...
    @overload
    def __mul__(self, other: Velocity) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Impulse: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Force) -> Time: ...
    @overload
    def __truediv__(self, other: Impulse) -> Proportion: ...
    @overload
    def __truediv__(self, other: Length) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: Mass) -> Velocity: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Length: ...
    @overload
    def __truediv__(self, other: Momentum) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Impulse: ...
    @overload
    def __truediv__(self, other: Time) -> Force: ...
    @overload
    def __truediv__(self, other: Velocity) -> Mass: ...
    @overload
    def __truediv__(self, other: Numeric) -> Impulse: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_momentum(cls, momentum: Momentum) -> Self:
        """Return the impulse that brings a body from rest to `momentum`.

            Impulse.from_momentum(KilogramMetrePerSecond(6)) == NewtonSecond(6)

        A newton second and a kilogram metre per second are the same amount.
        """
        if not isinstance(momentum, Momentum):
            raise IncompatibleDimensionError(
                "build an impulse from", momentum, momentum
            )
        return cls(momentum._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_momentum(self) -> Momentum:
        """Return the momentum this impulse gives a body that starts at rest.

        NewtonSecond(6).to_momentum() == KilogramMetrePerSecond(6)
        """
        return Momentum(self._magnitude, Momentum._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes


_register(IMPULSE, Impulse, contested_with=Momentum)
_rule(Force, "*", Time, Impulse)
_register_hint(
    Impulse,
    Momentum,
    "An impulse changes a momentum by the same amount: convert with "
    "`Impulse.to_momentum()` or `Impulse.from_momentum(momentum)`.",
)

__all__ = ["Impulse"]
