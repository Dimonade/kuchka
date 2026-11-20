"""`kuchka.attrs.parse_field` makes an `attrs` field a quantity, whatever arrives.

The converter is `kuchka.wire.load` for one quantity type, so what it reads and what it
refuses is tested once for every input in the tests of `wire`; this module covers what
the converter adds: the contract inside an `attrs` class, and a failure at definition
time for a field that cannot work.
"""

from __future__ import annotations

import subprocess
import sys
from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import ArchaicPolicy
from kuchka import Current
from kuchka import Length
from kuchka import ParseError
from kuchka import Proportion
from kuchka import Temperature
from kuchka import UnknownUnitError
from kuchka import Voltage
from kuchka.attrs import parse_field
from kuchka.units import current
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.archaic.russian import length as russian_length
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("attrs")

import attrs


@attrs.define(frozen=True)
class SensorSpec:
    """A sensor limit and a duty, both converted by their fields."""

    threshold: Voltage = attrs.field(converter=parse_field(Voltage))
    duty: Proportion = attrs.field(converter=parse_field(Proportion))


@attrs.define
class Reading:
    """A reading with a converted default."""

    temperature: Temperature = attrs.field(converter=parse_field(Temperature))
    drive: Voltage = attrs.field(converter=parse_field(Voltage), default="0 V")


QUARTER = proportion.Ratio(Fraction(1, 4))


@pytest.mark.parametrize(
    "threshold",
    [
        "2800 mV",
        "2.8 V",
        "14/5 V",
        {"value": "2800", "unit": "mV"},
        voltage.Millivolt(2800),
    ],
)
def test_a_field_is_the_quantity_whatever_arrived(threshold: object) -> None:
    spec = SensorSpec(threshold, 0.25)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert spec.threshold == voltage.Volt(Decimal("2.8"))
    assert isinstance(spec.threshold, Voltage)


@pytest.mark.parametrize(
    "duty", [0.25, Decimal("0.25"), Fraction(1, 4), "0.25", "25 %"]
)
def test_a_proportion_field_reads_a_number_too(duty: object) -> None:
    assert SensorSpec("1 V", duty).duty == QUARTER  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_an_instance_passes_through_unchanged() -> None:
    threshold = voltage.Volt(3.3)
    assert SensorSpec(threshold, 0.25).threshold is threshold


def test_the_field_keeps_the_unit_that_was_written() -> None:
    assert SensorSpec("2800 mV", 0.25).threshold.unit is voltage.MILLIVOLT


@pytest.mark.parametrize(
    ("threshold", "error"),
    [
        (3.3, ParseError),
        (3, ParseError),
        (True, ParseError),
        (None, ParseError),
        ("3.3", ParseError),
        ("five volts", ParseError),
        ("150 mA", UnknownUnitError),
        (current.Ampere(1), ParseError),
        ({"value": "3.3"}, ParseError),
    ],
)
def test_a_value_that_is_no_voltage_fails_when_the_instance_is_made(
    threshold: object, error: type[Exception]
) -> None:
    with pytest.raises(error):
        SensorSpec(threshold, 0.25)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_failure_is_a_value_error_and_names_the_value() -> None:
    with pytest.raises(ValueError, match="has no unit") as raised:
        SensorSpec(3.3, 0.25)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert "3.3" in str(raised.value)


def test_a_default_is_converted_too() -> None:
    assert Reading("21.5 degC").drive == voltage.Volt(0)


def test_converting_on_assignment_is_left_to_attrs() -> None:
    reading = Reading("21.5 degC")
    reading.temperature = "-40 °C"  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
    assert reading.temperature == thermal.Celsius(-40)
    assert attrs.evolve(reading, drive="3 V").drive == voltage.Volt(3)


def test_the_converter_names_the_quantity() -> None:
    assert parse_field(Voltage).__name__ == "parse_field(Voltage)"
    field = attrs.fields(SensorSpec).threshold
    assert field.converter is not None
    assert field.converter("1 V") == voltage.Volt(1)


def test_an_archaic_unit_is_read_where_the_field_allows_it() -> None:
    @attrs.define
    class Plot:
        side: Length = attrs.field(converter=parse_field(Length, allow_archaic=True))

    @attrs.define
    class Modern:
        side: Length = attrs.field(converter=parse_field(Length))

    assert Plot("3 arshin").side == russian_length.Arshin(3)
    with pytest.raises(UnknownUnitError, match="archaic"):
        Modern("3 arshin")
    allowed = parse_field(Length, allow_archaic=ArchaicPolicy.Allow)
    assert allowed("3 arshin") == russian_length.Arshin(3)


@pytest.mark.parametrize("quantity", [voltage.Volt, "Voltage", None, object, 5])
def test_a_field_that_is_no_quantity_type_fails_when_the_class_is_defined(
    quantity: object,
) -> None:
    with pytest.raises(TypeError, match="quantity type"):
        parse_field(quantity)  # type: ignore[call-overload]  # ty: ignore[no-matching-overload]


def test_a_policy_that_is_no_policy_fails_when_the_class_is_defined() -> None:
    with pytest.raises(TypeError, match="ArchaicPolicy"):
        parse_field(Current, allow_archaic="yes")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_module_needs_nothing_from_attrs() -> None:
    program = (
        "import sys\n"
        "sys.modules['attrs'] = sys.modules['attr'] = None\n"
        "from kuchka import Voltage\n"
        "from kuchka.attrs import parse_field\n"
        "print(parse_field(Voltage)('1 V'))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "1 V"
