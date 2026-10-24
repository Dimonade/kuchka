"""`parse` reads a number and a unit from text into the quantity type it is given.

What every unit spelling of every type does is covered once for all types in the
contract tests; this module covers the text forms, the exactness, the errors, and the
arguments.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest
from hypothesis import example
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from kuchka import ArchaicPolicy
from kuchka import Area
from kuchka import Energy
from kuchka import Instant
from kuchka import InvalidMeasurementError
from kuchka import ParseError
from kuchka import Proportion
from kuchka import SamplingPeriod
from kuchka import Temperature
from kuchka import Time
from kuchka import UnknownUnitError
from kuchka import Voltage
from kuchka import parse
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.quantities.base import LinearQuantity
from kuchka.units import area
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units import time
from kuchka.units import voltage


@pytest.mark.parametrize(
    "text",
    [
        "5 mV",
        "5mV",
        "  5   mV  ",
        "5\tmV",
        "5\u00a0mV",
        "5\u2009mV",
        "\uff15 mV",
        "5 millivolts",
        "5 Millivolt",
    ],
)
def test_the_number_and_the_unit_read_through_the_spacing_and_the_spelling(
    text: str,
) -> None:
    assert parse(text, Voltage) == voltage.Millivolt(5)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("5 V", Fraction(5)),
        ("+5 V", Fraction(5)),
        ("-5 V", Fraction(-5)),
        ("\u22125 V", Fraction(-5)),
        ("5.5 V", Fraction(11, 2)),
        ("5. V", Fraction(5)),
        (".5 V", Fraction(1, 2)),
        ("0.1 V", Fraction(1, 10)),
        ("1e3 V", Fraction(1000)),
        ("1E3 V", Fraction(1000)),
        ("1.5e-3 V", Fraction(3, 2000)),
        ("1e\u22123 V", Fraction(1, 1000)),
        ("1e+3 V", Fraction(1000)),
        ("123456789012345678901234567890 V", Fraction(123456789012345678901234567890)),
    ],
)
def test_a_number_reads_exactly(text: str, expected: Fraction) -> None:
    assert parse(text, Voltage) == voltage.Volt(expected)


def test_an_exponent_does_not_swallow_the_unit_that_follows() -> None:
    assert parse("5eV", Energy) == parse("5 eV", Energy)
    assert parse("5e3V", Voltage) == voltage.Volt(5000)


def test_the_result_displays_in_the_unit_that_was_written() -> None:
    assert repr(parse("5 mV", Voltage)) == "5 mV"
    assert repr(parse("0.005 V", Voltage)) == "0.005 V"
    assert repr(parse("20 degrees C", Temperature)) == "20 \u00b0C"


def test_the_same_text_is_read_by_the_type_it_is_given() -> None:
    assert parse("5 s", Time) == time.Second(5)
    assert type(parse("5 s", Instant)) is Instant
    assert type(parse("5 s", SamplingPeriod)) is SamplingPeriod
    assert type(parse("5 s", Time)) is Time


def test_an_affine_type_reads_its_own_units() -> None:
    assert parse("-40 \u00b0C", Temperature) == thermal.Celsius(-40)
    assert parse("-40 degC", Temperature) == thermal.Celsius(-40)


def test_superscripts_and_carets_read_as_powers() -> None:
    assert parse("4 m\u00b2", Area) == area.SquareMetre(4)
    assert parse("4 m^2", Area) == area.SquareMetre(4)


def test_a_unit_that_starts_with_a_digit_takes_the_space() -> None:
    assert parse("7 1", Proportion) == proportion.Ratio(7)


@pytest.mark.parametrize(
    "text", ["", "   ", "mV", "five volts", "nan V", "inf V", "V 5"]
)
def test_text_without_a_number_at_its_start_is_refused(text: str) -> None:
    with pytest.raises(ParseError, match="number"):
        parse(text, Voltage)


@pytest.mark.parametrize("text", ["5", "5   ", "-5.5e3"])
def test_a_number_without_a_unit_is_refused(text: str) -> None:
    with pytest.raises(ParseError, match="no unit"):
        parse(text, Voltage)


@pytest.mark.parametrize("text", ["1,5 V", "1,000 V", "1_000 V", "1.2.3 V"])
def test_a_number_in_a_form_that_is_not_read_is_refused(text: str) -> None:
    with pytest.raises(ParseError, match="decimal point"):
        parse(text, Voltage)


def test_a_number_out_of_range_is_refused() -> None:
    with pytest.raises(ParseError, match="out of range"):
        parse("1e99999999999999999999 V", Voltage)


_MAX_EXPONENT = NUMERIC_LIMITS.max_decimal_exponent
_MAX_DIGITS = NUMERIC_LIMITS.max_decimal_digits


@pytest.mark.parametrize(
    "text",
    [
        f"1e{_MAX_EXPONENT + 1} V",
        f"1e-{_MAX_EXPONENT + 1} V",
        f"{'1' * (_MAX_DIGITS + 1)} V",
        "1e100000000 V",
    ],
    ids=["exponent_above", "exponent_below", "digits", "exponent_far_above"],
)
def test_a_number_beyond_the_numeric_limits_is_text_that_cannot_be_read(
    text: str,
) -> None:
    with pytest.raises(ParseError, match="out of range") as raised:
        parse(text, Voltage)
    cause = raised.value.__cause__
    assert isinstance(cause, InvalidMeasurementError)
    assert not isinstance(cause, ParseError)


@pytest.mark.parametrize(
    "text",
    [f"1e{_MAX_EXPONENT}", f"1e-{_MAX_EXPONENT}", "1" * _MAX_DIGITS],
    ids=["exponent_above", "exponent_below", "digits"],
)
def test_a_number_at_the_numeric_limits_is_read(text: str) -> None:
    assert parse(f"{text} V", Voltage) == voltage.Volt(Decimal(text))


def test_a_number_read_but_no_valid_measurement_is_not_a_parse_error() -> None:
    with pytest.raises(InvalidMeasurementError) as raised:
        parse("-300 \u00b0C", Temperature)
    assert not isinstance(raised.value, ParseError)


_TEXT_LIKE_A_MEASUREMENT = st.from_regex(
    r"[+\-\u2212]?[0-9]{0,1100}(\.[0-9]{0,12})?"
    r"([eE][+\-]?[0-9]{0,12})?[ ]?[A-Za-z\u00b5\u03a9]{0,6}",
    fullmatch=True,
)


@settings(max_examples=300, deadline=None)
@given(text=st.one_of(st.text(max_size=40), _TEXT_LIKE_A_MEASUREMENT))
@example(text="1e999999999 V")
@example(text="1e-999999999 V")
@example(text="1" * (_MAX_DIGITS + 1) + " V")
@example(text="1e99999999999999999999 V")
@example(text="\uff15 mV")
def test_any_text_is_read_as_a_voltage_or_refused_as_a_parse_error(text: str) -> None:
    try:
        result = parse(text, Voltage)
    except ParseError:
        return
    assert isinstance(result, Voltage)


def test_a_unit_of_the_type_that_is_unknown_names_the_type_and_its_table() -> None:
    with pytest.raises(UnknownUnitError) as raised:
        parse("5 A", Voltage)
    assert raised.value.unit == "A"
    assert raised.value.quantity is Voltage
    assert "Voltage" in str(raised.value)
    assert "VOLTAGE_UNITS" in str(raised.value)


def test_a_unit_of_another_quantity_is_unknown_to_this_one() -> None:
    with pytest.raises(UnknownUnitError):
        parse("5 Hz", Time)


def test_a_symbol_is_matched_with_its_case() -> None:
    with pytest.raises(UnknownUnitError):
        parse("5 mv", Voltage)


def test_the_errors_are_measurement_errors_and_value_errors() -> None:
    for text in ("five volts", "5", "5 A"):
        with pytest.raises(InvalidMeasurementError):
            parse(text, Voltage)
        with pytest.raises(ValueError, match=r"."):
            parse(text, Voltage)
    assert issubclass(UnknownUnitError, ParseError)


@pytest.mark.parametrize("value", [5, None, b"5 V", 5.0, ["5 V"]])
def test_text_is_what_parse_reads(value: object) -> None:
    with pytest.raises(TypeError, match="text"):
        parse(value, Voltage)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize(
    "quantity", [voltage.Volt, "Voltage", 5, None, LinearQuantity, object]
)
def test_the_quantity_has_to_be_a_quantity_type_with_units(quantity: object) -> None:
    with pytest.raises(TypeError, match="quantity type"):
        parse("5 V", quantity)  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize("policy", ["yes", 1, 0, None, "allow"])
def test_the_archaic_policy_is_a_policy_or_a_bool(policy: object) -> None:
    with pytest.raises(TypeError, match="ArchaicPolicy"):
        parse("5 V", Voltage, allow_archaic=policy)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_modern_units_read_under_every_policy() -> None:
    for policy in (False, True, ArchaicPolicy.Deny, ArchaicPolicy.Allow):
        assert parse("5 mV", Voltage, allow_archaic=policy) == voltage.Millivolt(5)
