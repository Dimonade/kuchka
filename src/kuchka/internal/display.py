"""How the magnitude of a measurement is rendered as text.

A magnitude is an exact `Fraction`, and rendering is the one place it is approximated.
The approximation runs in a `Decimal` context built here, so the text depends on the
value and the format spec alone: the precision, rounding mode, and traps of the
caller's active context have no effect, and the caller's context flags are left as
they were.

Rounding happens once, from the exact value.
The `Decimal` handed to the formatter carries enough digits, plus a marker digit for
any remainder, that a tie in the requested precision is a tie only when the exact
value is one.
"""

from __future__ import annotations

import re
from decimal import MAX_EMAX
from decimal import MAX_PREC
from decimal import MIN_EMIN
from decimal import ROUND_DOWN
from decimal import ROUND_HALF_UP
from decimal import Context
from decimal import Decimal
from decimal import Inexact
from decimal import localcontext
from typing import TYPE_CHECKING
from typing import Final

if TYPE_CHECKING:
    from fractions import Fraction

DISPLAY_DIGITS: Final = 28
"""Significant digits shown when a format spec gives no precision."""

DISPLAY_ROUNDING: Final = ROUND_HALF_UP
"""How a tie rounds: away from zero, so `2.665` shows as `2.67` at two places."""

_GUARD_DIGITS: Final = 5
"""Digits kept beyond the requested precision before the marker digit."""

_PRECISION: Final = re.compile(r"\.(\d+)")


def _context(precision: int, rounding: str) -> Context:
    return Context(
        prec=precision,
        rounding=rounding,
        Emin=MIN_EMIN,
        Emax=MAX_EMAX,
        capitals=1,
        clamp=0,
        flags=[],
        traps=[],
    )


def _integer_digits(value: Fraction) -> int:
    """Upper bound on the digits left of the point, without rendering the integer."""
    bits = value.numerator.bit_length() - value.denominator.bit_length()
    return max(1, bits * 30103 // 100000 + 2)


def _requested_precision(format_spec: str) -> int | None:
    # NOTE: a `.` followed by digits is always the precision: a fill character is
    # followed by an alignment character, never by a digit.
    found = _PRECISION.search(format_spec)
    if found is None:
        return None
    precision = int(found.group(1))
    if precision > MAX_PREC // 2:
        raise ValueError(f"invalid format string: precision {precision} is too large")
    return precision


def _with_marker(value: Fraction, digits: int) -> Decimal:
    """`value` to `digits` significant digits, with a marker digit if truncated.

    The marker is a trailing `1`.
    It keeps a truncated remainder from looking like an exact tie when the result is
    rounded again to fewer digits.
    """
    context = _context(digits, ROUND_DOWN)
    quotient = context.divide(Decimal(value.numerator), Decimal(value.denominator))
    if not context.flags[Inexact]:
        return quotient
    sign, mantissa, exponent = quotient.as_tuple()
    assert isinstance(exponent, int)  # noqa: S101 -- a finite quotient has an int exponent
    return Decimal((sign, (*mantissa, 1), exponent - 1))


def render(value: Fraction, format_spec: str = "f") -> str:
    """Format `value` with `format_spec`, in the `Decimal` format mini-language.

    Without a precision in the spec the value is rounded to `DISPLAY_DIGITS`
    significant digits; with one, to exactly the places or digits it names.
    Ties follow `DISPLAY_ROUNDING`.
    """
    precision = _requested_precision(format_spec)
    if precision is None:
        digits = DISPLAY_DIGITS + _GUARD_DIGITS
        number = _context(DISPLAY_DIGITS, DISPLAY_ROUNDING).plus(
            _with_marker(value, digits)
        )
    else:
        digits = max(DISPLAY_DIGITS, _integer_digits(value) + precision) + _GUARD_DIGITS
        number = _with_marker(value, digits)
    with localcontext(_context(digits + 1, DISPLAY_ROUNDING)):
        return format(number, format_spec)


__all__ = ["DISPLAY_DIGITS", "DISPLAY_ROUNDING", "render"]
