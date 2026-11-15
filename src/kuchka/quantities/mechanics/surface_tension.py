"""SurfaceTension: the force along a line, which is also the energy on a surface."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SURFACE_TENSION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.length import Length
from kuchka.quantities.mechanics.pressure import Pressure

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.current import Current
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
    from kuchka.quantities.electromagnetics.surface_charge_density import (
        SurfaceChargeDensity,
    )
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_flux import HeatFlux


class SurfaceTension(LinearQuantity):
    """The force along a line, or the energy on a surface: force per length.

        water = MillinewtonPerMetre(72)
        spring = NewtonPerMetre(250)

    One newton per metre is one joule per square metre, so a surface tension is both a
    `Force / Length` and an `Energy / Area`, and `SurfaceTension * Length` is a `Force`
    where `SurfaceTension * Area` is an `Energy`.
    `Pressure * Length` is a `SurfaceTension` and `SurfaceTension / Length` is a
    `Pressure`, as the Young-Laplace relation of a curved interface has it.
    A stiffness, a line load, an interfacial tension, and an energy release rate read
    as a `SurfaceTension` too.
    `Energy / Area` is a `Fluence`, the kind of the same dimension that radiometry
    uses, and `Fluence.to_surface_tension()` reads one as a surface tension.
    """

    dimension: ClassVar[Dimension] = SURFACE_TENSION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Energy: ...
    @overload
    def __mul__(self, other: Frequency) -> HeatFlux: ...
    @overload
    def __mul__(self, other: KinematicViscosity) -> Power: ...
    @overload
    def __mul__(self, other: Length) -> Force: ...
    @overload
    def __mul__(self, other: LuminousEfficacy) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: Proportion) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: Time) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: TimeSquared) -> Mass: ...
    @overload
    def __mul__(self, other: Numeric) -> SurfaceTension: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Current) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: CurrentDensity) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: DynamicViscosity) -> Velocity: ...
    @overload
    def __truediv__(self, other: ElectricFieldStrength) -> LinearChargeDensity: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Length: ...
    @overload
    def __truediv__(self, other: Frequency) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: HeatFlux) -> Time: ...
    @overload
    def __truediv__(self, other: Length) -> Pressure: ...
    @overload
    def __truediv__(self, other: LinearChargeDensity) -> ElectricFieldStrength: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> CurrentDensity: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Current: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Frequency: ...
    @overload
    def __truediv__(self, other: Pressure) -> Length: ...
    @overload
    def __truediv__(self, other: Proportion) -> SurfaceTension: ...
    @overload
    def __truediv__(self, other: SurfaceChargeDensity) -> Voltage: ...
    @overload
    def __truediv__(self, other: SurfaceTension) -> Proportion: ...
    @overload
    def __truediv__(self, other: Time) -> HeatFlux: ...
    @overload
    def __truediv__(self, other: Velocity) -> DynamicViscosity: ...
    @overload
    def __truediv__(self, other: Voltage) -> SurfaceChargeDensity: ...
    @overload
    def __truediv__(self, other: Numeric) -> SurfaceTension: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SURFACE_TENSION, SurfaceTension)
_rule(SurfaceTension, "/", Length, Pressure)

__all__ = ["SurfaceTension"]
