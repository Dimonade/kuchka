"""The generic quantity engine, and the named engineering types built on it.

Ordinary users should not need to read this file.
It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
and ``TemperatureDelta`` do not each have to hand-roll their own arithmetic, conversion,
and comparison logic -- they share one implementation (:class:`LinearQuantity`)
and differ only in their :class:`~measurements.dimensions.Dimension`.

"Linear" here means: unit conversion within the quantity is a pure scale factor
(no offset).
Voltage, Current, Power, Resistance, and temperature *differences* are all linear
in this sense.
Absolute ``Temperature`` is not (20 degC + 5 degC is not a thing), so it lives in its
own module (``temperature.py``) with its own, deliberately smaller, set of operators.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import ClassVar, Self
from typing import overload
from typing import TypeVar

from kuchka.errors import InvalidMeasurementError
from kuchka.dimensions import CURRENT
from kuchka.dimensions import Dimension
from kuchka.dimensions import DIMENSIONLESS
from kuchka.dimensions import POWER
from kuchka.dimensions import RESISTANCE
from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.dimensions import VOLTAGE
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import UnrepresentableDimensionError
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal

_NUMERIC_TYPES = (int, float, Decimal, Fraction)

Q = TypeVar("Q", bound="LinearQuantity")


@dataclass(frozen=True, slots=True)
class UnitDef:
    """A named, purely multiplicative unit.

    This is internal machinery used by ``units.py`` and ``temperature.py`` to build unit
    constructors like ``Volt`` and ``Millivolt``.
    Ordinary users never construct a ``UnitDef`` themselves -- they import the
    constructor functions instead.

    This is not an offset unit.
    """

    name: str
    symbol: str
    scale: Decimal
    dimension: Dimension


class LinearQuantity:
    """Base class for physical quantities whose units differ by a pure scale.

    A ``LinearQuantity`` stores its magnitude in the quantity's canonical unit
    (volts for Voltage, amperes for Current, ...) plus the unit most recently asked to
    be see it in (``_display_unit``), purely for formatting.

    Arithmetic and equality always operate on the canonical magnitude,
    so the display unit never affects correctness -- only ``repr()``.
    """

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    _canonical_unit: ClassVar[UnitDef]

    _magnitude: Decimal
    _display_unit: UnitDef
    __slots__ = ("_display_unit", "_magnitude")

    def __init__(self, magnitude: Decimal, display_unit: UnitDef) -> None:
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

    def to(self: Self, unit: UnitDef) -> Self:
        """Return an equal measurement that displays as ``unit``.

        This never changes the value being represented -- ``Volt(1)`` and
        ``Volt(1).to(Millivolt_unit)`` compare equal.

        It only changes how ``repr()`` formats it and what `value_in` returns by
        default.
        """
        if not isinstance(unit, UnitDef):
            msg: str = (
                "conversion target must be a unit constructor's unit definition "
                f"(e.g. the one behind {self._canonical_unit.name.capitalize()}), "
                f"got {unit!r}"
            )
            raise InvalidConversionError(msg)
        if unit.dimension != self.dimension:
            msg: str = (
                f"cannot convert a {type(self).__name__} to {unit.name} "
                f"({unit.symbol}): that unit belongs to a different "
                f"physical dimension [{unit.dimension!r}], not "
                f"[{self.dimension!r}]"
            )
            raise InvalidConversionError(msg)
        return type(self)(self._magnitude, unit)

    def value_in(self, unit: UnitDef) -> Decimal:
        """Express the magnitude of this measurement expressed in ``unit``."""
        return self._magnitude / unit.scale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or self.dimension != other.dimension:
            return NotImplemented
        return self._magnitude == other._magnitude

    def __hash__(self) -> int:
        return hash((self.dimension, self._magnitude))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or self.dimension != other.dimension:
            action: str = "compare"
            raise IncompatibleDimensionError(action, self, other)
        return self._magnitude < other._magnitude

    def __le__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or self.dimension != other.dimension:
            action: str = "compare"
            raise IncompatibleDimensionError(action, self, other)
        return self._magnitude <= other._magnitude

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or self.dimension != other.dimension:
            action: str = "compare"
            raise IncompatibleDimensionError(action, self, other)
        return self._magnitude > other._magnitude

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, LinearQuantity) or self.dimension != other.dimension:
            action: str = "compare"
            raise IncompatibleDimensionError(action, self, other)
        return self._magnitude >= other._magnitude

    def __add__(self: Self, other: object) -> Self:
        if isinstance(other, LinearQuantity):
            if self.dimension != other.dimension:
                raise IncompatibleDimensionError("add", self, other)
            return type(self)(self._magnitude + other._magnitude, self._display_unit)
        if isinstance(other, _NUMERIC_TYPES):
            self._reject_naked_number("add", other)
        return NotImplemented

    def __radd__(self: Self, other: object) -> Self:
        return self.__add__(other)

    def __sub__(self: Self, other: object) -> Self:
        if isinstance(other, LinearQuantity):
            if self.dimension != other.dimension:
                raise IncompatibleDimensionError("subtract", self, other)
            return type(self)(self._magnitude - other._magnitude, self._display_unit)
        if isinstance(other, _NUMERIC_TYPES):
            self._reject_naked_number("subtract", other)
        return NotImplemented

    def _reject_naked_number(self, operation: str, other: object) -> None:

        unit_name = self._canonical_unit.name.capitalize()
        msg: str = (
            f"cannot {operation} a plain number ({other!r}) to a "
            f"{type(self).__name__}; wrap it in a unit constructor first, "
            f"e.g. {unit_name}({other!r})"
        )
        raise InvalidMeasurementError(msg)

    # NOTE ON TYPING: the return type here is intentionally broad
    # ("LinearQuantity | Decimal | NotImplementedType") because the *base*
    # implementation runs the fully general dimension algebra -- it has no
    # static way of knowing that a Voltage times a Current specifically
    # produces a Power.
    #
    # That precision is added on individual subclasses
    # (see the `@overload`-decorated methods on Voltage/Current/Power/
    # Resistance below) which narrow this signature for the specific pairs
    # this version supports, and delegate back to this method for the
    # actual runtime logic.
    #
    # This is deliberate: it is the "hand-written overload table" approach that allows
    # to develop the library step by step without being swamped.
    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension * other.dimension
            result_magnitude = self._magnitude * other._magnitude
            return _make(result_dimension, result_magnitude)
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude * to_decimal(other), self._display_unit)
        return NotImplemented

    def __rmul__(self: Self, other: object) -> Self:
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude * to_decimal(other), self._display_unit)
        return NotImplemented

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        if isinstance(other, LinearQuantity):
            result_dimension = self.dimension / other.dimension
            result_magnitude = self._magnitude / other._magnitude
            return _make(result_dimension, result_magnitude)
        if isinstance(other, _NUMERIC_TYPES):
            return type(self)(self._magnitude / to_decimal(other), self._display_unit)
        return NotImplemented

    def __neg__(self: Self) -> Self:
        return type(self)(-self._magnitude, self._display_unit)

    def __abs__(self: Self) -> Self:
        return type(self)(abs(self._magnitude), self._display_unit)

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"


class Voltage(LinearQuantity):
    dimension: ClassVar[Dimension] = VOLTAGE

    def __add__(self, other: Voltage) -> Voltage:
        return super().__add__(other)

    def __radd__(self, other: Voltage) -> Voltage:
        return super().__radd__(other)

    def __sub__(self, other: Voltage) -> Voltage:
        return super().__sub__(other)

    def __mul__(self, other: Current) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> Voltage: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Current) -> Resistance: ...
    @overload
    def __truediv__(self, other: Resistance) -> Current: ...
    @overload
    def __truediv__(self, other: Numeric) -> Voltage: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


class Current(LinearQuantity):
    dimension: ClassVar[Dimension] = CURRENT

    def __add__(self, other: Current) -> Current:
        return super().__add__(other)

    def __radd__(self, other: Current) -> Current:
        return super().__radd__(other)

    def __sub__(self, other: Current) -> Current:
        return super().__sub__(other)

    @overload
    def __mul__(self, other: Voltage) -> Power: ...
    @overload
    def __mul__(self, other: Resistance) -> Voltage: ...
    @overload
    def __mul__(self, other: Numeric) -> Current: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)


class Power(LinearQuantity):
    dimension: ClassVar[Dimension] = POWER

    def __add__(self, other: Power) -> Power:
        return super().__add__(other)

    def __radd__(self, other: Power) -> Power:
        return super().__radd__(other)

    def __sub__(self, other: Power) -> Power:
        return super().__sub__(other)

    @overload
    def __truediv__(self, other: Voltage) -> Current: ...
    @overload
    def __truediv__(self, other: Current) -> Voltage: ...
    @overload
    def __truediv__(self, other: Numeric) -> Power: ...

    def __truediv__(self, other: object) -> LinearQuantity | Decimal:
        return super().__truediv__(other)


class Resistance(LinearQuantity):
    dimension: ClassVar[Dimension] = RESISTANCE

    def __add__(self, other: Resistance) -> Resistance:
        return super().__add__(other)

    def __radd__(self, other: Resistance) -> Resistance:
        return super().__radd__(other)

    def __sub__(self, other: Resistance) -> Resistance:
        return super().__sub__(other)

    @overload
    def __mul__(self, other: Current) -> Voltage: ...
    @overload
    def __mul__(self, other: Numeric) -> Resistance: ...

    def __mul__(self, other: object) -> LinearQuantity | Decimal:
        return super().__mul__(other)


class TemperatureDelta(LinearQuantity):
    """A *difference* between two temperatures (e.g. a tolerance band).

    Unlike absolute ``Temperature`` (see ``temperature.py``), a delta is an
    ordinary linear quantity: two deltas can be added, a delta can be
    scaled by a plain number, and so on -- "the gap doubled" is physically
    meaningful in a way "the temperature doubled" is not.
    """

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA

    def __add__(self, other: TemperatureDelta) -> TemperatureDelta:
        return super().__add__(other)

    def __radd__(self, other: TemperatureDelta) -> TemperatureDelta:
        return super().__radd__(other)

    def __sub__(self, other: TemperatureDelta) -> TemperatureDelta:
        return super().__sub__(other)


"""Maps a dimension signature back to the named type that represents it.
`_make` uses this so that `Volt(5) * Ampere(2)` produces a real `Power`
instance, not a generic, un-typed quantity.
"""
_DIMENSION_REGISTRY: Dict[Dimension, Type[LinearQuantity]] = {
    VOLTAGE: Voltage,
    CURRENT: Current,
    POWER: Power,
    RESISTANCE: Resistance,
    TEMPERATURE_DELTA: TemperatureDelta,
}


def _make(dimension: Dimension, magnitude: Decimal) -> LinearQuantity | Decimal:
    """Build the correctly-typed result of a multiplication/division.

    A dimensionless result (e.g. Resistance / Resistance) is returned as a
    plain ``Decimal`` ratio, matching ordinary physics convention -- it is
    not a measurement of anything, so it should not pretend to be one.
    """
    if dimension == DIMENSIONLESS:
        return magnitude
    try:
        cls = _DIMENSION_REGISTRY[dimension]
    except KeyError:
        raise UnrepresentableDimensionError(dimension) from None
    return cls(magnitude, cls._canonical_unit)
