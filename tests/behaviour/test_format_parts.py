"""`format_parts` returns the formatted magnitude and the unit symbol apart.

It is the one rule behind `format`, `str`, and `repr`, so a table, a CSV column, or a
protocol that renders the two apart never splits a formatted string on its space.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Celsius
from kuchka import Decibel
from kuchka import Millivolt
from kuchka import Percent
from kuchka import Ratio
from kuchka import Volt


@pytest.mark.parametrize(
    ("value", "spec", "expected"),
    [
        (Volt(1234.5), ".2f", ("1234.50", "V")),
        (Volt(1234.5), "", ("1234.5", "V")),
        (Volt(1234.5), ",.2f", ("1,234.50", "V")),
        (Volt(1234.5), ".2e", ("1.23e+3", "V")),
        (Millivolt(2800), "", ("2800", "mV")),
        (Volt(-0.5), ".3f", ("-0.500", "V")),
        (Celsius(21.5), ".1f", ("21.5", "\u00b0C")),
        (Decibel(-3), "", ("-3", "dB")),
        (Ratio(0.25), "", ("0.25", "1")),
        (Percent(25), ".1f", ("25.0", "%")),
    ],
)
def test_the_magnitude_and_the_symbol_are_returned_apart(
    value: object, spec: str, expected: tuple[str, str]
) -> None:
    assert value.format_parts(spec) == expected  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_a_tie_rounds_away_from_zero_once_from_the_exact_value() -> None:
    assert Volt(2.5).format_parts(".0f") == ("3", "V")
    assert Volt(-2.5).format_parts(".0f") == ("-3", "V")
    assert Volt(0.125).format_parts(".2f") == ("0.13", "V")
    assert Volt(2.665).format_parts(".2f") == ("2.67", "V")


def test_a_value_with_no_finite_decimal_form_shows_28_digits() -> None:
    assert (Volt(1) / 3).format_parts() == ("0.3333333333333333333333333333", "V")
    assert (Volt(Fraction(2, 3))).format_parts() == (
        "0.6666666666666666666666666667",
        "V",
    )


@pytest.mark.parametrize(
    "spec", ["", ".2f", ".0f", "10.3f", "+.1f", ",.2f", ".3e", ".4g"]
)
def test_the_parts_joined_are_what_format_and_repr_write(spec: str) -> None:
    for value in (Volt(1234.5), Millivolt(Fraction(7, 3)), Celsius(-40), Ratio(0.25)):
        assert " ".join(value.format_parts(spec)) == format(value, spec)
    assert " ".join(Volt(4.2).format_parts()) == repr(Volt(4.2)) == str(Volt(4.2))


def test_a_bad_specification_is_the_error_format_raises() -> None:
    with pytest.raises(ValueError, match="format"):
        Volt(1).format_parts("q")
    with pytest.raises(ValueError, match="format"):
        format(Volt(1), "q")


def test_the_parts_are_two_strings() -> None:
    magnitude, symbol = Volt(1234.5).format_parts(".2f")
    assert (type(magnitude), type(symbol)) == (str, str)
