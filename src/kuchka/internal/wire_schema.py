"""The JSON Schema of a quantity in its wire form, shared by the integrations.

A quantity is written as text such as `"5 V"`, and a `Proportion` may also be a number,
so the schema is a string whose description names the quantity and shows how it is
written; the text is what `kuchka.wire` reads and writes.
"""

from __future__ import annotations

from typing import Any

from kuchka.internal.reading import example_unit
from kuchka.internal.reading import unit_table_of
from kuchka.quantities import Proportion


def json_schema(quantity: type[Any]) -> dict[str, Any]:
    """Return the JSON Schema of a field of the quantity type `quantity`."""
    name = quantity.__name__
    if issubclass(quantity, Proportion):
        return {
            "anyOf": [{"type": "string"}, {"type": "number"}],
            "description": (
                f'A {name}, written as a number, such as "0.25", '
                'or as a number and a unit, such as "25 %".'
            ),
        }
    example = f"5 {example_unit(unit_table_of(quantity))}"
    return {
        "type": "string",
        "description": (
            f'A {name}, written as a number and a unit, such as "{example}".'
        ),
        "examples": [example],
    }


__all__ = ["json_schema"]
