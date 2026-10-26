"""Energy: the capacity to do work, e.g. a laser pulse's delivered energy."""

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
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Energy(LinearQuantity):
    """The capacity to do work: a delivered or dissipated quantity of energy."""

    dimension: ClassVar[Dimension] = ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Frequency) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Energy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AngularDisplacement) -> Torque: ...
    @overload
    def __truediv__(self, other: Charge) -> Voltage: ...
    @overload
    def __truediv__(self, other: Energy) -> Proportion: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Volume: ...
    @overload
    def __truediv__(self, other: Force) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Force: ...
    @overload
    def __truediv__(self, other: Power) -> Time: ...
    @overload
    def __truediv__(self, other: Pressure) -> Volume: ...
    @overload
    def __truediv__(self, other: Proportion) -> Energy: ...
    @overload
    def __truediv__(self, other: Time) -> Power: ...
    @overload
    def __truediv__(self, other: Torque) -> AngularDisplacement: ...
    @overload
    def __truediv__(self, other: Voltage) -> Charge: ...
    @overload
    def __truediv__(self, other: Volume) -> EnergyDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Energy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ENERGY, Energy)

__all__ = ["Energy"]
