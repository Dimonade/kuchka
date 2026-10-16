"""Dividing logarithmic and modular quantities by zero."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import DivisionByZeroError
from kuchka.units import angular
from kuchka.units import logarithmic

ZEROS = [0, 0.0, Decimal(0), Fraction(0), Decimal("0E+5")]


ZERO_IDS = ["int", "float", "decimal", "fraction", "decimal_exponent"]


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_a_level_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        logarithmic.Decibel(3) / zero  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_level_divided_by_a_zero_level() -> None:
    with pytest.raises(DivisionByZeroError):
        logarithmic.Decibel(3) / logarithmic.Decibel(0)


def test_a_level_divided_by_a_non_zero_number_is_unchanged() -> None:
    assert logarithmic.Decibel(6) / 2 == logarithmic.Decibel(3)


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_an_angle_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        angular.Degree(90) / zero


def test_an_angle_divided_by_a_non_zero_number_is_unchanged() -> None:
    assert angular.Degree(90) / 2 == angular.Degree(45)
