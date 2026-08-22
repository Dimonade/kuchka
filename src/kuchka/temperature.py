"""Temperature: the one quantity in v0.1.0 that isn't purely linear.

Celsius and Kelvin are not just different scale factors on the same axis
the way Volt and Millivolt are -- they also differ by an *offset*
(0 degC = 273.15 K).
That makes absolute temperature an *affine* quantity, not a vector one,
and the arithmetic has to reflect that:

* ``Temperature - Temperature`` is meaningful (it's a *difference*: "how
  much hotter is A than B") and produces a :class:`~measurements.quantities.TemperatureDelta`.
* ``Temperature + Temperature`` is **not** meaningful -- there is no
  physical sense in which "20 degC + 5 degC" is a temperature -- so it is
  rejected with an explanatory error rather than silently computing 25 degC
  or 25 K or anything else.
* ``Temperature * <number>`` is likewise not defined. "Twice as hot" is not
  a coherent statement for an affine scale (it depends on which zero point
  you measure from), so multiplication is simply not implemented. Because
  neither ``Temperature`` nor ``int``/``float`` defines the operation,
  Python raises ``TypeError`` on its own, and mypy/pyright reject the
  expression at the type level for the same reason -- no extra code is
  needed to "ban" it, only the absence of a method.

For the *difference* type, none of this applies: a gap of 5 degrees is a
perfectly ordinary linear quantity, so ``TemperatureDelta`` is just another
``LinearQuantity`` (see ``quantities.py``) and behaves exactly like
Voltage or Current -- deltas can be added, subtracted, scaled, compared.

Design note on Kelvin specifically: physically, "2 x 300 K" has a
respectable meaning in some thermodynamic contexts (Kelvin is a true ratio
scale), while "2 x 20 degC" does not.
This version deliberately does not special-case Kelvin to allow that --
both ``Celsius`` and ``Kelvin`` produce the same ``Temperature`` type,
uniformly disallowing multiplication.
Splitting Kelvin into its own multiplicable type would reopen the
"one class per unit" problem the whole design tries to avoid,
for a use case (thermodynamic scaling) outside this library's stated scope
(electrical/optical/medical device engineering).
If that turns out to be needed later, the extension point is a distinct
ratio-scale type for Kelvin specifically -- not a special case bolted onto
``Temperature``.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar
from typing import overload

from kuchka.dimensions import Dimension
from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.errors import InvalidConversionError
from kuchka.errors import MeasurementError
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import TemperatureDelta
from kuchka.quantities import UnitDef

DELTA_KELVIN = UnitDef("kelvin_delta", "\u0394K", Decimal(1), TEMPERATURE_DELTA)
# A one-degree change is the same size in Celsius and Kelvin -- only the
# absolute zero point differs, and a delta has no zero point.
DELTA_CELSIUS = UnitDef("celsius_delta", "\u0394\u00b0C", Decimal(1), TEMPERATURE_DELTA)

TemperatureDelta._canonical_unit = DELTA_KELVIN


def DeltaKelvin(value: Numeric) -> TemperatureDelta:
    return TemperatureDelta(to_decimal(value) * DELTA_KELVIN.scale, DELTA_KELVIN)


def DeltaCelsius(value: Numeric) -> TemperatureDelta:
    return TemperatureDelta(to_decimal(value) * DELTA_CELSIUS.scale, DELTA_CELSIUS)


@dataclass(frozen=True, slots=True)
class AffineUnitDef:
    """A unit with both a scale and an offset (e.g. Celsius relative to Kelvin)."""

    name: str
    symbol: str
    scale: Decimal
    offset: Decimal


KELVIN = AffineUnitDef("kelvin", "K", Decimal(1), Decimal(0))
CELSIUS = AffineUnitDef("celsius", "\u00b0C", Decimal(1), Decimal("273.15"))


class Temperature:
    """An absolute thermodynamic temperature reading.

    See the module docstring for why this is not a :class:`LinearQuantity`
    subclass: absolute temperature is a point on a scale, not a vector, and
    supports a deliberately smaller set of operations as a result.
    """

    dimension: ClassVar[Dimension] = TEMPERATURE_DELTA

    # See the identical note in quantities.py: these annotations are what
    # let mypy --strict see through __slots__ at all.
    _kelvin: Decimal
    _display_unit: AffineUnitDef
    __slots__ = ("_display_unit", "_kelvin")

    def __init__(self, kelvin: Decimal, display_unit: AffineUnitDef) -> None:
        object.__setattr__(self, "_kelvin", kelvin)
        object.__setattr__(self, "_display_unit", display_unit)

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @property
    def kelvin(self) -> Decimal:
        """The magnitude expressed in Kelvin (this type's canonical unit)."""
        return self._kelvin

    @property
    def unit(self) -> AffineUnitDef:
        return self._display_unit

    def to(self, unit: AffineUnitDef) -> Temperature:
        if not isinstance(unit, AffineUnitDef):
            raise InvalidConversionError(
                "conversion target must be a temperature unit such as "
                f"Kelvin or Celsius, got {unit!r}"
            )
        return Temperature(self._kelvin, unit)

    def value_in(self, unit: AffineUnitDef) -> Decimal:
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

    # arithmetic: point +/- delta -> point; point - point -> delta.
    #
    # The static signature only admits TemperatureDelta -- that's the only
    # operation that's ever legal here, so `Celsius(20) + Celsius(5)` is
    # now a mypy error, not just a runtime one, matching how Voltage,
    # Current, Power, Resistance, and TemperatureDelta itself all reject
    # cross-type addition statically (see quantities.py).
    # The isinstance check for a second Temperature stays in the body regardless, as a
    # runtime guard for values that arrive from somewhere mypy never saw
    # (an untyped boundary, an `Any`, a `# type: ignore` upstream) --
    # exactly the acquisition-boundary problem the whole library exists
    # to contain.
    def __add__(self, other: TemperatureDelta) -> Temperature:
        if isinstance(other, Temperature):
            raise MeasurementError(
                "Cannot add two Temperature values: an absolute temperature "
                "is a point on a scale, not a vector, so 'hot + hot' has no "
                "physical meaning. Use (a - b) to get a TemperatureDelta, "
                "or add a TemperatureDelta to a Temperature instead."
            )
        if isinstance(other, TemperatureDelta):
            return Temperature(self._kelvin + other.magnitude, self._display_unit)
        return NotImplemented

    __radd__ = __add__

    @overload
    def __sub__(self, other: Temperature) -> TemperatureDelta: ...
    @overload
    def __sub__(self, other: TemperatureDelta) -> Temperature: ...

    def __sub__(self, other: object) -> Temperature | TemperatureDelta:
        if isinstance(other, Temperature):
            return TemperatureDelta(self._kelvin - other._kelvin, DELTA_KELVIN)
        if isinstance(other, TemperatureDelta):
            return Temperature(self._kelvin - other.magnitude, self._display_unit)
        return NotImplemented

    # Deliberately no __mul__ / __rmul__ / __truediv__ by a scalar here --
    # see the module docstring.
    #
    # Leaving them undefined means both `Temperature(20) * 2` and
    # `2 * Temperature(20)` raise TypeError from Python itself,
    # and mypy reject the expression because Temperature has no such operator
    # to type-check against.

    def __repr__(self) -> str:
        value = self.value_in(self._display_unit)
        return f"{format(value, 'f')} {self._display_unit.symbol}"


def Kelvin(value: Numeric) -> Temperature:
    raw = to_decimal(value)
    return Temperature(raw * KELVIN.scale + KELVIN.offset, KELVIN)


def Celsius(value: Numeric) -> Temperature:
    raw = to_decimal(value)
    return Temperature(raw * CELSIUS.scale + CELSIUS.offset, CELSIUS)
