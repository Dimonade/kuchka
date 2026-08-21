"""Not a pytest file directly-- run through mypy directly.

Every line below is something the design proposal explicitly says must be a type error,
not just a runtime one.
`reveal_type()`` calls double as documentation of what mypy infers.
"""

from kuchka import Ampere
from kuchka import Celsius
from kuchka import Current
from kuchka import Power
from kuchka import Resistance
from kuchka import Volt
from kuchka import Voltage
from kuchka import Watt


def analyse_voltage(voltage: Voltage) -> None: ...


# Naked numerics must be statically rejected.
analyse_voltage(4.2)  # type: ignore

# Incompatible dimensions must be statically rejected.
analyse_voltage(Ampere(2))  # type: ignore

# Temperature cannot be scaled as no __mul__ exists on it at all.
_scale_temp_a = Celsius(20) * 2  # type: ignore
_scale_temp_b = 2 * Celsius(20)  # type: ignore

_bad_add = Volt(5) + Ampere(2)  # type: ignore
_bad_sub = Volt(5) - Ampere(2)  # type: ignore
_bad_temp_add = Celsius(20) + Celsius(5)  # type: ignore

# Things that are OK to do.
power: Power = Volt(5) * Ampere(2)  # OK: statically known to be Power
current: Current = Watt(10) / Volt(5)  # OK: statically known to be Current
resistance: Resistance = Volt(5) / Ampere(2)  # OK: statically known to be Resistance

# And things that are not OK to do.
wrong: Current = Volt(5) * Ampere(2)  # type: ignore
