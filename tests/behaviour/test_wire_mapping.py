"""`wire.to_dict` writes a measurement as a mapping, and `wire.from_dict` reads it back.

The text of `wire.dump` stays the canonical form; the mapping is the same exact data as
the two fields that a JSON document or a database row wants.
"""

from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kuchka import Celsius
from kuchka import Current
from kuchka import Decibel
from kuchka import Degree
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Length
from kuchka import Millivolt
from kuchka import ParseError
from kuchka import Percent
from kuchka import Proportion
from kuchka import Ratio
from kuchka import Temperature
from kuchka import UnknownUnitError
from kuchka import Volt
from kuchka import Voltage
from kuchka import wire
from kuchka.units import AMPERE
from kuchka.units import KELVIN
from kuchka.units.archaic.russian import length as russian_length
from kuchka.units.electromagnetics.voltage import VOLT


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Millivolt(2800), {"value": "2800", "unit": "mV"}),
        (Volt(4.2), {"value": "4.2", "unit": "V"}),
        (Volt(-0.5), {"value": "-0.5", "unit": "V"}),
        (Volt(0), {"value": "0", "unit": "V"}),
        (Volt(1) / 3, {"value": "1/3", "unit": "V"}),
        (Millivolt(Fraction(-7, 3)), {"value": "-7/3", "unit": "mV"}),
        (Celsius(-40), {"value": "-40", "unit": "\u00b0C"}),
        (Ratio(0.25), {"value": "0.25", "unit": "1"}),
        (Percent(25), {"value": "25", "unit": "%"}),
    ],
)
def test_a_measurement_is_written_as_its_exact_value_and_its_unit(
    value: object, expected: dict[str, str]
) -> None:
    assert wire.to_dict(value) == expected  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_mapping_is_the_data_of_the_text() -> None:
    value = Millivolt(Fraction(7, 3))
    mapping = wire.to_dict(value)
    assert f"{mapping['value']} {mapping['unit']}" == wire.dump(value)


@pytest.mark.parametrize(
    ("unit", "expected"),
    [
        ("V", {"value": "2.8", "unit": "V"}),
        (VOLT, {"value": "2.8", "unit": "V"}),
        ("mV", {"value": "2800", "unit": "mV"}),
        ("volts", {"value": "2.8", "unit": "V"}),
        ("\u00b5V", {"value": "2800000", "unit": "\u00b5V"}),
    ],
)
def test_a_measurement_is_written_in_another_unit_of_its_quantity(
    unit: object, expected: dict[str, str]
) -> None:
    assert wire.to_dict(Millivolt(2800), unit=unit) == expected  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_conversion_is_exact_and_covers_every_shape() -> None:
    assert wire.to_dict(Celsius(20), unit="K") == {"value": "293.15", "unit": "K"}
    assert wire.to_dict(Celsius(-40), unit="\u00b0F") == {
        "value": "-40",
        "unit": "\u00b0F",
    }
    assert wire.to_dict(Volt(1) / 3, unit="mV") == {"value": "1000/3", "unit": "mV"}
    assert wire.to_dict(Percent(25), unit="1") == {"value": "0.25", "unit": "1"}


def test_a_unit_of_another_quantity_is_refused() -> None:
    with pytest.raises(UnknownUnitError, match="'mA' is not a unit of Voltage"):
        wire.to_dict(Volt(1), unit="mA")
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        wire.to_dict(Volt(1), unit=AMPERE)


@pytest.mark.parametrize("value", ["1", 1, 1.5, None, Volt])
def test_to_dict_writes_a_measurement_only(value: object) -> None:
    with pytest.raises(TypeError, match="measurement"):
        wire.to_dict(value)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (Volt(4.2), {"value": 4.2, "unit": "V"}),
        (Millivolt(2800), {"value": 2800, "unit": "mV"}),
        (Volt(0), {"value": 0, "unit": "V"}),
        (Volt(-0.5), {"value": -0.5, "unit": "V"}),
        (Volt(1) / 3, {"value": 1 / 3, "unit": "V"}),
        (Celsius(21.5), {"value": 21.5, "unit": "\u00b0C"}),
    ],
)
def test_a_json_number_is_an_int_when_whole_and_a_float_otherwise(
    value: object, expected: dict[str, object]
) -> None:
    written = wire.to_dict(value, form=wire.ValueForm.Float)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert written == expected
    assert type(written["value"]) is type(expected["value"])


def test_a_float_is_lossy_only_where_a_float_is() -> None:
    exact = Volt(4.2)
    written = wire.to_dict(exact, form=wire.ValueForm.Float)
    assert wire.from_dict(written, Voltage) == exact
    third = Volt(1) / 3
    assert (
        wire.from_dict(wire.to_dict(third, form=wire.ValueForm.Float), Voltage) != third
    )
    assert wire.from_dict(wire.to_dict(third), Voltage) == third


def test_a_value_a_float_cannot_hold_is_refused_and_not_written_as_zero() -> None:
    with pytest.raises(InvalidMeasurementError, match="so small"):
        wire.to_dict(Volt(Fraction(1, 10**400)), form=wire.ValueForm.Float)
    with pytest.raises(InvalidMeasurementError, match="beyond the range"):
        wire.to_dict(Volt(Fraction(10**400, 3)), form=wire.ValueForm.Float)
    tiny = Volt(Fraction(1, 10**400))
    assert wire.from_dict(wire.to_dict(tiny), Voltage) == tiny


def test_the_mapping_is_json_and_reads_back_exactly() -> None:
    value = Millivolt(Fraction(7, 3))
    restored = wire.from_dict(json.loads(json.dumps(wire.to_dict(value))), Voltage)
    assert restored == value
    assert restored.unit is value.unit


@given(
    magnitude=st.fractions(min_value=-(10**6), max_value=10**6, max_denominator=10**6)
)
def test_every_magnitude_round_trips_through_the_mapping(magnitude: Fraction) -> None:
    value = Millivolt(magnitude)
    restored = wire.from_dict(wire.to_dict(value), Voltage)
    assert restored == value
    assert restored.unit is value.unit


@pytest.mark.parametrize(
    "data",
    [
        {"value": "2800", "unit": "mV"},
        {"value": 2800, "unit": "mV"},
        {"value": 2800.0, "unit": "mV"},
        {"value": Decimal(2800), "unit": "mV"},
        {"value": Fraction(2800), "unit": "mV"},
        {"value": "28/10", "unit": "V"},
        {"value": " 2800 ", "unit": " millivolts "},
    ],
)
def test_from_dict_reads_a_value_and_a_unit(data: dict[str, object]) -> None:
    assert wire.from_dict(data, Voltage) == Millivolt(2800)


@pytest.mark.parametrize(
    ("data", "error"),
    [
        ({"unit": "V"}, ParseError),
        ({"value": "5"}, ParseError),
        ({"value": "5", "unit": None}, ParseError),
        ({"value": None, "unit": "V"}, ParseError),
        ({}, ParseError),
        ({"value": "5", "unit": "V", "extra": 1}, ParseError),
        ({"value": True, "unit": "V"}, ParseError),
        ({"value": "5", "unit": 5}, ParseError),
        ({"value": "5", "unit": ""}, ParseError),
        ({"value": "five", "unit": "V"}, ParseError),
        ({"value": "5 V", "unit": "V"}, ParseError),
        ({"value": ["5"], "unit": "V"}, ParseError),
        ({"value": float("nan"), "unit": "V"}, ParseError),
        ({"value": "5", "unit": "mA"}, UnknownUnitError),
        ("5 V", ParseError),
        (["5", "V"], ParseError),
        (None, ParseError),
        (5, ParseError),
    ],
)
def test_from_dict_refuses_everything_else_as_a_parse_error(
    data: object, error: type[Exception]
) -> None:
    with pytest.raises(error) as raised:
        wire.from_dict(data, Voltage)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert isinstance(raised.value, InvalidMeasurementError)
    assert isinstance(raised.value, ValueError)


def test_from_dict_refuses_a_value_the_quantity_cannot_hold() -> None:
    with pytest.raises(ParseError):
        wire.from_dict({"value": "-300", "unit": "\u00b0C"}, Temperature)


def test_from_dict_needs_a_unit_even_where_load_would_not() -> None:
    assert wire.load({"value": "0.25"}, Proportion) == Ratio(0.25)
    with pytest.raises(ParseError, match="'unit' missing"):
        wire.from_dict({"value": "0.25"}, Proportion)
    assert wire.from_dict({"value": "0.25", "unit": "1"}, Proportion) == Ratio(0.25)


def test_from_dict_reads_archaic_units_where_asked() -> None:
    data = {"value": "2", "unit": "arshin"}
    assert wire.from_dict(data, Length, allow_archaic=True) == russian_length.Arshin(2)
    with pytest.raises(UnknownUnitError, match="archaic"):
        wire.from_dict(data, Length)
    assert wire.to_dict(russian_length.Arshin(2)) == data


def test_from_dict_takes_a_quantity_type_with_units() -> None:
    with pytest.raises(TypeError, match="quantity type"):
        wire.from_dict({"value": "5", "unit": "V"}, Volt)  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


def test_a_mapping_of_another_quantity_is_read_as_that_quantity_only() -> None:
    data = wire.to_dict(Volt(1))
    with pytest.raises(UnknownUnitError):
        wire.from_dict(data, Current)


def test_a_degree_written_in_radians_keeps_its_value() -> None:
    written = wire.to_dict(Degree(90), unit="rad")
    assert wire.from_dict(written, type(Degree(90))) == Degree(90)


class Dinosaur:
    """Nothing `to_dict` should take for a unit."""


@pytest.mark.parametrize(
    "unit",
    [5, 1.5, True, [VOLT], {"unit": "V"}, Dinosaur(), Voltage, Volt(1), AMPERE, KELVIN],
    ids=lambda unit: type(unit).__name__ + ":" + str(getattr(unit, "name", unit))[:12],
)
def test_a_unit_that_is_no_unit_of_the_quantity_is_refused(unit: object) -> None:
    with pytest.raises(InvalidConversionError):
        wire.to_dict(Millivolt(2800), unit=unit)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_unit_of_a_temperature_or_a_level_is_a_unit_constant_too() -> None:
    from kuchka.units import DECIBEL
    from kuchka.units.thermal import KELVIN as KELVIN_OF_TEMPERATURE

    assert wire.to_dict(Celsius(20), unit=KELVIN_OF_TEMPERATURE) == {
        "value": "293.15",
        "unit": "K",
    }
    assert wire.to_dict(Decibel(3), unit=DECIBEL) == {"value": "3", "unit": "dB"}


@pytest.mark.parametrize(
    "form", [True, False, None, "float", "exact", 1, 0.5, object()]
)
def test_the_form_of_the_value_is_a_value_form_and_nothing_else(form: object) -> None:
    with pytest.raises(TypeError, match="ValueForm"):
        wire.to_dict(Volt(1), form=form)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_default_form_is_exact() -> None:
    assert wire.to_dict(Volt(1) / 3) == wire.to_dict(
        Volt(1) / 3, form=wire.ValueForm.Exact
    )
    assert [member.name for member in wire.ValueForm] == ["Exact", "Float"]
