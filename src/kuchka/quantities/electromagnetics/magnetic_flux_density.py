"""Magnetic flux density: the strength of a magnetic field."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MAGNETIC_FLUX_DENSITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.linear_charge_density import (
        LinearChargeDensity,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency


class MagneticFluxDensity(LinearQuantity):
    """The strength of a magnetic field: the flux per unit area through a surface."""

    dimension: ClassVar[Dimension] = MAGNETIC_FLUX_DENSITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: Charge) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Conductance) -> SurfaceChargeDensity: ...
    @overload
    def __mul__(self, other: KinematicViscosity) -> Voltage: ...
    @overload
    def __mul__(self, other: LinearChargeDensity) -> DynamicViscosity: ...
    @overload
    def __mul__(self, other: MagneticFieldStrength) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: Proportion) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> Frequency: ...
    @overload
    def __mul__(self, other: Velocity) -> ElectricFieldStrength: ...
    @overload
    def __mul__(self, other: Numeric) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: CurrentDensity) -> Inductance: ...
    @overload
    def __truediv__(self, other: Inductance) -> CurrentDensity: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> Permeability: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Permeability) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Proportion) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Resistance) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Resistance: ...
    @overload
    def __truediv__(self, other: Numeric) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MAGNETIC_FLUX_DENSITY, MagneticFluxDensity)

__all__ = ["MagneticFluxDensity"]
