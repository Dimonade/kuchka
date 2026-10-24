"""Dividing linear quantities by zero."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import DivisionByZeroError
from kuchka.units import current
from kuchka.units import frequency
from kuchka.units import proportion
from kuchka.units import resistance
from kuchka.units import time
from kuchka.units import voltage
from tests.support.families import FAMILIES
from tests.support.families import FAMILY_IDS

ZEROS = [0, 0.0, Decimal(0), Fraction(0), Decimal("0E+5")]


ZERO_IDS = ["int", "float", "decimal", "fraction", "decimal_exponent"]


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_a_linear_quantity_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        voltage.Volt(1) / zero


def test_a_linear_quantity_divided_by_a_zero_quantity_of_its_own_type() -> None:
    with pytest.raises(DivisionByZeroError):
        voltage.Volt(1) / voltage.Volt(0)


def test_a_linear_quantity_divided_by_a_zero_quantity_of_another_type() -> None:
    with pytest.raises(DivisionByZeroError):
        voltage.Volt(1) / current.Ampere(0)


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_the_reciprocal_of_a_zero_quantity(zero: object) -> None:
    quantity = time.Second(zero)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(DivisionByZeroError):
        1 / quantity


def test_zero_over_zero_is_still_a_division_by_zero() -> None:
    with pytest.raises(DivisionByZeroError):
        voltage.Volt(0) / voltage.Volt(0)
    with pytest.raises(DivisionByZeroError):
        0 / resistance.Ohm(0)


def test_the_error_takes_precedence_over_a_dimension_the_library_cannot_name() -> None:
    with pytest.raises(DivisionByZeroError):
        resistance.Ohm(1) / resistance.Ohm(0)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_every_linear_family_reports_a_zero_divisor(family) -> None:
    with pytest.raises(DivisionByZeroError):
        family.canonical(1) / 0
    with pytest.raises(DivisionByZeroError):
        family.canonical(1) / family.canonical(0)


def test_division_by_a_non_zero_divisor_is_unchanged() -> None:
    assert voltage.Volt(6) / 3 == voltage.Volt(2)
    assert voltage.Volt(6) / voltage.Volt(3) == proportion.Ratio(2)
    assert 1 / time.Second(4) == frequency.Hertz(Fraction(1, 4))


def test_a_zero_dividend_is_fine() -> None:
    assert voltage.Volt(0) / 3 == voltage.Volt(0)
    assert voltage.Volt(0) / voltage.Volt(2) == proportion.Ratio(0)
    assert 0 / time.Second(2) == frequency.Hertz(0)
