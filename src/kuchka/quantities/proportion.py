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
from typing import Literal
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
    from kuchka.quantities.chemistry.catalytic_activity import CatalyticActivity
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_concentration import MolarConcentration
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarEntropy
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarHeatCapacity
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.chemistry.molar_volume import MolarVolume
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.ac_power import ApparentPower
    from kuchka.quantities.electromagnetics.ac_power import ReactivePower
    from kuchka.quantities.electromagnetics.capacitance import Capacitance
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.conductance import Conductance
    from kuchka.quantities.electromagnetics.inductance import Inductance
    from kuchka.quantities.electromagnetics.magnetic_field_strength import (
        MagneticFieldStrength,
    )
    from kuchka.quantities.electromagnetics.magnetic_field_strength import Magnetization
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.permeability import Permeability
    from kuchka.quantities.electromagnetics.permittivity import Permittivity
    from kuchka.quantities.electromagnetics.resistance import Impedance
    from kuchka.quantities.electromagnetics.resistance import Reactance
    from kuchka.quantities.electromagnetics.resistance import Resistance
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.information.data import Data
    from kuchka.quantities.information.data_rate import DataRate
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.angular_acceleration import AngularAcceleration
    from kuchka.quantities.kinematics.angular_jerk import AngularJerk
    from kuchka.quantities.kinematics.angular_velocity import AngularVelocity
    from kuchka.quantities.kinematics.angular_velocity_squared import (
        AngularVelocitySquared,
    )
    from kuchka.quantities.kinematics.jerk import Jerk
    from kuchka.quantities.kinematics.snap import Snap
    from kuchka.quantities.kinematics.time_cubed import TimeCubed
    from kuchka.quantities.kinematics.time_fourth_power import TimeFourthPower
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.luminous_intensity import LuminousIntensity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.angular_momentum import AngularMomentum
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.energy_density import EnergyDensity
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.pressure import Pressure
    from kuchka.quantities.mechanics.pressure import Stress
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.torque import Torque
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminance import Luminance
    from kuchka.quantities.photometry.luminous_efficacy import LuminousEfficacy
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.photometry.luminous_exposure import LuminousExposure
    from kuchka.quantities.photometry.luminous_flux import LuminousFlux
    from kuchka.quantities.radiation.absorbed_dose import AbsorbedDose
    from kuchka.quantities.radiation.absorbed_dose_rate import AbsorbedDoseRate
    from kuchka.quantities.radiation.activity import Activity
    from kuchka.quantities.radiation.activity_concentration import ActivityConcentration
    from kuchka.quantities.radiation.equivalent_dose import EquivalentDose
    from kuchka.quantities.radiation.equivalent_dose_rate import EquivalentDoseRate
    from kuchka.quantities.radiation.exposure import Exposure
    from kuchka.quantities.radiation.exposure_rate import ExposureRate
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity
    from kuchka.quantities.solid_angle import SolidAngle
    from kuchka.quantities.temporal import BaudRate
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import SampleRate
    from kuchka.quantities.temporal import SamplingPeriod
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import Entropy
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate
    from kuchka.quantities.thermodynamics.specific_heat_capacity import SpecificEntropy
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class Proportion(LinearQuantity):
    """A dimensionless quantity: how much of something, relative to a whole."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AbsorbedDose) -> AbsorbedDose: ...
    @overload
    def __mul__(self, other: AbsorbedDoseRate) -> AbsorbedDoseRate: ...
    @overload
    def __mul__(self, other: Acceleration) -> Acceleration: ...
    @overload
    def __mul__(self, other: Activity) -> Activity: ...
    @overload
    def __mul__(self, other: ActivityConcentration) -> ActivityConcentration: ...
    @overload
    def __mul__(self, other: AmountOfSubstance) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: AngularAcceleration) -> AngularAcceleration: ...
    @overload
    def __mul__(self, other: AngularDisplacement) -> AngularDisplacement: ...
    @overload
    def __mul__(self, other: AngularJerk) -> AngularJerk: ...
    @overload
    def __mul__(self, other: AngularMomentum) -> AngularMomentum: ...
    @overload
    def __mul__(self, other: AngularVelocity) -> AngularVelocity: ...
    @overload
    def __mul__(self, other: AngularVelocitySquared) -> AngularVelocitySquared: ...
    @overload
    def __mul__(self, other: ApparentPower) -> ApparentPower: ...
    @overload
    def __mul__(self, other: Area) -> Area: ...
    @overload
    def __mul__(self, other: BaudRate) -> BaudRate: ...
    @overload
    def __mul__(self, other: Capacitance) -> Capacitance: ...
    @overload
    def __mul__(self, other: CatalyticActivity) -> CatalyticActivity: ...
    @overload
    def __mul__(self, other: Charge) -> Charge: ...
    @overload
    def __mul__(self, other: Conductance) -> Conductance: ...
    @overload
    def __mul__(self, other: Current) -> Current: ...
    @overload
    def __mul__(self, other: Data) -> Data: ...
    @overload
    def __mul__(self, other: DataRate) -> DataRate: ...
    @overload
    def __mul__(self, other: Density) -> Density: ...
    @overload
    def __mul__(self, other: Energy) -> Energy: ...
    @overload
    def __mul__(self, other: EnergyDensity) -> EnergyDensity: ...
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> EntitiesPerAmount: ...
    @overload
    def __mul__(self, other: Entropy) -> Entropy: ...
    @overload
    def __mul__(self, other: EquivalentDose) -> EquivalentDose: ...
    @overload
    def __mul__(self, other: EquivalentDoseRate) -> EquivalentDoseRate: ...
    @overload
    def __mul__(self, other: Exposure) -> Exposure: ...
    @overload
    def __mul__(self, other: ExposureRate) -> ExposureRate: ...
    @overload
    def __mul__(self, other: FirstMomentOfMass) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Force) -> Force: ...
    @overload
    def __mul__(self, other: Frequency) -> Frequency: ...
    @overload
    def __mul__(self, other: HeatCapacity) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: HeatingRate) -> HeatingRate: ...
    @overload
    def __mul__(self, other: Illuminance) -> Illuminance: ...
    @overload
    def __mul__(self, other: Impedance) -> Impedance: ...
    @overload
    def __mul__(self, other: Impulse) -> Impulse: ...
    @overload
    def __mul__(self, other: Inductance) -> Inductance: ...
    @overload
    def __mul__(self, other: Jerk) -> Jerk: ...
    @overload
    def __mul__(self, other: Length) -> Length: ...
    @overload
    def __mul__(self, other: Luminance) -> Luminance: ...
    @overload
    def __mul__(self, other: LuminousEfficacy) -> LuminousEfficacy: ...
    @overload
    def __mul__(self, other: LuminousEnergy) -> LuminousEnergy: ...
    @overload
    def __mul__(self, other: LuminousExposure) -> LuminousExposure: ...
    @overload
    def __mul__(self, other: LuminousFlux) -> LuminousFlux: ...
    @overload
    def __mul__(self, other: LuminousIntensity) -> LuminousIntensity: ...
    @overload
    def __mul__(self, other: MagneticFieldStrength) -> MagneticFieldStrength: ...
    @overload
    def __mul__(self, other: MagneticFlux) -> MagneticFlux: ...
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> MagneticFluxDensity: ...
    @overload
    def __mul__(self, other: Magnetization) -> Magnetization: ...
    @overload
    def __mul__(self, other: Mass) -> Mass: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Molality) -> Molality: ...
    @overload
    def __mul__(self, other: MolarCharge) -> MolarCharge: ...
    @overload
    def __mul__(self, other: MolarConcentration) -> MolarConcentration: ...
    @overload
    def __mul__(self, other: MolarEnergy) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: MolarEntropy) -> MolarEntropy: ...
    @overload
    def __mul__(self, other: MolarFlowRate) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: MolarHeatCapacity) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: MolarMass) -> MolarMass: ...
    @overload
    def __mul__(self, other: MolarVolume) -> MolarVolume: ...
    @overload
    def __mul__(self, other: MomentOfInertia) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: Momentum) -> Momentum: ...
    @overload
    def __mul__(self, other: Permeability) -> Permeability: ...
    @overload
    def __mul__(self, other: Permittivity) -> Permittivity: ...
    @overload
    def __mul__(self, other: Power) -> Power: ...
    @overload
    def __mul__(self, other: Pressure) -> Pressure: ...
    @overload
    def __mul__(self, other: Proportion) -> Proportion: ...
    @overload
    def __mul__(self, other: Reactance) -> Reactance: ...
    @overload
    def __mul__(self, other: ReactivePower) -> ReactivePower: ...
    @overload
    def __mul__(self, other: Resistance) -> Resistance: ...
    @overload
    def __mul__(self, other: SampleRate) -> SampleRate: ...
    @overload
    def __mul__(self, other: SamplingPeriod) -> SamplingPeriod: ...
    @overload
    def __mul__(self, other: Snap) -> Snap: ...
    @overload
    def __mul__(self, other: SolidAngle) -> SolidAngle: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> SpecificActivity: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> SpecificCharge: ...
    @overload
    def __mul__(self, other: SpecificCurrent) -> SpecificCurrent: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: SpecificEntropy) -> SpecificEntropy: ...
    @overload
    def __mul__(self, other: SpecificHeatCapacity) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: SpecificPower) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Stress) -> Stress: ...
    @overload
    def __mul__(self, other: SurfaceActivity) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> TemperatureDelta: ...
    @overload
    def __mul__(self, other: Time) -> Time: ...
    @overload
    def __mul__(self, other: TimeCubed) -> TimeCubed: ...
    @overload
    def __mul__(self, other: TimeFourthPower) -> TimeFourthPower: ...
    @overload
    def __mul__(self, other: TimeSquared) -> TimeSquared: ...
    @overload
    def __mul__(self, other: Torque) -> Torque: ...
    @overload
    def __mul__(self, other: Velocity) -> Velocity: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> VelocitySquared: ...
    @overload
    def __mul__(self, other: Voltage) -> Voltage: ...
    @overload
    def __mul__(self, other: Volume) -> Volume: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> VolumetricFlowRate: ...
    @overload
    def __mul__(self, other: Numeric) -> Proportion: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: Conductance) -> Resistance: ...
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Frequency) -> Time: ...
    @overload
    def __truediv__(self, other: Molality) -> MolarMass: ...
    @overload
    def __truediv__(self, other: MolarConcentration) -> MolarVolume: ...
    @overload
    def __truediv__(self, other: MolarMass) -> Molality: ...
    @overload
    def __truediv__(self, other: MolarVolume) -> MolarConcentration: ...
    @overload
    def __truediv__(self, other: Proportion) -> Proportion: ...
    @overload
    def __truediv__(self, other: Resistance) -> Conductance: ...
    @overload
    def __truediv__(self, other: SampleRate) -> SamplingPeriod: ...
    @overload
    def __truediv__(self, other: SamplingPeriod) -> SampleRate: ...
    @overload
    def __truediv__(self, other: Time) -> Frequency: ...
    @overload
    def __truediv__(self, other: Numeric) -> Proportion: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    # BEGIN GENERATED __pow__
    @overload
    def __pow__(self, exponent: Literal[2]) -> Proportion: ...
    @overload
    def __pow__(self, exponent: Literal[3]) -> Proportion: ...
    @overload
    def __pow__(self, exponent: Literal[4]) -> Proportion: ...
    @overload
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __pow__(self, exponent: int) -> LinearQuantity | Fraction:
        return super().__pow__(exponent)


_register(DIMENSIONLESS, Proportion)
_register_ratio(Proportion)

__all__ = ["Proportion"]
