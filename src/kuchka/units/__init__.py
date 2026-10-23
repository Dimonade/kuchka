"""Engineer-facing unit constructors, one module per physical dimension.

    from kuchka import Volt, Milliampere

    voltage = Volt(4.2)
    current = Milliampere(150)
    power = voltage * current

Each quantity's canonical unit (the one arithmetic results come back in, e.g.
``Voltage * Current`` yields a result expressed in ``Watt``) is assigned onto the
corresponding domain class from ``kuchka.quantities`` at the bottom of the module that
owns that dimension.

Each leaf module owns one hand-written ``__all__`` naming exactly what it defines.
This package imports each leaf and composes its own ``__all__`` from theirs, so adding
a unit to an existing dimension never requires touching this file.
A new leaf module needs three lines here (its module import, its wildcard import, and
its ``__all__ +=``), and ``tests/test_public_api_surface.py`` fails if one is missing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from kuchka import quantities
from kuchka.internal.unit_table import units_of
from kuchka.quantities.base.units import bind_table
from kuchka.quantities.base.units import bind_units
from kuchka.units import ac_power
from kuchka.units import activity
from kuchka.units import amount
from kuchka.units import angular
from kuchka.units import angular_velocity
from kuchka.units import area
from kuchka.units import charge
from kuchka.units import conductance
from kuchka.units import current
from kuchka.units import data
from kuchka.units import data_rate
from kuchka.units import density
from kuchka.units import energy
from kuchka.units import energy_density
from kuchka.units import length
from kuchka.units import logarithmic
from kuchka.units import luminous_intensity
from kuchka.units import mass
from kuchka.units import power
from kuchka.units import pressure
from kuchka.units import proportion
from kuchka.units import resistance
from kuchka.units import stress
from kuchka.units import thermal
from kuchka.units import torque
from kuchka.units import voltage
from kuchka.units import volume
from kuchka.units.ac_power import *
from kuchka.units.activity import *
from kuchka.units.amount import *
from kuchka.units.angular import *
from kuchka.units.angular_velocity import *
from kuchka.units.area import *
from kuchka.units.charge import *
from kuchka.units.conductance import *
from kuchka.units.current import *
from kuchka.units.data import *
from kuchka.units.data_rate import *
from kuchka.units.density import *
from kuchka.units.energy import *
from kuchka.units.energy_density import *
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import force
from kuchka.units.kinematics import velocity
from kuchka.units.kinematics.acceleration import *
from kuchka.units.kinematics.force import *
from kuchka.units.kinematics.velocity import *
from kuchka.units.length import *
from kuchka.units.logarithmic import *
from kuchka.units.luminous_intensity import *
from kuchka.units.mass import *
from kuchka.units.power import *
from kuchka.units.pressure import *
from kuchka.units.proportion import *
from kuchka.units.resistance import *
from kuchka.units.stress import *
from kuchka.units.temporal import baud_rate
from kuchka.units.temporal import frequency
from kuchka.units.temporal import instant
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import sampling_period
from kuchka.units.temporal import time
from kuchka.units.temporal.baud_rate import *
from kuchka.units.temporal.frequency import *
from kuchka.units.temporal.instant import *
from kuchka.units.temporal.sample_rate import *
from kuchka.units.temporal.sampling_period import *
from kuchka.units.temporal.time import *
from kuchka.units.thermal import *
from kuchka.units.torque import *
from kuchka.units.voltage import *
from kuchka.units.volume import *

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
    quantities.Instant: INSTANT_UNITS,
    quantities.Length: LENGTH_UNITS,
    quantities.LogarithmicRatio: LOGARITHMIC_RATIO_UNITS,
    quantities.LuminousIntensity: LUMINOUS_INTENSITY_UNITS,
    quantities.Mass: MASS_UNITS,
    quantities.Power: POWER_UNITS,
    quantities.Pressure: PRESSURE_UNITS,
    quantities.Stress: STRESS_UNITS,
    quantities.Proportion: PROPORTION_UNITS,
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

__all__: list[str] = []
__all__ += ac_power.__all__
__all__ += activity.__all__
__all__ += amount.__all__
__all__ += angular.__all__
__all__ += angular_velocity.__all__
__all__ += area.__all__
__all__ += charge.__all__
__all__ += data.__all__
__all__ += data_rate.__all__
__all__ += conductance.__all__
__all__ += current.__all__
__all__ += density.__all__
__all__ += energy.__all__
__all__ += energy_density.__all__
__all__ += length.__all__
__all__ += logarithmic.__all__
__all__ += luminous_intensity.__all__
__all__ += mass.__all__
__all__ += power.__all__
__all__ += pressure.__all__
__all__ += stress.__all__
__all__ += proportion.__all__
__all__ += resistance.__all__
__all__ += thermal.__all__
__all__ += voltage.__all__
__all__ += volume.__all__
__all__ += torque.__all__
__all__ += acceleration.__all__
__all__ += force.__all__
__all__ += velocity.__all__
__all__ += baud_rate.__all__
__all__ += frequency.__all__
__all__ += instant.__all__
__all__ += sample_rate.__all__
__all__ += sampling_period.__all__
__all__ += time.__all__
