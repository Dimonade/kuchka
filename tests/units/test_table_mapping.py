"""A table is a read-only mapping from display symbol to constructor."""

from __future__ import annotations

import pytest

from tests.units.table_fixtures import BASE
from tests.units.table_fixtures import MEGA
from tests.units.table_fixtures import MILLI
from tests.units.table_fixtures import TABLE
from tests.units.table_fixtures import make_ctor


def test_iteration_yields_each_display_symbol_once_in_order() -> None:
    assert list(TABLE) == ["mx", "Mx", "x"]


def test_length_counts_units_not_spellings() -> None:
    assert len(TABLE) == 3  # noqa: PLR2004


def test_membership_uses_every_spelling() -> None:
    assert "ex" in TABLE
    assert "Base Unit X" in TABLE
    assert "nope" not in TABLE


def test_get_returns_a_default_for_an_unknown_spelling() -> None:
    assert TABLE.get("nope") is None
    assert TABLE.get("nope", 7) == 7  # noqa: PLR2004


def test_a_missing_spelling_raises_key_error_with_the_text_as_given() -> None:
    with pytest.raises(KeyError) as caught:
        TABLE["  Nope "]
    assert caught.value.args == ("  Nope ",)


@pytest.mark.parametrize(
    "key", [None, 5, b"x", ("x",)], ids=["none", "int", "bytes", "tuple"]
)
def test_a_key_that_is_not_text_is_a_key_error(key: object) -> None:
    with pytest.raises(KeyError):
        TABLE[key]


def test_the_table_is_read_only() -> None:
    with pytest.raises(TypeError):
        TABLE["z"] = make_ctor("z")  # type: ignore[index]  # ty: ignore[invalid-assignment]


def test_the_units_are_exposed_in_definition_order() -> None:
    assert TABLE.units == (MILLI, MEGA, BASE)


def test_the_representation_names_the_table() -> None:
    assert repr(TABLE) == "UnitTable('TEST_UNITS', 3 units)"


def test_map_keeps_the_spellings_and_replaces_the_constructors() -> None:
    wrapped = TABLE.map(
        "WRAPPED", lambda constructor: lambda value: constructor(-value)
    )
    assert wrapped["Base Unit X"](2) == ("base", -2)
    assert list(wrapped) == list(TABLE)
    assert repr(wrapped) == "UnitTable('WRAPPED', 3 units)"
