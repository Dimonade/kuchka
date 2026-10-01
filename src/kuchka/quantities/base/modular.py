"""ModularQuantity: the base for quantities that wrap around after a fixed period.

A position on a circle.
Two readings that differ by exactly one full period represent the same physical value
(``30 degrees == 390 degrees``).

No total order.
``Angle(350) < Angle(10)`` is a plain ``TypeError`` -- comparison operators are not
implemented at all, the same mechanism ``AffineQuantity`` uses for "no ``__mul__``".
The reasoning is that different domains define these relationships in a different
way, and ``kuchka`` does not decide it for anyone.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import UnitDef

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension


class ModularQuantity(_ScalarStorage[UnitDef]):
    """Base class for quantities that wrap around after a fixed period.

    Composes `_ScalarStorage` directly, no total order for a cyclic quantity.

    Two operations, kept separate because they answer different questions:

    * ``+``/``-``: wraparound group arithmetic, result in ``[0, period)``.
        ``Angle(300) - Angle(350) == Angle(310)``.
    * `difference()`: shortest signed path, result in ``(-period/2, +period/2]``.
        ``Angle(300).difference(Angle(350)) == Angle(-50)``.

    Construction does not normalize.
    ``Angle(370)`` is a distinct stored value from ``Angle(10)`` until compared
    (equality compares normalized magnitude) or `normalize()`-d.
    Every arithmetic operation wraps its result; the constructor does not.

    A concrete subclass (`Angle`) assigns:
    - `_period`: magnitude of one full cycle, in the canonical unit.
    - `_canonical_unit`: same role as `LinearQuantity._canonical_unit`.
    """

    dimension: ClassVar[Dimension]
    _period: ClassVar[Fraction]
    _canonical_unit: ClassVar[UnitDef]
    _unit_type: ClassVar[type] = UnitDef
    __slots__ = ()

    @property
    def magnitude(self) -> Fraction:
        """Magnitude in this quantity's canonical unit."""
        return self._magnitude

    def to(self, unit: UnitDef) -> Self:
        """Return an equal reading that displays as ``unit``."""
        if not isinstance(unit, UnitDef):
            msg = (
                f"invalid conversion target {unit!r}: expected a Kuchka unit definition"
            )
            raise InvalidConversionError(msg)
        if unit.dimension != self.dimension:
            msg = (
                f"cannot convert {self.unit.name} ({self.unit.symbol}) "
                f"to {unit.name} ({unit.symbol}): "
                f"incompatible dimensions - "
                f"[{self.dimension!r}] and [{unit.dimension!r}]."
            )
            raise InvalidConversionError(msg)
        return type(self)(self._magnitude, unit)

    @override
    def value_in(self, unit: UnitDef) -> Fraction:
        """Exact magnitude expressed in ``unit``."""
        return self._magnitude / unit.scale

    def _wrap(self, magnitude: Fraction) -> Fraction:
        """Reduce `magnitude` into ``[0, period)``.

        `Fraction.__mod__` matches Python's `int`/`float` sign convention:
        the result carries the sign of the divisor, non-negative for a positive period.
        `Fraction(-10) % Fraction(360) == 350`.
        """
        return magnitude % self._period

    def normalize(self) -> Self:
        """Return an equal reading whose magnitude lies in ``[0, period)``."""
        return type(self)(self._wrap(self._magnitude), self._display_unit)

    def difference(self, other: Self) -> Self:
        """Return the shortest signed path from `other` to `self`.

        Result in ``(-period/2, +period/2]``.
        Positive: `self` is ahead of `other` the short way round.
        Negative: behind.
        Different from plain ``self - other`` -- see the class docstring.
        """
        if type(self) is not type(other):
            raise IncompatibleDimensionError(
                "compute the difference between", self, other
            )
        half_period = self._period / 2
        raw = self._wrap(self._magnitude - other._magnitude)
        if raw > half_period:
            raw -= self._period
        return type(self)(raw, self._display_unit)

    @override
    def __eq__(self, other: object) -> bool:
        # Compares normalized magnitude: `Angle(0) == Angle(360)` is true.
        if not isinstance(other, ModularQuantity) or type(self) is not type(other):
            return NotImplemented
        return self._wrap(self._magnitude) == other._wrap(other._magnitude)

    @override
    def __hash__(self) -> int:
        return hash((type(self), self._wrap(self._magnitude)))

    def __add__(self, other: Self) -> Self:
        if isinstance(other, ModularQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            magnitude = self._wrap(self._magnitude + other._magnitude)
            return type(self)(magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self) -> Self:
        """Wraparound subtraction, result in ``[0, period)``.

        Different question from `difference()` -- see the class docstring.
        """
        if isinstance(other, ModularQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            magnitude = self._wrap(self._magnitude - other._magnitude)
            return type(self)(magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("subtract", other)
        return NotImplemented

    def _reject_naked_number(self, operation: str, other: object) -> None:
        unit_name = self._canonical_unit.name.capitalize()
        msg = (
            f"cannot {operation} a plain number ({other!r}) to a "
            f"{type(self).__name__}; wrap it in a unit constructor first, "
            f"e.g. {unit_name}({other!r})"
        )
        raise InvalidMeasurementError(msg)

    def __mul__(self, other: object) -> Self:
        if isinstance(other, Numeric):
            magnitude = self._wrap(self._magnitude * to_exact(other))
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        return self.__mul__(other)

    def __truediv__(self, other: object) -> Self:
        if isinstance(other, Numeric):
            magnitude = self._wrap(self._magnitude / to_exact(other))
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __neg__(self) -> Self:
        """Reverse direction: ``-Angle(30) == Angle(330)``."""
        return type(self)(self._wrap(-self._magnitude), self._display_unit)

    # NOTE: No __abs__: no meaningful absolute value for a cyclic reading -- 30 degrees
    # and 330 degrees are opposite directions, not a sign-and-magnitude pair.
    # No __lt__/__le__/__gt__/__ge__ -- see the module docstring.


__all__ = ["ModularQuantity"]
