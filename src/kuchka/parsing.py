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

from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from kuchka.errors import ParseError
from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.reading import split_number
from kuchka.internal.reading import unit_constructor
from kuchka.internal.reading import unit_table_of
from kuchka.internal.spelling import normalize

if TYPE_CHECKING:
    from kuchka.quantities.base.storage import _ScalarStorage

_QuantityT = TypeVar("_QuantityT", bound="_ScalarStorage[Any]")


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
    policy = archaic_policy_of(allow_archaic)
    table = unit_table_of(quantity)
    if not isinstance(value, str):
        msg = f"parse reads text, not {type(value).__name__}."
        raise TypeError(msg)
    text = normalize(value).strip()
    number, unit_text = split_number(text, value)
    if unit_text:
        constructor = unit_constructor(quantity, table, unit_text, policy)
    else:
        bare = table.bare
        if bare is None:
            msg = f"{value!r} has a number and no unit."
            raise ParseError(msg)
        constructor = bare[1]
    result: _QuantityT = constructor(number)
    return result


__all__ = ["ArchaicPolicy", "parse"]
