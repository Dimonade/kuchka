"""Size limits on numbers that enter the library.

Every number that becomes a measurement is converted to an exact `Fraction`, and an
exact `Fraction` costs memory and time in proportion to its digits.
`Decimal("1E+1000000")` is a legal `Decimal` that turns into a million-digit integer
which then takes seconds to display.
The limits here keep exact input within a size that stays cheap to store, compare,
and display.

All limits live on one `NumericLimits` value, `NUMERIC_LIMITS`, which is the single
point consulted by the code enforcing them.
A different set of limits, for example one chosen per platform, replaces that value
and nothing else.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class NumericLimits:
    """How large an exact number may be when it enters the library.

    The defaults accept every IEEE-754 double (about 1E-324 to 1E+308) and every
    physical constant with room to spare.
    """

    max_decimal_exponent: int = 1_000
    """Largest absolute exponent of a `Decimal` input: `Decimal("1E+1000")` passes."""

    max_decimal_digits: int = 1_000
    """Most significant digits a `Decimal` input may carry."""

    max_exact_bits: int = 8_192
    """Largest bit length of the numerator and of the denominator of an exact input.

    Applies to `int` and `Fraction` input, and to the result of converting a
    `Decimal`.
    Wide enough for the largest `Decimal` the two limits above allow.
    """


NUMERIC_LIMITS: Final = NumericLimits()
"""The limits in force."""

__all__ = ["NUMERIC_LIMITS", "NumericLimits"]
