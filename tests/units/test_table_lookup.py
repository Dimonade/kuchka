"""How the text of a unit resolves to a constructor: exactly, then by name."""

from __future__ import annotations

import pytest

from kuchka.internal.unit_table import unit_table
from tests.units.table_fixtures import TABLE
from tests.units.table_fixtures import make_ctor
from tests.units.table_fixtures import make_unit
from tests.units.table_fixtures import resolves_to


def test_a_symbol_resolves_to_its_unit() -> None:
    assert resolves_to("mx") == "milli"
    assert resolves_to("Mx") == "mega"
    assert resolves_to("x") == "base"


def test_an_alias_resolves_to_its_unit() -> None:
    assert resolves_to("ex") == "base"


def test_symbols_that_differ_only_in_case_stay_separate() -> None:
    assert resolves_to("mx") != resolves_to("Mx")


@pytest.mark.parametrize("text", ["MX", "mX", "X", "EX", "Ex"])
def test_case_never_loosens_a_symbol(text: str) -> None:
    with pytest.raises(KeyError):
        TABLE[text]


def test_a_symbol_is_normalized_before_matching() -> None:
    micro = unit_table(
        "MICRO_UNITS", {make_unit("microx", "\u00b5x"): make_ctor("micro")}
    )
    assert micro["\u00b5x"](1)[0] == "micro"
    assert micro["\u03bcx"](1)[0] == "micro"


def test_surrounding_whitespace_is_ignored() -> None:
    assert resolves_to("  mx\t") == "milli"


def test_whitespace_inside_a_symbol_is_not_dropped() -> None:
    with pytest.raises(KeyError):
        TABLE["m x"]


@pytest.mark.parametrize("text", ["millix", "Millix", "MILLIX", " millix "])
def test_the_name_resolves_ignoring_case(text: str) -> None:
    assert resolves_to(text) == "milli"


@pytest.mark.parametrize(
    "text", ["base unit x", "Base Unit X", "BASE   UNIT X", "the x", "The X"]
)
def test_a_word_resolves_ignoring_case_and_spacing(text: str) -> None:
    assert resolves_to(text) == "base"


@pytest.mark.parametrize("text", ["millixs", "Basexs", "base unit xs", "the xs"])
def test_a_trailing_plural_s_is_tolerated_on_a_word(text: str) -> None:
    assert resolves_to(text) in {"milli", "base"}


def test_the_plural_tolerance_applies_to_words_only() -> None:
    with pytest.raises(KeyError):
        TABLE["mxs"]
    with pytest.raises(KeyError):
        TABLE["exs"]


def test_underscores_in_a_name_read_as_spaces() -> None:
    table = unit_table("U", {make_unit("solar_mass", "Ms"): make_ctor("solar")})
    assert table["solar mass"](1)[0] == "solar"


def test_a_word_does_not_resolve_a_different_unit() -> None:
    with pytest.raises(KeyError):
        TABLE["megaxx"]


def test_resolve_gives_the_unit_with_its_constructor() -> None:
    unit, constructor = TABLE.resolve("mx")
    assert unit.symbol == "mx"
    assert constructor(1)[0] == "milli"


def test_resolve_reads_every_spelling_that_the_table_reads() -> None:
    for text in ("mx", "Mx", "x", "ex"):
        assert TABLE.resolve(text)[1] is TABLE[text]


@pytest.mark.parametrize("text", ["MX", "nothing", ""])
def test_resolve_refuses_what_the_table_refuses(text: str) -> None:
    with pytest.raises(KeyError):
        TABLE.resolve(text)


def test_a_table_has_the_label_it_was_built_with() -> None:
    assert unit_table("SOME_UNITS", {make_unit("u", "u"): make_ctor("u")}).label == (
        "SOME_UNITS"
    )
