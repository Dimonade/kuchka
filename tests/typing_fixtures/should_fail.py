"""Not a pytest file directly-- run through mypy directly.

Every line below is something the design proposal explicitly says must be a type error,
not just a runtime one.
`reveal_type()`` calls double as documentation of what mypy infers.
"""

from kuchka import Ampere
from kuchka import Baud
from kuchka import BaudRate
from kuchka import Celsius
from kuchka import ConvertibleToFrequency
from kuchka import Current
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Power
from kuchka import Resistance
from kuchka import SampleRate
from kuchka import SamplesPerSecond
from kuchka import SamplingPeriod
from kuchka import Second
from kuchka import SecondSamplingPeriod
from kuchka import Time
from kuchka import Volt
from kuchka import Voltage
from kuchka import Watt


def analyse_voltage(voltage: Voltage) -> None: ...


# Naked numerics must be statically rejected.
analyse_voltage(4.2)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Incompatible dimensions must be statically rejected.
analyse_voltage(Ampere(2))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Temperature cannot be scaled as no __mul__ exists on it at all.
_scale_temp_a = Celsius(20) * 2  # type: ignore[operator]  # ty: ignore[unsupported-operator]
_scale_temp_b = 2 * Celsius(20)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

_bad_add = Volt(5) + Ampere(2)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types
_bad_sub = Volt(5) - Ampere(2)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types
_bad_temp_add = Celsius(20) + Celsius(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]

# Things that are OK to do.
power: Power = Volt(5) * Ampere(2)  # OK: statically known to be Power
current: Current = Watt(10) / Volt(5)  # OK: statically known to be Current
resistance: Resistance = Volt(5) / Ampere(2)  # OK: statically known to be Resistance

# And things that are not OK to do.
wrong: Current = Volt(5) * Ampere(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# Frequency and SampleRate share a dimension but must be rejected as
# statically incompatible, the same way Voltage and Current are.
_bad_temporal_add = Hertz(50) + SamplesPerSecond(50)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

# Reciprocals of the registered pair fall out of the general `1 / x`
# mechanism and are statically precise about which type they produce.
reciprocal_of_time: Frequency = 1 / Second(2)  # OK: statically known to be Frequency
reciprocal_of_frequency: Time = 1 / Hertz(50)  # OK: statically known to be Time
wrong_temporal_reciprocal: SampleRate = 1 / Second(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# SamplingPeriod and SampleRate are reciprocals of each other specifically,
# not of Time/Frequency, even though they share the same dimensions.
reciprocal_of_sampling_period: SampleRate = 1 / SecondSamplingPeriod(2)  # OK
reciprocal_of_sample_rate: SamplingPeriod = 1 / SamplesPerSecond(500)  # OK
wrong_sampling_reciprocal: SamplingPeriod = 1 / SecondSamplingPeriod(2)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# BaudRate has no reciprocal and no as_frequency(): both are deliberately
# unmodelled, so neither should exist as an attribute at all.
_no_as_frequency = Baud(9600).as_frequency()  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def take_frequency_like(value: ConvertibleToFrequency) -> Frequency:
    return value.as_frequency()


# BaudRate does not satisfy ConvertibleToFrequency: it has no as_frequency().
take_frequency_like(Baud(9600))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# Frequency and SampleRate do satisfy it.
take_frequency_like(Hertz(50))
take_frequency_like(SamplesPerSecond(500))

# BaudRate still type-checks against its own type, same as any other quantity.
baud_rate: BaudRate = Baud(9600)
