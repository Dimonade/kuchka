"""Volumetric flow rate: the volume that passes a section per unit of time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import VOLUMETRIC_FLOW_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.volume_charge_density import (
        VolumeChargeDensity,
    )
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.dynamic_viscosity import DynamicViscosity
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.kinematic_viscosity import KinematicViscosity
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class VolumetricFlowRate(LinearQuantity):
    """The volume that passes a section per unit of time: cubic metres per second."""

    dimension: ClassVar[Dimension] = VOLUMETRIC_FLOW_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Density) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: DynamicViscosity) -> Energy: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> Power: ...
    @overload
    def __mul__(self, other: MolarConcentration) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: Pressure) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: SurfaceActivity) -> Acceleration: ...
    @overload
    def __mul__(self, other: Time) -> Volume: ...
    @overload
    def __mul__(self, other: VolumeChargeDensity) -> Current: ...
    @overload
    def __mul__(self, other: Numeric) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Area) -> Velocity: ...
    @overload
    def __truediv__(self, other: Frequency) -> Volume: ...
    @overload
    def __truediv__(self, other: KinematicViscosity) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> KinematicViscosity: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> MolarVolume: ...
    @overload
    def __truediv__(self, other: MolarVolume) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: Proportion) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Velocity) -> Area: ...
    @overload
    def __truediv__(self, other: Volume) -> Frequency: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(VOLUMETRIC_FLOW_RATE, VolumetricFlowRate)

__all__ = ["VolumetricFlowRate"]
