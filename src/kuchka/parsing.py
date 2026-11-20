"""Reading a measurement from text.

    from kuchka import Voltage
    from kuchka import parse

    voltage = parse("5 mV", Voltage)

`parse(text, quantity)` reads a number and a unit from `text` and builds a `quantity`
through the table of that type's units, so `"5 mV"` is a `Voltage` of five millivolts.
The caller names the type, because the text of a unit does not say what it measures:
`"5 s"` is a `Time`, an `Instant`, or a `SamplingPeriod`, and each reads it through
its own table.

The text is a number and a unit, with or without a space between them, and a unit
that starts with a digit, such as the `1` of a `Proportion`, takes the space.
The number has an optional sign and is read exactly, in one of two forms:
digits with an optional decimal point and an optional exponent, so `"0.1 V"` is the
exact fraction one tenth of a volt, or two whole numbers around a slash, so `"1/3 V"`
is exactly one third of a volt.
A fraction is written without spaces and without an exponent, and its denominator is
not zero.
A number with no unit is read only where the quantity's table names a unit for it,
which is the ratio of a `Proportion`: `"0.25"` is a ratio of a quarter.
The unit is anything the quantity's own table accepts, so the symbols, the aliases,
and the spoken forms all read.
Text is normalized the way the tables normalize it, so a micro sign, a superscript,
a non-breaking space, and the minus sign U+2212 read as the characters they stand for.

Examples
--------
A voltage, and the same text for the three kinds a second can be:

>>> from kuchka import Instant
>>> from kuchka import SamplingPeriod
>>> from kuchka import Time
>>> from kuchka import Voltage
>>> parse("5 mV", Voltage)
5 mV
>>> parse("5 s", Time)
5 s
>>> type(parse("5 s", Instant)).__name__
'Instant'
>>> type(parse("5 s", SamplingPeriod)).__name__
'SamplingPeriod'

The number is exact, and the space is optional:

>>> from kuchka import Volt
>>> parse("0.1V", Voltage) == Volt(0.1)
True
>>> parse("-4.5e-3 V", Voltage) == Volt(-0.0045)
True

A fraction keeps what a decimal cannot hold:

>>> parse("1/3 V", Voltage) == Volt(1) / 3
True
>>> parse("1/4 V", Voltage)
0.25 V

A proportion reads without a unit, as the ratio it is:

>>> from kuchka import Proportion
>>> parse("0.25", Proportion)
0.25 1
>>> parse("25 %", Proportion)
25 %
>>> parse("0.25", Voltage)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.ParseError: '0.25' has a number and no unit.

Text that is no measurement of the type raises `ParseError`, and a unit the type does
not have raises `UnknownUnitError`:

>>> parse("5 A", Voltage)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.UnknownUnitError: 'A' is not a unit of Voltage (see VOLTAGE_UNITS).
>>> parse("five volts", Voltage)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.ParseError: ...

Similarly:

>>> parse("42 banana-bzzzt-volt", Voltage)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.UnknownUnitError: ...

Archaic units
-------------
Archaic units are read only when the caller allows them, and only the ones whose
module the application has imported:

>>> from kuchka import Length
>>> from kuchka.units.archaic.russian import length
>>> parse("2 arshin", Length, allow_archaic=True) == length.Arshin(2)
True
>>> parse("2 arshin", Length)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.UnknownUnitError: 'arshin' is not a unit of Length (see LENGTH_UNITS). ...


A text that a modern unit and an archaic unit, or two archaic units, both claim is
ambiguous, and `parse` raises `ParseError` naming the tables.
`ArchaicPolicy.Deny` reads modern units only, and `ArchaicPolicy.Allow` reads the
archaic ones as well; `False` and `True` stand for them.

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
from typing import TypeVar

from kuchka.errors import InvalidMeasurementError
from kuchka.errors import ParseError
from kuchka.errors import UnknownUnitError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.internal.spelling import normalize
from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.numeric import Numeric
    from kuchka.quantities.base.storage import _ScalarStorage

_QuantityT = TypeVar("_QuantityT", bound="_ScalarStorage[Any]")

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
    """Whether `parse` reads the units of the archaic modules an application imported.

    `Deny` reads the modern units of the quantity's own table.
    `Allow` reads those and the units of every archaic module the application has
    imported, and a text that more than one of them claims is an error.
    """

    Deny = "deny"
    Allow = "allow"


def parse(
    value: str,
    quantity: type[_QuantityT],
    allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny,  # noqa: FBT001 -- a policy, or its two bool shorthands
) -> _QuantityT:
    """Read `value`, a number and a unit, as a measurement of type `quantity`.

    Parameters
    ----------
    value : str
        The text, such as ``"5 mV"``, ``"-40 °C"``, ``"1.5e3 Hz"``, ``"1/3 V"``, or
        ``"0.25"`` for a `Proportion`.
    quantity : type
        The quantity type to build, such as `Voltage`.
        Its own table of unit spellings reads the unit.
    allow_archaic : ArchaicPolicy or bool, optional
        Whether to read archaic units as well, from the archaic modules the
        application has imported.
        `True` is `ArchaicPolicy.Allow` and `False` is `ArchaicPolicy.Deny`.

    Returns
    -------
    _QuantityT
        The measurement, built in the unit the text named.

    Raises
    ------
    ParseError
        The text has no number, or a number with no unit where the quantity has no
        bare unit, writes its number in a form that is not read, writes a fraction
        with a zero denominator, writes a number outside the numeric limits of the
        library, or names a unit that two tables claim.
    UnknownUnitError
        The unit is no unit of `quantity`.
    TypeError
        `value` is not text, `quantity` is not a quantity type, or `allow_archaic`
        is neither an `ArchaicPolicy` nor a `bool`.

    Examples
    --------
    >>> from kuchka import Voltage
    >>> parse("5 mV", Voltage)
    5 mV

    """
    policy = _policy(allow_archaic)
    table = _table_of(quantity)
    if not isinstance(value, str):
        msg = f"parse reads text, not {type(value).__name__}."
        raise TypeError(msg)
    text = normalize(value).strip()
    number, unit_text = _split(text, value)
    if unit_text:
        constructor = _constructor(quantity, table, unit_text, policy)
    else:
        bare = table.bare
        if bare is None:
            msg = f"{value!r} has a number and no unit."
            raise ParseError(msg)
        constructor = bare[1]
    result: _QuantityT = constructor(number)
    return result


def _policy(value: object) -> ArchaicPolicy:
    """Return the policy `value` names, with `True` and `False` as shorthands."""
    if isinstance(value, ArchaicPolicy):
        return value
    if isinstance(value, bool):
        return ArchaicPolicy.Allow if value else ArchaicPolicy.Deny
    msg = f"allow_archaic is an ArchaicPolicy or a bool, not {type(value).__name__}."
    raise TypeError(msg)


def _table_of(quantity: object) -> UnitTable[Any]:
    """Return the table of the units of `quantity`, a quantity type."""
    table = vars(quantity).get("_unit_table") if isinstance(quantity, type) else None
    if table is None:
        msg = f"{quantity!r} is not a quantity type with units to read."
        raise TypeError(msg)
    return table  # type: ignore[no-any-return]  # a table bound by `bind_table`


def _split(text: str, original: str) -> tuple[Decimal | Fraction, str]:
    """Split normalized `text` into its number and its unit text, which may be empty."""
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


def _constructor(
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


__all__ = ["ArchaicPolicy", "parse"]
