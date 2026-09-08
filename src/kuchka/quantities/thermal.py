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

from decimal import Decimal
from typing import ClassVar
from typing import overload
from typing import TYPE_CHECKING

from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.errors import InvalidConversionError
from kuchka.errors import MeasurementError
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import register

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class TemperatureDelta(LinearQuantity):
    """A difference between two temperatures, e.g. a tolerance band."""

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA


register(TEMPERATURE_DELTA, TemperatureDelta)


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

    def __getstate__(self) -> tuple[Decimal, AffineUnitDef]:
        """Return the pickle/copy state. See `LinearQuantity.__getstate__`."""
        return (self._kelvin, self._display_unit)

    def __setstate__(self, state: tuple[Decimal, AffineUnitDef]) -> None:
        """Restore a pickled/copied instance without going through `__setattr__`."""
        kelvin, display_unit = state
        object.__setattr__(self, "_kelvin", kelvin)
        object.__setattr__(self, "_display_unit", display_unit)

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
        # NOTE: The static signature only admits TemperatureDelta, so
        # `Celsius(20) + Celsius(5)` is a mypy error, matching how other units, and
        # TemperatureDelta itself all reject cross-type addition statically.
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
            return TemperatureDelta(
                self._kelvin - other._kelvin,
                TemperatureDelta._canonical_unit,
            )
        if isinstance(other, TemperatureDelta):
            return Temperature(self._kelvin - other.magnitude, self._display_unit)
        return NotImplemented

    # NOTE: Deliberately no __mul__ / __rmul__ / __truediv__ by a scalar:
    # see the module docstring for why scaling an absolute temperature is left
    # undefined rather than implemented.

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"

    def __format__(self, format_spec: str) -> str:
        """Format the reading in the display unit. See `LinearQuantity.__format__`."""
        if not format_spec:
            return repr(self)
        value = self.value_in(self._display_unit)
        return f"{format(value, format_spec)} {self._display_unit.symbol}"


__all__ = ["Temperature", "TemperatureDelta"]
