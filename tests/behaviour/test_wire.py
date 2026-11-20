"""`wire.dump` writes a measurement as text, and `wire.load` reads boundary data.

What every unit of every type does is covered once for all of them in the contract
tests; this module covers the written form, what `load` accepts, and how it refuses.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st

from kuchka import ArchaicPolicy
from kuchka import Current
from kuchka import InvalidMeasurementError
from kuchka import Length
from kuchka import ParseError
from kuchka import Proportion
from kuchka import SamplingPeriod
from kuchka import Temperature
from kuchka import Time
from kuchka import UnknownUnitError
from kuchka import Voltage
from kuchka import wire
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.units import current
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.archaic.russian import length as russian_length
from kuchka.units.electromagnetics import voltage
from kuchka.units.temporal import time


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (voltage.Millivolt(2800), "2800 mV"),
        (voltage.Volt(4.2), "4.2 V"),
        (voltage.Volt(Decimal("2.50")), "2.5 V"),
        (voltage.Volt(-0.5), "-0.5 V"),
        (voltage.Volt(0), "0 V"),
        (voltage.Volt(10**6), "1000000 V"),
        (voltage.Volt(Fraction(1, 1024)), "0.0009765625 V"),
        (voltage.Volt(Fraction(1, 3)), "1/3 V"),
        (voltage.Volt(Fraction(-1, 3)), "-1/3 V"),
        (voltage.Millivolt(Fraction(7, 3)), "7/3 mV"),
        (thermal.Celsius(-40), "-40 \u00b0C"),
        (thermal.Fahrenheit(Fraction(1, 3)), "1/3 \u00b0F"),
        (proportion.Ratio(0.25), "0.25"),
        (proportion.Ratio(Fraction(1, 3)), "1/3"),
        (proportion.Percent(25), "25 %"),
    ],
)
def test_a_measurement_is_written_as_its_exact_number_and_its_unit(
    value: object, expected: str
) -> None:
    assert wire.dump(value) == expected  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_a_decimal_that_terminates_beyond_the_limits_is_written_as_a_fraction() -> None:
    places = NUMERIC_LIMITS.max_decimal_exponent + 1
    value = voltage.Volt(Fraction(1, 2**places))
    text = wire.dump(value)
    assert text == f"1/{2**places} V"
    assert wire.load(text, Voltage) == value


def test_the_written_form_is_read_by_parse() -> None:
    from kuchka import parse

    value = voltage.Millivolt(Fraction(7, 3))
    assert parse(wire.dump(value), Voltage) == value


@pytest.mark.parametrize("value", [5, 5.0, "5 V", None, voltage.Volt])
def test_dump_writes_a_measurement_only(value: object) -> None:
    with pytest.raises(TypeError, match="measurement"):
        wire.dump(value)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_an_instance_of_the_type_passes_through_unchanged() -> None:
    value = voltage.Millivolt(2800)
    assert wire.load(value, Voltage) is value


@pytest.mark.parametrize("text", ["2800 mV", "2.8 V", "28/10 V", "2800 millivolts"])
def test_text_is_read_as_parse_reads_it(text: str) -> None:
    assert wire.load(text, Voltage) == voltage.Volt(Decimal("2.8"))


@pytest.mark.parametrize(
    "mapping",
    [
        {"value": "2800", "unit": "mV"},
        {"value": 2800, "unit": "mV"},
        {"value": 2800.0, "unit": "mV"},
        {"value": Decimal(2800), "unit": "mV"},
        {"value": Fraction(2800), "unit": "mV"},
        {"value": "2800", "unit": "millivolts"},
        {"value": " 2800 ", "unit": " mV "},
        {"value": "28/10", "unit": "V"},
    ],
)
def test_a_value_and_a_unit_read_as_the_text_of_both(
    mapping: dict[str, object],
) -> None:
    result = wire.load(mapping, Voltage)
    assert result == voltage.Millivolt(2800)


def test_a_mapping_reads_in_the_unit_that_was_written() -> None:
    assert wire.load({"value": "7/3", "unit": "mV"}, Voltage).unit is voltage.MILLIVOLT


def test_a_float_is_read_by_the_digits_it_shows() -> None:
    assert wire.load({"value": 0.1, "unit": "V"}, Voltage) == voltage.Volt(
        Fraction(1, 10)
    )


@pytest.mark.parametrize(
    "value", [0.25, Decimal("0.25"), Fraction(1, 4), "0.25", "1/4", "25 %", "0.25 1"]
)
def test_a_proportion_reads_a_number_or_its_text(value: object) -> None:
    assert wire.load(value, Proportion) == proportion.Ratio(Fraction(1, 4))


def test_a_proportion_reads_an_integer_as_a_ratio() -> None:
    assert wire.load(1, Proportion) == proportion.Percent(100)


def test_a_mapping_without_a_unit_reads_for_a_proportion_only() -> None:
    assert wire.load({"value": "0.25"}, Proportion) == proportion.Ratio(Fraction(1, 4))
    assert wire.load({"value": 0.25, "unit": None}, Proportion) == proportion.Ratio(
        Fraction(1, 4)
    )
    with pytest.raises(ParseError, match="no unit"):
        wire.load({"value": "0.25"}, Voltage)


@pytest.mark.parametrize("number", [2.8, 3, Decimal("2.8"), Fraction(14, 5)])
def test_a_number_is_refused_for_a_quantity_that_needs_a_unit(number: object) -> None:
    with pytest.raises(ParseError, match="has no unit") as raised:
        wire.load(number, Voltage)
    assert '"5 V"' in str(raised.value)


@pytest.mark.parametrize("value", [True, False])
def test_a_bool_is_no_number(value: bool) -> None:  # noqa: FBT001
    for quantity in (Voltage, Proportion):
        with pytest.raises(ParseError):
            wire.load(value, quantity)
    with pytest.raises(ParseError):
        wire.load({"value": value, "unit": "V"}, Voltage)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), Decimal("NaN")])
def test_a_number_that_is_no_finite_number_is_refused(value: object) -> None:
    with pytest.raises(ParseError):
        wire.load(value, Proportion)
    with pytest.raises(ParseError):
        wire.load({"value": value, "unit": "V"}, Voltage)


def test_a_measurement_of_another_quantity_type_is_refused() -> None:
    with pytest.raises(ParseError, match=r"is no Voltage"):
        wire.load(current.Ampere(1), Voltage)


def test_a_measurement_of_another_kind_of_one_dimension_is_refused() -> None:
    period = time.Second(1).to_sampling_period()
    with pytest.raises(ParseError, match=r"is no Time"):
        wire.load(period, Time)
    with pytest.raises(ParseError, match=r"is no SamplingPeriod"):
        wire.load(time.Second(1), SamplingPeriod)


@pytest.mark.parametrize(
    "mapping",
    [
        {},
        {"unit": "V"},
        {"value": "5", "unit": "V", "extra": 1},
        {"value": "5", "unit": 5},
        {"value": "5", "unit": ""},
        {"value": "5", "unit": "   "},
        {"value": "5 V", "unit": "V"},
        {"value": "five", "unit": "V"},
        {"value": None, "unit": "V"},
        {"value": ["5"], "unit": "V"},
        {"value": "5", "unit": "A"},
        {"value": "5"},
    ],
)
def test_a_mapping_in_any_other_shape_is_refused(mapping: dict[str, object]) -> None:
    with pytest.raises(ParseError):
        wire.load(mapping, Voltage)


def test_a_unit_the_type_does_not_have_is_an_unknown_unit() -> None:
    with pytest.raises(UnknownUnitError):
        wire.load("150 mA", Voltage)
    with pytest.raises(UnknownUnitError):
        wire.load({"value": "150", "unit": "mA"}, Voltage)


@pytest.mark.parametrize("value", [None, b"5 V", ["5 V"], ("5", "V"), {5}, object()])
def test_a_value_of_any_other_python_type_is_refused(value: object) -> None:
    with pytest.raises(ParseError, match="cannot read a Voltage"):
        wire.load(value, Voltage)


def test_a_value_out_of_the_range_of_the_quantity_is_a_parse_error() -> None:
    with pytest.raises(ParseError) as raised:
        wire.load("-300 \u00b0C", Temperature)
    assert isinstance(raised.value, InvalidMeasurementError)
    assert isinstance(raised.value.__cause__, InvalidMeasurementError)
    assert not isinstance(raised.value.__cause__, ParseError)


def test_every_refusal_of_data_is_a_value_error() -> None:
    refused: list[object] = [
        "five",
        "5",
        "150 mA",
        2.8,
        None,
        True,
        current.Ampere(1),
        {"value": "5"},
        "-300 \u00b0C",
    ]
    for value in refused:
        quantity = Temperature if value == "-300 \u00b0C" else Voltage
        with pytest.raises(ValueError, match=r"."):
            wire.load(value, quantity)


@pytest.mark.parametrize("quantity", [voltage.Volt, "Voltage", 5, None, object])
def test_the_quantity_has_to_be_a_quantity_type_with_units(quantity: object) -> None:
    with pytest.raises(TypeError, match="quantity type"):
        wire.load("5 V", quantity)  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize("policy", ["yes", 1, None])
def test_the_archaic_policy_is_a_policy_or_a_bool(policy: object) -> None:
    with pytest.raises(TypeError, match="ArchaicPolicy"):
        wire.load("5 V", Voltage, allow_archaic=policy)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_an_archaic_unit_is_written_like_any_other_and_read_when_allowed() -> None:
    value = russian_length.Arshin(2)
    text = wire.dump(value)
    assert text == "2 arshin"
    assert wire.load(text, Length, allow_archaic=True) == value
    assert wire.load(text, Length, allow_archaic=ArchaicPolicy.Allow) == value
    mapping = {"value": "2", "unit": "arshin"}
    assert wire.load(mapping, Length, allow_archaic=True) == value
    with pytest.raises(UnknownUnitError, match="archaic"):
        wire.load(text, Length)
    with pytest.raises(UnknownUnitError, match="archaic"):
        wire.load(mapping, Length)


_ANYTHING = st.recursive(
    st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(),
        st.decimals(),
        st.fractions(),
        st.text(max_size=20),
        st.binary(max_size=8),
    ),
    lambda inner: st.one_of(
        st.lists(inner, max_size=3),
        st.dictionaries(st.sampled_from(["value", "unit", "x"]), inner, max_size=3),
    ),
    max_leaves=6,
)


@settings(max_examples=400, deadline=None)
@given(value=_ANYTHING)
def test_any_value_is_read_or_refused_as_a_parse_error(value: object) -> None:
    for quantity in (Voltage, Proportion, Current):
        try:
            result = wire.load(value, quantity)
        except ParseError:
            continue
        assert isinstance(result, quantity)
