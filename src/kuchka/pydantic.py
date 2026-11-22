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
from typing import TypeVar

try:
    from pydantic import PydanticSchemaGenerationError
    from pydantic_core import core_schema
except (
    ImportError
) as exc:  # pragma: no cover -- the module is for installs with pydantic
    msg = "kuchka.pydantic needs pydantic: `pip install kuchka[pydantic]`."
    raise ImportError(msg) from exc

from kuchka.bounds import Bounds as _Bounds
from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.reading import unit_table_of
from kuchka.internal.wire_schema import json_schema
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.wire import dump
from kuchka.wire import load

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pydantic import GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import CoreSchema

_METADATA_KEY = "kuchka.quantity"
_BOUNDS_KEY = "kuchka.bounds"
_QuantityT = TypeVar("_QuantityT", bound=_OrderedScalarMixin)


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


def _all_metadata(schema: CoreSchema, key: str) -> list[Any]:
    """Return what a field schema, and the schemas it wraps, stored under `key`."""
    found: list[Any] = []
    current: Any = schema
    while isinstance(current, dict):
        stored = (current.get("metadata") or {}).get(key)
        if stored is not None:
            found.append(stored)
        current = current.get("schema")
    return found


def _metadata_of(schema: CoreSchema, key: str) -> Any:  # noqa: ANN401 -- what was stored
    """Return what a field schema, or a schema it wraps, stored under `key`."""
    current: Any = schema
    while isinstance(current, dict):
        found = (current.get("metadata") or {}).get(key)
        if found is not None:
            return found
        current = current.get("schema")
    return None


class _BoundsWithoutQuantityError(TypeError):
    """`Bounds` found no `Quantity` inside it; a `Quantity` written after it takes over.

    Pydantic applies the annotation written last outermost, and `Quantity` builds the
    schema of the field itself, so bounds written before it are carried to it in this
    error, and an error no `Quantity` caught is the report that the annotation lacks
    one.
    """

    def __init__(self, source: object) -> None:
        name = getattr(source, "__name__", source)
        super().__init__(
            f"Bounds needs Quantity beside it in the annotation, as in "
            f"Annotated[{name}, Quantity, Bounds(...)]."
        )
        self.bounds: list[Bounds[Any]] = []


def _bounds_written_before(
    source: type[Any], handler: GetCoreSchemaHandler
) -> list[Bounds[Any]]:
    """Return the `Bounds` annotations written before `Quantity`, innermost first.

    What was written before `Quantity` is built inside it, and `Quantity` replaces the
    schema of the field, so it takes the bounds over: from the error a `Bounds` raises
    when nothing inside it can read the type, or from the schema when Pydantic can
    build one for the class (`arbitrary_types_allowed`).
    """
    try:
        inner = handler(source)
    except _BoundsWithoutQuantityError as exc:
        return exc.bounds
    except PydanticSchemaGenerationError:
        return []
    return list(reversed(_all_metadata(inner, _BOUNDS_KEY)))


def _checked(bounds: Bounds[Any], inner: CoreSchema) -> CoreSchema:
    """Return `inner` with the check of `bounds` after it."""
    return core_schema.no_info_after_validator_function(
        bounds.check, inner, metadata={_BOUNDS_KEY: bounds}
    )


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

        schema: CoreSchema = core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                _to_json, when_used="json"
            ),
            metadata={_METADATA_KEY: quantity},
        )
        for bounds in _bounds_written_before(source, handler):
            schema = _checked(bounds, schema)
        return schema

    def __get_pydantic_json_schema__(
        self,
        schema: CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """Return the JSON Schema of a quantity field: its text, and a number if any."""
        quantity = _metadata_of(schema, _METADATA_KEY)
        if quantity is None:  # pragma: no cover -- a schema that holds no quantity
            return {"type": "string", "description": "A number and a unit."}
        result = json_schema(quantity)
        for bounds in _all_metadata(schema, _BOUNDS_KEY):
            result["description"] += f" It is {bounds.describe()}."
        return result


class Bounds(_Bounds[_QuantityT]):
    """The range a quantity field accepts, as an `Annotated` marker after `Quantity`.

        max_voltage: Annotated[Voltage, Quantity, Bounds(gt=Volt(0), le=Volt(60))]

    `kuchka.bounds.Bounds` for Pydantic: a value outside the range is a validation
    error that writes the value and the bound, and the JSON Schema description of the
    field says the range.
    The marker sits beside `Quantity`, which reads the value the bounds check, and its
    bounds are of the quantity type of the field; a missing `Quantity` and bounds of
    another type are reported when the class is defined.
    The marker may be written before or after `Quantity`, and several markers may be
    given: each is checked and each adds its range to the JSON Schema description.
    Only a validated value is checked, so a default is checked when the model asks for
    its defaults to be validated.
    """

    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Return the schema of the field with the bounds checked after it is read."""
        if not (isinstance(source, type) and issubclass(source, self.quantity)):
            msg = (
                f"bounds of {self.quantity.__name__} on a field of "
                f"{getattr(source, '__name__', source)}: the bounds are of the type "
                "of the field."
            )
            raise TypeError(msg)
        try:
            inner = handler(source)
        except _BoundsWithoutQuantityError as exc:
            exc.bounds.append(self)
            raise
        except PydanticSchemaGenerationError as exc:
            error = _BoundsWithoutQuantityError(source)
            error.bounds.append(self)
            raise error from exc
        if _metadata_of(inner, _METADATA_KEY) is None:
            error = _BoundsWithoutQuantityError(source)
            error.bounds.append(self)
            raise error
        return _checked(self, inner)


Quantity = _Quantity()
"""The marker for `Annotated[Voltage, Quantity]`; `Quantity(allow_archaic=True)` reads
archaic units."""

__all__ = ["Bounds", "Quantity"]
