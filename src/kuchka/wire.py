"""The wire form of a measurement: how it crosses a boundary as data.

    from kuchka import Voltage
    from kuchka import wire

    text = wire.dump(voltage)
    voltage = wire.load(text, Voltage)

A configuration file, a JSON payload, a database column, and a command line carry a
measurement as plain data.
`dump(quantity)` writes it as one string, the number and the unit symbol, and
`load(value, quantity)` reads what a boundary delivers back into the type the field
expects, so the two are the pair every integration is built on.

The form
--------
The written form is the number, a space, and the unit's display symbol:
`"2800 mV"`, `"-40 °C"`, `"0.25 W/m²"`.
The number is the exact magnitude in the unit the measurement is displayed in, and it is
written as a decimal when the magnitude is a terminating decimal and as a fraction when
it is not, so that no digit is rounded away: `Volt(4.2)` is `"4.2 V"`, a third of a volt
is `"1/3 V"`, and `parse` reads both back to the value that was written.
A proportion in ratios is written as its number alone, `"0.25"`, which `parse` reads as
the ratio it is; a percent keeps its unit, `"25 %"`.

Reading
-------
`load` accepts what a boundary delivers for a field of one quantity type:

- an instance of the type, which passes through unchanged;
- text, read by `parse`, so `"2800 mV"`, `"1/3 V"`, and every spelling of a unit that
  the type's table reads are accepted;
- a mapping with the keys `"value"` and `"unit"`, such as `{"value": "7/3", "unit":
  "mV"}`, whose value is a number or the text of one and whose unit is a spelling of a
  unit of the type;
- for a quantity whose table names a bare unit, which is the `Proportion`, a number: a
  field typed `Proportion` accepts `0.25`, `"0.25"`, and `"25 %"`.

Everything else is refused, and a bare number is refused for every other quantity,
since `2.8` does not say whether it is volts.
A `float` is read by the digits it shows, the way the unit constructors read it, so
`0.1` is exactly one tenth.

As a mapping
------------
`to_dict(quantity)` writes the same exact data as the two fields a JSON document or a
database row wants, `{"value": "2800", "unit": "mV"}`, and `from_dict(data, Voltage)`
reads it back; the value is the text of `dump`, a decimal when it terminates and a
fraction when it does not, so `{"value": "1/3", "unit": "V"}` is a third of a volt.
`to_dict(quantity, unit="V")` writes the measurement in another unit of its quantity,
converted exactly, and `as_float=True` writes `value` as a JSON number for a consumer
that accepts nothing else, which is as exact as a `float` is.
The text of `dump` stays the canonical form; the mapping is for storage that wants
fields, and `load` reads both.

Errors
------
Every refusal of data is a `ParseError`, which is a `ValueError`: text that is no
measurement of the type, a unit the type does not have (`UnknownUnitError`), a number
with no unit, an instance of another quantity type, a value outside what the quantity
can hold such as `-300 °C`.
A framework that reports a `ValueError` from a validator as a validation error needs
nothing else, and one `except ParseError` around the loading of a file catches every
bad value in it.
A `TypeError` is raised only for a mistake in the program: a `quantity` that is no
quantity type with units, or an `allow_archaic` that is no policy.

Examples
--------
>>> from kuchka import Millivolt
>>> from kuchka import Volt
>>> from kuchka import Voltage
>>> dump(Millivolt(2800))
'2800 mV'
>>> dump(Volt(4.2))
'4.2 V'
>>> dump(Volt(1) / 3)
'1/3 V'
>>> load("1/3 V", Voltage) == Volt(1) / 3
True

A mapping with a value and a unit reads the same, and an instance of the type passes
through:

>>> load({"value": "2800", "unit": "mV"}, Voltage)
2800 mV
>>> load(Volt(3.3), Voltage)
3.3 V

Written as a mapping and read back:

>>> to_dict(Millivolt(2800))
{'value': '2800', 'unit': 'mV'}
>>> to_dict(Volt(1) / 3)
{'value': '1/3', 'unit': 'V'}
>>> to_dict(Millivolt(2800), unit="V")
{'value': '2.8', 'unit': 'V'}
>>> from_dict({"value": "1/3", "unit": "V"}, Voltage) == Volt(1) / 3
True

A proportion needs no unit, and every other quantity does:

>>> from kuchka import Percent
>>> from kuchka import Proportion
>>> from kuchka import Ratio
>>> dump(Ratio(0.25))
'0.25'
>>> dump(Percent(25))
'25 %'
>>> load(0.25, Proportion)
0.25 1
>>> load(3.3, Voltage)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.ParseError: 3.3 has no unit, ...

Archaic units
-------------
An archaic unit is written like any other, and read back only where the caller allows
archaic units, with the same policy `parse` takes:

>>> from kuchka import Length
>>> from kuchka.units.archaic.russian import length
>>> dump(length.Arshin(2))
'2 arshin'
>>> load("2 arshin", Length, allow_archaic=True) == length.Arshin(2)
True

"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import ParseError
from kuchka.errors import UnknownUnitError
from kuchka.internal.limits import NUMERIC_LIMITS
from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.reading import example_unit
from kuchka.internal.reading import split_number
from kuchka.internal.reading import unit_constructor
from kuchka.internal.reading import unit_table_of
from kuchka.internal.spelling import normalize
from kuchka.parsing import parse
from kuchka.quantities.base.storage import _ScalarStorage

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable
    from kuchka.quantities.base.units import UnitDef

_QuantityT = TypeVar("_QuantityT", bound="_ScalarStorage[Any]")

_KEYS = ("value", "unit")
_NUMBER_TYPES = (int, float, Decimal, Fraction)


def dump(quantity: _ScalarStorage[Any]) -> str:
    """Write `quantity` as text: its exact magnitude and its unit's symbol.

    Parameters
    ----------
    quantity : _ScalarStorage
        A measurement of any quantity type and shape.

    Returns
    -------
    str
        The magnitude in the unit the measurement displays in, a space, and the unit's
        symbol.
        The magnitude is a decimal when it is a terminating decimal that fits the
        numeric limits of the library, and a fraction when it is not.
        A ratio is written as its magnitude alone.

    Raises
    ------
    TypeError
        `quantity` is no measurement.

    Notes
    -----
    `load(dump(q), type(q))` is a measurement equal to `q`, displayed in the same
    unit, for every magnitude the numeric limits allow in the unit it is written in.

    Examples
    --------
    >>> from kuchka import Celsius
    >>> from kuchka import Millivolt
    >>> dump(Millivolt(2800))
    '2800 mV'
    >>> dump(Celsius(-40))
    '-40 °C'

    """
    if not isinstance(quantity, _ScalarStorage):
        msg = f"dump writes a measurement, not {type(quantity).__name__}."
        raise TypeError(msg)
    unit = quantity.unit
    text = _magnitude_text(quantity.value_in(unit))
    bare = unit_table_of(type(quantity)).bare
    if bare is not None and bare[0] == unit:
        return text
    return f"{text} {unit.symbol}"


def load(
    value: object,
    quantity: type[_QuantityT],
    *,
    allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny,
) -> _QuantityT:
    """Read what a boundary delivered as a measurement of type `quantity`.

    Parameters
    ----------
    value : object
        An instance of `quantity`, text such as ``"2800 mV"`` or ``"1/3 V"``, a mapping
        with ``"value"`` and ``"unit"``, or, for a `Proportion`, a number.
    quantity : type
        The quantity type the field holds, such as `Voltage`.
    allow_archaic : ArchaicPolicy or bool, optional
        Whether to read archaic units, as `parse` does.

    Returns
    -------
    _QuantityT
        `value` itself for an instance of `quantity`, and otherwise the measurement
        built in the unit that was written.

    Raises
    ------
    ParseError
        `value` is no measurement of `quantity`, for any reason; see the module
        documentation.
    UnknownUnitError
        The unit is no unit of `quantity`.
    TypeError
        `quantity` is not a quantity type with units, or `allow_archaic` is neither
        an `ArchaicPolicy` nor a `bool`.

    Examples
    --------
    >>> from kuchka import Voltage
    >>> load("2800 mV", Voltage)
    2800 mV
    >>> load({"value": "7/3", "unit": "mV"}, Voltage) == load("7/3 mV", Voltage)
    True

    """
    policy = archaic_policy_of(allow_archaic)
    table = unit_table_of(quantity)
    try:
        result: _QuantityT = _load(value, quantity, table, policy)
    except ParseError:
        raise
    except InvalidMeasurementError as exc:
        raise ParseError(str(exc)) from exc
    return result


def to_dict(
    quantity: _ScalarStorage[Any],
    *,
    unit: UnitDef | str | None = None,
    as_float: bool = False,
) -> dict[str, str | int | float]:
    """Write `quantity` as a mapping of its exact `value` and its `unit` symbol.

    Parameters
    ----------
    quantity : _ScalarStorage
        A measurement of any quantity type and shape.
    unit : UnitDef or str, optional
        The unit to write it in, as a unit constant or a spelling that the table of
        the quantity reads, converted exactly; the unit the measurement displays in
        if omitted.
    as_float : bool, optional
        Write `value` as a JSON number, an `int` when the magnitude is whole and a
        `float` otherwise, for a consumer that accepts no text.
        The text of the default is exact and this is as exact as a `float`.

    Returns
    -------
    dict
        ``{"value": ..., "unit": ...}``, where the value is the text `dump` writes: a
        decimal when the magnitude terminates and a fraction when it does not.
        A ratio keeps its symbol, ``"1"``.

    Raises
    ------
    TypeError
        `quantity` is no measurement.
    UnknownUnitError
        `unit` is a spelling that the table of the quantity does not read.
    InvalidConversionError
        `unit` is a unit of another quantity, or a unit that the quantity is never
        displayed in, such as the milliseconds of an `Instant`.
    InvalidMeasurementError
        `as_float` is set, and the magnitude is beyond the range of a `float`, or so
        small that a `float` would write it as zero.

    Examples
    --------
    >>> from kuchka import Millivolt
    >>> to_dict(Millivolt(2800))
    {'value': '2800', 'unit': 'mV'}
    >>> to_dict(Millivolt(2800), unit="V", as_float=True)
    {'value': 2.8, 'unit': 'V'}

    """
    if not isinstance(quantity, _ScalarStorage):
        msg = f"to_dict writes a measurement, not {type(quantity).__name__}."
        raise TypeError(msg)
    shown = quantity if unit is None else _in_unit(quantity, unit)
    written = shown.unit
    magnitude = shown.value_in(written)
    value = _float_value(magnitude) if as_float else _magnitude_text(magnitude)
    return {"value": value, "unit": written.symbol}


def from_dict(
    data: Mapping[str, object],
    quantity: type[_QuantityT],
    *,
    allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny,
) -> _QuantityT:
    """Read a mapping of a `value` and a `unit` as a measurement of type `quantity`.

    Parameters
    ----------
    data : Mapping
        ``{"value": ..., "unit": ...}``: the value is a number or the text of one,
        including a fraction such as ``"1/3"``, and the unit is a spelling of a unit
        of `quantity`.
    quantity : type
        The quantity type the field holds, such as `Voltage`.
    allow_archaic : ArchaicPolicy or bool, optional
        Whether to read archaic units, as `parse` does.

    Returns
    -------
    _QuantityT
        The measurement, in the unit that was written.

    Raises
    ------
    ParseError
        `data` is no mapping, lacks the `value` or the `unit`, has another key, holds
        a `bool` or another value that is no number, or holds a measurement that
        `quantity` cannot hold, such as ``-300`` in ``°C``.
    UnknownUnitError
        The unit is no unit of `quantity`.
    TypeError
        `quantity` is not a quantity type with units.

    Examples
    --------
    >>> from kuchka import Voltage
    >>> from_dict({"value": "2800", "unit": "mV"}, Voltage)
    2800 mV

    """
    if not isinstance(data, Mapping):
        msg = (
            f"a {quantity.__name__} is read from a mapping of a 'value' and a 'unit', "
            f"not {type(data).__name__} ({data!r})."
        )
        raise ParseError(msg)
    absent = [key for key in _KEYS if data.get(key) is None]
    if absent:
        msg = (
            f"a {quantity.__name__} is read from a mapping of a 'value' and a 'unit': "
            f"{' and '.join(repr(key) for key in absent)} missing from {data!r}."
        )
        raise ParseError(msg)
    return load(data, quantity, allow_archaic=allow_archaic)


def _in_unit(quantity: _ScalarStorage[Any], unit: UnitDef | str) -> Any:  # noqa: ANN401 -- same type
    """Return `quantity` displayed in `unit`, which has to be a unit of its type."""
    target: Any = unit
    asked: str | None = None
    if isinstance(unit, str):
        kind = type(quantity)
        table = unit_table_of(kind)
        try:
            spelled, constructor = table.resolve(unit)
        except KeyError:
            msg = f"{unit!r} is not a unit of {kind.__name__} (see {table.label})."
            raise UnknownUnitError(msg, unit=unit, quantity=kind) from None
        target = constructor(0).unit  # the unit the table builds, of whatever shape
        asked = spelled.symbol
    converting: Any = quantity  # `to` is on every shape, and typed on each
    shown = converting.to(target)
    if asked is not None and shown.unit.symbol != asked:
        msg = (
            f"a {type(quantity).__name__} is displayed in {shown.unit.symbol}, "
            f"and cannot be written in {asked}."
        )
        raise InvalidConversionError(msg)
    return shown


def _float_value(magnitude: Fraction) -> int | float:
    """Write a magnitude as a JSON number: an `int` if whole, else a `float`."""
    if magnitude.denominator == 1:
        return magnitude.numerator
    try:
        result = float(magnitude)
    except OverflowError:
        msg = f"{magnitude} is beyond the range of a float."
        raise InvalidMeasurementError(msg) from None
    if result == 0.0:
        msg = f"{magnitude} is so small that a float would write it as zero."
        raise InvalidMeasurementError(msg)
    return result


def _load(
    value: object,
    quantity: type[_ScalarStorage[Any]],
    table: UnitTable[Any],
    policy: ArchaicPolicy,
) -> Any:  # noqa: ANN401 -- an instance of `quantity`, which the caller types
    """Read `value` as a `quantity`, or raise an `InvalidMeasurementError`."""
    if isinstance(value, quantity):
        return value
    if isinstance(value, str):
        return parse(value, quantity, policy)
    if isinstance(value, Mapping):
        return _from_mapping(value, quantity, table, policy)
    if isinstance(value, _NUMBER_TYPES) and not isinstance(value, bool):
        return _from_number(value, table)
    if isinstance(value, _ScalarStorage):
        msg = (
            f"a {type(value).__name__} ({value!r}) is no {quantity.__name__}: "
            f"the field holds a {quantity.__name__}."
        )
        raise ParseError(msg)
    msg = (
        f"cannot read a {quantity.__name__} from {type(value).__name__} "
        f"({value!r}); expected {_expectation(table)}."
    )
    raise ParseError(msg)


def _from_number(value: float | Decimal | Fraction, table: UnitTable[Any]) -> Any:  # noqa: ANN401 -- an instance of the quantity, which the caller types
    """Read a number with no unit, which only a quantity with a bare unit accepts."""
    bare = table.bare
    if bare is None:
        msg = (
            f"{value!r} has no unit, so it does not say what it measures; "
            f"write it with one, as {_expectation(table)}."
        )
        raise ParseError(msg)
    return bare[1](value)


def _from_mapping(
    value: Mapping[Any, Any],
    quantity: type[_ScalarStorage[Any]],
    table: UnitTable[Any],
    policy: ArchaicPolicy,
) -> Any:  # noqa: ANN401 -- an instance of `quantity`, which the caller types
    """Read a mapping of a ``"value"`` and a ``"unit"``."""
    extra = [key for key in value if key not in _KEYS]
    if extra:
        msg = (
            f"a {quantity.__name__} is written with the keys {', '.join(_KEYS)}, "
            f"not {', '.join(repr(key) for key in extra)}."
        )
        raise ParseError(msg)
    if "value" not in value:
        msg = f"a {quantity.__name__} written as a mapping needs a 'value'."
        raise ParseError(msg)
    number = _number_of(value["value"])
    unit = value.get("unit")
    if unit is None:
        bare = table.bare
        if bare is None:
            msg = (
                f"{value!r} has no unit, so it does not say what it measures; "
                f"a {quantity.__name__} needs a 'unit' such as "
                f"{example_unit(table)!r}."
            )
            raise ParseError(msg)
        return bare[1](number)
    if not isinstance(unit, str):
        msg = f"the 'unit' of {value!r} is text, not {type(unit).__name__}."
        raise ParseError(msg)
    unit_text = normalize(unit).strip()
    if not unit_text:
        msg = f"the 'unit' of {value!r} is empty."
        raise ParseError(msg)
    return unit_constructor(quantity, table, unit_text, policy)(number)


def _number_of(value: object) -> Decimal | Fraction | int | float:
    """Read the ``"value"`` of a mapping: a number, or the text of exactly one."""
    if isinstance(value, bool) or not isinstance(value, (str, *_NUMBER_TYPES)):
        msg = f"the 'value' of a measurement is a number or text, not {value!r}."
        raise ParseError(msg)
    if not isinstance(value, str):
        return value
    number, unit_text = split_number(normalize(value).strip(), value)
    if unit_text:
        msg = f"the 'value' {value!r} holds more than a number: the unit is the 'unit'."
        raise ParseError(msg)
    return number


def _expectation(table: UnitTable[Any]) -> str:
    """Return what a quantity of `table` can be written as, for an error message."""
    if table.bare is not None:
        return 'a number, or text such as "0.25"'
    return f'text such as "5 {example_unit(table)}"'


def _magnitude_text(magnitude: Fraction) -> str:
    """Write `magnitude` exactly: a decimal if it terminates, else a fraction."""
    decimal = _decimal_text(magnitude)
    if decimal is not None:
        return decimal
    return f"{magnitude.numerator}/{magnitude.denominator}"


def _decimal_text(magnitude: Fraction) -> str | None:
    """Return `magnitude` as decimal text, or `None` if it has none within limits."""
    denominator = magnitude.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        return None
    places = max(twos, fives)
    if places > NUMERIC_LIMITS.max_decimal_exponent:
        return None
    scaled = abs(magnitude.numerator) * 10**places // magnitude.denominator
    if len(str(scaled)) > NUMERIC_LIMITS.max_decimal_digits:
        return None
    digits = str(scaled).rjust(places + 1, "0")
    whole, fraction = digits[: len(digits) - places], digits[len(digits) - places :]
    sign = "-" if magnitude < 0 else ""
    return f"{sign}{whole}.{fraction}" if places else f"{sign}{whole}"


__all__ = ["dump", "from_dict", "load", "to_dict"]
