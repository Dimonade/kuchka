"""`kuchka.pydantic.Quantity` makes a Pydantic field a quantity, whatever arrived.

The reading and the writing are `kuchka.wire`, tested once for every input in the tests
of `wire`; this module covers what the bridge adds: the validation error, the
serialization modes, the JSON Schema, the places a field can sit, and the failures at
definition time.
"""

from __future__ import annotations

import copy
import pickle
import subprocess
import sys
import warnings
from decimal import Decimal
from fractions import Fraction
from typing import Annotated

import pytest

from kuchka import Current
from kuchka import Length
from kuchka import Proportion
from kuchka import Temperature
from kuchka import Voltage
from kuchka.units import current
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.archaic.russian import length as russian_length
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("pydantic")

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import TypeAdapter
from pydantic import ValidationError

from kuchka.pydantic import Quantity

VoltageField = Annotated[Voltage, Quantity]


class PowerSupplyConfig(BaseModel):
    """A supply limit and a duty."""

    max_voltage: VoltageField
    duty: Annotated[Proportion, Quantity] = Field(default="25 %", validate_default=True)


class Nested(BaseModel):
    """Fields of every shape a field can take."""

    optional: VoltageField | None = None
    many: list[VoltageField] = []
    by_name: dict[str, VoltageField] = {}
    temperature: Annotated[Temperature, Quantity] | None = None


QUARTER = proportion.Ratio(Fraction(1, 4))


@pytest.mark.parametrize(
    "value",
    [
        "2800 mV",
        "2.8 V",
        "14/5 V",
        {"value": "2800", "unit": "mV"},
        voltage.Millivolt(2800),
    ],
)
def test_a_field_is_the_quantity_whatever_arrived(value: object) -> None:
    config = PowerSupplyConfig.model_validate({"max_voltage": value})
    assert config.max_voltage == voltage.Volt(Decimal("2.8"))
    assert isinstance(config.max_voltage, Voltage)


def test_an_instance_passes_through_unchanged() -> None:
    value = voltage.Volt(3.3)
    assert PowerSupplyConfig.model_validate({"max_voltage": value}).max_voltage is value


def test_a_field_keeps_the_unit_that_was_written() -> None:
    config = PowerSupplyConfig.model_validate({"max_voltage": "2800 mV"})
    assert config.max_voltage.unit is voltage.MILLIVOLT


@pytest.mark.parametrize(
    "duty", [0.25, Decimal("0.25"), Fraction(1, 4), "0.25", "25 %"]
)
def test_a_proportion_field_reads_a_number_too(duty: object) -> None:
    config = PowerSupplyConfig.model_validate({"max_voltage": "1 V", "duty": duty})
    assert config.duty == QUARTER


def test_a_json_number_is_read_for_a_proportion_only() -> None:
    config = PowerSupplyConfig.model_validate_json(
        '{"max_voltage": "1 V", "duty": 0.1}'
    )
    assert config.duty == proportion.Ratio(Fraction(1, 10))
    with pytest.raises(ValidationError, match="has no unit"):
        PowerSupplyConfig.model_validate_json('{"max_voltage": 3.3}')


def test_a_default_is_read_when_validation_of_defaults_is_on() -> None:
    config = PowerSupplyConfig.model_validate({"max_voltage": "1 V"})
    assert config.duty.unit is proportion.PERCENT


@pytest.mark.parametrize(
    "value",
    [
        3.3,
        3,
        True,
        None,
        "3.3",
        "five volts",
        "150 mA",
        current.Ampere(1),
        {"value": "3"},
    ],
)
def test_a_value_that_is_no_voltage_is_a_validation_error(value: object) -> None:
    with pytest.raises(ValidationError) as raised:
        PowerSupplyConfig.model_validate({"max_voltage": value})
    (error,) = raised.value.errors()
    assert error["loc"] == ("max_voltage",)
    assert error["type"] == "value_error"


def test_the_validation_error_says_what_to_write() -> None:
    with pytest.raises(ValidationError, match=r'such as "5 V"'):
        PowerSupplyConfig.model_validate({"max_voltage": 3.3})
    with pytest.raises(ValidationError, match=r"is no Voltage"):
        PowerSupplyConfig.model_validate({"max_voltage": current.Ampere(1)})
    with pytest.raises(ValidationError, match=r"not a unit of Voltage"):
        PowerSupplyConfig.model_validate({"max_voltage": "150 mA"})


def test_a_value_the_quantity_cannot_hold_is_a_validation_error() -> None:
    adapter = TypeAdapter(Annotated[Temperature, Quantity])
    with pytest.raises(ValidationError):
        adapter.validate_python("-300 \u00b0C")


def test_python_dumping_keeps_the_quantity_and_json_dumping_writes_text() -> None:
    value = voltage.Millivolt(Fraction(7, 3))
    config = PowerSupplyConfig(max_voltage=value, duty=QUARTER)
    assert config.model_dump()["max_voltage"] is value
    assert config.model_dump(mode="json") == {"max_voltage": "7/3 mV", "duty": "0.25"}
    assert config.model_dump_json() == '{"max_voltage":"7/3 mV","duty":"0.25"}'


def test_json_round_trips_exactly() -> None:
    config = PowerSupplyConfig(
        max_voltage=voltage.Millivolt(Fraction(7, 3)), duty=proportion.Percent(25)
    )
    restored = PowerSupplyConfig.model_validate_json(config.model_dump_json())
    assert restored == config
    assert restored.max_voltage.unit is voltage.MILLIVOLT
    assert restored.duty.unit is proportion.PERCENT


def test_a_field_works_inside_containers_and_unions() -> None:
    model = Nested.model_validate(
        {
            "optional": None,
            "many": ["1 V", {"value": "2", "unit": "mV"}],
            "by_name": {"a": "3 V"},
            "temperature": "-40 \u00b0C",
        }
    )
    assert model.optional is None
    assert model.many == [voltage.Volt(1), voltage.Millivolt(2)]
    assert model.by_name == {"a": voltage.Volt(3)}
    assert model.temperature == thermal.Celsius(-40)
    assert Nested.model_validate_json(model.model_dump_json()) == model
    with pytest.raises(ValidationError):
        Nested.model_validate({"many": ["1 V", 2.5]})


def test_assignment_is_validated_when_the_model_asks_for_it() -> None:
    class Live(BaseModel):
        model_config = ConfigDict(validate_assignment=True)
        limit: VoltageField

    live = Live(limit=voltage.Volt(1))
    live.limit = "5 V"  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
    assert live.limit == voltage.Volt(5)
    with pytest.raises(ValidationError):
        live.limit = 5  # type: ignore[assignment]  # ty: ignore[invalid-assignment]


def test_a_model_copies_and_pickles_with_its_quantities() -> None:
    config = PowerSupplyConfig(max_voltage=voltage.Millivolt(Fraction(7, 3)))
    assert copy.deepcopy(config) == config
    assert config.model_copy(deep=True) == config
    assert pickle.loads(pickle.dumps(config)) == config


def test_the_json_schema_of_a_quantity_is_a_string_that_names_it() -> None:
    schema = PowerSupplyConfig.model_json_schema()["properties"]["max_voltage"]
    assert schema["type"] == "string"
    assert "Voltage" in schema["description"]
    assert schema["examples"] == ["5 V"]
    serialization = PowerSupplyConfig.model_json_schema(mode="serialization")
    assert serialization["properties"]["max_voltage"] == schema | {
        "title": "Max Voltage"
    }


def test_the_json_schema_of_a_proportion_allows_a_number() -> None:
    schema = PowerSupplyConfig.model_json_schema()["properties"]["duty"]
    assert schema["anyOf"] == [{"type": "string"}, {"type": "number"}]
    assert "Proportion" in schema["description"]


def test_the_json_schema_carries_a_default_written_as_text() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        schema = PowerSupplyConfig.model_json_schema()
    assert schema["properties"]["duty"]["default"] == "25 %"


@pytest.mark.parametrize("value", [3.3, 3, None, object()])
def test_a_value_that_is_no_quantity_and_no_text_is_not_written(value: object) -> None:
    class Loose(BaseModel):
        limit: VoltageField

    loose = Loose.model_construct(limit=value)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        loose.model_dump_json()


def test_the_json_schema_reaches_through_containers() -> None:
    properties = Nested.model_json_schema()["properties"]
    assert properties["many"]["items"]["type"] == "string"
    assert properties["by_name"]["additionalProperties"]["type"] == "string"
    assert {"type": "null"} in properties["optional"]["anyOf"]


def test_an_archaic_unit_is_read_where_the_field_allows_it() -> None:
    class Plot(BaseModel):
        side: Annotated[Length, Quantity(allow_archaic=True)]

    class Modern(BaseModel):
        side: Annotated[Length, Quantity]

    assert Plot.model_validate({"side": "3 arshin"}).side == russian_length.Arshin(3)
    with pytest.raises(ValidationError, match="archaic"):
        Modern.model_validate({"side": "3 arshin"})


def test_a_field_that_is_no_quantity_type_fails_when_the_class_is_defined() -> None:
    with pytest.raises(TypeError, match="quantity type"):

        class Bad(BaseModel):
            count: Annotated[int, Quantity]


def test_a_policy_that_is_no_policy_fails_when_the_marker_is_made() -> None:
    with pytest.raises(TypeError, match="ArchaicPolicy"):
        Quantity(allow_archaic="yes")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_quantity_classes_carry_no_pydantic_code() -> None:
    for quantity in (Voltage, Current, Temperature, Proportion):
        assert not hasattr(quantity, "__get_pydantic_core_schema__")


def test_importing_kuchka_loads_no_integration_library() -> None:
    program = (
        "import sys\n"
        "import kuchka\n"
        "loaded = [name for name in ('pydantic', 'pydantic_core', 'attrs', 'attr')"
        " if name in sys.modules]\n"
        "print(loaded)\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"


def test_a_missing_pydantic_says_how_to_install_it() -> None:
    program = (
        "import sys\nsys.modules['pydantic_core'] = None\nimport kuchka.pydantic\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True, check=False
    )
    assert result.returncode != 0
    assert "kuchka[pydantic]" in result.stderr
