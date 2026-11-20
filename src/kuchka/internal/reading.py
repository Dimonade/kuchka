"""The reading machinery behind `parse` and `kuchka.wire`.

A measurement arrives as a number and a unit spelling.
This module splits text into the two, reads the number exactly, in the forms the
library accepts, and finds the constructor a quantity type's table has for a spelling,
so that every way of reading a measurement shares one set of rules and one set of
messages.
`parse` reads one text, and `kuchka.wire` reads the pieces of a value that a boundary
delivered.
"""

from __future__ import annotations

import math
import re
from decimal import Decimal
from decimal import InvalidOperation
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Any

from kuchka.errors import InvalidMeasurementError
from kuchka.errors import ParseError
from kuchka.errors import UnknownUnitError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric

_MINUS = "\u2212"
_NUMBER = re.compile(
    rf"[+\-{_MINUS}]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+\-{_MINUS}]?[0-9]+)?"
)
_FRACTION = re.compile(rf"([+\-{_MINUS}]?)([0-9]+)/([0-9]+)")
_NOT_A_UNIT = ".,_"
"""What a unit text cannot start with: the rest of a number written in a form that
is not read, such as `1,5` or `1_000`."""
_SLASH_AFTER_NUMBER = re.compile(r"/\s*[0-9]")
"""What follows a number that was meant as a fraction written in a form that is not
read: the `/3` of `1 /3` and of `1.5/3`."""
_EXPONENT_AFTER_FRACTION = re.compile(r"[eE][+\-]?[0-9]")
"""What follows a fraction that was given an exponent, as in `1/3e2`."""
_FRACTION_FORM_HELP = (
    "a fraction is written with two whole numbers around a slash, without spaces "
    "and without an exponent, such as 1/3."
)
_MAX_FRACTION_DIGITS = math.ceil(NUMERIC_LIMITS.max_exact_bits / math.log2(10)) + 1
"""Most digits either whole number of a fraction may have before it is read: the
digits of the largest integer of `max_exact_bits` bits, so that text is not turned
into an integer just to be refused for its size."""


class ArchaicPolicy(Enum):
    """Whether `parse` and `wire.load` read the units of the archaic modules imported.

    `Deny` reads the modern units of the quantity's own table.
    `Allow` reads those and the units of every archaic module the application has
    imported, and a text that more than one of them claims is an error.
    """

    Deny = "deny"
    Allow = "allow"


def archaic_policy_of(value: object) -> ArchaicPolicy:
    """Return the policy `value` names, with `True` and `False` as shorthands."""
    if isinstance(value, ArchaicPolicy):
        return value
    if isinstance(value, bool):
        return ArchaicPolicy.Allow if value else ArchaicPolicy.Deny
    msg = f"allow_archaic is an ArchaicPolicy or a bool, not {type(value).__name__}."
    raise TypeError(msg)


def unit_table_of(quantity: object) -> UnitTable[Any]:
    """Return the table of the units of `quantity`, a quantity type."""
    table = vars(quantity).get("_unit_table") if isinstance(quantity, type) else None
    if table is None:
        msg = f"{quantity!r} is not a quantity type with units to read."
        raise TypeError(msg)
    return table  # type: ignore[no-any-return]  # a table bound by `bind_table`


def split_number(text: str, original: str) -> tuple[Decimal | Fraction, str]:
    """Split normalized `text` into its number and its unit text, which may be empty.

    `original` is the text as the caller wrote it, for the messages.
    """
    fraction = _FRACTION.match(text)
    if fraction is not None:
        exact = _fraction(fraction, original)
        unit_text = text[fraction.end() :].strip()
        if unit_text and (
            unit_text[0] in _NOT_A_UNIT or _EXPONENT_AFTER_FRACTION.match(unit_text)
        ):
            msg = f"cannot read the number in {original!r}: {_FRACTION_FORM_HELP}"
            raise ParseError(msg)
        return exact, unit_text
    match = _NUMBER.match(text)
    if match is None:
        msg = f"cannot read a number at the start of {original!r}."
        raise ParseError(msg)
    unit_text = text[match.end() :].strip()
    if _SLASH_AFTER_NUMBER.match(unit_text):
        msg = f"cannot read the number in {original!r}: {_FRACTION_FORM_HELP}"
        raise ParseError(msg)
    if unit_text and unit_text[0] in _NOT_A_UNIT:
        msg = (
            f"cannot read the number in {original!r}: a number is written with a "
            "decimal point and without digit grouping."
        )
        raise ParseError(msg)
    try:
        number = Decimal(match.group().replace(_MINUS, "-"))
    except InvalidOperation:
        msg = f"the number in {original!r} is out of range."
        raise ParseError(msg) from None
    _check_in_range(number, original)
    return number, unit_text


def _fraction(match: re.Match[str], original: str) -> Fraction:
    """Return the exact value of a fraction `match`ed by `_FRACTION`."""
    sign, numerator, denominator = match.groups()
    if max(len(numerator), len(denominator)) > _MAX_FRACTION_DIGITS:
        msg = f"the number in {original!r} is out of range."
        raise ParseError(msg)
    try:
        top, bottom = int(numerator), int(denominator)
    except ValueError:  # pragma: no cover -- a limit raised past the integer text limit
        msg = f"the number in {original!r} is out of range."
        raise ParseError(msg) from None
    if bottom == 0:
        msg = f"the number in {original!r} divides by zero."
        raise ParseError(msg)
    number = Fraction(-top if sign in {"-", _MINUS} else top, bottom)
    _check_in_range(number, original)
    return number


def _check_in_range(number: Decimal | Fraction, original: str) -> None:
    """Raise `ParseError` unless `number` is within the numeric limits."""
    try:
        to_exact(number)
    except InvalidMeasurementError as exc:
        msg = f"the number in {original!r} is out of range: {exc}"
        raise ParseError(msg) from exc


def _resolve(table: UnitTable[Any], text: str) -> tuple[Any, Callable[..., Any]] | None:
    """Return the unit and the constructor `table` has for `text`, or `None`."""
    try:
        return table.resolve(text)
    except KeyError:
        return None


def unit_constructor(
    quantity: type,
    table: UnitTable[Any],
    text: str,
    policy: ArchaicPolicy,
) -> Callable[[Numeric], Any]:
    """Return the constructor that `policy` lets read `text` as a unit of `quantity`.

    Several tables may hold one unit, as a table of the units of a region does with the
    table of the units of a country, so a text is ambiguous when two different units
    claim it and not when two tables do.
    """
    archaic: dict[Any, tuple[UnitTable[Any], Callable[..., Any]]] = {}
    for candidate in vars(quantity).get("_extension_tables", ()):
        hit = _resolve(candidate, text)
        if hit is not None:
            archaic.setdefault(hit[0], (candidate, hit[1]))
    found: dict[Any, tuple[UnitTable[Any], Callable[..., Any]]] = {}
    modern = _resolve(table, text)
    if modern is not None:
        found[modern[0]] = (table, modern[1])
    if policy is ArchaicPolicy.Allow:
        for unit, entry in archaic.items():
            found.setdefault(unit, entry)
    if len(found) == 1:
        return next(iter(found.values()))[1]
    if found:
        labels = ", ".join(
            dict.fromkeys(candidate.label for candidate, _ in found.values())
        )
        msg = (
            f"{text!r} is a unit of more than one table ({labels}), so it does not "
            f"say which {quantity.__name__} unit it means."
        )
        raise ParseError(msg)
    hint = ""
    if archaic:
        labels = ", ".join(
            dict.fromkeys(candidate.label for candidate, _ in archaic.values())
        )
        hint = f" It is an archaic unit ({labels}); pass allow_archaic=True to read it."
    msg = f"{text!r} is not a unit of {quantity.__name__} (see {table.label}).{hint}"
    raise UnknownUnitError(msg, unit=text, quantity=quantity)


__all__ = [
    "ArchaicPolicy",
    "archaic_policy_of",
    "split_number",
    "unit_constructor",
    "unit_table_of",
]
