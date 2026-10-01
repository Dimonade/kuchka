"""Immutable storage, pickling, and text rendering shared by every scalar quantity.

Does not implement any operator at all.
Algebraic shape (linear, affine, modular, ...) decides equality and ordering;
added by the mixins and concrete bases built on top of this one, in sibling modules
of this package.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Generic
from typing import TypeVar

from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import to_decimal
from kuchka.quantities.base.units import _DisplayUnit

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

_UnitT = TypeVar("_UnitT", bound=_DisplayUnit)


class _ScalarStorage(Generic[_UnitT]):
    """State every scalar quantity needs, independent of algebraic shape.

    A `Fraction` magnitude in this quantity's own canonical frame (volts for Voltage,
    kelvin for Temperature, ...), plus the unit it currently displays as.
    `Fraction`, not `Decimal`: an exact rational input (`Litre(Fraction(5, 18))`) stays
    exact through storage; approximation happens only at `repr()`/`__format__`, via
    `to_decimal`.

    The class itself is part of the public surface (`Voltage`, ...), so its constructor
    is a validation boundary just like the unit constructors are:
    it accepts only an exact `Fraction` and a display unit of the right kind and
    dimension, and rejects everything else instead of storing it.
    Plain numbers in a particular unit are what the unit constructors (`Volt`,
    `Celsius`, ...) are for.
    """

    _magnitude: Fraction
    _display_unit: _UnitT
    dimension: ClassVar[Dimension]
    _unit_type: ClassVar[type]
    """The kind of unit definition this algebraic shape displays in.

    Assigned by each algebraic base (`LinearQuantity`, `AffineQuantity`, ...).
    """
    __slots__ = ("_display_unit", "_magnitude")

    def __init__(self, magnitude: Fraction, display_unit: _UnitT) -> None:
        """Store `magnitude` (canonical unit) and `display_unit`, validating both."""
        cls = type(self)
        if not isinstance(magnitude, Fraction):
            msg = (
                f"{cls.__name__} takes an exact `Fraction` magnitude in its "
                f"canonical unit, got {type(magnitude).__name__} ({magnitude!r}). "
                "To build a measurement from a plain number, use one of the unit "
                "constructors in `kuchka.units` instead."
            )
            raise InvalidMeasurementError(msg)
        if not isinstance(display_unit, cls._unit_type):
            msg = (
                f"{cls.__name__} needs a {cls._unit_type.__name__} as its display "
                f"unit, got {display_unit!r}."
            )
            raise InvalidMeasurementError(msg)
        # NOTE: Affine and logarithmic unit definitions carry no dimension of
        # their own; their `_unit_type` check above is the whole contract.
        unit_dimension = getattr(display_unit, "dimension", None)
        if (
            unit_dimension is not None
            and unit_dimension is not cls.dimension
            and unit_dimension != cls.dimension
        ):
            msg = (
                f"cannot construct a {cls.__name__} displayed in "
                f"{display_unit.name} ({display_unit.symbol}): "
                f"incompatible dimensions - "
                f"[{cls.dimension!r}] and [{unit_dimension!r}]."
            )
            raise InvalidMeasurementError(msg)
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def unit(self) -> _UnitT:
        """Unit this measurement currently displays as."""
        return self._display_unit

    @override
    def __getstate__(self) -> tuple[Fraction, _UnitT]:
        """Pickle/copy state: magnitude and display unit.

        `__setattr__` blocks the default slot-restoring path `pickle`/`copy` use for
        `__slots__`-only classes, since that path calls plain `setattr()`.
        `object.__setattr__`, the same way `__init__` does it, restores state without
        going through the guard.
        """
        return (self._magnitude, self._display_unit)

    def __setstate__(self, state: tuple[Fraction, _UnitT]) -> None:
        """Restore a pickled/copied instance without going through `__setattr__`."""
        magnitude, display_unit = state
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    def value_in(self, unit: _UnitT) -> Fraction:
        """Exact magnitude expressed in `unit`.

        Overridden per algebraic base: a pure scale (`LinearQuantity`) vs. a
        scale-plus-offset (`AffineQuantity`).
        """
        raise NotImplementedError

    @override
    def __repr__(self) -> str:
        value = to_decimal(self.value_in(self._display_unit))
        return f"{format(value, 'f')} {self._display_unit.symbol}"

    @override
    def __format__(self, format_spec: str) -> str:
        """Format the magnitude in the display unit, e.g. `f"{Volt(4.2):.2f}"`.

        Empty `format_spec` (`f"{voltage}"`, `str(voltage)`) matches `repr()`.
        Non-empty spec applies to the materialized `Decimal`; unit symbol appended
        after -- `f"{Volt(4.2):.2f}"` reads `"4.20 V"`.
        """
        if not format_spec:
            return repr(self)
        value = to_decimal(self.value_in(self._display_unit))
        return f"{format(value, format_spec)} {self._display_unit.symbol}"


__all__ = ["_ScalarStorage"]
