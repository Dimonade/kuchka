"""HeatFlux: the heat that flows through a surface."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import HEAT_FLUX
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.current_density import CurrentDensity
    from kuchka.quantities.electromagnetics.electric_field_strength import (
        ElectricFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.fluence import Fluence
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.surface_tension import SurfaceTension
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class HeatFlux(LinearQuantity):
    """The heat that flows through a surface: power per area.

    An irradiance and a sound intensity are measured in the same watts per square
    metre, and read as a `HeatFlux` too.
    `HeatFlux * Area` is a `Power`, and `HeatFlux * Time` is a `Fluence`.
    """

    dimension: ClassVar[Dimension] = HEAT_FLUX
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Power: ...
    @overload
    def __mul__(self, other: LuminousEfficacy) -> Illuminance: ...
    @overload
    def __mul__(self, other: Proportion) -> HeatFlux: ...
    @overload
    def __mul__(self, other: Time) -> Fluence: ...
    @overload
    def __mul__(self, other: TimeCubed) -> Mass: ...
    @overload
    def __mul__(self, other: TimeSquared) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Numeric) -> HeatFlux: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: CurrentDensity) -> Voltage: ...
    @overload
    def __truediv__(self, other: DynamicViscosity) -> Acceleration: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> MagneticFieldStrength: ...
    @overload
    def __truediv__(self, other: Energy) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Velocity: ...
    @overload
    def __truediv__(self, other: Frequency) -> SurfaceTension: ...
    @overload
    def __truediv__(self, other: HeatFlux) -> Proportion: ...
    @overload
    def __truediv__(self, other: MagneticFieldStrength) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: Pressure) -> Velocity: ...
    @overload
    def __truediv__(self, other: Proportion) -> HeatFlux: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> Energy: ...
    @overload
    def __truediv__(self, other: SurfaceTension) -> Frequency: ...
    @overload
    def __truediv__(self, other: Voltage) -> CurrentDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> HeatFlux: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(HEAT_FLUX, HeatFlux)

__all__ = ["HeatFlux"]
