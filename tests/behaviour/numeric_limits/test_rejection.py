"""Rejection is cheap, and every entry point is bounded."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.numeric import to_exact
from kuchka.units import voltage

BITS = NUMERIC_LIMITS.max_exact_bits


MESSAGE_LENGTH_CEILING = 300


def test_an_enormous_int_is_rejected_with_the_library_error() -> None:
    # Rendering an int this large would raise ValueError (the interpreter's
    # digit-conversion limit) instead of InvalidMeasurementError.
    with pytest.raises(InvalidMeasurementError) as caught:
        to_exact(10**100_000)
    assert len(str(caught.value)) < MESSAGE_LENGTH_CEILING


def test_an_enormous_fraction_is_rejected_with_a_short_message() -> None:
    with pytest.raises(InvalidMeasurementError) as caught:
        to_exact(Fraction(10**100_000, 7))
    assert len(str(caught.value)) < MESSAGE_LENGTH_CEILING


def test_a_decimal_with_millions_of_digits_is_rejected_with_a_short_message() -> None:
    value = Decimal("9" * 2_000_000)
    with pytest.raises(InvalidMeasurementError) as caught:
        to_exact(value)
    assert len(str(caught.value)) < MESSAGE_LENGTH_CEILING


def test_unit_constructor_rejects_an_oversized_number() -> None:
    with pytest.raises(InvalidMeasurementError):
        voltage.Volt(10**100_000)


def test_scalar_multiplication_rejects_an_oversized_factor() -> None:
    with pytest.raises(InvalidMeasurementError):
        voltage.Volt(1) * 2**BITS


def test_scalar_division_rejects_an_oversized_divisor() -> None:
    with pytest.raises(InvalidMeasurementError):
        voltage.Volt(1) / Decimal("1E+5000000")


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_decimal_is_reported_as_not_finite(literal: str) -> None:
    with pytest.raises(InvalidMeasurementError, match="not finite"):
        to_exact(Decimal(literal))
