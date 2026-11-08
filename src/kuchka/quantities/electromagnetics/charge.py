"""Charge: an accumulated flow of electric current over time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CHARGE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Charge(LinearQuantity):
    """An accumulated flow of electric current: how much charge has moved."""

    dimension: ClassVar[Dimension] = CHARGE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: ElectricFieldStrength) -> Force: ...
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> MolarCharge: ...
    @overload
    def __mul__(self, other: Frequency) -> Current: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> Charge: ...
    @overload
    def __mul__(self, other: Resistance) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> SpecificCurrent: ...
    @overload
    def __mul__(self, other: SurfaceActivity) -> CurrentDensity: ...
    @overload
    def __mul__(self, other: Voltage) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Charge: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> MolarCharge: ...
    @overload
    def __truediv__(self, other: Area) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: Capacitance) -> Voltage: ...
    @overload
    def __truediv__(self, other: Charge) -> Proportion: ...
    @overload
    def __truediv__(self, other: Conductance) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: Current) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> Length: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> Conductance: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: MolarCharge) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Proportion) -> Charge: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> Mass: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Time) -> Current: ...
    @overload
    def __truediv__(self, other: Voltage) -> Capacitance: ...
    @overload
    def __truediv__(self, other: Volume) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> Volume: ...
    @overload
    def __truediv__(self, other: Numeric) -> Charge: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CHARGE, Charge)

__all__ = ["Charge"]
