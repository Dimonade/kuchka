"""An electric current: a base quantity, beside `Length` and `Mass`."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import CURRENT
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
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
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class Current(LinearQuantity):
    """An electric current."""

    dimension: ClassVar[Dimension] = CURRENT
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Inductance) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> Energy: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: Proportion) -> Current: ...
    @overload
    def __mul__(self, other: Resistance) -> Voltage: ...
    @overload
    def __mul__(self, other: Time) -> Charge: ...
    @overload
    def __mul__(self, other: Voltage) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Current: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> CurrentDensity: ...
    @overload
    def __truediv__(self, other: Charge) -> Frequency: ...
    @overload
    def __truediv__(self, other: Conductance) -> Voltage: ...
    @overload
    def __truediv__(self, other: Current) -> Proportion: ...
    @overload
    def __truediv__(self, other: CurrentDensity) -> Area: ...
    @overload
    def __truediv__(self, other: Frequency) -> Charge: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: Length) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> Velocity: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> Length: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificCurrent: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: MolarCharge) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> MolarCharge: ...
    @overload
    def __truediv__(self, other: Proportion) -> Current: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: SpecificCurrent) -> Mass: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: Velocity) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: Voltage) -> Conductance: ...
    @overload
    def __truediv__(self, other: VolumeChargeDensity) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> VolumeChargeDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> Current: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(CURRENT, Current)

__all__ = ["Current"]
