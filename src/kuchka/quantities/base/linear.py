"""LinearQuantity: the base for every physical quantity whose units differ by scale.

``LinearQuantity`` means unit conversion within the quantity is a pure scale factor,
with no offset: ``2 * Volt(1) == Volt(2)``.
``Voltage``, ``Current``, ``Power``, ``Resistance``, ``TemperatureDelta``, ``Time``,
``Frequency``, and ``Length`` all subclass it, differing only in their
:class:`~kuchka.dimensions.Dimension` and in the handful of ``@overload`` signatures
that give multiplication and division a precise static type.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import Dimension
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import Numeric
from kuchka.numeric import exact_quotient
from kuchka.numeric import to_exact
from kuchka.quantities.base.ordering import _OrderedScalarMixin
from kuchka.quantities.base.registry import _DIMENSION_REGISTRY
from kuchka.quantities.base.registry import _promote
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.quantities.base.units import UnitDef

if TYPE_CHECKING:
    from fractions import Fraction


class LinearQuantity(_OrderedScalarMixin, _ScalarStorage[UnitDef]):
    """Base class for physical quantities whose units differ by a pure scale.

    Stores its magnitude in the quantity's canonical unit (volts for Voltage,
    amperes for Current, ...) plus the unit most recently asked to be seen in
    (``_display_unit``), which affects only ``repr()``.

    Arithmetic and equality always operate on the canonical magnitude, so the display
    unit never affects correctness.
    """

    dimension: ClassVar[Dimension]
    _canonical_unit: ClassVar[UnitDef]
    _unit_type: ClassVar[type] = UnitDef
    __slots__ = ()

    @property
    def magnitude(self) -> Fraction:
        """Magnitude in this quantity's canonical unit."""
        return self._magnitude

    def to(self, unit: UnitDef) -> Self:
        """Return an equal measurement that displays as ``unit``.

        This never changes the value being represented: ``Volt(1)`` and
        ``Volt(1).to(MILLIVOLT)`` compare equal. It only changes what
        ``repr()`` and ``value_in()`` return by default.
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
        self._reject_foreign_unit(unit)
        return type(self)(self._magnitude, unit)

    @override
    def value_in(self, unit: UnitDef) -> Fraction:
        """Exact magnitude expressed in ``unit``."""
        return self._magnitude / unit.scale

    def __add__(self, other: Self) -> Self:
        # NOTE: `other` is typed as `Self` instead of an `object` so that
        # `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both rejected by type checkers,
        # not just at runtime.
        #
        # Because this method is inherited as-is (no subclass overrides it), `Self`
        # binds to whichever quantity type it is actually called on, e.g. Voltage for
        # `Voltage.__add__`.
        # The isinstance checks below remain the authoritative guard for values that
        # reach this call dynamically typed, e.g. from an unchecked boundary or a
        # suppressed type error.
        #
        # The runtime guard compares `type(self) is type(other)` and not
        # `self.dimension != other.dimension`:
        # two different types can share a dimension (`Frequency` and `BaudRate` are
        # both T^-1), and adding across that boundary is exactly the mistake this check
        # exists to catch, even though the dimensions agree.
        if isinstance(other, LinearQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            return type(self)(self._magnitude + other._magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, LinearQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            return type(self)(self._magnitude - other._magnitude, self._display_unit)
        if isinstance(other, Numeric):
            self._reject_naked_number("subtract", other)
        return NotImplemented

    def is_close(self, other: Self, *, tolerance: Self) -> bool:
        """Return whether `other` is within `tolerance` of `self`, inclusive.

        The comparison is exact, and the tolerance is a quantity of the same type with
        no default: what counts as close is always written down by the caller.
        Closeness is not transitive: `a` can be close to `b`, and `b` to `c`, while
        `a` is not close to `c`.
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

    # NOTE ON TYPING: the return type here is intentionally broad
    # (`LinearQuantity | Fraction`) because this base implementation runs the fully
    # general dimension algebra -- it has no static way of knowing that a Voltage times
    # a Current specifically produces a Power.
    #
    # That precision is added by the `@overload`-decorated methods on
    # Voltage/Current/Power/Resistance, which narrow this signature for the specific
    # pairs this version supports, and delegate back to this method for the actual
    # runtime logic.
    #
    # Each subclass overload list ends with a fallback overload matching this exact
    # signature (`other: object -> LinearQuantity | Fraction`) so that overriding it
    # remains compatible with this base signature.
    def __mul__(self, other: object) -> LinearQuantity | Fraction:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension * other.dimension
            result_magnitude = self._magnitude * other._magnitude
            return _promote(result_dimension, result_magnitude)
        if isinstance(other, Numeric):
            return type(self)(self._magnitude * to_exact(other), self._display_unit)
        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        if isinstance(other, Numeric):
            return type(self)(self._magnitude * to_exact(other), self._display_unit)
        return NotImplemented

    def __truediv__(self, other: object) -> LinearQuantity | Fraction:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension / other.dimension
            result_magnitude = exact_quotient(
                self._magnitude, other._magnitude, left=self, right=other
            )
            return _promote(result_dimension, result_magnitude)
        if isinstance(other, Numeric):
            magnitude = exact_quotient(
                self._magnitude, to_exact(other), left=self, right=other
            )
            return type(self)(magnitude, self._display_unit)
        return NotImplemented

    def __rtruediv__(self, other: object) -> LinearQuantity | Fraction:
        # NOTE: `Numeric / self`, e.g. `1 / Time(2)`.
        # This only derives an answer through the shared dimension registry when
        # `self`'s own type is the *canonical* one for its dimension (the guard below).
        # That guard matters the moment two types share a dimension:
        # `SamplingPeriod` and `Time` are both T^1, so a naive `1 / self._magnitude`
        # promoted through `_promote` would always hand back a `Time` --
        # the registered T^-1 owner -- even when `self` was a `SamplingPeriod`,
        # silently mislabelling a sample rate as a generic frequency.
        #
        # Non-canonical types are expected to override this method themselves if they
        # have a specific, well-defined reciprocal (see `SamplingPeriod`/`SampleRate`,
        # or to have none at all if they do not (see `BaudRate`, whose reciprocal is
        # not a modelled concept).
        if isinstance(other, Numeric):
            if _DIMENSION_REGISTRY.get(self.dimension) is not type(self):
                return NotImplemented
            result_dimension = DIMENSIONLESS / self.dimension
            result_magnitude = exact_quotient(
                to_exact(other), self._magnitude, left=other, right=self
            )
            return _promote(result_dimension, result_magnitude)
        return NotImplemented

    def __neg__(self) -> Self:
        return type(self)(-self._magnitude, self._display_unit)

    def __abs__(self) -> Self:
        return type(self)(abs(self._magnitude), self._display_unit)


__all__ = ["LinearQuantity"]
