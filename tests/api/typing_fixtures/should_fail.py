"""Not a pytest file directly-- run through mypy directly.

Every line below is something the design proposal explicitly says must be a type error,
not just a runtime one.
`reveal_type()`` calls double as documentation of what mypy infers.
"""

from decimal import Decimal
from fractions import Fraction

from kuchka import Ampere
from kuchka import AngularVelocity
from kuchka import Area
from kuchka import Baud
from kuchka import BaudRate
from kuchka import Celsius
from kuchka import Conductance
from kuchka import ConvertibleToFrequency
from kuchka import CubicMetre
from kuchka import Current
from kuchka import Decibel
from kuchka import DegreeDisplacement
from kuchka import Energy
from kuchka import EnergyDensity
from kuchka import Fahrenheit
from kuchka import Frequency
from kuchka import Gibibyte
from kuchka import Hertz
from kuchka import Joule
from kuchka import Length
from kuchka import LogarithmicRatio
from kuchka import MegabitPerSecond
from kuchka import Meter
from kuchka import Newton
from kuchka import NewtonMetre
from kuchka import Ohm
from kuchka import Percent
from kuchka import Power
from kuchka import Pressure
from kuchka import Proportion
from kuchka import RadianDisplacement
from kuchka import RadianPerSecond
from kuchka import Ratio
from kuchka import Resistance
from kuchka import SampleRate
from kuchka import SamplesPerSecond
from kuchka import SamplingPeriod
from kuchka import Second
from kuchka import Siemens
from kuchka import SquareMetre
from kuchka import Time
from kuchka import Torque
from kuchka import Volt
from kuchka import Voltage
from kuchka import Volume
from kuchka import Watt


def analyse_voltage(_voltage: Voltage) -> None: ...


# Naked numerics must be statically rejected.
analyse_voltage(4.2)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Incompatible dimensions must be statically rejected.
analyse_voltage(Ampere(2))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Temperature cannot be scaled as no __mul__ exists on it at all.
_scale_temp_a = Celsius(20) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_scale_temp_b = 2 * Celsius(20)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_scale_temp_c = Fahrenheit(68) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_scale_temp_d = 2 * Fahrenheit(68)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

_bad_add = Volt(5) + Ampere(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_sub = Volt(5) - Ampere(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_temp_add = Celsius(20) + Celsius(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_fahrenheit_add = Fahrenheit(68) + Fahrenheit(9)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

# Things that are OK to do.
power: Power = Volt(5) * Ampere(2)  # OK: statically known to be Power.
current: Current = Watt(10) / Volt(5)  # OK: statically known to be Current.
resistance: Resistance = Volt(5) / Ampere(2)  # OK: statically known to be Resistance.

# And things that are not OK to do.
wrong: Current = Volt(5) * Ampere(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Frequency and SampleRate share a dimension but must be rejected as statically
# incompatible, the same way Voltage and Current are.
_bad_temporal_add = Hertz(50) + SamplesPerSecond(50)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

# Reciprocals of the registered pair fall out of the general `1 / x` mechanism and are
# statically precise about which type they produce.
reciprocal_of_time: Frequency = 1 / Second(2)  # OK: statically known to be Frequency.
reciprocal_of_frequency: Time = 1 / Hertz(50)  # OK: statically known to be Time.
wrong_temporal_reciprocal: SampleRate = 1 / Second(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# SamplingPeriod and SampleRate are reciprocals of each other specifically, not of
# Time/Frequency, even though they share the same dimensions.
reciprocal_of_sampling_period: SampleRate = 1 / Second(2).to_sampling_period()  # OK
reciprocal_of_sample_rate: SamplingPeriod = 1 / SamplesPerSecond(500)  # OK
wrong_sampling_reciprocal: SamplingPeriod = 1 / Second(2).to_sampling_period()  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# BaudRate has no reciprocal and no to_frequency(): both are deliberately unmodelled,
# so neither should exist as an attribute at all.
_no_as_frequency = Baud(9600).to_frequency()  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def take_frequency_like(value: ConvertibleToFrequency) -> Frequency:
    return value.to_frequency()


# BaudRate does not satisfy ConvertibleToFrequency: it has no to_frequency().
take_frequency_like(Baud(9600))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Frequency and SampleRate do satisfy it.
take_frequency_like(Hertz(50))
take_frequency_like(SamplesPerSecond(500))

# BaudRate still type-checks against its own type, same as any other quantity.
baud_rate: BaudRate = Baud(9600)

# Percent and Ratio construct the same type, the Volt/Millivolt shape, not a
# domain-specific sibling like SampleRate/BaudRate.
tolerance: Proportion = Percent(5)
duty_cycle: Proportion = Ratio(Decimal("0.8"))

# A Proportion is still statically incompatible with a dimensioned quantity:
# dimensionless is not the same as "any dimension".
_bad_proportion_add = Percent(5) + Volt(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

# Multiplying a dimensioned quantity by a Proportion keeps its type, statically too.
scaled_voltage: Voltage = Volt(5) * Ratio(Decimal("0.1"))  # OK: statically a Voltage.

# Length * Length is statically known to produce Area, and Area * Length / Length *
# Area both statically produce Volume -- the same overload-table shape Voltage,
# Current, Power, and Resistance already get for the power triangle.
area: Area = Meter(5) * Meter(2)  # OK: statically known to be Area.
volume_a: Volume = area * Meter(3)  # OK: statically known to be Volume.
volume_b: Volume = Meter(3) * area  # OK: statically known to be Volume.
side: Length = area / Meter(5)  # OK: statically known to be Length.
base: Area = volume_a / Meter(3)  # OK: statically known to be Area.
height: Length = volume_a / area  # OK: statically known to be Length.

# Area * Length is Volume, not Area -- the fallback `object` overload accepts the
# assignment statically (the same known gap Ohm(5) * Ohm(2) already has), and only
# the runtime type actually disagrees.
wrong_area: Area = area * Meter(3)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Energy / Volume is an EnergyDensity, and Force / Area a Pressure: the two kinds share
# a dimension, and the overloads tell them apart.
density_of_energy: EnergyDensity = Joule(5) / CubicMetre(
    1
)  # OK: statically an EnergyDensity.
pressure_of_force: Pressure = Newton(5) / SquareMetre(1)  # OK: statically a Pressure.
energy_back: Energy = density_of_energy * CubicMetre(2)  # OK: statically an Energy.
volume_back: Volume = Joule(5) / density_of_energy  # OK: statically a Volume.
wrong_kind: Pressure = Joule(5) / CubicMetre(1)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# A quotient of two quantities of one dimension is a Proportion, and a product of two
# proportions stays one.
voltage_ratio: Proportion = Volt(5) / Volt(2)  # OK: statically a Proportion.
pressure_ratio: Proportion = (
    pressure_of_force / density_of_energy
)  # OK: kinds that share a dimension.
tolerance_squared: Proportion = Percent(5) * Percent(5)  # OK: statically a Proportion.
wrong_voltage_ratio: Fraction = Volt(5) / Volt(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Resistance and Conductance are reciprocals of each other, the same shape
# Time/Frequency already have, and Ohm's law works from either side of that
# reciprocal.
conductance: Conductance = 1 / Ohm(5)  # OK: statically known to be Conductance.
resistance_back: Resistance = 1 / Siemens(Decimal("0.2"))  # OK: back to Resistance.
current_via_conductance: Current = Volt(10) * Siemens(Decimal("0.5"))  # OK: Current.
conductance_via_current: Conductance = Ampere(5) / Volt(10)  # OK: Conductance.
voltage_via_conductance: Voltage = Ampere(5) / Siemens(Decimal("0.5"))  # OK: Voltage.

# The reciprocal only narrows for the two registered canonical types -- a plain
# assignment mismatch between them is still statically rejected.
wrong_conductance_reciprocal: Resistance = 1 / Ohm(5)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Levels add, subtract, and scale; they neither multiply each other nor mix with
# linear ratios or naked numbers.
_bad_level_mul = Decibel(3) * Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_level_add_ratio = Decibel(3) + Ratio(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_level_add_number = Decibel(3) + 3  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_bad_level_reciprocal = 2 / Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

cascade: LogarithmicRatio = Decibel(20) + Decibel(-3)  # OK: statically a level.
loss: LogarithmicRatio = Decibel(-0.2) * 30  # OK: scaling a level gives a level.
steps: Proportion = Decibel(6) / Decibel(3)  # OK: level over level is a proportion.
scaled_down: LogarithmicRatio = Decibel(6) / 3  # OK: level over a number is a level.
linear: Proportion = Decibel(3).to_power_ratio()  # OK: a linear ratio.
wrong_steps: LogarithmicRatio = Decibel(6) / Decibel(3)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# With the angle axis counted, torque is energy per angle and angular velocity is angle
# per time; the overloads tell them apart from energy and from the hertz.
torque_of_work: Torque = Joule(5) / RadianDisplacement(1)  # OK: a Torque.
work_back: Energy = torque_of_work * RadianDisplacement(2)  # OK: an Energy.
turn_rate: AngularVelocity = DegreeDisplacement(90) / Second(
    1
)  # OK: an AngularVelocity.
shaft_power: Power = NewtonMetre(2) * RadianPerSecond(5)  # OK: a Power.
shaft_torque: Torque = Watt(10) / RadianPerSecond(5)  # OK: a Torque.
wrong_torque_kind: Energy = Joule(5) / RadianDisplacement(1)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Data and DataRate have dimensions of their own: neither mixes with the other, with
# time, or with a frequency, which a bit rate is not.
_data_plus_rate = Gibibyte(4) + MegabitPerSecond(100)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_rate_plus_frequency = MegabitPerSecond(100) + Hertz(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
duration: Time = Gibibyte(4) / MegabitPerSecond(100)  # OK
wrong_duration: Frequency = Gibibyte(4) / MegabitPerSecond(100)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
