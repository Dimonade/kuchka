"""Engineer-facing unit constructors, grouped by the physical dimension they measure.

from kuchka import Milliampere
from kuchka import Volt

voltage = Volt(4.2)
current = Milliampere(150)
power = voltage * current

The base dimensions and the axes that are not dimensions of their own (angle,
proportion, logarithmic ratio) each have a module at this level, and `temporal` is a
package because the time family shares its dimensions.
Related derived dimensions live in themed packages, and `archaic` holds historical
units that applications import explicitly.

Each quantity's canonical unit (the one arithmetic results come back in, e.g.
``Voltage * Current`` yields a result expressed in ``Watt``) is assigned onto the
corresponding domain class from ``kuchka.quantities`` at the bottom of the module that
owns that dimension.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from kuchka import quantities
from kuchka.internal.unit_table import units_of
from kuchka.quantities.base.units import bind_clock_units
from kuchka.quantities.base.units import bind_ladders
from kuchka.quantities.base.units import bind_table
from kuchka.quantities.base.units import bind_units
from kuchka.units import amount
from kuchka.units import angular
from kuchka.units import chemistry
from kuchka.units import current
from kuchka.units import electromagnetics
from kuchka.units import geometry
from kuchka.units import information
from kuchka.units import kinematics
from kuchka.units import length
from kuchka.units import logarithmic
from kuchka.units import luminous_intensity
from kuchka.units import mass
from kuchka.units import mechanics
from kuchka.units import photometry
from kuchka.units import proportion
from kuchka.units import radiation
from kuchka.units import solid_angle
from kuchka.units import temporal
from kuchka.units import thermal
from kuchka.units import thermodynamics
from kuchka.units.amount import *
from kuchka.units.angular import *
from kuchka.units.chemistry.catalytic_activity import *
from kuchka.units.chemistry.entities_per_amount import *
from kuchka.units.chemistry.molality import *
from kuchka.units.chemistry.molar_charge import *
from kuchka.units.chemistry.molar_concentration import *
from kuchka.units.chemistry.molar_energy import *
from kuchka.units.chemistry.molar_entropy import *
from kuchka.units.chemistry.molar_flow_rate import *
from kuchka.units.chemistry.molar_heat_capacity import *
from kuchka.units.chemistry.molar_mass import *
from kuchka.units.chemistry.molar_volume import *
from kuchka.units.current import *
from kuchka.units.electromagnetics.ac_power import *
from kuchka.units.electromagnetics.capacitance import *
from kuchka.units.electromagnetics.charge import *
from kuchka.units.electromagnetics.conductance import *
from kuchka.units.electromagnetics.current_density import *
from kuchka.units.electromagnetics.electric_field_strength import *
from kuchka.units.electromagnetics.electric_flux_density import *
from kuchka.units.electromagnetics.impedance import *
from kuchka.units.electromagnetics.inductance import *
from kuchka.units.electromagnetics.linear_charge_density import *
from kuchka.units.electromagnetics.magnetic_field_strength import *
from kuchka.units.electromagnetics.magnetic_flux import *
from kuchka.units.electromagnetics.magnetic_flux_density import *
from kuchka.units.electromagnetics.magnetization import *
from kuchka.units.electromagnetics.permeability import *
from kuchka.units.electromagnetics.permittivity import *
from kuchka.units.electromagnetics.reactance import *
from kuchka.units.electromagnetics.resistance import *
from kuchka.units.electromagnetics.specific_charge import *
from kuchka.units.electromagnetics.specific_current import *
from kuchka.units.electromagnetics.surface_charge_density import *
from kuchka.units.electromagnetics.voltage import *
from kuchka.units.electromagnetics.volume_charge_density import *
from kuchka.units.geometry.area import *
from kuchka.units.geometry.volume import *
from kuchka.units.information.data import *
from kuchka.units.information.data_rate import *
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.angular_acceleration import *
from kuchka.units.kinematics.angular_jerk import *
from kuchka.units.kinematics.angular_velocity import *
from kuchka.units.kinematics.angular_velocity_squared import *
from kuchka.units.kinematics.jerk import *
from kuchka.units.kinematics.snap import *
from kuchka.units.kinematics.time_cubed import *
from kuchka.units.kinematics.time_fourth_power import *
from kuchka.units.kinematics.time_squared import *
from kuchka.units.kinematics.velocity import *
from kuchka.units.length import *
from kuchka.units.logarithmic import *
from kuchka.units.luminous_intensity import *
from kuchka.units.mass import *
from kuchka.units.mechanics.angular_momentum import *
from kuchka.units.mechanics.density import *
from kuchka.units.mechanics.dynamic_viscosity import *
from kuchka.units.mechanics.energy import *
from kuchka.units.mechanics.energy_density import *
from kuchka.units.mechanics.first_moment_of_mass import *
from kuchka.units.mechanics.fluence import *
from kuchka.units.mechanics.force import *
from kuchka.units.mechanics.impulse import *
from kuchka.units.mechanics.kinematic_viscosity import *
from kuchka.units.mechanics.mass_flow_rate import *
from kuchka.units.mechanics.moment_of_inertia import *
from kuchka.units.mechanics.momentum import *
from kuchka.units.mechanics.power import *
from kuchka.units.mechanics.pressure import *
from kuchka.units.mechanics.specific_energy import *
from kuchka.units.mechanics.specific_power import *
from kuchka.units.mechanics.stress import *
from kuchka.units.mechanics.surface_tension import *
from kuchka.units.mechanics.torque import *
from kuchka.units.mechanics.velocity_squared import *
from kuchka.units.mechanics.volumetric_flow_rate import *
from kuchka.units.photometry.illuminance import *
from kuchka.units.photometry.luminance import *
from kuchka.units.photometry.luminous_efficacy import *
from kuchka.units.photometry.luminous_energy import *
from kuchka.units.photometry.luminous_exposure import *
from kuchka.units.photometry.luminous_flux import *
from kuchka.units.proportion import *
from kuchka.units.radiation.absorbed_dose import *
from kuchka.units.radiation.absorbed_dose_rate import *
from kuchka.units.radiation.activity import *
from kuchka.units.radiation.activity_concentration import *
from kuchka.units.radiation.equivalent_dose import *
from kuchka.units.radiation.equivalent_dose_rate import *
from kuchka.units.radiation.exposure import *
from kuchka.units.radiation.exposure_rate import *
from kuchka.units.radiation.specific_activity import *
from kuchka.units.radiation.surface_activity import *
from kuchka.units.solid_angle import *
from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
from kuchka.units.temporal.instant import *
from kuchka.units.temporal.sample_rate import *
from kuchka.units.temporal.sampling_period import *
from kuchka.units.temporal.time import *
from kuchka.units.thermal import *
from kuchka.units.thermodynamics.entropy import *
from kuchka.units.thermodynamics.heat_capacity import *
from kuchka.units.thermodynamics.heat_flux import *
from kuchka.units.thermodynamics.heating_rate import *
from kuchka.units.thermodynamics.specific_entropy import *
from kuchka.units.thermodynamics.specific_heat_capacity import *
from kuchka.units.thermodynamics.thermal_conductivity import *

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_TABLE_OF: dict[type[Any], Mapping[str, Callable[..., Any]]] = {
    quantities.AbsorbedDose: ABSORBED_DOSE_UNITS,
    quantities.ActivityConcentration: ACTIVITY_CONCENTRATION_UNITS,
    quantities.AbsorbedDoseRate: ABSORBED_DOSE_RATE_UNITS,
    quantities.Acceleration: ACCELERATION_UNITS,
    quantities.Activity: ACTIVITY_UNITS,
    quantities.ApparentPower: APPARENT_POWER_UNITS,
    quantities.CurrentDensity: CURRENT_DENSITY_UNITS,
    quantities.DynamicViscosity: DYNAMIC_VISCOSITY_UNITS,
    quantities.ElectricFieldStrength: ELECTRIC_FIELD_STRENGTH_UNITS,
    quantities.ElectricFluxDensity: ELECTRIC_FLUX_DENSITY_UNITS,
    quantities.KinematicViscosity: KINEMATIC_VISCOSITY_UNITS,
    quantities.ReactivePower: REACTIVE_POWER_UNITS,
    quantities.AmountOfSubstance: AMOUNT_OF_SUBSTANCE_UNITS,
    quantities.Angle: ANGLE_UNITS,
    quantities.AngularDisplacement: ANGULAR_DISPLACEMENT_UNITS,
    quantities.AngularJerk: ANGULAR_JERK_UNITS,
    quantities.AngularVelocity: ANGULAR_VELOCITY_UNITS,
    quantities.AngularAcceleration: ANGULAR_ACCELERATION_UNITS,
    quantities.AngularVelocitySquared: ANGULAR_VELOCITY_SQUARED_UNITS,
    quantities.AngularMomentum: ANGULAR_MOMENTUM_UNITS,
    quantities.FirstMomentOfMass: FIRST_MOMENT_OF_MASS_UNITS,
    quantities.MomentOfInertia: MOMENT_OF_INERTIA_UNITS,
    quantities.ThermalConductivity: THERMAL_CONDUCTIVITY_UNITS,
    quantities.Torque: TORQUE_UNITS,
    quantities.Area: AREA_UNITS,
    quantities.BaudRate: BAUD_RATE_UNITS,
    quantities.Capacitance: CAPACITANCE_UNITS,
    quantities.Charge: CHARGE_UNITS,
    quantities.Conductance: CONDUCTANCE_UNITS,
    quantities.Current: CURRENT_UNITS,
    quantities.Data: DATA_UNITS,
    quantities.DataRate: DATA_RATE_UNITS,
    quantities.CatalyticActivity: CATALYTIC_ACTIVITY_UNITS,
    quantities.Density: DENSITY_UNITS,
    quantities.EntitiesPerAmount: ENTITIES_PER_AMOUNT_UNITS,
    quantities.EquivalentDose: EQUIVALENT_DOSE_UNITS,
    quantities.EquivalentDoseRate: EQUIVALENT_DOSE_RATE_UNITS,
    quantities.Exposure: EXPOSURE_UNITS,
    quantities.ExposureRate: EXPOSURE_RATE_UNITS,
    quantities.Energy: ENERGY_UNITS,
    quantities.EnergyDensity: ENERGY_DENSITY_UNITS,
    quantities.Fluence: FLUENCE_UNITS,
    quantities.Force: FORCE_UNITS,
    quantities.Frequency: FREQUENCY_UNITS,
    quantities.Entropy: ENTROPY_UNITS,
    quantities.HeatCapacity: HEAT_CAPACITY_UNITS,
    quantities.HeatFlux: HEAT_FLUX_UNITS,
    quantities.HeatingRate: HEATING_RATE_UNITS,
    quantities.Impulse: IMPULSE_UNITS,
    quantities.MassFlowRate: MASS_FLOW_RATE_UNITS,
    quantities.Molality: MOLALITY_UNITS,
    quantities.MolarCharge: MOLAR_CHARGE_UNITS,
    quantities.MolarConcentration: MOLAR_CONCENTRATION_UNITS,
    quantities.MolarEnergy: MOLAR_ENERGY_UNITS,
    quantities.MolarEntropy: MOLAR_ENTROPY_UNITS,
    quantities.MolarFlowRate: MOLAR_FLOW_RATE_UNITS,
    quantities.MolarHeatCapacity: MOLAR_HEAT_CAPACITY_UNITS,
    quantities.MolarMass: MOLAR_MASS_UNITS,
    quantities.MolarVolume: MOLAR_VOLUME_UNITS,
    quantities.Momentum: MOMENTUM_UNITS,
    quantities.VelocitySquared: VELOCITY_SQUARED_UNITS,
    quantities.Illuminance: ILLUMINANCE_UNITS,
    quantities.Impedance: IMPEDANCE_UNITS,
    quantities.Inductance: INDUCTANCE_UNITS,
    quantities.Instant: INSTANT_UNITS,
    quantities.Jerk: JERK_UNITS,
    quantities.Length: LENGTH_UNITS,
    quantities.LinearChargeDensity: LINEAR_CHARGE_DENSITY_UNITS,
    quantities.LogarithmicRatio: LOGARITHMIC_RATIO_UNITS,
    quantities.Luminance: LUMINANCE_UNITS,
    quantities.LuminousEfficacy: LUMINOUS_EFFICACY_UNITS,
    quantities.LuminousEnergy: LUMINOUS_ENERGY_UNITS,
    quantities.LuminousExposure: LUMINOUS_EXPOSURE_UNITS,
    quantities.LuminousFlux: LUMINOUS_FLUX_UNITS,
    quantities.LuminousIntensity: LUMINOUS_INTENSITY_UNITS,
    quantities.MagneticFieldStrength: MAGNETIC_FIELD_STRENGTH_UNITS,
    quantities.MagneticFlux: MAGNETIC_FLUX_UNITS,
    quantities.MagneticFluxDensity: MAGNETIC_FLUX_DENSITY_UNITS,
    quantities.Magnetization: MAGNETIZATION_UNITS,
    quantities.Mass: MASS_UNITS,
    quantities.Permeability: PERMEABILITY_UNITS,
    quantities.Permittivity: PERMITTIVITY_UNITS,
    quantities.Power: POWER_UNITS,
    quantities.Pressure: PRESSURE_UNITS,
    quantities.SpecificActivity: SPECIFIC_ACTIVITY_UNITS,
    quantities.SpecificCharge: SPECIFIC_CHARGE_UNITS,
    quantities.SpecificCurrent: SPECIFIC_CURRENT_UNITS,
    quantities.SpecificEnergy: SPECIFIC_ENERGY_UNITS,
    quantities.SpecificEntropy: SPECIFIC_ENTROPY_UNITS,
    quantities.SpecificHeatCapacity: SPECIFIC_HEAT_CAPACITY_UNITS,
    quantities.SpecificPower: SPECIFIC_POWER_UNITS,
    quantities.SurfaceActivity: SURFACE_ACTIVITY_UNITS,
    quantities.SurfaceChargeDensity: SURFACE_CHARGE_DENSITY_UNITS,
    quantities.SurfaceTension: SURFACE_TENSION_UNITS,
    quantities.Stress: STRESS_UNITS,
    quantities.Proportion: PROPORTION_UNITS,
    quantities.Reactance: REACTANCE_UNITS,
    quantities.Resistance: RESISTANCE_UNITS,
    quantities.SampleRate: SAMPLE_RATE_UNITS,
    quantities.SamplingPeriod: SAMPLING_PERIOD_UNITS,
    quantities.Snap: SNAP_UNITS,
    quantities.SolidAngle: SOLID_ANGLE_UNITS,
    quantities.Temperature: TEMPERATURE_UNITS,
    quantities.TemperatureDelta: TEMPERATURE_DELTA_UNITS,
    quantities.Time: TIME_UNITS,
    quantities.TimeCubed: TIME_CUBED_UNITS,
    quantities.TimeFourthPower: TIME_FOURTH_POWER_UNITS,
    quantities.TimeSquared: TIME_SQUARED_UNITS,
    quantities.Velocity: VELOCITY_UNITS,
    quantities.Voltage: VOLTAGE_UNITS,
    quantities.Volume: VOLUME_UNITS,
    quantities.VolumeChargeDensity: VOLUME_CHARGE_DENSITY_UNITS,
    quantities.VolumetricFlowRate: VOLUMETRIC_FLOW_RATE_UNITS,
}

for _quantity_type, _table in _TABLE_OF.items():
    bind_units(
        _quantity_type,
        (INSTANT_SECOND,) if _quantity_type is quantities.Instant else units_of(_table),
    )
    bind_table(_quantity_type, _table)
"""Each quantity type displays in the units of its own table, and parse reads them.

A unit of one quantity that shares the type's dimension (a `baud` for a `frequency`) is
not accepted by another.
"""

_LADDERS_OF = {
    quantities.AbsorbedDose: ABSORBED_DOSE_LADDERS,
    quantities.AbsorbedDoseRate: ABSORBED_DOSE_RATE_LADDERS,
    quantities.Acceleration: ACCELERATION_LADDERS,
    quantities.Activity: ACTIVITY_LADDERS,
    quantities.ActivityConcentration: ACTIVITY_CONCENTRATION_LADDERS,
    quantities.AmountOfSubstance: AMOUNT_OF_SUBSTANCE_LADDERS,
    quantities.ApparentPower: APPARENT_POWER_LADDERS,
    quantities.BaudRate: BAUD_RATE_LADDERS,
    quantities.Capacitance: CAPACITANCE_LADDERS,
    quantities.CatalyticActivity: CATALYTIC_ACTIVITY_LADDERS,
    quantities.Charge: CHARGE_LADDERS,
    quantities.Conductance: CONDUCTANCE_LADDERS,
    quantities.Current: CURRENT_LADDERS,
    quantities.CurrentDensity: CURRENT_DENSITY_LADDERS,
    quantities.Data: DATA_LADDERS,
    quantities.DataRate: DATA_RATE_LADDERS,
    quantities.Density: DENSITY_LADDERS,
    quantities.DynamicViscosity: DYNAMIC_VISCOSITY_LADDERS,
    quantities.ElectricFieldStrength: ELECTRIC_FIELD_STRENGTH_LADDERS,
    quantities.ElectricFluxDensity: SURFACE_CHARGE_DENSITY_LADDERS,
    quantities.Energy: ENERGY_LADDERS,
    quantities.EnergyDensity: ENERGY_DENSITY_LADDERS,
    quantities.Entropy: HEAT_CAPACITY_LADDERS,
    quantities.EquivalentDose: EQUIVALENT_DOSE_LADDERS,
    quantities.EquivalentDoseRate: EQUIVALENT_DOSE_RATE_LADDERS,
    quantities.Exposure: EXPOSURE_LADDERS,
    quantities.ExposureRate: EXPOSURE_RATE_LADDERS,
    quantities.Fluence: FLUENCE_LADDERS,
    quantities.Force: FORCE_LADDERS,
    quantities.Frequency: FREQUENCY_LADDERS,
    quantities.HeatCapacity: HEAT_CAPACITY_LADDERS,
    quantities.HeatFlux: HEAT_FLUX_LADDERS,
    quantities.Illuminance: ILLUMINANCE_LADDERS,
    quantities.Impedance: RESISTANCE_LADDERS,
    quantities.Impulse: IMPULSE_LADDERS,
    quantities.Inductance: INDUCTANCE_LADDERS,
    quantities.Jerk: JERK_LADDERS,
    quantities.Length: LENGTH_LADDERS,
    quantities.LinearChargeDensity: LINEAR_CHARGE_DENSITY_LADDERS,
    quantities.Luminance: LUMINANCE_LADDERS,
    quantities.LuminousExposure: LUMINOUS_EXPOSURE_LADDERS,
    quantities.LuminousFlux: LUMINOUS_FLUX_LADDERS,
    quantities.MagneticFieldStrength: MAGNETIC_FIELD_STRENGTH_LADDERS,
    quantities.MagneticFlux: MAGNETIC_FLUX_LADDERS,
    quantities.MagneticFluxDensity: MAGNETIC_FLUX_DENSITY_LADDERS,
    quantities.Magnetization: MAGNETIC_FIELD_STRENGTH_LADDERS,
    quantities.Mass: MASS_LADDERS,
    quantities.MassFlowRate: MASS_FLOW_RATE_LADDERS,
    quantities.Molality: MOLALITY_LADDERS,
    quantities.MolarCharge: MOLAR_CHARGE_LADDERS,
    quantities.MolarConcentration: MOLAR_CONCENTRATION_LADDERS,
    quantities.MolarEnergy: MOLAR_ENERGY_LADDERS,
    quantities.MolarEntropy: MOLAR_HEAT_CAPACITY_LADDERS,
    quantities.MolarFlowRate: MOLAR_FLOW_RATE_LADDERS,
    quantities.MolarHeatCapacity: MOLAR_HEAT_CAPACITY_LADDERS,
    quantities.MolarMass: MOLAR_MASS_LADDERS,
    quantities.MomentOfInertia: MOMENT_OF_INERTIA_LADDERS,
    quantities.Permeability: PERMEABILITY_LADDERS,
    quantities.Permittivity: PERMITTIVITY_LADDERS,
    quantities.Power: POWER_LADDERS,
    quantities.Pressure: PRESSURE_LADDERS,
    quantities.Reactance: RESISTANCE_LADDERS,
    quantities.ReactivePower: REACTIVE_POWER_LADDERS,
    quantities.Resistance: RESISTANCE_LADDERS,
    quantities.SampleRate: SAMPLE_RATE_LADDERS,
    quantities.SamplingPeriod: TIME_LADDERS,
    quantities.Snap: SNAP_LADDERS,
    quantities.SolidAngle: SOLID_ANGLE_LADDERS,
    quantities.SpecificActivity: SPECIFIC_ACTIVITY_LADDERS,
    quantities.SpecificCharge: SPECIFIC_CHARGE_LADDERS,
    quantities.SpecificCurrent: SPECIFIC_CURRENT_LADDERS,
    quantities.SpecificEnergy: SPECIFIC_ENERGY_LADDERS,
    quantities.SpecificEntropy: SPECIFIC_HEAT_CAPACITY_LADDERS,
    quantities.SpecificHeatCapacity: SPECIFIC_HEAT_CAPACITY_LADDERS,
    quantities.SpecificPower: SPECIFIC_POWER_LADDERS,
    quantities.Stress: PRESSURE_LADDERS,
    quantities.SurfaceActivity: SURFACE_ACTIVITY_LADDERS,
    quantities.SurfaceChargeDensity: SURFACE_CHARGE_DENSITY_LADDERS,
    quantities.SurfaceTension: SURFACE_TENSION_LADDERS,
    quantities.Temperature: TEMPERATURE_LADDERS,
    quantities.TemperatureDelta: TEMPERATURE_DELTA_LADDERS,
    quantities.ThermalConductivity: THERMAL_CONDUCTIVITY_LADDERS,
    quantities.Time: TIME_LADDERS,
    quantities.Torque: TORQUE_LADDERS,
    quantities.Voltage: VOLTAGE_LADDERS,
    quantities.Volume: VOLUME_LADDERS,
    quantities.VolumeChargeDensity: VOLUME_CHARGE_DENSITY_LADDERS,
    quantities.VolumetricFlowRate: VOLUMETRIC_FLOW_RATE_LADDERS,
}

for _quantity_type, _ladders in _LADDERS_OF.items():
    bind_ladders(_quantity_type, _ladders)
"""Each quantity type with a ladder moves along it in `auto_scale`.

A type that is not listed shows a measurement in the unit it was given.
"""

bind_clock_units(quantities.Time, CLOCK_UNITS)
"""A time splits into these units in `clock_parts`, the largest first."""

# Export rule, for every package under `kuchka.units` and `kuchka.quantities`.
# A leaf module owns the only hand-written `__all__`, naming exactly what it defines.
# A package composes its own `__all__` from its leaves with `__all__ += leaf.__all__`,
# and the package above composes its own from the packages'.
# This file star-imports every leaf directly, because the type checkers do not follow
# a star import through two packages.
# A new leaf therefore takes a wildcard import here, plus its module import, its
# wildcard import, and its `__all__ +=` in its own package; a test fails if one is
# missing.
__all__: list[str] = []
__all__ += amount.__all__
__all__ += angular.__all__
__all__ += chemistry.__all__
__all__ += current.__all__
__all__ += electromagnetics.__all__
__all__ += geometry.__all__
__all__ += information.__all__
__all__ += kinematics.__all__
__all__ += length.__all__
__all__ += logarithmic.__all__
__all__ += luminous_intensity.__all__
__all__ += mass.__all__
__all__ += mechanics.__all__
__all__ += photometry.__all__
__all__ += proportion.__all__
__all__ += radiation.__all__
__all__ += solid_angle.__all__
__all__ += temporal.__all__
__all__ += thermal.__all__
__all__ += thermodynamics.__all__
