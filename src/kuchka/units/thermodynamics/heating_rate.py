"""Heating rate constructors: kelvin, Celsius, and Fahrenheit per time.

    from kuchka import CelsiusPerMinute
    from kuchka import KelvinPerSecond

    oven_ramp = CelsiusPerMinute(5)
    cooling = KelvinPerSecond(-0.2)

A heating rate is a rate of temperature *change*, so a degree Celsius per minute is
exactly a kelvin per minute and a degree Fahrenheit per minute exactly 5/9 of one.
Every scale is exact.

`HEATING_RATE_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import HEATING_RATE
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import HeatingRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_DEGREE_C = f"{symbols.DEGREE}C"
_DEGREE_F = f"{symbols.DEGREE}F"

KELVIN_PER_SECOND = UnitDef(
    "kelvin_per_second",
    "K/s",
    Decimal(1),
    HEATING_RATE,
    aliases=("K/sec",),
    words=("kelvins per second",),
)
KELVIN_PER_MINUTE = UnitDef(
    "kelvin_per_minute",
    "K/min",
    Fraction(1, 60),
    HEATING_RATE,
    words=("kelvins per minute",),
)
KELVIN_PER_HOUR = UnitDef(
    "kelvin_per_hour",
    "K/h",
    Fraction(1, 3600),
    HEATING_RATE,
    aliases=("K/hr",),
    words=("kelvins per hour",),
)
CELSIUS_PER_SECOND = UnitDef(
    "celsius_per_second",
    f"{_DEGREE_C}/s",
    Decimal(1),
    HEATING_RATE,
    aliases=("C/s", "degC/s", f"{_DEGREE_C}/sec"),
    words=("degrees C per second", "degrees celsius per second"),
)
CELSIUS_PER_MINUTE = UnitDef(
    "celsius_per_minute",
    f"{_DEGREE_C}/min",
    Fraction(1, 60),
    HEATING_RATE,
    aliases=("C/min", "degC/min"),
    words=("degrees C per minute", "degrees celsius per minute"),
)
CELSIUS_PER_HOUR = UnitDef(
    "celsius_per_hour",
    f"{_DEGREE_C}/h",
    Fraction(1, 3600),
    HEATING_RATE,
    aliases=("C/h", "degC/h", f"{_DEGREE_C}/hr"),
    words=("degrees C per hour", "degrees celsius per hour"),
)
FAHRENHEIT_PER_SECOND = UnitDef(
    "fahrenheit_per_second",
    f"{_DEGREE_F}/s",
    Fraction(5, 9),
    HEATING_RATE,
    aliases=("F/s", "degF/s", f"{_DEGREE_F}/sec"),
    words=("degrees F per second", "degrees fahrenheit per second"),
)
FAHRENHEIT_PER_MINUTE = UnitDef(
    "fahrenheit_per_minute",
    f"{_DEGREE_F}/min",
    Fraction(5, 9) / 60,
    HEATING_RATE,
    aliases=("F/min", "degF/min"),
    words=("degrees F per minute", "degrees fahrenheit per minute"),
)

HeatingRate._canonical_unit = KELVIN_PER_SECOND  # noqa: SLF001 -- this module owns HeatingRate's canonical unit


def KelvinPerSecond(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in kelvin per second."""
    return HeatingRate(to_exact(value) * KELVIN_PER_SECOND.scale, KELVIN_PER_SECOND)


def KelvinPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in kelvin per minute."""
    return HeatingRate(to_exact(value) * KELVIN_PER_MINUTE.scale, KELVIN_PER_MINUTE)


def KelvinPerHour(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in kelvin per hour."""
    return HeatingRate(to_exact(value) * KELVIN_PER_HOUR.scale, KELVIN_PER_HOUR)


def CelsiusPerSecond(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per second."""
    return HeatingRate(to_exact(value) * CELSIUS_PER_SECOND.scale, CELSIUS_PER_SECOND)


def CelsiusPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per minute."""
    return HeatingRate(to_exact(value) * CELSIUS_PER_MINUTE.scale, CELSIUS_PER_MINUTE)


def CelsiusPerHour(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per hour."""
    return HeatingRate(to_exact(value) * CELSIUS_PER_HOUR.scale, CELSIUS_PER_HOUR)


def FahrenheitPerSecond(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Fahrenheit per second."""
    return HeatingRate(
        to_exact(value) * FAHRENHEIT_PER_SECOND.scale, FAHRENHEIT_PER_SECOND
    )


def FahrenheitPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Fahrenheit per minute."""
    return HeatingRate(
        to_exact(value) * FAHRENHEIT_PER_MINUTE.scale, FAHRENHEIT_PER_MINUTE
    )


HEATING_RATE_UNITS: Mapping[str, Callable[[Numeric], HeatingRate]] = unit_table(
    "HEATING_RATE_UNITS",
    {
        KELVIN_PER_SECOND: KelvinPerSecond,
        KELVIN_PER_MINUTE: KelvinPerMinute,
        KELVIN_PER_HOUR: KelvinPerHour,
        CELSIUS_PER_SECOND: CelsiusPerSecond,
        CELSIUS_PER_MINUTE: CelsiusPerMinute,
        CELSIUS_PER_HOUR: CelsiusPerHour,
        FAHRENHEIT_PER_SECOND: FahrenheitPerSecond,
        FAHRENHEIT_PER_MINUTE: FahrenheitPerMinute,
    },
)

__all__ = [
    "CELSIUS_PER_HOUR",
    "CELSIUS_PER_MINUTE",
    "CELSIUS_PER_SECOND",
    "FAHRENHEIT_PER_MINUTE",
    "FAHRENHEIT_PER_SECOND",
    "HEATING_RATE_UNITS",
    "KELVIN_PER_HOUR",
    "KELVIN_PER_MINUTE",
    "KELVIN_PER_SECOND",
    "CelsiusPerHour",
    "CelsiusPerMinute",
    "CelsiusPerSecond",
    "FahrenheitPerMinute",
    "FahrenheitPerSecond",
    "KelvinPerHour",
    "KelvinPerMinute",
    "KelvinPerSecond",
]
