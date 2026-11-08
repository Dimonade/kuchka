"""Voltage: an electric potential difference."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLTAGE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class Voltage(LinearQuantity):
    """An electric potential difference."""

    dimension: ClassVar[Dimension] = VOLTAGE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Capacitance) -> Charge: ...
    @overload
    def __mul__(self, other: Charge) -> Energy: ...
    @overload
    def __mul__(self, other: Conductance) -> Current: ...
    @overload
    def __mul__(self, other: Current) -> Power: ...
    @overload
    def __mul__(self, other: CurrentDensity) -> HeatFlux: ...
    @overload
    def __mul__(self, other: LinearChargeDensity) -> Force: ...
    @overload
    def __mul__(self, other: MolarCharge) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Permittivity) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> Voltage: ...
    @overload
    def __mul__(self, other: SpecificCurrent) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Time) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Numeric) -> Voltage: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Current) -> Resistance: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Length: ...
    @overload
    def __truediv__(self, other: Frequency) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: Length) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> Frequency: ...
    @overload
    def __truediv__(self, other: Proportion) -> Voltage: ...
    @overload
    def __truediv__(self, other: Resistance) -> Current: ...
    @overload
    def __truediv__(self, other: Voltage) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> Voltage: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(VOLTAGE, Voltage)

__all__ = ["Voltage"]
