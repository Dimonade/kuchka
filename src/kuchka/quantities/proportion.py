"""Proportion: a dimensionless quantity, expressed as a ratio or a percentage.

Built by explicit construction (`Percent(5)`, `Ratio(0.05)`) and as the result of a
ratio: the quotient of two quantities of one dimension, and the product or quotient of
two proportions.
`Volt(5) / Volt(2)` is `Ratio(Fraction(5, 2))`, and `Percent(50) * Percent(50)` is
`Ratio(Fraction(1, 4))`.
Other dimensionless results, such as `Hertz(2) * Second(3)`, are plain `Fraction`
values.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import DIMENSIONLESS
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _register_ratio

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.angular import AngularDisplacement
    from kuchka.quantities.area import Area
    from kuchka.quantities.charge import Charge
    from kuchka.quantities.density import Density
    from kuchka.quantities.electrical import Conductance
    from kuchka.quantities.electrical import Current
    from kuchka.quantities.electrical import Power
    from kuchka.quantities.electrical import Resistance
    from kuchka.quantities.electrical import Voltage
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.energy_density import EnergyDensity
    from kuchka.quantities.kinematics import Acceleration
    from kuchka.quantities.kinematics import Force
    from kuchka.quantities.kinematics import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.pressure import Pressure
    from kuchka.quantities.rotational import AngularVelocity
    from kuchka.quantities.rotational import Torque
    from kuchka.quantities.temporal import BaudRate
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import SampleRate
    from kuchka.quantities.temporal import SamplingPeriod
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.volume import Volume


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()

    @overload
    def __mul__(self, other: Proportion) -> Proportion: ...
    @overload
    def __mul__(self, other: AmountOfSubstance) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: AngularDisplacement) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: Area) -> Area: ...
    @overload
    def __mul__(self, other: Charge) -> Charge: ...
    @overload
    def __mul__(self, other: Density) -> Density: ...
    @overload
    def __mul__(self, other: Voltage) -> Voltage: ...
    @overload
    def __mul__(self, other: Current) -> Current: ...
    @overload
    def __mul__(self, other: Power) -> Power: ...
    @overload
    def __mul__(self, other: Resistance) -> Resistance: ...
    @overload
    def __mul__(self, other: Conductance) -> Conductance: ...
    @overload
    def __mul__(self, other: Energy) -> Energy: ...
    @overload
    def __mul__(self, other: Velocity) -> Velocity: ...
    @overload
    def __mul__(self, other: Acceleration) -> Acceleration: ...
    @overload
    def __mul__(self, other: Force) -> Force: ...
    @overload
    def __mul__(self, other: Pressure) -> Pressure: ...
    @overload
    def __mul__(self, other: Volume) -> Volume: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Length) -> Length: ...
    @overload
    def __mul__(self, other: LuminousIntensity) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: Mass) -> Mass: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: Torque) -> Torque: ...
    @overload
    def __mul__(self, other: Time) -> Time: ...
    @overload
    def __mul__(self, other: Frequency) -> Frequency: ...
    @overload
    def __mul__(self, other: SamplingPeriod) -> SamplingPeriod: ...
    @overload
    def __mul__(self, other: SampleRate) -> SampleRate: ...
    @overload
    def __mul__(self, other: BaudRate) -> BaudRate: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> TemperatureDelta: ...
    @overload
    def __mul__(self, other: Numeric) -> Proportion: ...
    @overload
    def __mul__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Proportion) -> Proportion: ...
    @overload
    def __truediv__(self, other: Time) -> Frequency: ...
    @overload
    def __truediv__(self, other: Frequency) -> Time: ...
    @overload
    def __truediv__(self, other: Resistance) -> Conductance: ...
    @overload
    def __truediv__(self, other: Conductance) -> Resistance: ...
    @overload
    def __truediv__(self, other: SampleRate) -> SamplingPeriod: ...
    @overload
    def __truediv__(self, other: SamplingPeriod) -> SampleRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> Proportion: ...
    @overload
    def __truediv__(self, other: LinearQuantity) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(DIMENSIONLESS, Proportion)
_register_ratio(Proportion)

__all__ = ["Proportion"]
