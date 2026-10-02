"""Numeric coercion: boundary validation into Fraction, materialization into Decimal.

Two functions, two directions:

- `to_exact`: raw input at a construction boundary -> `Fraction`.
    Every unit constructor (`Volt`, `Ampere`, `Celsius`, ...) routes through this.
    Rejects anything that is not `int`, `float`, `Decimal`, or `Fraction`, plus `bool`,
    non-finite `float`/`Decimal` values, and numbers larger than
    `kuchka.internal.limits.NUMERIC_LIMITS` allows.
- `to_decimal`: an already-exact `Fraction` -> `Decimal`, for computations that run
    in `Decimal` (logarithms and powers).
    Exact when the denominator's prime factors are 2 and 5;
    rounded to the active `Decimal` context precision otherwise.
    Display has its own path, `kuchka.internal.display.render`, which does not read
    the active context.

`int` and `Decimal` convert to `Fraction` exactly, with no rounding, in either
direction.
`float` is routed through `str()` before parsing: `Volt(4.2)` stores the digits typed
(`Fraction(str(4.2)) == Fraction(21, 5)`), not float's binary representation of them.
`Fraction` is stored as-is: `Litre(Fraction(5, 18)).magnitude == Fraction(5, 18)`.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from kuchka.errors import InvalidMeasurementError
from kuchka.internal.limits import NUMERIC_LIMITS

Numeric = int | float | Decimal | Fraction


def _too_large(subject: str, detail: str) -> InvalidMeasurementError:
    # NOTE: `subject` describes the value by its size; the value itself is never
    # rendered, because rendering a number of this size is the cost being avoided.
    return InvalidMeasurementError(
        f"cannot construct a measurement from {subject}: {detail}.",
    )


def _check_integer(value: int, subject: str) -> None:
    limit = NUMERIC_LIMITS.max_exact_bits
    if value.bit_length() > limit:
        raise _too_large(subject, f"it needs more than {limit} bits to store exactly")


def _check_fraction(value: Fraction) -> None:
    subject = (
        f"a Fraction with a {value.numerator.bit_length()}-bit numerator and a "
        f"{value.denominator.bit_length()}-bit denominator"
    )
    _check_integer(value.numerator, subject)
    _check_integer(value.denominator, subject)


def _check_decimal(value: Decimal) -> None:
    limits = NUMERIC_LIMITS
    _, digits, exponent = value.as_tuple()
    subject = f"a Decimal with {len(digits)} digits and exponent {exponent}"
    if abs(int(exponent)) > limits.max_decimal_exponent:
        raise _too_large(
            subject, f"the exponent must be within +/-{limits.max_decimal_exponent}"
        )
    if len(digits) > limits.max_decimal_digits:
        raise _too_large(
            subject, f"at most {limits.max_decimal_digits} digits are accepted"
        )


def to_exact(value: object) -> Fraction:
    """Coerce `value` into an exact `Fraction`."""
    # NOTE: bool is a subclass of int.
    # Therefore, True/False silently becoming 1/0 is rejected explicitly.
    if isinstance(value, bool):
        raise InvalidMeasurementError(
            f"cannot construct a measurement from a bool ({value!r}); "
            "expected int, float, Decimal, or Fraction",
        )
    if isinstance(value, Fraction):
        _check_fraction(value)
        return value
    if isinstance(value, int):
        _check_integer(value, f"an int of {value.bit_length()} bits")
        return Fraction(value)
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise InvalidMeasurementError(
                f"cannot construct a measurement from {value!r}: not finite.",
            )
        _check_decimal(value)
        return Fraction(value)
    if isinstance(value, float):
        try:
            return Fraction(str(value))
        except ValueError as exc:
            raise InvalidMeasurementError(
                f"cannot construct a measurement from {value!r}: not finite.",
            ) from exc

    type_name = type(value).__name__
    hint = ""
    if hasattr(value, "magnitude") or hasattr(value, "dimension"):
        hint = (
            " It looks like you passed a measurement where a plain number "
            "was expected -- did you mean to use its .magnitude, or is "
            "this a dimension mismatch?"
        )
    raise InvalidMeasurementError(
        f"cannot construct a measurement from {type_name}; expected int, "
        f"float, Decimal, or Fraction.{hint}",
    )


def to_decimal(value: Fraction) -> Decimal:
    """Materialize an exact `Fraction` as a `Decimal` at the active precision."""
    return Decimal(value.numerator) / Decimal(value.denominator)


__all__ = ["Numeric", "to_decimal", "to_exact"]
