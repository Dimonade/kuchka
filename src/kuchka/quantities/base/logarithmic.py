"""PureLogarithmicQuantity: the base for a ratio expressed as a logarithm.

A level -- the logarithm of a ratio, such as 20 dB, 3 dB, or -6 dB.
Multiplying two ratios adds their levels, so the gain of an amplifier and the loss of
a cable in series combine by plain addition:
``Decibel(20) + Decibel(-3.5) == Decibel(16.5)``.

The level itself is stored as an exact `Fraction`, so every operation in this module
is exact.
Converting between a level and the linear ratio it describes involves a logarithm and
lives on the concrete quantity type that owns the ratio.

Levels have a total order, since a larger ratio is a larger level.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import Numeric
from kuchka.numeric import exact_quotient
from kuchka.numeric import to_exact
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import LogarithmicUnitDef

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension


class PureLogarithmicQuantity(_OrderedScalarMixin, _ScalarStorage[LogarithmicUnitDef]):
    """Base class for a ratio expressed as a logarithm, with no reference level.

    Stores its magnitude in the canonical unit (decibels) plus the unit most recently
    asked to be seen in (``_display_unit``), which affects only ``repr()``.

    * ``+``/``-``: combine two levels.
        Adding levels multiplies the ratios they describe, and subtracting divides
        them: ``Decibel(20) - Decibel(3) == Decibel(17)``.
    * ``*``/``/`` by a plain number: scale the level.
        ``Decibel(-0.2) * 30 == Decibel(-6)``, the loss of a 30 m cable at
        0.2 dB per metre.
    * ``/`` by another level: how many times one fits into the other, a plain
        `Fraction`.
    * ``-level``: the reciprocal ratio.
        ``-Decibel(3)`` is the attenuation that undoes a 3 dB gain.
    * ``abs(level)``: the size of a deviation, e.g. gain error against a tolerance.
    * Comparison: ordinary numeric ordering of the levels.

    A concrete subclass assigns:
    - `dimension`: the dimension of the ratio's underlying quantity.
    - `_canonical_unit`: the unit the magnitude is stored in.
    """

    dimension: ClassVar[Dimension]
    _canonical_unit: ClassVar[LogarithmicUnitDef]
    _unit_type: ClassVar[type] = LogarithmicUnitDef
    __slots__ = ()

    @property
    def magnitude(self) -> Fraction:
        """Magnitude in this quantity's canonical unit."""
        return self._magnitude

    def to(self, unit: LogarithmicUnitDef) -> Self:
        """Return an equal level that displays as ``unit``.

        This never changes the value being represented: ``Decibel(10)`` and
        ``Decibel(10).to(BEL)`` compare equal.
        It only changes what ``repr()`` and ``value_in()`` return by default.
        """
        if not isinstance(unit, LogarithmicUnitDef):
            msg = (
                f"invalid conversion target {unit!r}: expected a logarithmic unit "
                "such as DECIBEL or BEL"
            )
            raise InvalidConversionError(msg)
        self._reject_foreign_unit(unit)
        return type(self)(self._magnitude, unit)

    @override
    def value_in(self, unit: LogarithmicUnitDef) -> Fraction:
        """Exact magnitude expressed in ``unit``."""
        return self._magnitude / unit.scale

    def __add__(self, other: Self) -> Self:
        # NOTE: `other` is typed as `Self` so that `Decibel(3) + Ratio(2)` and
        # `Decibel(3) + 3` are both rejected by type checkers, the same way
        # `LinearQuantity.__add__` does it.
        # The isinstance checks below remain the authoritative guard for values that
        # reach this call dynamically typed.
        if isinstance(other, PureLogarithmicQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            return type(self)(self._magnitude + other._magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, PureLogarithmicQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            return type(self)(self._magnitude - other._magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("subtract", other)
        return NotImplemented

    def is_close(self, other: Self, *, tolerance: Self) -> bool:
        """Return whether `other` is within `tolerance` of `self`, inclusive.

        The tolerance is a level of the same type, e.g. ``Decibel(0.1)``, and has no
        default.
        """
        limit = self._tolerance_limit(other, tolerance, type(self))
        return abs(self._magnitude - other._magnitude) <= limit

    def _reject_naked_number(self, operation: str, other: object) -> None:
        unit_name = self._canonical_unit.name.capitalize()
        msg = (
            f"cannot {operation} a plain number ({other!r}) to a "
            f"{type(self).__name__}; wrap it in a unit constructor first, "
            f"e.g. {unit_name}({other!r})"
        )
        raise InvalidMeasurementError(msg)

    def __mul__(self, other: Numeric) -> Self:
        if isinstance(other, Numeric):
            return type(self)(self._magnitude * to_exact(other), self._display_unit)
        return NotImplemented

    def __rmul__(self, other: Numeric) -> Self:
        return self.__mul__(other)

    @overload
    def __truediv__(self, other: Numeric) -> Self: ...
    @overload
    def __truediv__(self, other: Self) -> Fraction: ...

    def __truediv__(self, other: object) -> Self | Fraction:
        if isinstance(other, PureLogarithmicQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("divide", self, other)
            return exact_quotient(
                self._magnitude, other._magnitude, left=self, right=other
            )
        if isinstance(other, Numeric):
            magnitude = exact_quotient(
                self._magnitude, to_exact(other), left=self, right=other
            )
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __neg__(self) -> Self:
        return type(self)(-self._magnitude, self._display_unit)

    def __abs__(self) -> Self:
        return type(self)(abs(self._magnitude), self._display_unit)


__all__ = ["PureLogarithmicQuantity"]
