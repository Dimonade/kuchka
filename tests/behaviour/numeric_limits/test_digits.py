"""The decimal digits limit."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.numeric import to_exact
from kuchka.units import voltage

EXPONENT = NUMERIC_LIMITS.max_decimal_exponent


DIGITS = NUMERIC_LIMITS.max_decimal_digits


BITS = NUMERIC_LIMITS.max_exact_bits


def test_decimal_with_the_most_digits_is_accepted() -> None:
    value = Decimal("1." + "3" * (DIGITS - 1))
    assert to_exact(value) == Fraction(value)


def test_decimal_with_one_digit_too_many_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="digits"):
        to_exact(Decimal("1." + "3" * DIGITS))


def test_the_widest_accepted_decimal_displays() -> None:
    value = Decimal("1" + "3" * (DIGITS - 1)).scaleb(-EXPONENT)
    assert repr(voltage.Volt(value))


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
