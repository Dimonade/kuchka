"""AffineQuantity: the base for quantities that are a point on a scale, not a vector.

``AffineQuantity`` means the quantity is a point on a scale:
its units differ by both a scale and an offset (0 degC = 273.15 K), so doubling a
reading or adding two readings together has no physical meaning.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Generic
from typing import Self
from typing import TypeVar
from typing import overload

from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import MeasurementError
from kuchka.internal.typing import override
from kuchka.quantities.base.linear import LinearQuantity
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import AffineUnitDef

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension

_DeltaT = TypeVar("_DeltaT", bound=LinearQuantity)
"""The `LinearQuantity` type representing a difference between two readings of a
particular `AffineQuantity`, e.g. `TemperatureDelta` for `Temperature`.

Bound to `LinearQuantity` because a delta is always an ordinary vector quantity --
"5 degrees warmer" adds and scales the same way a voltage does, even though the
`Temperature` reading it was derived from does not.
"""


class AffineQuantity(
    _OrderedScalarMixin, _ScalarStorage[AffineUnitDef], Generic[_DeltaT]
):
    """Base class for quantities that are a point on a scale, not a vector.

    Its units differ by both a scale and an offset (0 degC = 273.15 K for
    `Temperature`), unlike `LinearQuantity`, whose units differ only by scale.
    That makes a reading a point rather than a vector, and the available operations
    follow directly from that:

    * ``Point - Point`` produces a `_DeltaT` instance:
        "how much more is A than B" is a well-defined question.
    * ``Point + Delta`` produces another `Point`:
        shifting a reading by a tolerance band is a well-defined question too.
    * ``Point + Point`` has no called-for interpretation:
        there is no reading that "20 degC + 5 degC" should produce, so it is
        rejected -- and, because `__add__`'s parameter is typed as `_DeltaT` rather
        than `object` (the same reason `LinearQuantity.__add__` types its parameter
        as `Self`), this is rejected *statically* as well: `Celsius(20) +
        Celsius(5)` is a mypy/ty error, not only a runtime one.
    * Scaling a `Point` by a plain number is undefined, for the same reason "twice as
        hot" depends on which zero point is being measured from: no ``__mul__`` is
        implemented at all, so both ``Celsius(20) * 2`` and the reflected
        ``2 * Celsius(20)`` are ``TypeError`` at runtime and rejected by mypy/ty/
        pyright statically, with no extra code needed to enforce it.

    A concrete subclass (`Temperature`) is parametrized with its own delta type
    (``class Temperature(AffineQuantity[TemperatureDelta])``) and assigns two class
    attributes once, the same way a `LinearQuantity` subclass's owning unit module
    assigns `_canonical_unit`:

    - `_delta_type`: the same type passed as the generic parameter, repeated as a
      plain `ClassVar` so the runtime methods below can construct and `isinstance`-
      check against it -- the generic parameter itself is erased at runtime.
    - `_conversion_target_hint`: a short phrase naming what `.to(...)` expects,
      used only in the error message when it is given something that is not an
      `AffineUnitDef` at all.

    Unlike `LinearQuantity`'s `__mul__`/`__truediv__`, a concrete subclass does not
    need to restate `__add__`/`__sub__` with its own `@overload`s: generic parameter
    substitution alone gives `Temperature` the precise static signature it needs
    (`TemperatureDelta -> Temperature`, `Temperature -> TemperatureDelta`) purely by
    inheritance.
    """

    dimension: ClassVar[Dimension]
    _delta_type: ClassVar[type[LinearQuantity]]
    _conversion_target_hint: ClassVar[str] = "a matching affine unit"
    _unit_type: ClassVar[type] = AffineUnitDef
    __slots__ = ()

    def to(self, unit: AffineUnitDef) -> Self:
        """Return an equal reading that displays as ``unit``.

        This never changes the value being represented, only what ``repr()`` and
        ``value_in()`` return by default.
        """
        if not isinstance(unit, AffineUnitDef):
            msg = (
                f"conversion target must be {self._conversion_target_hint}, "
                f"got {unit!r}"
            )
            raise InvalidConversionError(msg)
        return type(self)(self._magnitude, unit)

    @override
    def value_in(self, unit: AffineUnitDef) -> Fraction:
        """Exact magnitude expressed in ``unit``."""
        return (self._magnitude - unit.offset) / unit.scale

    def __add__(self, other: _DeltaT) -> Self:
        # NOTE: `other` is typed as `_DeltaT`, not `object`, so `Celsius(20) +
        # Celsius(5)` is a *static* error (a `Temperature` is not a
        # `TemperatureDelta`) -- see the class docstring. The `isinstance` checks
        # below remain the authoritative runtime guard for values that arrive
        # dynamically typed, e.g. from an unchecked boundary or a suppressed type
        # error.
        if isinstance(other, AffineQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            msg = (
                f"Cannot add two `{type(self).__name__}` values: "
                f"`{type(self).__name__}` is a point on a scale, so two readings "
                f"don't sum to a third reading. Subtract one `{type(self).__name__}` "
                f"from another to get `{self._delta_type.__name__}`, or add "
                f"`{self._delta_type.__name__}` to `{type(self).__name__}` to shift "
                "the reading."
            )
            raise MeasurementError(msg)
        if isinstance(other, self._delta_type):
            return type(self)(self._magnitude + other.magnitude, self._display_unit)
        return NotImplemented

    def __radd__(self, other: _DeltaT) -> Self:
        return self.__add__(other)

    @overload
    def __sub__(self, other: Self) -> _DeltaT: ...
    @overload
    def __sub__(self, other: _DeltaT) -> Self: ...

    def __sub__(self, other: object) -> Self | LinearQuantity:
        """Subtract a `Point` to get a delta, or a delta to shift the reading."""
        if isinstance(other, AffineQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            delta_magnitude = self._magnitude - other._magnitude
            return self._delta_type(delta_magnitude, self._delta_type._canonical_unit)
        if isinstance(other, self._delta_type):
            return type(self)(self._magnitude - other.magnitude, self._display_unit)
        return NotImplemented

    # NOTE: Deliberately no __mul__ / __rmul__ / __truediv__ by a scalar:
    # see the class docstring for why scaling a point on a scale is left undefined
    # rather than implemented.


__all__ = ["AffineQuantity"]
