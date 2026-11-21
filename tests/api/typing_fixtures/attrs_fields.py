"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of `kuchka.attrs.parse_field` in an `attrs` class: the attribute is
the exact quantity type, the `__init__` takes what the converter reads, and a bare
number for a field that needs a unit is refused before the program runs.
`pyright` holds it; `mypy` does not yet, because its `attrs` plugin reads only named
functions, types, and lambdas as converters, and the test for `mypy` is an `xfail` that
fails when `mypy` starts to hold it (see the ticket on typing `attrs` quantity fields).
"""

import attrs

from kuchka import Ampere
from kuchka import Current
from kuchka import Proportion
from kuchka import Volt
from kuchka import Voltage
from kuchka.attrs import parse_field


@attrs.define(frozen=True)
class SensorSpec:
    """A threshold and a duty, each converted by its field."""

    threshold: Voltage = attrs.field(converter=parse_field(Voltage))
    duty: Proportion = attrs.field(converter=parse_field(Proportion))


# What the converters read is what `__init__` takes.
from_text = SensorSpec("2800 mV", 0.25)  # OK
from_instances = SensorSpec(Volt(3.3), "25 %")  # OK
from_mapping = SensorSpec({"value": "2800", "unit": "mV"}, 0.25)  # OK
from_a_ratio_number = SensorSpec("1 V", 1)  # OK

# The attribute is the exact type, whatever arrived.
threshold: Voltage = from_text.threshold  # OK
duty: Proportion = from_text.duty  # OK
wrong_attribute: Current = from_text.threshold  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# A number needs its unit, and a proportion is the one quantity without one.
_bare_number = SensorSpec(3.3, 0.25)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_wrong_quantity = SensorSpec(Ampere(1), 0.25)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_not_a_quantity_type = parse_field(Volt)  # type: ignore[call-overload]  # ty: ignore[no-matching-overload]
