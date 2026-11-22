"""`kuchka.pydantic.Bounds` limits the range of a Pydantic quantity field."""

from __future__ import annotations

from typing import Annotated

import pytest

from kuchka import Current
from kuchka import Proportion
from kuchka import Temperature
from kuchka import Voltage
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("pydantic")

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import TypeAdapter
from pydantic import ValidationError

from kuchka.pydantic import Bounds
from kuchka.pydantic import Quantity

SUPPLY = Bounds(gt=voltage.Volt(0), le=voltage.Volt(60))


class PowerSupplyConfig(BaseModel):
    """A supply limit and a duty, both bounded."""

    max_voltage: Annotated[Voltage, Quantity, SUPPLY]
    duty: Annotated[
        Proportion, Quantity, Bounds(ge=proportion.Ratio(0), le=proportion.Ratio(1))
    ] = Field(default="25 %", validate_default=True)


@pytest.mark.parametrize(
    "value", ["12 V", "60 V", "60000 mV", "0.001 V", voltage.Volt(5)]
)
def test_a_value_within_the_bounds_is_accepted(value: object) -> None:
    config = PowerSupplyConfig.model_validate({"max_voltage": value})
    assert config.max_voltage in SUPPLY


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("0 V", "0 V is not above 0 V."),
        ("-1 V", "-1 V is not above 0 V."),
        ("61 V", "61 V is above 60 V, the most allowed."),
        (voltage.Millivolt(60001), "60001 mV is above 60 V, the most allowed."),
    ],
)
def test_a_value_outside_the_bounds_is_a_validation_error_that_says_why(
    value: object, message: str
) -> None:
    with pytest.raises(ValidationError) as raised:
        PowerSupplyConfig.model_validate({"max_voltage": value})
    (error,) = raised.value.errors()
    assert error["loc"] == ("max_voltage",)
    assert error["msg"] == f"Value error, {message}"


def test_a_value_that_does_not_read_is_refused_before_the_bounds_see_it() -> None:
    with pytest.raises(ValidationError, match="has no unit"):
        PowerSupplyConfig.model_validate({"max_voltage": 3.3})


def test_a_proportion_in_percent_is_held_to_the_bounds_in_ratios() -> None:
    assert PowerSupplyConfig.model_validate({"max_voltage": "1 V", "duty": "100 %"})
    for bad in (25, "25", 1.5, "101 %"):
        with pytest.raises(ValidationError, match="is above 1, the most allowed"):
            PowerSupplyConfig.model_validate({"max_voltage": "1 V", "duty": bad})


def test_a_default_is_checked_when_the_model_validates_defaults() -> None:
    class Defaulted(BaseModel):
        limit: Annotated[Voltage, Quantity, SUPPLY] = Field(
            default="99 V", validate_default=True
        )

    with pytest.raises(ValidationError, match="is above 60 V"):
        Defaulted()


def test_an_unvalidated_default_is_not_checked() -> None:
    class Unvalidated(BaseModel):
        limit: Annotated[Voltage, Quantity, SUPPLY] = voltage.Volt(99)

    assert Unvalidated().limit == voltage.Volt(99)


def test_json_input_and_output_are_checked_and_unchanged() -> None:
    config = PowerSupplyConfig.model_validate_json(
        '{"max_voltage": "12 V", "duty": 0.5}'
    )
    assert config.model_dump_json() == '{"max_voltage":"12 V","duty":"0.5"}'
    with pytest.raises(ValidationError, match="is above 60 V"):
        PowerSupplyConfig.model_validate_json('{"max_voltage": "99 V"}')


def test_the_bounds_apply_inside_containers_and_unions() -> None:
    class Nested(BaseModel):
        optional: Annotated[Voltage, Quantity, SUPPLY] | None = None
        many: list[Annotated[Voltage, Quantity, SUPPLY]] = []

    assert Nested.model_validate({"optional": None}).optional is None
    with pytest.raises(ValidationError, match=r"many\.1"):
        Nested.model_validate({"many": ["1 V", "99 V"]})
    with pytest.raises(ValidationError, match="is above 60 V"):
        Nested.model_validate({"optional": "99 V"})


def test_the_json_schema_says_the_range_in_the_description() -> None:
    schema = PowerSupplyConfig.model_json_schema()["properties"]
    assert schema["max_voltage"]["description"].endswith(
        "It is above 0 V and at most 60 V."
    )
    assert schema["max_voltage"]["type"] == "string"
    assert schema["duty"]["description"].endswith("It is at least 0 and at most 1.")
    assert "anyOf" in schema["duty"]


LOWER = Bounds(ge=voltage.Volt(1))
UPPER = Bounds(le=voltage.Volt(60))
ORDERS = [
    pytest.param(order, id="-".join(name for name in names))
    for order, names in [
        ((Quantity, LOWER, UPPER), ("Q", "lo", "hi")),
        ((Quantity, UPPER, LOWER), ("Q", "hi", "lo")),
        ((LOWER, Quantity, UPPER), ("lo", "Q", "hi")),
        ((UPPER, LOWER, Quantity), ("hi", "lo", "Q")),
        ((LOWER, UPPER, Quantity), ("lo", "hi", "Q")),
        ((UPPER, Quantity, LOWER), ("hi", "Q", "lo")),
    ]
]


CONFIGS = [
    pytest.param(ConfigDict(), id="default"),
    pytest.param(ConfigDict(arbitrary_types_allowed=True), id="arbitrary_types"),
]


@pytest.mark.parametrize("config", CONFIGS)
@pytest.mark.parametrize("order", ORDERS)
def test_every_bound_is_checked_whichever_order_the_annotations_are_written(
    order: tuple[object, ...], config: ConfigDict
) -> None:
    adapter = TypeAdapter(Annotated[Voltage, *order], config=config)
    assert adapter.validate_python("12 V") == voltage.Volt(12)
    with pytest.raises(ValidationError, match="is below 1 V, the least allowed"):
        adapter.validate_python("0 V")
    with pytest.raises(ValidationError, match="is above 60 V, the most allowed"):
        adapter.validate_python("61 V")


@pytest.mark.parametrize("config", CONFIGS)
@pytest.mark.parametrize("order", ORDERS)
def test_every_range_is_in_the_description_whichever_order_they_are_written(
    order: tuple[object, ...], config: ConfigDict
) -> None:
    adapter = TypeAdapter(Annotated[Voltage, *order], config=config)
    description = adapter.json_schema()["description"]
    assert "It is at least 1 V." in description
    assert "It is at most 60 V." in description


def test_bounds_written_before_quantity_survive_a_container() -> None:
    class Listed(BaseModel):
        many: list[Annotated[Voltage, SUPPLY, Quantity]]

    assert Listed.model_validate({"many": ["1 V"]}).many == [voltage.Volt(1)]
    with pytest.raises(ValidationError, match="is above 60 V"):
        Listed.model_validate({"many": ["99 V"]})


def test_a_field_of_another_quantity_type_is_reported_when_the_class_is_defined() -> (
    None
):
    with pytest.raises(TypeError, match="bounds of Voltage on a field of Current"):

        class Wrong(BaseModel):
            limit: Annotated[Current, Quantity, SUPPLY]


def test_bounds_without_quantity_are_reported_when_the_class_is_defined() -> None:
    with pytest.raises(TypeError, match="needs Quantity beside it"):

        class Bare(BaseModel):
            limit: Annotated[Voltage, SUPPLY]


def test_bounds_of_a_quantity_with_no_ordering_are_refused_where_they_are_written() -> (
    None
):
    from kuchka.units import angular

    with pytest.raises(TypeError, match="no ordering"):
        Bounds(ge=angular.Degree(0))  # type: ignore[type-var]  # ty: ignore[invalid-argument-type]


def test_the_bounds_of_an_affine_field_hold() -> None:
    adapter = TypeAdapter(
        Annotated[
            Temperature,
            Quantity,
            Bounds(ge=thermal.Celsius(-40), le=thermal.Celsius(85)),
        ]
    )
    assert adapter.validate_python("-40 \u00b0C") == thermal.Celsius(-40)
    assert adapter.validate_python("-40 \u00b0F") == thermal.Fahrenheit(-40)
    with pytest.raises(ValidationError, match="is above 85"):
        adapter.validate_python("86 \u00b0C")


def test_bounds_without_quantity_are_reported_even_for_a_type_pydantic_can_build() -> (
    None
):
    with pytest.raises(TypeError, match="needs Quantity beside it"):
        TypeAdapter(
            Annotated[Voltage, SUPPLY], config=ConfigDict(arbitrary_types_allowed=True)
        )


def test_a_second_quantity_does_not_drop_the_bounds_written_between() -> None:
    adapter = TypeAdapter(Annotated[Voltage, Quantity, LOWER, Quantity])
    with pytest.raises(ValidationError, match="is below 1 V"):
        adapter.validate_python("0 V")
