"""Raising a linear quantity to an integer power."""

from __future__ import annotations

import pytest

from kuchka import Area
from kuchka import IncompatibleDimensionError
from kuchka import UnrepresentableDimensionError
from kuchka import VelocitySquared
from kuchka import Volume
from kuchka.units import length
from kuchka.units import proportion
from kuchka.units.electromagnetics import resistance
from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.kinematics import velocity
from kuchka.units.temporal import frequency
from kuchka.units.temporal import sample_rate
from kuchka.units.temporal import time


def test_a_square_and_a_cube_are_the_products_written_out() -> None:
    side = length.Metre(3)
    assert side**2 == area.SquareMetre(9)
    assert side**3 == volume.CubicMetre(27)
    assert type(side**2) is Area
    assert type(side**3) is Volume


def test_a_rule_applies_to_the_product_a_power_is() -> None:
    assert type(velocity.MetrePerSecond(3) ** 2) is VelocitySquared


def test_a_power_is_exact() -> None:
    assert length.Metre(0.1) ** 3 == volume.CubicMetre(0.001)


def test_a_negative_exponent_is_the_reciprocal_of_the_power() -> None:
    assert time.Second(2) ** -1 == frequency.Hertz(0.5)


def test_an_exponent_of_zero_is_a_ratio_of_one() -> None:
    assert length.Metre(0) ** 0 == proportion.Ratio(1)


def test_a_power_with_no_type_is_unrepresentable() -> None:
    with pytest.raises(UnrepresentableDimensionError):
        resistance.Ohm(2) ** 2


def test_a_role_is_raised_to_a_power_through_its_conversion() -> None:
    with pytest.raises(IncompatibleDimensionError):
        sample_rate.SamplesPerSecond(10) ** 2


@pytest.mark.parametrize("exponent", [0.5, 2.0, True], ids=["half", "float", "bool"])
def test_an_exponent_is_an_integer(exponent: object) -> None:
    with pytest.raises(TypeError):
        length.Metre(4) ** exponent  # type: ignore[operator]  # ty: ignore[unsupported-operator]
