"""A Pydantic field round-trips every unit of every quantity type, exactly.

JSON written by the model validates back into the same value in the same unit, for
every published unit and every shape.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Annotated
from typing import Any

import pytest

from tests.support.kinds import UNIT_TABLES
from tests.support.libraries import require_or_skip

require_or_skip("pydantic")

from pydantic import TypeAdapter

from kuchka.pydantic import Quantity

MAGNITUDES = (Fraction(0), Fraction(5), Fraction(7, 3), Fraction(21, 5))
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]
_ADAPTERS: dict[type, TypeAdapter[Any]] = {}


def _adapter(quantity: type) -> TypeAdapter[Any]:
    """Return the adapter of the field type `quantity`, built once."""
    if quantity not in _ADAPTERS:
        _ADAPTERS[quantity] = TypeAdapter(Annotated[quantity, Quantity])
    return _ADAPTERS[quantity]


@pytest.mark.parametrize(
    ("name", "symbol"), UNITS, ids=[f"{name}-{symbol}" for name, symbol in UNITS]
)
def test_every_unit_round_trips_through_json(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        original = table[symbol](magnitude)
        adapter = _adapter(type(original))
        restored = adapter.validate_json(adapter.dump_json(original))
        assert restored == original
        assert restored.unit is original.unit
        assert adapter.dump_python(original) is original
