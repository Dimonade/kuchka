"""An `Angle` does not take part in arithmetic, and says what to use instead.

An angle is a position on a circle and wraps: 370 degrees is 10 degrees, so there is no
product or quotient of it that means anything.
Scaling it by a plain number is allowed.
Combining it with a quantity is refused with a message that points at
`to_angular_displacement()`, the angle swept, which does take part.
"""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka.units import angular
from kuchka.units import energy
from kuchka.units import proportion
from kuchka.units import time
from kuchka.units import torque

ANGLE = angular.Radian(1)
QUANTITIES = (
    ("a torque", torque.NewtonMetre(1)),
    ("an energy", energy.Joule(1)),
    ("a time", time.Second(1)),
    ("a proportion", proportion.Ratio(2)),
    ("another angle", angular.Degree(90)),
)
IDS = [name.replace(" ", "-") for name, _ in QUANTITIES]


@pytest.mark.parametrize(("name", "other"), QUANTITIES, ids=IDS)
def test_an_angle_times_a_quantity_is_refused_with_a_pointer(name, other) -> None:
    del name
    for left, right in ((ANGLE, other), (other, ANGLE)):
        with pytest.raises(IncompatibleDimensionError, match="multiply") as caught:
            left * right
        assert "to_angular_displacement()" in str(caught.value)


@pytest.mark.parametrize(("name", "other"), QUANTITIES, ids=IDS)
def test_an_angle_divided_by_or_into_a_quantity_is_refused_with_a_pointer(
    name, other
) -> None:
    del name
    for left, right in ((ANGLE, other), (other, ANGLE)):
        with pytest.raises(IncompatibleDimensionError, match="divide") as caught:
            left / right
        assert "to_angular_displacement()" in str(caught.value)


def test_the_refusal_names_both_operands() -> None:
    with pytest.raises(IncompatibleDimensionError, match="`Energy` and `Angle`"):
        energy.Joule(1) / ANGLE


def test_a_plain_number_still_scales_an_angle() -> None:
    assert angular.Radian(2) == ANGLE * 2
    assert angular.Radian(2) == 2 * ANGLE
    assert angular.Radian(1) / 2 == ANGLE / 2
    assert angular.Degree(90) * 4 == angular.Degree(360)


def test_a_plain_number_does_not_divide_into_an_angle() -> None:
    with pytest.raises(TypeError):
        1 / ANGLE  # type: ignore[operator]


def test_the_pointer_works() -> None:
    swept = angular.Degree(90).to_angular_displacement()
    assert swept / time.Second(1) == angular.DegreeDisplacement(90) / time.Second(1)
    assert type(torque.NewtonMetre(2) * swept) is energy.Energy


def test_something_that_is_not_a_number_is_neither_a_factor_nor_a_divisor() -> None:
    for operand in ("x", None, object()):
        with pytest.raises(TypeError):
            ANGLE * operand  # type: ignore[operator]
        with pytest.raises(TypeError):
            ANGLE / operand  # type: ignore[operator]
        with pytest.raises(TypeError):
            operand / ANGLE  # type: ignore[operator]
