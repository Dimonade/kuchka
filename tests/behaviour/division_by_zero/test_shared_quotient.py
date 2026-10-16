"""Every shape reaches the same exact quotient."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import DivisionByZeroError
from kuchka.numeric import exact_quotient

ZERO_IDS = ["int", "float", "decimal", "fraction", "decimal_exponent"]


def test_the_exact_quotient_divides_exactly() -> None:
    assert exact_quotient(Fraction(1), Fraction(3), left=1, right=3) == Fraction(1, 3)


def test_the_exact_quotient_rejects_a_zero_divisor() -> None:
    with pytest.raises(DivisionByZeroError, match="divisor is zero"):
        exact_quotient(Fraction(1), Fraction(0), left="a", right="b")
