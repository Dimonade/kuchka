"""The range of measurements a field accepts.

    from kuchka import Volt
    from kuchka.bounds import Bounds

    supply = Bounds(gt=Volt(0), le=Volt(60))
    supply.check(Volt(12))
    Volt(61) in supply

A supply voltage is above zero and at most 60 V, a duty is between 0 and 1, a
temperature is above absolute zero: configuration is validated against such limits,
and `Bounds` holds one.
`gt`, `ge`, `lt`, and `le` are the exclusive and inclusive lower and upper bounds, as
measurements of one quantity type, and a measurement is compared with each exactly, in
whatever unit either was written, so `Percent(100)` is the same bound as `Ratio(1)`.
`check(value)` returns the value or raises `BoundsError`, and `value in bounds` answers
with a `bool`.

The bounds are typed to ordered quantities, so a checker reports `Bounds(ge=Degree(0))`
before the program runs.
The class is the framework-free part: `kuchka.pydantic.Bounds` and
`kuchka.attrs.Bounds` are the same bounds as a Pydantic annotation and an `attrs`
validator, and a `msgspec` struct calls `check` in `__post_init__`.

A quantity with no ordering has no bounds: an `Angle` is a point on a circle, so `Angle`
bounds raise `TypeError` when they are made.
The bounds are checked when they are made, so a mistake in the program shows at the
line that wrote it: no bound, two lower or two upper bounds, bounds of different
quantity types, and a range that no value is in.

Examples
--------
>>> from kuchka import Millivolt
>>> from kuchka import Volt
>>> supply = Bounds(gt=Volt(0), le=Volt(60))
>>> supply.check(Millivolt(12000))
12000 mV
>>> Volt(61) in supply
False
>>> supply.describe()
'above 0 V and at most 60 V'
>>> supply.check(Volt(61))
Traceback (most recent call last):
...
kuchka.errors.BoundsError: 61 V is above 60 V, the most allowed.

"""

from __future__ import annotations

import operator
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import cast

from kuchka.errors import BoundsError
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.wire import dump

_QuantityT = TypeVar("_QuantityT", bound=_OrderedScalarMixin)

_BOUNDS = ("gt", "ge", "lt", "le")


@dataclass(frozen=True, kw_only=True)
class Bounds(Generic[_QuantityT]):
    """The range of measurements of one quantity type that a field accepts.

    Parameters
    ----------
    gt : quantity, optional
        The measurement must be above this one.
    ge : quantity, optional
        The measurement must be at least this one.
    lt : quantity, optional
        The measurement must be below this one.
    le : quantity, optional
        The measurement must be at most this one.

    Raises
    ------
    ValueError
        No bound is given, `gt` and `ge` or `lt` and `le` are both given, or no
        measurement is within the range.
    TypeError
        A bound is no measurement, the bounds are of different quantity types, or the
        quantity type has no ordering.

    Attributes
    ----------
    quantity : type
        The quantity type of the bounds.

    Examples
    --------
    >>> from kuchka import Percent
    >>> from kuchka import Ratio
    >>> share = Bounds(ge=Ratio(0), le=Percent(100))
    >>> Ratio(0.5) in share
    True
    >>> Percent(101) in share
    False

    """

    gt: _QuantityT | None = None
    ge: _QuantityT | None = None
    lt: _QuantityT | None = None
    le: _QuantityT | None = None
    quantity: type[_QuantityT] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Check that the bounds make a range, raising if they do not."""
        given = {name: getattr(self, name) for name in _BOUNDS}
        given = {name: bound for name, bound in given.items() if bound is not None}
        if not given:
            msg = "Bounds needs at least one of gt, ge, lt, and le."
            raise ValueError(msg)
        for first, second in (("gt", "ge"), ("lt", "le")):
            if first in given and second in given:
                msg = f"{first} and {second} are both {_side(first)} bounds: give one."
                raise ValueError(msg)
        for name, bound in given.items():
            if not isinstance(bound, _ScalarStorage):
                msg = f"{name} is {bound!r}, not a measurement."
                raise TypeError(msg)
        types = {type(bound) for bound in given.values()}
        if len(types) > 1:
            names = ", ".join(sorted(kind.__name__ for kind in types))
            msg = f"the bounds are of different quantity types ({names})."
            raise TypeError(msg)
        (quantity,) = types
        sample = next(iter(given.values()))
        try:
            operator.lt(sample, sample)  # asks whether the type is ordered
        except TypeError:
            msg = f"{quantity.__name__} has no ordering, so it has no bounds."
            raise TypeError(msg) from None
        object.__setattr__(self, "quantity", quantity)
        self._require_a_range()

    def _require_a_range(self) -> None:
        """Raise `ValueError` if no measurement is within the bounds."""
        lower, upper = self._lower(), self._upper()
        if lower is None or upper is None:
            return
        (low_name, low), (high_name, high) = lower, upper
        exclusive = low_name == "gt" or high_name == "lt"
        if low > high or (low == high and exclusive):
            msg = f"no measurement is {self.describe()}."
            raise ValueError(msg)

    def _lower(self) -> tuple[str, _QuantityT] | None:
        if self.gt is not None:
            return "gt", self.gt
        if self.ge is not None:
            return "ge", self.ge
        return None

    def _upper(self) -> tuple[str, _QuantityT] | None:
        if self.lt is not None:
            return "lt", self.lt
        if self.le is not None:
            return "le", self.le
        return None

    def describe(self) -> str:
        """Write the range in words, such as ``'above 0 V and at most 60 V'``."""
        words = {"gt": "above", "ge": "at least", "lt": "below", "le": "at most"}
        parts = [
            f"{words[name]} {_text(getattr(self, name))}"
            for name in _BOUNDS
            if getattr(self, name) is not None
        ]
        return " and ".join(parts)

    def check(self, value: _QuantityT) -> _QuantityT:
        """Return `value` if it is within the bounds, and raise `BoundsError` if not.

        Parameters
        ----------
        value : quantity
            A measurement of the quantity type of the bounds.

        Returns
        -------
        quantity
            `value`, so that a check can sit in a chain of conversions.

        Raises
        ------
        BoundsError
            `value` is below, above, or on an excluded edge of the bounds.
        TypeError
            `value` is no measurement of the quantity type of the bounds.

        """
        self._require_a_measurement(value)
        text = _text(value)
        if (low := self._lower()) is not None:
            name, bound = low
            if name == "ge" and value < bound:
                msg = f"{text} is below {_text(bound)}, the least allowed."
                raise BoundsError(msg)
            if name == "gt" and value <= bound:
                msg = f"{text} is not above {_text(bound)}."
                raise BoundsError(msg)
        if (high := self._upper()) is not None:
            name, bound = high
            if name == "le" and value > bound:
                msg = f"{text} is above {_text(bound)}, the most allowed."
                raise BoundsError(msg)
            if name == "lt" and value >= bound:
                msg = f"{text} is not below {_text(bound)}."
                raise BoundsError(msg)
        return value

    def __contains__(self, value: object) -> bool:
        """Return whether `value` is within the bounds, raising for a wrong type."""
        self._require_a_measurement(value)
        try:
            self.check(cast("_QuantityT", value))
        except BoundsError:
            return False
        return True

    def _require_a_measurement(self, value: object) -> None:
        """Raise `TypeError` unless `value` is a measurement of the bounds' type."""
        if not isinstance(value, self.quantity):
            msg = (
                f"bounds of {self.quantity.__name__} cannot check "
                f"{type(value).__name__} ({value!r})."
            )
            raise TypeError(msg)


def _text(quantity: object) -> str:
    """Write an ordered quantity in the wire form, for a message."""
    return dump(cast("_ScalarStorage[Any]", quantity))


def _side(name: str) -> str:
    """Return whether the bound `name` is a lower or an upper one."""
    return "lower" if name in {"gt", "ge"} else "upper"


__all__ = ["Bounds"]
