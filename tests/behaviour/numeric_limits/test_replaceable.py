"""The limits are one replaceable value."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

import kuchka.numeric
from kuchka import InvalidMeasurementError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.internal.limits import NumericLimits
from kuchka.numeric import to_exact


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
