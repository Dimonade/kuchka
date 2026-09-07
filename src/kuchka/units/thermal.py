"""Unit constructors for TemperatureDelta and Temperature.

    from kuchka import Kelvin, Celsius, DeltaCelsius

    reading = Celsius(20)
    tolerance = DeltaCelsius(5)

Temperature behaves differently when compared to other modules:
- neither family goes through `prefixed_unit`, as temperature deltas have no
    SI-prefixed variants in this vocabulary, and
- absolute temperature's Celsius/Kelvin relationship is an offset, not a scale, which
    `AffineUnitDef` models directly.

`TEMPERATURE_DELTA_UNITS` and `TEMPERATURE_UNITS` map a symbol to its constructor,
for boundary code that reads a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities.base import UnitDef
from kuchka.quantities.thermal import AffineUnitDef
from kuchka.quantities.thermal import Temperature
from kuchka.quantities.thermal import TemperatureDelta

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

from kuchka.dimensions import TEMPERATURE_DELTA

DELTA_KELVIN = UnitDef("kelvin_delta", "\u0394K", Decimal(1), TEMPERATURE_DELTA)
"""A one-degree temperature change.

It is the same size in Celsius and Kelvin:
only the absolute zero point differs, and a delta has no zero point.
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
    MappingProxyType({"dK": DeltaKelvin, "dC": DeltaCelsius})
)

KELVIN = AffineUnitDef("kelvin", "K", Decimal(1), Decimal(0))
CELSIUS = AffineUnitDef("celsius", "\u00b0C", Decimal(1), Decimal("273.15"))


def Kelvin(value: Numeric) -> Temperature:
    """Construct a Temperature from a magnitude expressed in Kelvin."""
    raw = to_decimal(value)
    return Temperature(raw * KELVIN.scale + KELVIN.offset, KELVIN)


def Celsius(value: Numeric) -> Temperature:
    """Construct a Temperature from a magnitude expressed in degrees Celsius."""
    raw = to_decimal(value)
    return Temperature(raw * CELSIUS.scale + CELSIUS.offset, CELSIUS)


TEMPERATURE_UNITS: Mapping[str, Callable[[Numeric], Temperature]] = MappingProxyType(
    {"K": Kelvin, "C": Celsius}
)

__all__ = [
    "CELSIUS",
    "DELTA_CELSIUS",
    "DELTA_KELVIN",
    "KELVIN",
    "TEMPERATURE_DELTA_UNITS",
    "TEMPERATURE_UNITS",
    "Celsius",
    "DeltaCelsius",
    "DeltaKelvin",
    "Kelvin",
]
