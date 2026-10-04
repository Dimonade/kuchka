"""`UnitTable`: how the text of a unit resolves to a constructor.

A table is built from unit definitions, and each definition says what it is known by:
a display `symbol`, exact-match `aliases`, and a `name` and case-insensitive `words`.
The rules, in the order they apply to a lookup:

1. The text is normalized (NFKC, whitespace collapsed), so characters that look the same
   are the same: the micro sign and the Greek mu, the Ohm sign and the Greek omega,
   `℃` and `°C`.
2. It is compared exactly with symbols and aliases.
   Case matters, because it carries meaning in a symbol (`mV` and `MV` differ).
3. Failing that, it is compared with names and words ignoring case, and a trailing
   plural `s` is tolerated.
4. Otherwise it is a `KeyError`.

Building a table rejects any spelling that could mean two units, so every table that
exists is unambiguous.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Any

import pytest

from kuchka import InvalidMeasurementError
from kuchka.dimensions import LENGTH
from kuchka.internal.spelling import fold
from kuchka.internal.spelling import normalize
from kuchka.internal.unit_table import UnitTable
from kuchka.internal.unit_table import unit_table
from kuchka.quantities.base import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric


def _unit(name: str, symbol: str, **spellings: tuple[str, ...]) -> UnitDef:
    return UnitDef(name, symbol, Fraction(1), LENGTH, **spellings)


def _ctor(label: str) -> Callable[[Numeric], tuple[str, Numeric]]:
    def construct(value: Numeric) -> tuple[str, Numeric]:
        return (label, value)

    return construct


MILLI = _unit("millix", "mx")
MEGA = _unit("megax", "Mx")
BASE = _unit("basex", "x", aliases=("ex",), words=("base unit x", "the x"))
TABLE = unit_table(
    "TEST_UNITS",
    {MILLI: _ctor("milli"), MEGA: _ctor("mega"), BASE: _ctor("base")},
)


def _resolves_to(text: str) -> str:
    return TABLE[text](1)[0]


# Helpers.


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("mV", "mV"),
        ("\u00b5V", "\u03bcV"),
        ("\u2126", "\u03a9"),
        ("\u2103", "\u00b0C"),
        ("\u2109", "\u00b0F"),
        ("\uff05", "%"),
        ("  degrees \t C ", "degrees C"),
        ("\u212a", "K"),
    ],
    ids=[
        "plain",
        "micro",
        "ohm",
        "celsius",
        "fahrenheit",
        "percent",
        "space",
        "kelvin",
    ],
)
def test_normalize_unifies_characters_that_read_the_same(
    text: str, expected: str
) -> None:
    assert normalize(text) == expected


def test_normalize_keeps_case() -> None:
    assert normalize("mV") != normalize("MV")


def test_fold_ignores_case_and_reads_underscores_as_spaces() -> None:
    assert fold("Solar_Mass") == fold("solar MASS") == "solar mass"


def test_fold_is_normalize_then_casefold() -> None:
    assert fold("  Degrees   C ") == "degrees c"
    assert fold("STRASSE") == fold("Stra\u00dfe")


# Symbols and aliases are exact.


def test_a_symbol_resolves_to_its_unit() -> None:
    assert _resolves_to("mx") == "milli"
    assert _resolves_to("Mx") == "mega"
    assert _resolves_to("x") == "base"


def test_an_alias_resolves_to_its_unit() -> None:
    assert _resolves_to("ex") == "base"


def test_symbols_that_differ_only_in_case_stay_separate() -> None:
    assert _resolves_to("mx") != _resolves_to("Mx")


@pytest.mark.parametrize("text", ["MX", "mX", "X", "EX", "Ex"])
def test_case_never_loosens_a_symbol(text: str) -> None:
    with pytest.raises(KeyError):
        TABLE[text]


def test_a_symbol_is_normalized_before_matching() -> None:
    micro = unit_table("MICRO_UNITS", {_unit("microx", "\u00b5x"): _ctor("micro")})
    assert micro["\u00b5x"](1)[0] == "micro"
    assert micro["\u03bcx"](1)[0] == "micro"


def test_surrounding_whitespace_is_ignored() -> None:
    assert _resolves_to("  mx\t") == "milli"


def test_whitespace_inside_a_symbol_is_not_dropped() -> None:
    with pytest.raises(KeyError):
        TABLE["m x"]


# Names and words ignore case.


@pytest.mark.parametrize("text", ["millix", "Millix", "MILLIX", " millix "])
def test_the_name_resolves_ignoring_case(text: str) -> None:
    assert _resolves_to(text) == "milli"


@pytest.mark.parametrize(
    "text", ["base unit x", "Base Unit X", "BASE   UNIT X", "the x", "The X"]
)
def test_a_word_resolves_ignoring_case_and_spacing(text: str) -> None:
    assert _resolves_to(text) == "base"


@pytest.mark.parametrize("text", ["millixs", "Basexs", "base unit xs", "the xs"])
def test_a_trailing_plural_s_is_tolerated_on_a_word(text: str) -> None:
    assert _resolves_to(text) in {"milli", "base"}


def test_the_plural_tolerance_applies_to_words_only() -> None:
    with pytest.raises(KeyError):
        TABLE["mxs"]
    with pytest.raises(KeyError):
        TABLE["exs"]


def test_underscores_in_a_name_read_as_spaces() -> None:
    table = unit_table("U", {_unit("solar_mass", "Ms"): _ctor("solar")})
    assert table["solar mass"](1)[0] == "solar"


def test_a_word_does_not_resolve_a_different_unit() -> None:
    with pytest.raises(KeyError):
        TABLE["megaxx"]


# The mapping contract.


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
        TABLE["z"] = _ctor("z")  # type: ignore[index]  # ty: ignore[invalid-assignment]


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


# A table with an ambiguous spelling cannot be built.


def _build(*units: UnitDef) -> UnitTable[Any]:
    return unit_table("AMBIGUOUS", {unit: _ctor(unit.name) for unit in units})


def test_two_units_with_the_same_symbol_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "q"), _unit("two", "q"))


def test_an_alias_that_is_another_units_symbol_is_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "q"), _unit("two", "r", aliases=("q",)))


def test_two_units_sharing_an_alias_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "q", aliases=("z",)), _unit("two", "r", aliases=("z",)))


def test_two_units_sharing_a_word_are_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "q", words=("thing",)), _unit("two", "r", words=("Thing",)))


def test_a_word_that_repeats_another_units_name_is_rejected() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "q"), _unit("two", "r", words=("one",)))


def test_a_symbol_that_reads_as_another_units_word_is_rejected() -> None:
    with pytest.raises(ValueError, match="reads as a word"):
        _build(_unit("one", "q"), _unit("two", "r", words=("Q",)))


def test_a_word_that_is_another_units_word_plus_s_is_rejected() -> None:
    with pytest.raises(ValueError, match="plural"):
        _build(_unit("gram", "g"), _unit("grams", "gs"))


def test_a_unit_may_list_the_same_spelling_twice() -> None:
    table = _build(_unit("one", "q", aliases=("z", "z"), words=("thing", "thing")))
    assert table["z"](1)[0] == "one"


def test_a_unit_may_list_its_symbol_as_an_alias() -> None:
    table = _build(_unit("one", "q", aliases=("q",)))
    assert table["q"](1)[0] == "one"


def test_spellings_that_normalize_to_the_same_text_are_one_spelling() -> None:
    with pytest.raises(ValueError, match="claimed by both"):
        _build(_unit("one", "\u00b5x"), _unit("two", "\u03bcx"))


# Unit definitions validate their spellings.


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
