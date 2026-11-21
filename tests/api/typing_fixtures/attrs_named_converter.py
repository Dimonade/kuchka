"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

A converter written as a named function, the form `mypy` reads: the attribute is the
exact quantity type, the `__init__` takes what the converter takes, and a bare number
is refused before the program runs, under both checkers.
"""

from collections.abc import Mapping

import attrs

from kuchka import Ampere
from kuchka import Current
from kuchka import Voltage
from kuchka import wire


def to_voltage(value: Voltage | str | Mapping[str, object]) -> Voltage:
    """Read a voltage from what a caller hands the class."""
    return wire.load(value, Voltage)


@attrs.define(frozen=True)
class Probe:
    """A limit, converted by its field."""

    limit: Voltage = attrs.field(converter=to_voltage)


from_text = Probe("2800 mV")  # OK
from_mapping = Probe({"value": "2800", "unit": "mV"})  # OK
limit: Voltage = from_text.limit  # OK
wrong_attribute: Current = from_text.limit  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
_bare_number = Probe(3.3)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_wrong_quantity = Probe(Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
