"""ElectricFieldStrength: the force a charge feels, per charge."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ELECTRIC_FIELD_STRENGTH
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.electromagnetics.charge import Charge
from kuchka.quantities.electromagnetics.permittivity import Permittivity
from kuchka.quantities.electromagnetics.surface_charge_density import (
    ElectricFluxDensity,
)
from kuchka.quantities.geometry.area import Area
from kuchka.quantities.mechanics.energy_density import EnergyDensity

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.proportion import Proportion


class ElectricFieldStrength(LinearQuantity):
    """The force on a charge per unit charge, E: voltage per length.

    `Voltage / Length`, `Force / Charge`, and `MagneticFluxDensity * Velocity` are an
    `ElectricFieldStrength`, and `ElectricFieldStrength * Length` is a `Voltage`.
    `Permittivity * ElectricFieldStrength` is an `ElectricFluxDensity`, and
    `ElectricFieldStrength * ElectricFluxDensity` is an `EnergyDensity`, the product
    `E·D`: the energy stored in a linear dielectric is half of it, `w = E·D / 2`.
    """

    dimension: ClassVar[Dimension] = ELECTRIC_FIELD_STRENGTH
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Capacitance) -> LinearChargeDensity: ...
    @overload
    def __mul__(self, other: Charge) -> Force: ...
    @overload
    def __mul__(self, other: Conductance) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: ElectricFluxDensity) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Length) -> Voltage: ...
    @overload
    def __mul__(self, other: Permittivity) -> ElectricFluxDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> ElectricFieldStrength: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> Acceleration: ...
    @overload
    def __mul__(self, other: SpecificCurrent) -> Jerk: ...
    @overload
    def __mul__(self, other: Numeric) -> ElectricFieldStrength: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> Proportion: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> Resistance: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Velocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: Resistance) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Velocity) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ELECTRIC_FIELD_STRENGTH, ElectricFieldStrength)

_rule(Permittivity, "*", ElectricFieldStrength, ElectricFluxDensity)
_rule(ElectricFluxDensity, "/", ElectricFieldStrength, Permittivity)
_rule(ElectricFluxDensity, "/", Permittivity, ElectricFieldStrength)
_rule(ElectricFieldStrength, "*", ElectricFluxDensity, EnergyDensity)
_rule(ElectricFluxDensity, "*", Area, Charge)

__all__ = ["ElectricFieldStrength"]
