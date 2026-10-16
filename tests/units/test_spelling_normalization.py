"""`normalize` and `fold` unify characters that read the same."""

from __future__ import annotations

import pytest

from kuchka.internal.spelling import fold
from kuchka.internal.spelling import normalize


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
