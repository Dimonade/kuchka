"""Quantity fields for `attrs` classes.

    import attrs

    from kuchka import Voltage
    from kuchka.attrs import parse_field


    @attrs.define(frozen=True)
    class SensorSpec:
        threshold: Voltage = attrs.field(converter=parse_field(Voltage))

`parse_field(Voltage)` is a converter for `attrs.field`: it reads what a caller or a
loader hands the class into a `Voltage`, so the attribute is a `Voltage` whatever
arrived, and a value that is no voltage fails when the instance is made.
It reads what `kuchka.wire.load` reads: a `Voltage`, text such as `"2800 mV"` or
`"1/3 V"`, and a mapping of a `"value"` and a `"unit"`; a `Proportion` field reads
a number as well.

The converter is a plain function, so this module imports nothing from `attrs` and
needs no extra to install.
`Bounds(gt=Volt(0), le=Volt(60))` is the validator that limits the range of the field.

Static types
------------
`pyright` reads the converter in full: the `__init__` of `SensorSpec` takes a `Voltage`,
a `str`, or a mapping for `threshold`, so `SensorSpec(3.3)` is an error before the
program runs, and `threshold` is a `Voltage` on the instance.
`mypy` types the attribute as `Voltage` as well, and its `attrs` plugin accepts only a
named function, a type, or a lambda as a converter, so it reports `converter=
parse_field(Voltage)` as unsupported and types the `__init__` parameter as `Any`.
A converter written as a named function, `def to_voltage(value: Voltage | str |
Mapping[str, object]) -> Voltage: return load(value, Voltage)` with `load` from
`kuchka.wire`, gives `mypy` the same `__init__` that `pyright` reads.

Examples
--------
>>> import attrs
>>> from kuchka import Proportion
>>> from kuchka import Volt
>>> from kuchka import Voltage
>>> from kuchka.attrs import parse_field
>>> @attrs.define(frozen=True)
... class SensorSpec:
...     threshold: Voltage = attrs.field(converter=parse_field(Voltage))
...     duty: Proportion = attrs.field(converter=parse_field(Proportion))
>>> SensorSpec("2800 mV", 0.25)
SensorSpec(threshold=2800 mV, duty=0.25 1)
>>> SensorSpec(Volt(3.3), "25 %").threshold
3.3 V

A value that is no voltage raises `ParseError`, a `ValueError`, when the instance is
made:

>>> SensorSpec("150 mA", 0.25)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.UnknownUnitError: 'mA' is not a unit of Voltage (see VOLTAGE_UNITS).

"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar
from typing import overload

from kuchka.bounds import Bounds as _Bounds
from kuchka.errors import BoundsError
from kuchka.internal.reading import ArchaicPolicy
from kuchka.internal.reading import archaic_policy_of
from kuchka.internal.reading import unit_table_of
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.wire import load

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping
    from decimal import Decimal
    from fractions import Fraction

    from attrs import Attribute

    from kuchka.quantities import Proportion
    from kuchka.quantities.base.storage import _ScalarStorage

_QuantityT = TypeVar("_QuantityT", bound="_ScalarStorage[Any]")
_OrderedT = TypeVar("_OrderedT", bound=_OrderedScalarMixin)


@overload
def parse_field(
    quantity: type[Proportion],
    *,
    allow_archaic: ArchaicPolicy | bool = ...,
) -> Callable[
    [Proportion | str | Mapping[str, object] | float | Decimal | Fraction], Proportion
]: ...


@overload
def parse_field(
    quantity: type[_QuantityT],
    *,
    allow_archaic: ArchaicPolicy | bool = ...,
) -> Callable[[_QuantityT | str | Mapping[str, object]], _QuantityT]: ...


def parse_field(
    quantity: type[Any],
    *,
    allow_archaic: ArchaicPolicy | bool = ArchaicPolicy.Deny,
) -> Callable[[Any], Any]:
    """Return a converter that reads a value as a measurement of type `quantity`.

    Parameters
    ----------
    quantity : type
        The quantity type of the field, such as `Voltage`.
    allow_archaic : ArchaicPolicy or bool, optional
        Whether the converter reads archaic units, as `parse` does.

    Returns
    -------
    Callable
        A function for `attrs.field(converter=...)`.
        It returns an instance of `quantity` unchanged, reads text and a mapping of a
        `"value"` and a `"unit"`, and for a `Proportion` reads a number, all as
        `kuchka.wire.load` does.
        Anything else raises `ParseError`, which is a `ValueError`.

    Raises
    ------
    TypeError
        `quantity` is no quantity type with units, or `allow_archaic` is neither an
        `ArchaicPolicy` nor a `bool`, raised when the converter is made, which is
        when the class is defined.

    Examples
    --------
    >>> from kuchka import Voltage
    >>> convert = parse_field(Voltage)
    >>> convert("2800 mV")
    2800 mV

    """
    policy = archaic_policy_of(allow_archaic)
    unit_table_of(quantity)

    def convert(value: object) -> Any:  # noqa: ANN401 -- an instance of `quantity`
        return load(value, quantity, allow_archaic=policy)

    convert.__name__ = convert.__qualname__ = f"parse_field({quantity.__name__})"
    return convert


class Bounds(_Bounds[_OrderedT]):
    """The range an `attrs` quantity field accepts, as the validator of the field.

        threshold: Voltage = attrs.field(
            converter=parse_field(Voltage), validator=Bounds(gt=Volt(0), le=Volt(60))
        )

    `kuchka.bounds.Bounds` as an `attrs` validator, which attrs runs after the
    converter: a value outside the range raises `BoundsError`, a `ValueError`, that
    names the attribute and writes the value and the bound.
    A converter and bounds of different quantity types are reported, with the
    attribute, when the instance is made.
    """

    def __call__(
        self,
        instance: object,  # noqa: ARG002 -- the protocol of an attrs validator
        attribute: Attribute[Any],
        value: _OrderedT,
    ) -> None:
        """Raise `BoundsError` unless `value` is within the bounds."""
        try:
            self.check(value)
        except BoundsError as exc:
            msg = f"{attribute.name}: {exc}"
            raise BoundsError(msg) from exc
        except TypeError as exc:
            msg = f"{attribute.name}: {exc}"
            raise TypeError(msg) from exc


__all__ = ["Bounds", "parse_field"]
