"""Quantity fields for Pydantic v2 models.

    from typing import Annotated

    from pydantic import BaseModel

    from kuchka import Voltage
    from kuchka.pydantic import Quantity


    class PowerSupplyConfig(BaseModel):
        max_voltage: Annotated[Voltage, Quantity]

A field annotated `Annotated[Voltage, Quantity]` holds a `Voltage` whatever arrived.
Validation is `kuchka.wire.load` for the field's quantity type: an instance passes
through, text such as `"2800 mV"` or `"1/3 V"` is read, a mapping of a `"value"` and a
`"unit"` is read, and a `Proportion` field reads a number as well.
Everything else is a Pydantic `ValidationError`, since the refusals of `load` are
`ParseError`s, which are `ValueError`s: a bare number for a voltage, a unit the type
does not have, a measurement of another quantity type.
Serialization is `kuchka.wire.dump`: `model_dump()` keeps the quantity object, and
`model_dump(mode="json")` and `model_dump_json()` write the text, such as `"2800 mV"`,
which validation reads back exactly.
The JSON Schema of a field is a string with a description that names the quantity.

The module imports `pydantic`, an extra of the package (`kuchka[pydantic]`); the
quantity classes themselves carry no Pydantic code, and `import kuchka` loads none.

Static types
------------
The attribute is the exact quantity type under `mypy` and `pyright`.
A model's `__init__` takes the annotated type, `Voltage`, so a string is checked
statically only through the validating entry points, `model_validate` and
`model_validate_json`, which is where data from a file or a payload enters;
`PowerSupplyConfig(max_voltage="2800 mV")` is reported by both checkers and works
at runtime.

Archaic units
-------------
`Quantity(allow_archaic=True)` reads the archaic units that the application imported,
as `parse` does with the same argument.

Examples
--------
>>> from typing import Annotated
>>> from pydantic import BaseModel
>>> from pydantic import ValidationError
>>> from kuchka import Volt
>>> from kuchka import Voltage
>>> class PowerSupplyConfig(BaseModel):
...     max_voltage: Annotated[Voltage, Quantity]
>>> config = PowerSupplyConfig.model_validate({"max_voltage": "2800 mV"})
>>> config.max_voltage
2800 mV
>>> config.model_dump_json()
'{"max_voltage":"2800 mV"}'
>>> PowerSupplyConfig.model_validate_json(config.model_dump_json()) == config
True
>>> PowerSupplyConfig(max_voltage=Volt(3.3)).max_voltage
3.3 V

A value that is no voltage is a validation error:

>>> try:
...     PowerSupplyConfig.model_validate({"max_voltage": 3.3})
... except ValidationError as error:
...     print(error.errors()[0]["msg"])  # doctest: +ELLIPSIS
Value error, 3.3 has no unit, so it does not say what it measures; ...

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any

try:
    from pydantic_core import core_schema
except (
    ImportError
) as exc:  # pragma: no cover -- the module is for installs with pydantic
    msg = "kuchka.pydantic needs pydantic: `pip install kuchka[pydantic]`."
    raise ImportError(msg) from exc

from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.reading import example_unit
from kuchka.internal.reading import unit_table_of
from kuchka.quantities import Proportion
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.wire import dump
from kuchka.wire import load

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pydantic import GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import CoreSchema

_METADATA_KEY = "kuchka.quantity"


def _to_json(value: object) -> object:
    """Write a quantity as its text, and leave a text, such as a default, as it is.

    A default is serialized into the JSON Schema before it is validated, and a text
    is already the written form.
    """
    if isinstance(value, _ScalarStorage):
        return dump(value)
    if isinstance(value, str):
        return value
    msg = f"cannot write {type(value).__name__} ({value!r}) as a quantity."
    raise TypeError(msg)


@dataclass(frozen=True)
class _Quantity:
    """The `Annotated` marker that makes a field a quantity; see `Quantity`."""

    allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny

    def __call__(
        self, *, allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny
    ) -> _Quantity:
        """Return a marker that reads archaic units as `allow_archaic` says."""
        archaic_policy_of(allow_archaic)
        return _Quantity(allow_archaic)

    def __get_pydantic_core_schema__(
        self,
        source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Return the schema of a field of the quantity type `source`."""
        quantity = source
        unit_table_of(quantity)
        policy = archaic_policy_of(self.allow_archaic)

        def validate(value: object) -> Any:  # noqa: ANN401 -- an instance of `quantity`
            return load(value, quantity, allow_archaic=policy)

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                _to_json, when_used="json"
            ),
            metadata={_METADATA_KEY: quantity},
        )

    def __get_pydantic_json_schema__(
        self,
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Return the JSON Schema of a quantity field: its text, and a number if any."""
        quantity = (schema.get("metadata") or {}).get(_METADATA_KEY)
        if quantity is None:  # pragma: no cover -- a wrapper that dropped the metadata
            return {"type": "string", "description": "A number and a unit."}
        if issubclass(quantity, Proportion):
            return {
                "anyOf": [{"type": "string"}, {"type": "number"}],
                "description": (
                    f"A {quantity.__name__}, written as a number, such as "
                    '"0.25", or as a number and a unit, such as "25 %".'
                ),
            }
        example = f"5 {example_unit(unit_table_of(quantity))}"
        return {
            "type": "string",
            "description": (
                f"A {quantity.__name__}, written as a number and a unit, "
                f'such as "{example}".'
            ),
            "examples": [example],
        }


Quantity = _Quantity()
"""The marker for `Annotated[Voltage, Quantity]`; `Quantity(allow_archaic=True)` reads
archaic units."""

__all__ = ["Quantity"]
