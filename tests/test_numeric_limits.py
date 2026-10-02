"""Exact input has a bounded size.

A number becomes a measurement by turning into an exact `Fraction`, whose cost grows
with its digits.
`to_exact` accepts numbers up to the limits in `NUMERIC_LIMITS` and raises
`InvalidMeasurementError`, quickly and without rendering the value, for anything
larger.
Everything that builds a measurement from a plain number (unit constructors, scalar
arithmetic, unit scales) goes through `to_exact`, so the bound holds for all of them.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

import kuchka.numeric
from kuchka import InvalidMeasurementError
from kuchka import Volt
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.internal.limits import NumericLimits
from kuchka.numeric import to_exact

EXPONENT = NUMERIC_LIMITS.max_decimal_exponent
DIGITS = NUMERIC_LIMITS.max_decimal_digits
BITS = NUMERIC_LIMITS.max_exact_bits

MESSAGE_LENGTH_CEILING = 300


# Decimal exponent.


@pytest.mark.parametrize("exponent", [EXPONENT, -EXPONENT], ids=["high", "low"])
def test_decimal_exponent_at_the_limit_is_accepted(exponent: int) -> None:
    value = Decimal(1).scaleb(exponent)
    assert to_exact(value) == Fraction(value)


@pytest.mark.parametrize("exponent", [EXPONENT + 1, -EXPONENT - 1], ids=["high", "low"])
def test_decimal_exponent_past_the_limit_is_rejected(exponent: int) -> None:
    with pytest.raises(InvalidMeasurementError, match="exponent"):
        to_exact(Decimal(1).scaleb(exponent))


@pytest.mark.parametrize("literal", ["1E+1000000", "1E-1000000", "1E+5000000"])
def test_absurd_decimal_exponent_is_rejected_at_construction(literal: str) -> None:
    with pytest.raises(InvalidMeasurementError, match="exponent"):
        Volt(Decimal(literal))


# Decimal digits.


def test_decimal_with_the_most_digits_is_accepted() -> None:
    value = Decimal("1." + "3" * (DIGITS - 1))
    assert to_exact(value) == Fraction(value)


def test_decimal_with_one_digit_too_many_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="digits"):
        to_exact(Decimal("1." + "3" * DIGITS))


def test_the_widest_accepted_decimal_displays() -> None:
    value = Decimal("1" + "3" * (DIGITS - 1)).scaleb(-EXPONENT)
    assert repr(Volt(value))


# int and Fraction.


def test_int_at_the_bit_limit_is_accepted() -> None:
    value = 2**BITS - 1
    assert to_exact(value) == value


def test_int_past_the_bit_limit_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="bits"):
        to_exact(2**BITS)


def test_negative_int_past_the_bit_limit_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="bits"):
        to_exact(-(2**BITS))


def test_fraction_at_the_bit_limit_passes_through_unchanged() -> None:
    value = Fraction(2**BITS - 1, 2**BITS - 3)
    assert to_exact(value) is value


@pytest.mark.parametrize(
    "value",
    [Fraction(2**BITS, 3), Fraction(1, 2**BITS)],
    ids=["numerator", "denominator"],
)
def test_fraction_past_the_bit_limit_is_rejected(value: Fraction) -> None:
    with pytest.raises(InvalidMeasurementError, match="bits"):
        to_exact(value)


# float.


@pytest.mark.parametrize(
    "value",
    [1.7976931348623157e308, 5e-324, -1.7976931348623157e308],
    ids=["largest", "smallest", "most_negative"],
)
def test_every_float_extreme_is_accepted(value: float) -> None:
    assert to_exact(value) == Fraction(str(value))


def test_default_limits_cover_the_float_range() -> None:
    assert NUMERIC_LIMITS.max_decimal_exponent >= 324  # noqa: PLR2004 -- 5e-324
    assert NUMERIC_LIMITS.max_exact_bits >= 1024  # noqa: PLR2004 -- 2**1024 > any float


# Rejection is cheap and does not render the value.


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


# Every entry point is bounded.


def test_unit_constructor_rejects_an_oversized_number() -> None:
    with pytest.raises(InvalidMeasurementError):
        Volt(10**100_000)


def test_scalar_multiplication_rejects_an_oversized_factor() -> None:
    with pytest.raises(InvalidMeasurementError):
        Volt(1) * 2**BITS


def test_scalar_division_rejects_an_oversized_divisor() -> None:
    with pytest.raises(InvalidMeasurementError):
        Volt(1) / Decimal("1E+5000000")


# Non-finite values keep their own message.


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_decimal_is_reported_as_not_finite(literal: str) -> None:
    with pytest.raises(InvalidMeasurementError, match="not finite"):
        to_exact(Decimal(literal))


# The limits are one replaceable value.


def test_limits_are_immutable() -> None:
    with pytest.raises(AttributeError):
        NUMERIC_LIMITS.max_decimal_exponent = 5  # type: ignore[misc]  # ty: ignore[invalid-assignment]


def test_replacing_the_limits_changes_what_to_exact_accepts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        kuchka.numeric, "NUMERIC_LIMITS", NumericLimits(max_decimal_exponent=10)
    )
    assert to_exact(Decimal("1E+10")) == Fraction(10**10)
    with pytest.raises(InvalidMeasurementError, match="exponent"):
        to_exact(Decimal("1E+11"))
