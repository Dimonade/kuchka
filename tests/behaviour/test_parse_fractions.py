"""`parse` reads a fraction, two whole numbers around a slash, exactly.

A decimal cannot hold a third, so a value computed with fractions needs a written form
that can: `"1/3 V"`.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from kuchka import ParseError
from kuchka import Proportion
from kuchka import Voltage
from kuchka import parse
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.units import proportion
from kuchka.units.electromagnetics import voltage

_MAX_BITS = NUMERIC_LIMITS.max_exact_bits


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1/3 V", Fraction(1, 3)),
        ("1/3V", Fraction(1, 3)),
        ("  1/3   V  ", Fraction(1, 3)),
        ("+1/3 V", Fraction(1, 3)),
        ("-1/3 V", Fraction(-1, 3)),
        ("\u22121/3 V", Fraction(-1, 3)),
        ("6/4 V", Fraction(3, 2)),
        ("0/5 V", Fraction(0)),
        ("007/010 V", Fraction(7, 10)),
        ("\uff11/\uff13 V", Fraction(1, 3)),
        ("10/1 V", Fraction(10)),
    ],
)
def test_a_fraction_reads_exactly(text: str, expected: Fraction) -> None:
    assert parse(text, Voltage) == voltage.Volt(expected)


def test_a_fraction_reads_in_the_unit_that_was_written() -> None:
    result = parse("7/3 mV", Voltage)
    assert result == voltage.Millivolt(Fraction(7, 3))
    assert result.unit is voltage.MILLIVOLT


def test_a_fraction_before_a_unit_that_starts_with_a_digit_takes_the_space() -> None:
    assert parse("1/3 1", Proportion) == proportion.Ratio(Fraction(1, 3))


@given(
    numerator=st.integers(min_value=-(10**40), max_value=10**40),
    denominator=st.integers(min_value=1, max_value=10**40),
)
@example(numerator=1, denominator=3)
@example(numerator=0, denominator=1)
def test_every_fraction_reads_as_the_value_it_writes(
    numerator: int, denominator: int
) -> None:
    sign = "-" if numerator < 0 else ""
    text = f"{sign}{abs(numerator)}/{denominator} V"
    assert parse(text, Voltage) == voltage.Volt(Fraction(numerator, denominator))


def test_a_fraction_with_a_zero_denominator_is_refused() -> None:
    with pytest.raises(ParseError, match="divides by zero"):
        parse("1/0 V", Voltage)
    with pytest.raises(ParseError, match="divides by zero"):
        parse("0/0 V", Voltage)


@pytest.mark.parametrize(
    "text",
    [
        "1 /3 V",
        "1/ 3 V",
        "1.5/3 V",
        "1/3.5 V",
        "1/3e2 V",
        "1/3,5 V",
        "1/3_0 V",
        "1 1/3 V",
    ],
)
def test_a_fraction_in_a_form_that_is_not_read_is_refused(text: str) -> None:
    with pytest.raises(ParseError):
        parse(text, Voltage)


@pytest.mark.parametrize(
    "text", ["1 /3 V", "1.5/3 V", "1/3.5 V", "1/3e2 V", "1/3,5 V", "1/3_0 V"]
)
def test_the_refusal_says_how_a_fraction_is_written(text: str) -> None:
    with pytest.raises(ParseError, match="two whole numbers around a slash"):
        parse(text, Voltage)


@pytest.mark.parametrize("text", ["1/ V", "/3 V", "1/V", "1//3 V", "1/-3 V"])
def test_text_that_is_no_fraction_is_refused(text: str) -> None:
    with pytest.raises(ParseError):
        parse(text, Voltage)


def test_a_fraction_with_no_unit_is_refused_where_no_bare_unit_exists() -> None:
    with pytest.raises(ParseError, match="no unit"):
        parse("1/3", Voltage)


def test_a_fraction_at_the_size_limit_is_read() -> None:
    top = 2**_MAX_BITS - 1
    assert parse(f"{top}/{top - 1} V", Voltage) == voltage.Volt(Fraction(top, top - 1))


@pytest.mark.parametrize(
    "text",
    [
        f"{2**_MAX_BITS}/3 V",
        f"1/{2**_MAX_BITS} V",
        f"{'9' * 10_000}/3 V",
        f"1/{'9' * 10_000} V",
    ],
    ids=[
        "numerator_bits",
        "denominator_bits",
        "numerator_digits",
        "denominator_digits",
    ],
)
def test_a_fraction_beyond_the_numeric_limits_is_refused(text: str) -> None:
    with pytest.raises(ParseError, match="out of range"):
        parse(text, Voltage)


@settings(max_examples=300, deadline=None)
@given(
    text=st.from_regex(
        r"[+\-\u2212]?[0-9]{0,30}[/.e ]{0,2}[0-9]{0,30}[ ]?[A-Za-z]{0,3}",
        fullmatch=True,
    )
)
@example(text="1/0 V")
@example(text="1/")
@example(text="/1 V")
def test_text_shaped_like_a_fraction_is_read_or_refused_as_a_parse_error(
    text: str,
) -> None:
    try:
        result = parse(text, Voltage)
    except ParseError:
        return
    assert isinstance(result, Voltage)
