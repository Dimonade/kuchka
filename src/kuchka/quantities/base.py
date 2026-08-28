"""The generic quantity engine shared by every linear physical quantity.

``LinearQuantity`` implements arithmetic, conversion, comparison, and
dimensional-mismatch detection exactly once.
``Voltage``, ``Current``, ``Power``, ``Resistance``, ``TemperatureDelta``,
``Time``, ``Frequency``, and ``Length`` (see ``electrical.py``,
``thermal.py``, ``temporal.py``, and ``length.py``) each subclass it and
differ only in their :class:`~kuchka.dimensions.Dimension` and in the
handful of ``@overload`` signatures that give multiplication and division
a precise static type.

"Linear" means unit conversion within the quantity is a pure scale factor,
with no offset: ``2 * Volt(1) == Volt(2)``.
Absolute temperature is not linear in this sense (``2 * Celsius(1)`` is not a
meaningful statement), so it lives in its own, smaller class in
``temperature.py`` instead of here.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import ClassVar
from typing import Self

from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import Dimension
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.numeric import to_decimal

_NUMERIC_TYPES = (int, float, Decimal, Fraction)

"""Maps a dimension signature back to the named type that represents it, so
that e.g. ``Volt(5) * Ampere(2)`` produces a real ``Power`` instance
instead of a generic, untyped quantity.

Each quantity module populates this via ``register`` as a side effect of being
imported, which is what lets new quantity types be added without this module
knowing about them in advance.

LOAD-BEARING RULE: at most one type may ever be registered per dimension,
and it must always be the general SI/physics name for that dimension
(``Voltage`` for M L^2 T^-3 I^-1, ``Frequency`` for T^-1, and so on),
never a domain-specific vocabulary type.

This matters once more than one type can share a dimension:
``SampleRate`` and ``BaudRate`` are both T^-1, the same as ``Frequency``,
but neither of them registers.
They stay reachable only by explicit construction, exactly like
``Temperature`` -- ``register`` enforces this by refusing a second type
for a dimension that already has one, rather than silently overwriting it.
"""
_DIMENSION_REGISTRY: dict[Dimension, type[LinearQuantity]] = {}

"""Maps a dimension signature to the name of a quantity this library
intends to implement but does not yet, e.g. Length / Time -> Velocity.

Lets `_promote` raise `PlannedDimensionError` for a dimension this
library already has a name for, naming the result (e.g. "corresponds to
Velocity") instead of only printing its exponent vector. Curated by
hand, the same way the `@overload` tables are: adding an entry here
improves the error message, and is a marker for what to implement next.
"""
_PLANNED_DIMENSIONS: dict[Dimension, str] = {
    Dimension(length=1, time=-1): "Velocity",
}


def register(dimension: Dimension, quantity_type: type[LinearQuantity]) -> None:
    """Associate a dimension signature with the type that represents it.

    Called once per quantity type, at import time, by the module that
    defines that type. Application code never needs to call this
    directly. Raises `TypeError` if another type already claimed this
    dimension: this is a defect in kuchka's own quantity modules, not
    something a caller of the public API can trigger, so it is not part
    of the `MeasurementError` hierarchy that application code handles.
    """
    existing = _DIMENSION_REGISTRY.get(dimension)
    if existing is not None and existing is not quantity_type:
        msg = (
            f"dimension {dimension!r} is already registered to "
            f"{existing.__name__}; only one type per dimension may be the "
            f"canonical, arithmetic-derived type for it (see the note "
            f"above `_DIMENSION_REGISTRY`). {quantity_type.__name__} "
            f"should stay unregistered and reachable only by explicit "
            f"construction, the way `SampleRate` and `Temperature` are."
        )
        raise TypeError(msg)
    _DIMENSION_REGISTRY[dimension] = quantity_type


class UnitDef:
    """A named, purely multiplicative unit, e.g. the ``mV`` behind ``Millivolt``.

    This is internal machinery used by ``units/`` and ``temperature.py`` to
    build unit constructors like ``Volt`` and ``Millivolt``.

    Application code never constructs a ``UnitDef`` directly;
    it imports the constructor functions instead.
    """

    __slots__ = ("dimension", "name", "scale", "symbol")

    def __init__(
        self,
        name: str,
        symbol: str,
        scale: Decimal,
        dimension: Dimension,
    ) -> None:
        """Store the unit's display name, symbol, scale factor, and dimension."""
        self.name = name
        self.symbol = symbol
        self.scale = scale
        self.dimension = dimension

    def __repr__(self) -> str:
        return f"UnitDef({self.name!r}, {self.symbol!r})"


class LinearQuantity:
    """Base class for physical quantities whose units differ by a pure scale.

    Stores its magnitude in the quantity's canonical unit (volts for
    Voltage, amperes for Current, ...) plus the unit most recently asked to
    be seen in (``_display_unit``), which affects only ``repr()``.
    Arithmetic and equality always operate on the canonical magnitude, so
    the display unit never affects correctness.
    """

    dimension: ClassVar[Dimension]
    _canonical_unit: ClassVar[UnitDef]

    _magnitude: Decimal
    _display_unit: UnitDef
    __slots__ = ("_display_unit", "_magnitude")

    def __init__(self, magnitude: Decimal, display_unit: UnitDef) -> None:
        """Store a magnitude in the canonical unit, plus a unit to display it as."""
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def magnitude(self) -> Decimal:
        """The magnitude expressed in this quantity's canonical unit."""
        return self._magnitude

    @property
    def unit(self) -> UnitDef:
        """The unit this measurement currently displays as."""
        return self._display_unit

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
        return type(self)(self._magnitude, unit)

    def value_in(self, unit: UnitDef) -> Decimal:
        """Return the magnitude of this measurement expressed in ``unit``."""
        return self._magnitude / unit.scale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or type(self) is not type(other):
            return NotImplemented
        return self._magnitude == other._magnitude

    def __hash__(self) -> int:
        return hash((type(self), self._magnitude))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude < other._magnitude

    def __le__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude <= other._magnitude

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude > other._magnitude

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or type(self) is not type(other):
            raise IncompatibleDimensionError("compare", self, other)
        return self._magnitude >= other._magnitude

    def __add__(self, other: Self) -> Self:
        # `other` is typed as `Self` rather than `object` so that
        # `Volt(5) + Ampere(2)` and `Volt(5) + 4.2` are both rejected by
        # mypy/pyright, not just at runtime. Because this method is
        # inherited as-is (no subclass overrides it), `Self` binds to
        # whichever quantity type it is actually called on, e.g. Voltage
        # for `Voltage.__add__`. The isinstance checks below remain the
        # authoritative guard for values that reach this call dynamically
        # typed, e.g. from an unchecked boundary or a suppressed type error.
        #
        # The runtime guard compares `type(self) is type(other)` rather
        # than `self.dimension != other.dimension`: two different types
        # can share a dimension (`Frequency` and `BaudRate` are both
        # T^-1), and adding across that boundary is exactly the mistake
        # this check exists to catch, even though the dimensions agree.
        if isinstance(other, LinearQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("add", self, other)
            return type(self)(self._magnitude + other._magnitude, self._display_unit)
        if isinstance(other, _NUMERIC_TYPES):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self, other: Self) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self) -> Self:
        if isinstance(other, LinearQuantity):
            if type(self) is not type(other):
                raise IncompatibleDimensionError("subtract", self, other)
            return type(self)(self._magnitude - other._magnitude, self._display_unit)
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

    # NOTE ON TYPING: the return type here is intentionally broad
    # (`LinearQuantity | Decimal`) because this base implementation runs
    # the fully general dimension algebra -- it has no static way of
    # knowing that a Voltage times a Current specifically produces a
    # Power. That precision is added by the `@overload`-decorated methods
    # on Voltage/Current/Power/Resistance (see `electrical.py`), which
    # narrow this signature for the specific pairs this version supports,
    # and delegate back to this method for the actual runtime logic.
    #
    # Each subclass overload list ends with a fallback overload matching
    # this exact signature (`other: object -> LinearQuantity | Decimal`)
    # so that overriding it remains compatible with this base signature.
    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension * other.dimension
            result_magnitude = self._magnitude * other._magnitude
            return _promote(result_dimension, result_magnitude)
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude * to_decimal(other), self._display_unit)
        return NotImplemented

    def __rmul__(self, other: object) -> Self:
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude * to_decimal(other), self._display_unit)
        return NotImplemented

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension / other.dimension
            result_magnitude = self._magnitude / other._magnitude
            return _promote(result_dimension, result_magnitude)
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude / to_decimal(other), self._display_unit)
        return NotImplemented

    def __rtruediv__(self, other: object) -> LinearQuantity | Decimal:
        # `Numeric / self`, e.g. `1 / Time(2)`. This only derives an
        # answer through the shared dimension registry when `self`'s own
        # type is the *canonical* one for its dimension (the guard
        # below). That guard matters the moment two types share a
        # dimension: `SamplingPeriod` and `Time` are both T^1, so a naive
        # `1 / self._magnitude` promoted through `_promote` would always
        # hand back a `Time` -- the registered T^-1 owner -- even when
        # `self` was a `SamplingPeriod`, silently mislabelling a sample
        # rate as a generic frequency. Non-canonical types are expected to
        # override this method themselves if they have a specific,
        # well-defined reciprocal (see `SamplingPeriod`/`SampleRate` in
        # `temporal.py`), or to have none at all if they do not (see
        # `BaudRate`, whose reciprocal is not a modelled concept).
        if isinstance(other, _NUMERIC_TYPES):
            if _DIMENSION_REGISTRY.get(self.dimension) is not type(self):
                return NotImplemented
            result_dimension = DIMENSIONLESS / self.dimension
            result_magnitude = to_decimal(other) / self._magnitude
            return _promote(result_dimension, result_magnitude)
        return NotImplemented

    def __neg__(self) -> Self:
        return type(self)(-self._magnitude, self._display_unit)

    def __abs__(self) -> Self:
        return type(self)(abs(self._magnitude), self._display_unit)

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"


def _promote(dimension: Dimension, magnitude: Decimal) -> LinearQuantity | Decimal:
    """Build the correctly-typed result of a multiplication or division.

    A dimensionless result (e.g. Resistance / Resistance) is returned as a
    plain ``Decimal`` ratio, matching ordinary physics convention: it is
    not a measurement of anything, so it should not pretend to be one.
    """
    if dimension == DIMENSIONLESS:
        return magnitude
    try:
        quantity_type = _DIMENSION_REGISTRY[dimension]
    except KeyError:
        planned_name = _PLANNED_DIMENSIONS.get(dimension)
        if planned_name is not None:
            raise PlannedDimensionError(dimension, planned_name) from None
        raise UnrepresentableDimensionError(dimension) from None
    return quantity_type(magnitude, quantity_type._canonical_unit)  # noqa: SLF001 -- accessing the registered type's own canonical unit, not a foreign instance's internals
