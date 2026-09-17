"""Immutable storage, pickling, and text rendering shared by every scalar quantity.

Does not implement any operator at all.
Algebraic shape (linear, affine, modular, ...) decides equality and ordering;
added by the mixins and concrete bases built on top of this one, in sibling modules
of this package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

from kuchka.numeric import to_decimal
from kuchka.quantities.base.units import _DisplayUnit

if TYPE_CHECKING:
    from fractions import Fraction

_UnitT = TypeVar("_UnitT", bound=_DisplayUnit)


class _ScalarStorage(Generic[_UnitT]):
    """State every scalar quantity needs, independent of algebraic shape.

    A `Fraction` magnitude in this quantity's own canonical frame (volts for Voltage,
    kelvin for Temperature, ...), plus the unit it currently displays as.
    `Fraction`, not `Decimal`: an exact rational input (`Litre(Fraction(5, 18))`) stays
    exact through storage; approximation happens only at `repr()`/`__format__`, via
    `to_decimal`.
    """

    _magnitude: Fraction
    _display_unit: _UnitT
    __slots__ = ("_display_unit", "_magnitude")

    def __init__(self, magnitude: Fraction, display_unit: _UnitT) -> None:
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def unit(self) -> _UnitT:
        """Unit this measurement currently displays as."""
        return self._display_unit

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

    def __repr__(self) -> str:
        value = to_decimal(self.value_in(self._display_unit))
        return f"{format(value, 'f')} {self._display_unit.symbol}"

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
