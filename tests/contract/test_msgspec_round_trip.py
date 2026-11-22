"""`msgspec` round-trips every unit of every quantity type, exactly.

JSON encoded with the hook decodes back into the same value in the same unit, for every
published unit and every shape.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from tests.support.kinds import UNIT_TABLES
from tests.support.libraries import require_or_skip

require_or_skip("msgspec")

import msgspec.json

from kuchka.msgspec import kuchka_dec_hook
from kuchka.msgspec import kuchka_enc_hook

MAGNITUDES = (Fraction(0), Fraction(5), Fraction(7, 3), Fraction(21, 5))
UNITS = [
    (name, unit.symbol) for name, table in UNIT_TABLES.items() for unit in table.units
]


@pytest.mark.parametrize(
    ("name", "symbol"), UNITS, ids=[f"{name}-{symbol}" for name, symbol in UNITS]
)
def test_every_unit_round_trips_through_json(name: str, symbol: str) -> None:
    table = UNIT_TABLES[name]
    for magnitude in MAGNITUDES:
        original = table[symbol](magnitude)
        raw = msgspec.json.encode(original, enc_hook=kuchka_enc_hook)
        restored = msgspec.json.decode(
            raw, type=type(original), dec_hook=kuchka_dec_hook
        )
        assert restored == original
        assert restored.unit is original.unit
