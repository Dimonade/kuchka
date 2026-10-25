"""Copying a unit returns it, and copying a quantity keeps its library unit."""

from __future__ import annotations

import copy

import pytest

from kuchka.units import logarithmic
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage
from tests.units.helpers import _linear


def test_a_copied_quantity_keeps_the_library_unit() -> None:
    value = voltage.Volt(5)
    assert copy.copy(value).unit is voltage.VOLT
    assert copy.deepcopy(value).unit is voltage.VOLT
    assert copy.deepcopy(value).unit == voltage.VOLT


def test_a_copied_quantity_in_a_prefixed_unit_keeps_that_unit() -> None:
    assert (
        copy.deepcopy(voltage.Volt(5).to(voltage.MILLIVOLT)).unit is voltage.MILLIVOLT
    )


@pytest.mark.parametrize(
    "quantity", [thermal.Celsius(20), logarithmic.Decibel(3)], ids=["affine", "log"]
)
def test_copying_keeps_the_unit_of_every_shape(quantity: object) -> None:
    assert copy.deepcopy(quantity).unit is quantity.unit  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_a_custom_unit_copies_to_itself() -> None:
    unit = _linear(name="custom", symbol="cu")
    assert copy.copy(unit) is unit
    assert copy.deepcopy(unit) is unit


def test_deepcopy_of_a_container_of_units_keeps_each_unit() -> None:
    holder = {"units": [voltage.VOLT, voltage.MILLIVOLT, voltage.VOLT]}
    copied = copy.deepcopy(holder)
    assert copied["units"][0] is voltage.VOLT
    assert copied["units"][1] is voltage.MILLIVOLT
    assert copied["units"][2] is voltage.VOLT
