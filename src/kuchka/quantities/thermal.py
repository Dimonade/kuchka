"""TemperatureDelta and Temperature: linear and affine parts of thermal measurement.

A gap of N degrees can be added, subtracted, and scaled the same way a voltage or a
current can: "the gap doubled" is physically meaningful in a way "the temperature
doubled" is not.
That is what makes :class:`TemperatureDelta` an ordinary
:class:`~kuchka.quantities.base.LinearQuantity`, sitting alongside Voltage and Current,
while :class:`Temperature` is not.

Celsius and Kelvin differ by both a scale and an offset (0 degC = 273.15 K),
unlike Volt and Millivolt, which differ only by scale.
That makes absolute temperature a point on a scale rather than a vector, and the
available operations follow directly from that:

* ``Temperature - Temperature`` produces a ``TemperatureDelta``:
    "how much hotter is A than B" is a well-defined question.
* ``Temperature + TemperatureDelta`` produces a ``Temperature``:
    shifting a reading by a tolerance band is a well-defined question too.
* ``Temperature + Temperature`` has no called-for interpretation:
    there is no physical reading that "20 degC + 5 degC" should produce --
    so it raises :class:`~kuchka.errors.MeasurementError` with an explanation instead
    of guessing.
* Scaling a ``Temperature`` by a plain number is undefined:
    for the same reason "twice as hot" depends on which zero point is being measured
    from.
    No ``__mul__`` is implemented at all, so both ``Temperature(20) * 2`` and the
    reflected ``2 * Temperature(20)`` are ``TypeError`` at runtime and rejected by
    mypy/ty/pyright statically, with no extra code needed to enforce it.

This module treats Celsius and Kelvin identically:
both construct the same ``Temperature`` type, and neither supports scalar
multiplication, even though "2 x 300 K" has a defensible thermodynamic reading that
"2 x 20 degC" does not.
Giving Kelvin its own multiplicable type would be a reasonable extension for a use case
built around thermodynamic scaling, but it is out of scope for the device-engineering
vocabulary this library currently targets.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType
from typing import ClassVar
from typing import overload
from typing import TYPE_CHECKING

from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.errors import InvalidConversionError
from kuchka.errors import MeasurementError
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register
from kuchka.quantities.base import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from kuchka.dimensions import Dimension


class TemperatureDelta(LinearQuantity):
    """A difference between two temperatures, e.g. a tolerance band."""

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA


register(TEMPERATURE_DELTA, TemperatureDelta)

DELTA_KELVIN = UnitDef("kelvin_delta", "\u0394K", Decimal(1), TEMPERATURE_DELTA)
"""A one-degree change is the same size in Celsius and Kelvin.

Only the absolute zero point differs, and a delta has no zero point.
"""
DELTA_CELSIUS = UnitDef("celsius_delta", "\u0394\u00b0C", Decimal(1), TEMPERATURE_DELTA)

TemperatureDelta._canonical_unit = DELTA_KELVIN  # noqa: SLF001 -- this module owns TemperatureDelta's canonical unit


def DeltaKelvin(value: Numeric) -> TemperatureDelta:
    """Construct a TemperatureDelta from a magnitude expressed in Kelvin."""
    return TemperatureDelta(to_decimal(value) * DELTA_KELVIN.scale, DELTA_KELVIN)


def DeltaCelsius(value: Numeric) -> TemperatureDelta:
    """Construct a TemperatureDelta from a magnitude expressed in degrees Celsius."""
    return TemperatureDelta(to_decimal(value) * DELTA_CELSIUS.scale, DELTA_CELSIUS)


TEMPERATURE_DELTA_UNITS: Mapping[str, Callable[[Numeric], TemperatureDelta]] = (
    MappingProxyType(
        {
            "dK": DeltaKelvin,
            "dC": DeltaCelsius,
        }
    )
)


@dataclass(frozen=True, slots=True)
class AffineUnitDef:
    """A unit with both a scale and an offset, e.g. Celsius relative to Kelvin."""

    name: str
    symbol: str
    scale: Decimal
    offset: Decimal


KELVIN = AffineUnitDef("kelvin", "K", Decimal(1), Decimal(0))
CELSIUS = AffineUnitDef("celsius", "\u00b0C", Decimal(1), Decimal("273.15"))


class Temperature:
    """An absolute thermodynamic temperature reading.

    Supports the operations that are physically meaningful for a point on an affine
    scale:
    comparison, subtracting another ``Temperature`` to get a ``TemperatureDelta``,
    and shifting by a ``TemperatureDelta``.

    See the module docstring for the operations this deliberately omits, and why.
    """

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA

    # These annotations are what let mypy --strict see through __slots__.
    _kelvin: Decimal
    _display_unit: AffineUnitDef
    __slots__ = ("_display_unit", "_kelvin")

    def __init__(self, kelvin: Decimal, display_unit: AffineUnitDef) -> None:
        """Store a magnitude already expressed in Kelvin, plus its display unit."""
        object.__setattr__(self, "_kelvin", kelvin)
        object.__setattr__(self, "_display_unit", display_unit)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def kelvin(self) -> Decimal:
        """The magnitude expressed in Kelvin, this type's canonical unit."""
        return self._kelvin

    @property
    def unit(self) -> AffineUnitDef:
        """The unit this measurement currently displays as."""
        return self._display_unit

    def to(self, unit: AffineUnitDef) -> Temperature:
        """Return an equal reading that displays as ``unit``.

        This never changes the value being represented, only what ``repr()`` and
        ``value_in()`` return by default.
        """
        if not isinstance(unit, AffineUnitDef):
            msg = (
                "conversion target must be a temperature unit such as "
                f"Kelvin or Celsius, got {unit!r}"
            )
            raise InvalidConversionError(msg)
        return Temperature(self._kelvin, unit)

    def value_in(self, unit: AffineUnitDef) -> Decimal:
        """Return the magnitude of this reading expressed in ``unit``."""
        return (self._kelvin - unit.offset) / unit.scale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin == other._kelvin

    def __hash__(self) -> int:
        return hash(("Temperature", self._kelvin))

    def __lt__(self, other: Temperature) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin < other._kelvin

    def __le__(self, other: Temperature) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin <= other._kelvin

    def __gt__(self, other: Temperature) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin > other._kelvin

    def __ge__(self, other: Temperature) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._kelvin >= other._kelvin

    def __add__(self, other: TemperatureDelta) -> Temperature:
        # The static signature only admits TemperatureDelta, so
        # `Celsius(20) + Celsius(5)` is a mypy error, matching how other units, and
        # TemperatureDelta itself all reject cross-type addition statically
        # (see quantities/base.py).
        #
        # The isinstance check for a second Temperature stays in the body as a runtime
        # guard for values that arrive from somewhere mypy never saw, e.g. an untyped
        # boundary or an upstream `Any`.
        if isinstance(other, Temperature):
            msg = (
                "Cannot add two Temperature values: an absolute temperature "
                "is a point on a scale, so 'hot + hot' has no physical "
                "reading. Use (a - b) to get a TemperatureDelta, or add a "
                "TemperatureDelta to a Temperature instead."
            )
            raise MeasurementError(msg)
        if isinstance(other, TemperatureDelta):
            return Temperature(self._kelvin + other.magnitude, self._display_unit)
        return NotImplemented

    __radd__ = __add__

    @overload
    def __sub__(self, other: Temperature) -> TemperatureDelta: ...
    @overload
    def __sub__(self, other: TemperatureDelta) -> Temperature: ...

    def __sub__(self, other: object) -> Temperature | TemperatureDelta:
        """Subtract a Temperature to get a delta, or a delta to shift the reading."""
        if isinstance(other, Temperature):
            return TemperatureDelta(self._kelvin - other._kelvin, DELTA_KELVIN)
        if isinstance(other, TemperatureDelta):
            return Temperature(self._kelvin - other.magnitude, self._display_unit)
        return NotImplemented

    # Deliberately no __mul__ / __rmul__ / __truediv__ by a scalar: see the module
    # docstring for why scaling an absolute temperature is left undefined rather than
    # implemented.

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"


def Kelvin(value: Numeric) -> Temperature:
    """Construct a Temperature from a magnitude expressed in Kelvin."""
    raw = to_decimal(value)
    return Temperature(raw * KELVIN.scale + KELVIN.offset, KELVIN)


def Celsius(value: Numeric) -> Temperature:
    """Construct a Temperature from a magnitude expressed in degrees Celsius."""
    raw = to_decimal(value)
    return Temperature(raw * CELSIUS.scale + CELSIUS.offset, CELSIUS)


TEMPERATURE_UNITS: Mapping[str, Callable[[Numeric], Temperature]] = MappingProxyType(
    {
        "K": Kelvin,
        "C": Celsius,
    }
)
