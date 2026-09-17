"""Numeric coercion: boundary validation into Fraction, materialization into Decimal.

Two functions, two directions:

- `to_exact`: raw input at a construction boundary -> `Fraction`.
    Every unit constructor (`Volt`, `Ampere`, `Celsius`, ...) routes through this.
    Rejects anything that is not `int`, `float`, `Decimal`, or `Fraction`, plus `bool`
    and non-finite `float`/`Decimal` values.
- `to_decimal`: an already-exact `Fraction` -> `Decimal`, for display
    (`__repr__`, `__format__`) and explicit materialization.
    Exact when the denominator's prime factors are 2 and 5;
    rounded to the current `Decimal` context precision otherwise.

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

Numeric = int | float | Decimal | Fraction


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
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, Decimal):
        try:
            return Fraction(value)
        except (ValueError, OverflowError) as exc:
            raise InvalidMeasurementError(
                f"cannot construct a measurement from {value!r}: not finite.",
            ) from exc
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
    """Materialize an exact `Fraction` into a `Decimal`. Display only."""
    return Decimal(value.numerator) / Decimal(value.denominator)


__all__ = ["Numeric", "to_decimal", "to_exact"]
