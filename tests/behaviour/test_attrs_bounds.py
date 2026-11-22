"""`kuchka.attrs.Bounds` limits the range of an `attrs` quantity field."""

from __future__ import annotations

import pytest

from kuchka import BoundsError
from kuchka import Current
from kuchka import Proportion
from kuchka import Voltage
from kuchka.attrs import Bounds
from kuchka.attrs import parse_field
from kuchka.units import proportion
from kuchka.units.electromagnetics import voltage
from tests.support.libraries import require_or_skip

require_or_skip("attrs")

import attrs


@attrs.define(frozen=True)
class SensorSpec:
    """A bounded threshold and a bounded duty."""

    threshold: Voltage = attrs.field(
        converter=parse_field(Voltage),
        validator=Bounds(gt=voltage.Volt(0), le=voltage.Volt(60)),
    )
    duty: Proportion = attrs.field(
        converter=parse_field(Proportion),
        validator=Bounds(ge=proportion.Ratio(0), le=proportion.Ratio(1)),
        default="50 %",
    )


@pytest.mark.parametrize("threshold", ["12 V", "60 V", "60000 mV", voltage.Volt(5)])
def test_a_value_within_the_bounds_is_accepted(threshold: object) -> None:
    assert SensorSpec(threshold).threshold in Bounds(  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
        gt=voltage.Volt(0), le=voltage.Volt(60)
    )


@pytest.mark.parametrize(
    ("threshold", "message"),
    [
        ("0 V", "threshold: 0 V is not above 0 V."),
        ("61 V", "threshold: 61 V is above 60 V, the most allowed."),
        (voltage.Millivolt(-5), "threshold: -5 mV is not above 0 V."),
    ],
)
def test_a_value_outside_the_bounds_raises_with_the_name_of_the_attribute(
    threshold: object, message: str
) -> None:
    with pytest.raises(BoundsError) as raised:
        SensorSpec(threshold)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert str(raised.value) == message
    assert isinstance(raised.value, ValueError)


def test_the_bounds_run_after_the_converter() -> None:
    assert SensorSpec("12 V").threshold == voltage.Volt(12)
    with pytest.raises(ValueError, match="has no unit"):
        SensorSpec(12)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_a_proportion_in_percent_is_held_to_the_bounds_in_ratios() -> None:
    assert SensorSpec("1 V", "100 %").duty == proportion.Percent(100)
    for bad in (25, "25", "101 %"):
        with pytest.raises(BoundsError, match=r"duty: .* is above 1"):
            SensorSpec("1 V", bad)  # type: ignore[arg-type]


def test_the_bounds_are_checked_on_assignment_where_attrs_asks_for_it() -> None:
    @attrs.define
    class Live:
        limit: Voltage = attrs.field(
            converter=parse_field(Voltage),
            validator=Bounds(le=voltage.Volt(60)),
        )

    live = Live("5 V")
    live.limit = "7 V"  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
    assert live.limit == voltage.Volt(7)
    with pytest.raises(BoundsError, match="limit: 99 V is above 60 V"):
        live.limit = "99 V"  # type: ignore[assignment]  # ty: ignore[invalid-assignment]


def test_a_converter_and_bounds_of_different_types_name_the_attribute() -> None:
    @attrs.define
    class Mismatch:
        draw: Current = attrs.field(
            converter=parse_field(Current),
            validator=Bounds(le=voltage.Volt(60)),  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
        )

    with pytest.raises(TypeError, match="draw: bounds of Voltage cannot check Current"):
        Mismatch("1 A")


def test_bounds_sit_in_a_list_of_validators() -> None:
    @attrs.define
    class Listed:
        limit: Voltage = attrs.field(
            converter=parse_field(Voltage),
            validator=[Bounds(ge=voltage.Volt(1)), Bounds(le=voltage.Volt(60))],
        )

    assert Listed("5 V").limit == voltage.Volt(5)
    with pytest.raises(BoundsError):
        Listed("0 V")
    with pytest.raises(BoundsError):
        Listed("61 V")
