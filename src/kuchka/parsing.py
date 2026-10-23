"""Reading a measurement from text.

    from kuchka import Voltage, parse

    voltage = parse("5 mV", Voltage)

`parse(text, quantity)` reads a number and a unit from `text` and builds a `quantity`
through the table of that type's units, so `"5 mV"` is a `Voltage` of five millivolts.
The caller names the type, because the text of a unit does not say what it measures:
`"5 s"` is a `Time`, an `Instant`, or a `SamplingPeriod`, and each reads it through
its own table.

The text is a number and a unit, with or without a space between them, and a unit
that starts with a digit, such as the `1` of a `Proportion`, takes the space.
The number has an optional sign, digits with an optional decimal point, and an
optional exponent, and it is read exactly: `"0.1 V"` is the exact fraction one tenth
of a volt.
The unit is anything the quantity's own table accepts, so the symbols, the aliases,
and the spoken forms all read.
Text is normalized the way the tables normalize it, so a micro sign, a superscript,
a non-breaking space, and the minus sign U+2212 read as the characters they stand for.

Examples
--------
A voltage, and the same text for the three kinds a second can be:

>>> from kuchka import Instant, SamplingPeriod, Time, Voltage
>>> parse("5 mV", Voltage)
5 mV
>>> parse("5 s", Time)
5 s
>>> type(parse("5 s", Instant)).__name__
'Instant'
>>> type(parse("5 s", SamplingPeriod)).__name__
'SamplingPeriod'

The number is exact, and the space is optional:

>>> from fractions import Fraction
>>> from kuchka import Volt
>>> parse("0.1V", Voltage) == Volt(Fraction(1, 10))
True
>>> parse("-4.5e-3 V", Voltage) == Volt(Fraction(-9, 2000))
True

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

>>> parse("42 banana-bzzzt-volt", VOLTAGE)  # doctest: +ELLIPSIS
>>> Traceback (most recent call last):
    ...
kuchka.errors.ParseError: ...

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

import re
from decimal import Decimal
from decimal import InvalidOperation
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from kuchka.errors import ParseError
from kuchka.errors import UnknownUnitError
from kuchka.internal.spelling import normalize

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import UnitTable
    from kuchka.quantities.base.storage import _ScalarStorage

_QuantityT = TypeVar("_QuantityT", bound="_ScalarStorage[Any]")

_MINUS = "\u2212"
_NUMBER = re.compile(
    rf"[+\-{_MINUS}]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+\-{_MINUS}]?[0-9]+)?"
)
_NOT_A_UNIT = ".,_"
"""What a unit text cannot start with: the rest of a number written in a form that
is not read, such as `1,5` or `1_000`."""


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
        The text, such as ``"5 mV"``, ``"-40 °C"``, or ``"1.5e3 Hz"``.
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
        The text has no number or no unit, writes its number in a form that is not
        read, or names a unit that two tables claim.
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
    constructor = _constructor(quantity, table, unit_text, policy)
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


def _split(text: str, original: str) -> tuple[Decimal, str]:
    """Split normalized `text` into its number and its unit text."""
    match = _NUMBER.match(text)
    if match is None:
        msg = f"cannot read a number at the start of {original!r}."
        raise ParseError(msg)
    unit_text = text[match.end() :].strip()
    if not unit_text:
        msg = f"{original!r} has a number and no unit."
        raise ParseError(msg)
    if unit_text[0] in _NOT_A_UNIT:
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
    return number, unit_text


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
) -> Callable[[Decimal], Any]:
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
