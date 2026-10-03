"""Dividing by zero raises `DivisionByZeroError`, a `MeasurementError`.

Every division in the library goes through one exact quotient, so a zero divisor is
reported the same way wherever it comes from: a quantity or a plain number as the
divisor, a quantity in the denominator of `1 / x`, and a linear, logarithmic, or modular
dividend.
The error is also a `ZeroDivisionError`, so existing handlers for either class keep
working.
A unit definition cannot have a zero scale, since every value read back in that unit
would divide by it.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

import kuchka
import kuchka.errors
from kuchka import Ampere
from kuchka import Decibel
from kuchka import Degree
from kuchka import DivisionByZeroError
from kuchka import Hertz
from kuchka import InvalidMeasurementError
from kuchka import MeasurementError
from kuchka import Ohm
from kuchka import Second
from kuchka import Volt
from kuchka.numeric import exact_quotient
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import UnitDef
from tests.quantity_families import FAMILIES
from tests.quantity_families import FAMILY_IDS

ZEROS = [0, 0.0, Decimal(0), Fraction(0), Decimal("0E+5")]
ZERO_IDS = ["int", "float", "decimal", "fraction", "decimal_exponent"]


# The error.


def test_the_error_is_both_a_measurement_error_and_a_zero_division_error() -> None:
    assert issubclass(DivisionByZeroError, MeasurementError)
    assert issubclass(DivisionByZeroError, ZeroDivisionError)


def test_the_error_is_exported_at_the_top_level() -> None:
    assert kuchka.DivisionByZeroError is kuchka.errors.DivisionByZeroError
    assert "DivisionByZeroError" in kuchka.__all__


def test_the_message_quotes_both_operands() -> None:
    with pytest.raises(DivisionByZeroError) as caught:
        Volt(1) / Volt(0)
    assert str(caught.value) == "cannot divide 1 V by 0 V: the divisor is zero."


def test_the_operands_are_attributes_of_the_error() -> None:
    with pytest.raises(DivisionByZeroError) as caught:
        Volt(5) / 0
    assert caught.value.dividend == Volt(5)
    assert caught.value.divisor == 0


def test_either_base_class_catches_it() -> None:
    with pytest.raises(MeasurementError):
        Volt(1) / 0
    with pytest.raises(ZeroDivisionError):
        Volt(1) / 0


# Linear quantities.


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_a_linear_quantity_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        Volt(1) / zero


def test_a_linear_quantity_divided_by_a_zero_quantity_of_its_own_type() -> None:
    with pytest.raises(DivisionByZeroError):
        Volt(1) / Volt(0)


def test_a_linear_quantity_divided_by_a_zero_quantity_of_another_type() -> None:
    with pytest.raises(DivisionByZeroError):
        Volt(1) / Ampere(0)


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_the_reciprocal_of_a_zero_quantity(zero: object) -> None:
    quantity = Second(zero)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(DivisionByZeroError):
        1 / quantity


def test_zero_over_zero_is_still_a_division_by_zero() -> None:
    with pytest.raises(DivisionByZeroError):
        Volt(0) / Volt(0)
    with pytest.raises(DivisionByZeroError):
        0 / Ohm(0)


def test_the_error_takes_precedence_over_a_dimension_the_library_cannot_name() -> None:
    with pytest.raises(DivisionByZeroError):
        Ohm(1) / Ohm(0)


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_every_linear_family_reports_a_zero_divisor(family) -> None:
    with pytest.raises(DivisionByZeroError):
        family.canonical(1) / 0
    with pytest.raises(DivisionByZeroError):
        family.canonical(1) / family.canonical(0)


def test_division_by_a_non_zero_divisor_is_unchanged() -> None:
    assert Volt(6) / 3 == Volt(2)
    assert Volt(6) / Volt(3) == Fraction(2)
    assert 1 / Second(4) == Hertz(Fraction(1, 4))


def test_a_zero_dividend_is_fine() -> None:
    assert Volt(0) / 3 == Volt(0)
    assert Volt(0) / Volt(2) == Fraction(0)
    assert 0 / Second(2) == Hertz(0)


# Logarithmic quantities.


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_a_level_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        Decibel(3) / zero  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_level_divided_by_a_zero_level() -> None:
    with pytest.raises(DivisionByZeroError):
        Decibel(3) / Decibel(0)


def test_a_level_divided_by_a_non_zero_number_is_unchanged() -> None:
    assert Decibel(6) / 2 == Decibel(3)


# Modular quantities.


@pytest.mark.parametrize("zero", ZEROS, ids=ZERO_IDS)
def test_an_angle_divided_by_a_zero_number(zero: object) -> None:
    with pytest.raises(DivisionByZeroError):
        Degree(90) / zero


def test_an_angle_divided_by_a_non_zero_number_is_unchanged() -> None:
    assert Degree(90) / 2 == Degree(45)


# The shared quotient.


def test_the_exact_quotient_divides_exactly() -> None:
    assert exact_quotient(Fraction(1), Fraction(3), left=1, right=3) == Fraction(1, 3)


def test_the_exact_quotient_rejects_a_zero_divisor() -> None:
    with pytest.raises(DivisionByZeroError, match="divisor is zero"):
        exact_quotient(Fraction(1), Fraction(0), left="a", right="b")


# Unit definitions cannot have a zero scale.

DIMENSION = Volt(1).dimension
UNIT_DEFINITIONS = [
    pytest.param(lambda scale: UnitDef("test", "t", scale, DIMENSION), id="linear"),
    pytest.param(lambda scale: AffineUnitDef("test", "t", scale, 0), id="affine"),
    pytest.param(
        lambda scale: LogarithmicUnitDef("test", "t", scale), id="logarithmic"
    ),
]


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
@pytest.mark.parametrize("scale", [0, 0.0, Decimal(0), Fraction(0)], ids=ZERO_IDS[:4])
def test_a_zero_scale_is_rejected(build, scale: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="positive scale"):
        build(scale)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
@pytest.mark.parametrize("scale", [-1, Fraction(-1, 3)], ids=["int", "fraction"])
def test_a_negative_scale_is_rejected(build, scale: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="positive scale"):
        build(scale)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
def test_a_tiny_positive_scale_is_accepted(build) -> None:
    assert build(Fraction(1, 10**30)).scale == Fraction(1, 10**30)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
def test_the_scale_error_names_the_unit(build) -> None:
    with pytest.raises(InvalidMeasurementError, match="'test'"):
        build(0)
