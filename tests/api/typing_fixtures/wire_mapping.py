"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of `kuchka.wire.to_dict` and `kuchka.wire.from_dict`: a measurement
is written as a mapping of JSON values, and a mapping, and only a mapping, is read as
the quantity type that is asked for.
"""

from kuchka import Celsius
from kuchka import Current
from kuchka import Volt
from kuchka import Voltage
from kuchka import wire
from kuchka.units.thermal import KELVIN

mapping: dict[str, str | int | float] = wire.to_dict(Volt(1))  # OK
converted = wire.to_dict(Volt(1), unit="mV", form=wire.ValueForm.Float)  # OK
in_kelvin = wire.to_dict(Celsius(20), unit=KELVIN)  # OK
_bool_form = wire.to_dict(Volt(1), form=True)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_not_a_unit = wire.to_dict(Volt(1), unit=5)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_not_a_measurement = wire.to_dict(Voltage)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# The quantity type that is asked for is the one that is read.
read: Voltage = wire.from_dict({"value": "5", "unit": "V"}, Voltage)  # OK
wrong_type: Current = wire.from_dict(mapping, Voltage)  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
_from_text = wire.from_dict("5 V", Voltage)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_not_a_quantity_type = wire.from_dict(mapping, Volt)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
