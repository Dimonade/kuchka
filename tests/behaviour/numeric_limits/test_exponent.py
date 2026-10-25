"""The decimal exponent limit."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.numeric import to_exact
from kuchka.units.electromagnetics import voltage

EXPONENT = NUMERIC_LIMITS.max_decimal_exponent


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
        voltage.Volt(Decimal(literal))
