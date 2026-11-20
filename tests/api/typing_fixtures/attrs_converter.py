"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of the converter `kuchka.attrs.parse_field` returns, as both
checkers read it: it takes what `kuchka.wire.load` reads for the quantity, and returns
the exact quantity type.
"""

from kuchka import Ampere
from kuchka import Current
from kuchka import Proportion
from kuchka import Volt
from kuchka import Voltage
from kuchka.attrs import parse_field

convert = parse_field(Voltage)
convert_proportion = parse_field(Proportion)

# The converter returns the quantity type it is made for.
from_text: Voltage = convert("2800 mV")  # OK
from_instance: Voltage = convert(Volt(3.3))  # OK
from_mapping: Voltage = convert({"value": "2800", "unit": "mV"})  # OK
wrong_type: Current = convert("2800 mV")  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# A number needs its unit, and a proportion is the one quantity without one.
_bare_number = convert(3.3)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_wrong_quantity = convert(Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
ratio: Proportion = convert_proportion(0.25)  # OK
percent: Proportion = convert_proportion("25 %")  # OK

# Only a quantity type with units has a converter.
_not_a_quantity_type = parse_field(Volt)  # type: ignore[call-overload]  # ty: ignore[no-matching-overload]
