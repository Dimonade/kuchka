"""Strict numeric coercion into :class:`decimal.Decimal`.

SI prefixes (milli, kilo, mega, ...) are all powers of ten, and powers of
ten are exactly representable in ``Decimal`` but generally are *not*
exactly representable in binary ``float``.

That is the concrete, practical reason this library stores magnitudes as ``Decimal``
internally rather than ``float``:
it is what makes ``Volt(1) + Millivolt(500) == Volt(1.5)`` true by construction instead
of true by coincidence.

This module is the single place where "a plain number" is turned into a ``Decimal
for use inside a measurement.
Every unit constructor (``Volt``, ``Ampere``, ``Celsius``, ...) routes through
:func:`to_decimal`, which is deliberately strict:
it accepts the numeric types an engineer is likely to have on hand, and rejects
everything else -- including other measurements -- with a message that (hopefully)
explains what went wrong.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from kuchka.errors import InvalidMeasurementError

Numeric = int | float | Decimal | Fraction

_NUMERIC_TYPES = (int, float, Decimal, Fraction)


def to_decimal(value: object) -> Decimal:
    """Coerce ``value`` into an exact :class:`~decimal.Decimal`.

    ``float`` values are routed through ``str()`` first. ``Decimal(4.2)``
    would faithfully reproduce the binary float's rounding error
    (``4.20000000000000017763...``);
    ``Decimal(str(4.2))`` reproduces what an engineer actually typed.
    That one-line rule is what keeps float literals like ``Volt(4.2)``
    numerically sane without asking the engineer to write
    ``Volt(Decimal("4.2"))`` themselves.
    """
    # bool is a subclass of int in Python; True/False silently becoming 1/0
    # inside a measurement is a classic footgun, so it is rejected
    # explicitly rather than accepted by isinstance(value, int).
    if isinstance(value, bool):
        raise InvalidMeasurementError(
            f"cannot construct a measurement from a bool ({value!r}); "
            "expected int, float, Decimal, or Fraction",
        )
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, Fraction):
        return Decimal(value.numerator) / Decimal(value.denominator)
    if isinstance(value, float):
        return Decimal(str(value))

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
