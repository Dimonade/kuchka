"""ModularQuantity: the base for quantities that wrap around after a fixed period.

``ModularQuantity`` means the quantity is a position on a circle, not a point on a
line: two readings that differ by exactly one full period represent the same
physical value (``30 degrees == 390 degrees``).
``Angle`` is one such quantity; a compass heading or a wrapped instantaneous phase
could be later ones.

Unlike ``LinearQuantity`` and ``AffineQuantity``, this shape has no total order.
"Is 350 degrees greater than 10 degrees" depends on a direction-of-travel convention
this base deliberately does not pick, so comparison operators are not implemented at
all -- ``Angle(350) < Angle(10)`` is a plain ``TypeError``, the same mechanism
``AffineQuantity`` already relies on for "no ``__mul__``".
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.numeric import to_decimal
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import UnitDef

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

_NUMERIC_TYPES = (int, float, Decimal, Fraction)


class ModularQuantity(_ScalarStorage[UnitDef]):
    """Base class for quantities that wrap around after a fixed period.

    Composes `_ScalarStorage` directly, not `_OrderedScalarMixin`: there is no
    well-defined, universal "greater than" for a cyclic quantity (whether 350
    degrees is "more" than 10 degrees depends on a direction-of-travel convention
    this base does not pick), so no ordering operator is implemented -- see the
    module docstring.

    Two operations are provided, deliberately kept separate because they answer
    different questions and disagree on the answer:

    * ``+``/``-`` are ordinary wraparound group arithmetic:
        the result always lands in ``[0, period)``.
        ``Angle(300) - Angle(350)`` is ``Angle(310)`` -- "how far do I need to keep
        turning from 350 to reach 300, going the same way".
    * `difference()` is the shortest signed path between two readings, landing in
        ``(-period/2, +period/2]``.
        ``Angle(300).difference(Angle(350))`` is ``Angle(-50)`` -- "300 is 50 degrees
        behind 350, the short way round".
        This is the one to reach for for things like a heading error or a control-loop
        correction, where the sign and the "shortest way" both matter.

    Construction places no domain restriction on the magnitude, the same way
    `LinearQuantity` construction does not: ``Angle(370)`` is a valid, distinct
    stored value from ``Angle(10)`` until compared (equality compares normalized
    magnitude) or explicitly `normalize()`-d.
    Every arithmetic *operation* (``+``, ``-``, ``*``, `difference()`) wraps its result
    into ``[0, period)`` (or the signed range, for `difference()`);
    only the constructor leaves a raw value alone.

    A concrete subclass (`Angle`) assigns two class attributes, the same way a
    `LinearQuantity` subclass's owning unit module assigns `_canonical_unit`:

    - `_period`: the magnitude, in this quantity's canonical unit, of one full
      cycle (``Decimal(360)`` for `Angle`, stored in degrees).
    - `_canonical_unit`: same role as on `LinearQuantity` -- the coherent `UnitDef`
      this quantity's magnitude is stored in.
    """

    dimension: ClassVar[Dimension]
    _period: ClassVar[Decimal]
    _canonical_unit: ClassVar[UnitDef]
    __slots__ = ()

    def to(self, unit: UnitDef) -> Self:
        """Return an equal reading that displays as ``unit``.

        This never changes the value being represented, only what ``repr()`` and
        ``value_in()`` return by default. Same shape as `LinearQuantity.to`; not
        shared with it because the two types are not related by inheritance.
        """
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

    def value_in(self, unit: UnitDef) -> Decimal:
        """Return the magnitude of this reading expressed in ``unit``."""
        return self._magnitude / unit.scale

    def _wrap(self, magnitude: Decimal) -> Decimal:
        """Reduce `magnitude` into ``[0, period)`` using true mathematical modulo.

        `Decimal.__mod__` follows the sign of the *dividend*, not the divisor
        (``Decimal(-10) % Decimal(360) == Decimal(-10)``, not ``350``) -- the
        opposite convention from Python's own `int`/`float` ``%``.
        Every wraparound in this class routes through here specifically to correct for
        that.
        """
        wrapped = magnitude % self._period
        if wrapped < 0:
            wrapped += self._period
        return wrapped

    def normalize(self) -> Self:
        """Return an equal reading whose magnitude lies in ``[0, period)``."""
        return type(self)(self._wrap(self._magnitude), self._display_unit)

    def difference(self, other: Self) -> Self:
        """Return the shortest signed path from `other` to `self`.

        Lands in ``(-period/2, +period/2]``: positive means `self` is ahead of
        `other` the short way round, negative means behind.
        This is the version to use for a heading error or a control-loop correction;
        plain ``self - other`` answers a different question (see the class docstring).
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

    def __eq__(self, other: object) -> bool:
        # NOTE: compares *normalized* magnitude, unlike `_OrderedScalarMixin`'s
        # raw-magnitude equality -- `Angle(0) == Angle(360)` is true, because they
        # are the same physical reading. This is why `ModularQuantity` cannot just
        # compose `_OrderedScalarMixin`: the equality rule itself differs, not only
        # whether ordering exists.
        if not isinstance(other, ModularQuantity) or type(self) is not type(other):
            return NotImplemented
        return self._wrap(self._magnitude) == other._wrap(other._magnitude)

    def __hash__(self) -> int:
        return hash((type(self), self._wrap(self._magnitude)))

    def __add__(self, other: Self) -> Self:
        if isinstance(other, ModularQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            magnitude = self._wrap(self._magnitude + other._magnitude)
            return type(self)(magnitude, self._display_unit)
        if isinstance(other, _NUMERIC_TYPES):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self) -> Self:
        """Wraparound subtraction, landing in ``[0, period)``.

        Not the same question `difference()` answers -- see the class docstring.
        """
        if isinstance(other, ModularQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            magnitude = self._wrap(self._magnitude - other._magnitude)
            return type(self)(magnitude, self._display_unit)
        if isinstance(other, _NUMERIC_TYPES):
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
        if isinstance(other, _NUMERIC_TYPES):
            magnitude = self._wrap(self._magnitude * to_decimal(other))
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        return self.__mul__(other)

    def __truediv__(self, other: object) -> Self:
        if isinstance(other, _NUMERIC_TYPES):
            magnitude = self._wrap(self._magnitude / to_decimal(other))
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __neg__(self) -> Self:
        """Reverse direction: ``-Angle(30) == Angle(330)``."""
        return type(self)(self._wrap(-self._magnitude), self._display_unit)

    # NOTE: Deliberately no __abs__: there is no obviously meaningful "absolute
    # value" of a cyclic reading the way there is for a signed linear one -- 30
    # degrees and 330 degrees are opposite directions, not a sign-and-magnitude
    # pair. Deliberately no __lt__/__le__/__gt__/__ge__ either -- see the module
    # docstring.


__all__ = ["ModularQuantity"]
