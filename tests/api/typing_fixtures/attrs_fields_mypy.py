"""Not a pytest file directly-- run through mypy, like `should_fail.py`.

What `mypy` makes of `attrs.field(converter=parse_field(Voltage))`: the attribute is the
exact quantity type, and the converter is one `mypy` does not read, since its `attrs`
plugin supports only named functions, types, and lambdas, so it reports the converter
and types the `__init__` parameter as `Any`.
`pyright` reads the converter in full (see `attrs_fields.py`).
The ignore below is the line `mypy` reports; when a `mypy` release reads such
converters, it becomes unused and this fixture fails, which is the moment to update
the documentation.
"""

import attrs

from kuchka import Voltage
from kuchka.attrs import parse_field


@attrs.define
class SensorSpec:
    """A threshold, converted by its field."""

    threshold: Voltage = attrs.field(converter=parse_field(Voltage))  # type: ignore[misc]


spec = SensorSpec("2800 mV")  # OK
threshold: Voltage = spec.threshold  # OK
