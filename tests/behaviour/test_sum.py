"""`sum()` starts from a plain 0, so a quantity needs a start of its own type."""

from __future__ import annotations

import pytest

from kuchka import InvalidMeasurementError
from kuchka.units import angular
from kuchka.units import logarithmic
from kuchka.units.electromagnetics import voltage

SHAPES = [
    pytest.param(voltage.Volt, "Volt", id="linear"),
    pytest.param(angular.Degree, "Turn", id="modular"),
    pytest.param(logarithmic.Decibel, "Decibel", id="logarithmic"),
]


@pytest.mark.parametrize(("make", "zero"), SHAPES)
def test_sum_without_a_start_names_the_start_it_needs(make, zero) -> None:
    with pytest.raises(
        InvalidMeasurementError, match=rf"sum\(values, start={zero}\(0\)\)"
    ):
        sum([make(1), make(2)])


@pytest.mark.parametrize(
    "make",
    [shape.values[0] for shape in SHAPES],
    ids=["linear", "modular", "logarithmic"],
)
def test_sum_with_a_start_of_the_same_type_adds(make) -> None:
    assert sum([make(1), make(2)], start=make(0)) == make(3)


def test_a_plain_number_other_than_zero_gets_no_sum_hint() -> None:
    with pytest.raises(InvalidMeasurementError) as caught:
        voltage.Volt(1) + 5  # type: ignore[operator]
    assert "sum" not in str(caught.value)
