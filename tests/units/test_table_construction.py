"""A table with an ambiguous spelling cannot be built, and nor can a definition."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import pytest

from kuchka import InvalidMeasurementError
from kuchka.dimensions import LENGTH
from kuchka.internal.unit_table import UnitTable
from kuchka.internal.unit_table import unit_table
from kuchka.quantities.base import UnitDef
from tests.units.table_fixtures import make_ctor
from tests.units.table_fixtures import make_unit


def _build(*units: UnitDef) -> UnitTable[Any]:
    return unit_table("AMBIGUOUS", {unit: make_ctor(unit.name) for unit in units})


def test_two_units_with_the_same_symbol_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(make_unit("one", "q"), make_unit("two", "q"))


def test_an_alias_that_is_another_units_symbol_is_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(make_unit("one", "q"), make_unit("two", "r", aliases=("q",)))


def test_two_units_sharing_an_alias_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(
            make_unit("one", "q", aliases=("z",)),
            make_unit("two", "r", aliases=("z",)),
        )


def test_two_units_sharing_a_word_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(
            make_unit("one", "q", words=("thing",)),
            make_unit("two", "r", words=("Thing",)),
        )


def test_a_word_that_repeats_another_units_name_is_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(make_unit("one", "q"), make_unit("two", "r", words=("one",)))


def test_a_symbol_that_reads_as_another_units_word_is_rejected() -> None:
    with pytest.raises(ValueError, match="reads as a word"):
        _build(make_unit("one", "q"), make_unit("two", "r", words=("Q",)))


def test_a_word_that_is_another_units_word_plus_s_is_rejected() -> None:
    with pytest.raises(ValueError, match="plural"):
        _build(make_unit("gram", "g"), make_unit("grams", "gs"))


def test_a_unit_may_list_the_same_spelling_twice() -> None:
    table = _build(make_unit("one", "q", aliases=("z", "z"), words=("thing", "thing")))
    assert table["z"](1)[0] == "one"


def test_a_unit_may_list_its_symbol_as_an_alias() -> None:
    table = _build(make_unit("one", "q", aliases=("q",)))
    assert table["q"](1)[0] == "one"


def test_spellings_that_normalize_to_the_same_text_are_one_spelling() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(make_unit("one", "\u00b5x"), make_unit("two", "\u03bcx"))


@pytest.mark.parametrize("bad", [["a"], "ab", ("",), (" ",), (1,), None])
def test_aliases_must_be_a_tuple_of_non_empty_strings(bad: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="non-empty strings"):
        UnitDef("u", "u", Fraction(1), LENGTH, aliases=bad)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize("bad", [["a"], "ab", ("",), (" ",), (1,), None])
def test_words_must_be_a_tuple_of_non_empty_strings(bad: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="non-empty strings"):
        UnitDef("u", "u", Fraction(1), LENGTH, words=bad)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_spellings_default_to_none() -> None:
    unit = UnitDef("u", "u", Fraction(1), LENGTH)
    assert unit.aliases == ()
    assert unit.words == ()
