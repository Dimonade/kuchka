"""Immutable storage, pickling, and text rendering shared by every scalar quantity.

Does not implement any operator at all, not even equality: those differ by
algebraic shape (linear, affine, modular, ...) and are added by the mixins and
concrete bases built on top of this one, in sibling modules of this package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

from kuchka.quantities.base.units import _DisplayUnit

if TYPE_CHECKING:
    from decimal import Decimal

_UnitT = TypeVar("_UnitT", bound=_DisplayUnit)


class _ScalarStorage(Generic[_UnitT]):
    """Immutable storage, pickling, and text rendering shared by every scalar quantity.

    Owns exactly the state every concrete quantity needs regardless of its algebraic
    shape: a `Decimal` magnitude expressed in this quantity's own canonical frame
    (volts for Voltage, kelvin for Temperature, ...), plus the unit it currently
    displays as.

    Deliberately implements no operator at all, not even equality:
    those differ by algebraic shape, and are added by `_OrderedScalarMixin` and the
    concrete bases (`LinearQuantity`, `AffineQuantity`) that compose it.
    Keeping this layer operator-free is what lets a future shape with no total order
    build on the same storage without inheriting comparisons it would have to
    un-implement.
    """

    _magnitude: Decimal
    _display_unit: _UnitT
    __slots__ = ("_display_unit", "_magnitude")

    def __init__(self, magnitude: Decimal, display_unit: _UnitT) -> None:
        """Store a magnitude in this quantity's canonical frame, plus a display unit."""
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def unit(self) -> _UnitT:
        """The unit this measurement currently displays as."""
        return self._display_unit

    def __getstate__(self) -> tuple[Decimal, _UnitT]:
        """Return the pickle/copy state: the magnitude and the display unit.

        Blocking `__setattr__` for immutability also blocks the default
        slot-restoring path `pickle` and `copy` use for `__slots__`-only classes with
        no `__getstate__`/`__setstate__` pair, since that path calls plain
        `setattr()`.

        Routing through `object.__setattr__`, the same way `__init__` already does, is
        what lets an immutable, `__slots__`-only quantity still be pickled, copied,
        and deep-copied.
        """
        return (self._magnitude, self._display_unit)

    def __setstate__(self, state: tuple[Decimal, _UnitT]) -> None:
        """Restore a pickled/copied instance without going through `__setattr__`."""
        magnitude, display_unit = state
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    def value_in(self, unit: _UnitT) -> Decimal:
        """Return the magnitude of this measurement expressed in `unit`.

        Overridden by each algebraic base: the formula differs between a pure scale
        (`LinearQuantity`) and a scale-plus-offset (`AffineQuantity`).
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"

    def __format__(self, format_spec: str) -> str:
        """Format the magnitude in the display unit, e.g. `f"{Volt(4.2):.2f}"`.

        An empty `format_spec` (`f"{voltage}"`, `str(voltage)`) matches `repr()`.
        A non-empty spec is applied to the underlying `Decimal` the same way it would
        be to a `float` or `int`, and the unit symbol is appended after --
        `f"{Volt(4.2):.2f}"` reads `"4.20 V"`.
        """
        if not format_spec:
            return repr(self)
        value = self.value_in(self._display_unit)
        return f"{format(value, format_spec)} {self._display_unit.symbol}"


__all__ = ["_ScalarStorage"]
