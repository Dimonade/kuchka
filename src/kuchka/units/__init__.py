"""Engineer-facing unit constructors, grouped by the physical dimension they measure.

from kuchka import Volt, Milliampere

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
from kuchka.quantities.base.units import bind_table
from kuchka.quantities.base.units import bind_units
from kuchka.units import amount
from kuchka.units import angular
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
from kuchka.units import proportion
from kuchka.units import radiation
from kuchka.units import temporal
from kuchka.units import thermal
from kuchka.units.amount import *
from kuchka.units.angular import *
from kuchka.units.current import *
from kuchka.units.electromagnetics.ac_power import *
from kuchka.units.electromagnetics.capacitance import *
from kuchka.units.electromagnetics.charge import *
from kuchka.units.electromagnetics.conductance import *
from kuchka.units.electromagnetics.impedance import *
from kuchka.units.electromagnetics.inductance import *
from kuchka.units.electromagnetics.magnetization import *
from kuchka.units.electromagnetics.magnetic_flux import *
from kuchka.units.electromagnetics.magnetic_flux_density import *
from kuchka.units.electromagnetics.permeability import *
from kuchka.units.electromagnetics.permittivity import *
from kuchka.units.electromagnetics.reactance import *
from kuchka.units.electromagnetics.resistance import *
from kuchka.units.electromagnetics.voltage import *
from kuchka.units.geometry.area import *
from kuchka.units.geometry.volume import *
from kuchka.units.information.data import *
from kuchka.units.information.data_rate import *
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.angular_velocity import *
from kuchka.units.kinematics.velocity import *
from kuchka.units.length import *
from kuchka.units.logarithmic import *
from kuchka.units.luminous_intensity import *
from kuchka.units.mass import *
from kuchka.units.mechanics.density import *
from kuchka.units.mechanics.energy import *
from kuchka.units.mechanics.energy_density import *
from kuchka.units.mechanics.force import *
from kuchka.units.mechanics.power import *
from kuchka.units.mechanics.pressure import *
from kuchka.units.mechanics.stress import *
from kuchka.units.mechanics.torque import *
from kuchka.units.proportion import *
from kuchka.units.radiation.activity import *
from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
from kuchka.units.temporal.instant import *
from kuchka.units.temporal.sample_rate import *
from kuchka.units.temporal.sampling_period import *
from kuchka.units.temporal.time import *
from kuchka.units.thermal import *

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_TABLE_OF: dict[type[Any], Mapping[str, Callable[..., Any]]] = {
    quantities.Acceleration: ACCELERATION_UNITS,
    quantities.Activity: ACTIVITY_UNITS,
    quantities.ApparentPower: APPARENT_POWER_UNITS,
    quantities.ReactivePower: REACTIVE_POWER_UNITS,
    quantities.AmountOfSubstance: AMOUNT_OF_SUBSTANCE_UNITS,
    quantities.Angle: ANGLE_UNITS,
    quantities.AngularDisplacement: ANGULAR_DISPLACEMENT_UNITS,
    quantities.AngularVelocity: ANGULAR_VELOCITY_UNITS,
    quantities.Torque: TORQUE_UNITS,
    quantities.Area: AREA_UNITS,
    quantities.BaudRate: BAUD_RATE_UNITS,
    quantities.Capacitance: CAPACITANCE_UNITS,
    quantities.Charge: CHARGE_UNITS,
    quantities.Conductance: CONDUCTANCE_UNITS,
    quantities.Current: CURRENT_UNITS,
    quantities.Data: DATA_UNITS,
    quantities.DataRate: DATA_RATE_UNITS,
    quantities.Density: DENSITY_UNITS,
    quantities.Energy: ENERGY_UNITS,
    quantities.EnergyDensity: ENERGY_DENSITY_UNITS,
    quantities.Force: FORCE_UNITS,
    quantities.Frequency: FREQUENCY_UNITS,
    quantities.Impedance: IMPEDANCE_UNITS,
    quantities.Inductance: INDUCTANCE_UNITS,
    quantities.Instant: INSTANT_UNITS,
    quantities.Length: LENGTH_UNITS,
    quantities.LogarithmicRatio: LOGARITHMIC_RATIO_UNITS,
    quantities.LuminousIntensity: LUMINOUS_INTENSITY_UNITS,
    quantities.MagneticFlux: MAGNETIC_FLUX_UNITS,
    quantities.MagneticFluxDensity: MAGNETIC_FLUX_DENSITY_UNITS,
    quantities.Magnetization: MAGNETIZATION_UNITS,
    quantities.Mass: MASS_UNITS,
    quantities.Permeability: PERMEABILITY_UNITS,
    quantities.Permittivity: PERMITTIVITY_UNITS,
    quantities.Power: POWER_UNITS,
    quantities.Pressure: PRESSURE_UNITS,
    quantities.Stress: STRESS_UNITS,
    quantities.Proportion: PROPORTION_UNITS,
    quantities.Reactance: REACTANCE_UNITS,
    quantities.Resistance: RESISTANCE_UNITS,
    quantities.SampleRate: SAMPLE_RATE_UNITS,
    quantities.SamplingPeriod: SAMPLING_PERIOD_UNITS,
    quantities.Temperature: TEMPERATURE_UNITS,
    quantities.TemperatureDelta: TEMPERATURE_DELTA_UNITS,
    quantities.Time: TIME_UNITS,
    quantities.Velocity: VELOCITY_UNITS,
    quantities.Voltage: VOLTAGE_UNITS,
    quantities.Volume: VOLUME_UNITS,
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
__all__ += proportion.__all__
__all__ += radiation.__all__
__all__ += temporal.__all__
__all__ += thermal.__all__
