"""Energy: the capacity to do work, e.g. a laser pulse's delivered energy.

Defined alongside two relationships:
- `Power * Time -> Energy`, and its two inverses, `Energy / Time -> Power` and
  `Energy / Power -> Time`.
- `Pressure * Volume -> Energy`, the P-V work relationship, and its inverse
  `Energy / Pressure -> Volume`, whose other overload halves live on `Pressure` and
  `Volume` themselves.

Also carries the other overload halves of `Energy / Volume -> EnergyDensity` and its
inverse `Energy / EnergyDensity -> Volume` (see `EnergyDensity`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ENERGY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.charge import Charge
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.electrical import Voltage
    from kuchka.quantities.energy_density import EnergyDensity
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.length import Length
    from kuchka.quantities.pressure import Pressure
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.rotational import Torque
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.volume import Volume


class Energy(LinearQuantity):
    """The capacity to do work: a delivered or dissipated quantity of energy."""

    dimension: ClassVar[Dimension] = ENERGY
    __slots__ = ()

    @overload
    def __mul__(self, other: Frequency) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Energy: ...
    @overload
    def __mul__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Time) -> Power: ...
    @overload
    def __truediv__(self, other: Power) -> Time: ...
    @overload
    def __truediv__(self, other: Pressure) -> Volume: ...
    @overload
    def __truediv__(self, other: Volume) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Volume: ...
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Torque: ...
    @overload
    def __truediv__(self, other: Torque) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Charge) -> Voltage: ...
    @overload
    def __truediv__(self, other: Voltage) -> Charge: ...
    @overload
    def __truediv__(self, other: Energy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Force) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Force: ...
    @overload
    def __truediv__(self, other: Numeric) -> Energy: ...
    @overload
    def __truediv__(self, other: object) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ENERGY, Energy)

__all__ = ["Energy"]
