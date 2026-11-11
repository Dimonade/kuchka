"""Heating rate constructors: kelvin, Celsius, and Fahrenheit per time.

`HeatingRate` is the rate at which a temperature changes, and the kelvin per second
(`K/s`) is its canonical unit.
The module provides kelvin and degrees Celsius per second, minute, and hour, and
degrees Fahrenheit per second and minute, and a cooling rate is a negative heating
rate:

>>> from kuchka import CelsiusPerMinute
>>> from kuchka import KelvinPerSecond
>>> oven_ramp = CelsiusPerMinute(5)
>>> cooling = KelvinPerSecond(-0.2)

Wafer and thermal-cycler ramps are quoted in kelvin or degrees per second, laboratory
scans and ovens per minute, and kilns and annealing schedules per hour.

Examples
--------
An oven ramps at 5 °C/min from room temperature at 20 °C.
A heating rate times a time is a temperature difference, and a temperature plus that
difference is a temperature again:

>>> from kuchka import Celsius
>>> from kuchka import Minute
>>> rise = CelsiusPerMinute(5) * Minute(30)
>>> rise
150 ΔK
>>> Celsius(20) + rise
170 °C

A temperature difference over a heating rate is the time the heating takes:

>>> from kuchka import DeltaCelsius
>>> from kuchka.units import MINUTE
>>> (DeltaCelsius(100) / CelsiusPerMinute(5)).to(MINUTE)
20 min

Rates in different units add, and the sum displays in the unit of the first:

>>> CelsiusPerMinute(1) + KelvinPerSecond(1)
61 °C/min

An absolute temperature has no rate of its own, so it refuses to divide by a time, and
the rate of a temperature change is that of a temperature difference:

>>> Celsius(80) / Minute(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
TypeError: ...

Notes
-----
A heating rate is the rate of temperature change, so a degree Celsius per minute is
exactly a kelvin per minute, and a degree Fahrenheit per minute is exactly 5/9 of one.
Every scale is exact.

`HEATING_RATE_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
It accepts symbols such as ``"K/s"``, ``"°C/min"``, and ``"°F/min"``.

References
----------
BIPM, The International System of Units (SI Brochure), on the kelvin, the degree
Celsius, and temperature intervals:
https://www.bipm.org/en/publications/si-brochure

NIST, Guide for the Use of the International System of Units, Appendix B.8, factors
for units listed alphabetically:
https://www.nist.gov/node/777676

See Also
--------
~kuchka.quantities.Temperature
    The absolute temperature a heating rate moves.
~kuchka.quantities.TemperatureDelta
    A heating rate times a time is a temperature difference.
~kuchka.quantities.Time
    A temperature difference over a heating rate is the time it takes.

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
    """Construct a HeatingRate from a magnitude in kelvin per second.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in kelvin per second.

    Returns
    -------
    HeatingRate
        HeatingRate represented in kelvin per second.

    Examples
    --------
    A rapid thermal anneal ramps a silicon wafer at 10 K/s:

    >>> ramp = KelvinPerSecond(10)
    >>> ramp
    10 K/s

    From 25 °C to 1000 °C, the ramp takes a minute and a half:

    >>> from kuchka import DeltaCelsius
    >>> from kuchka.units import SECOND
    >>> (DeltaCelsius(975) / ramp).to(SECOND)
    97.5 s

    """
    return HeatingRate(to_exact(value) * KELVIN_PER_SECOND.scale, KELVIN_PER_SECOND)


def KelvinPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in kelvin per minute.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in kelvin per minute.

    Returns
    -------
    HeatingRate
        HeatingRate represented in kelvin per minute.

    Examples
    --------
    A differential scanning calorimeter heats a sample at 10 K/min:

    >>> scan = KelvinPerMinute(10)
    >>> scan
    10 K/min

    In kelvin per second, that is a sixth:

    >>> from kuchka.units import KELVIN_PER_SECOND
    >>> f"{scan.to(KELVIN_PER_SECOND):.3f}"
    '0.167 K/s'

    """
    return HeatingRate(to_exact(value) * KELVIN_PER_MINUTE.scale, KELVIN_PER_MINUTE)


def KelvinPerHour(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in kelvin per hour.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in kelvin per hour.

    Returns
    -------
    HeatingRate
        HeatingRate represented in kelvin per hour.

    Examples
    --------
    A precision glass blank is cooled at 2 K/h so that it keeps no stress:

    >>> cooling = KelvinPerHour(2)
    >>> cooling
    2 K/h

    Cooling from 480 K above room temperature down to it lasts ten days:

    >>> from kuchka import DeltaKelvin
    >>> from kuchka.units import HOUR
    >>> (DeltaKelvin(480) / cooling).to(HOUR)
    240 h

    """
    return HeatingRate(to_exact(value) * KELVIN_PER_HOUR.scale, KELVIN_PER_HOUR)


def CelsiusPerSecond(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per second.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in degrees Celsius per second.

    Returns
    -------
    HeatingRate
        HeatingRate represented in degrees Celsius per second.

    Examples
    --------
    A PCR thermal cycler ramps at 2.5 °C/s:

    >>> ramp = CelsiusPerSecond(2.5)
    >>> ramp
    2.5 °C/s

    Moving from the annealing step at 55 °C up to the denaturing step takes 16 s:

    >>> from kuchka import Celsius
    >>> from kuchka import Second
    >>> Celsius(55) + ramp * Second(16)
    95 °C

    """
    return HeatingRate(to_exact(value) * CELSIUS_PER_SECOND.scale, CELSIUS_PER_SECOND)


def CelsiusPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per minute.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in degrees Celsius per minute.

    Returns
    -------
    HeatingRate
        HeatingRate represented in degrees Celsius per minute.

    Examples
    --------
    A laboratory furnace is programmed to ramp at 5 °C/min:

    >>> preheat = CelsiusPerMinute(5)
    >>> preheat
    5 °C/min

    After half an hour from a 20 °C laboratory, it stands at:

    >>> from kuchka import Celsius
    >>> from kuchka import Minute
    >>> Celsius(20) + preheat * Minute(30)
    170 °C

    A degree Celsius per minute is exactly a kelvin per minute:

    >>> from kuchka import KelvinPerMinute
    >>> CelsiusPerMinute(1) == KelvinPerMinute(1)
    True

    """
    return HeatingRate(to_exact(value) * CELSIUS_PER_MINUTE.scale, CELSIUS_PER_MINUTE)


def CelsiusPerHour(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Celsius per hour.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in degrees Celsius per hour.

    Returns
    -------
    HeatingRate
        HeatingRate represented in degrees Celsius per hour.

    Examples
    --------
    A kiln fires a ceramic at 100 °C/h:

    >>> firing = CelsiusPerHour(100)
    >>> firing
    100 °C/h

    From 20 °C to 1000 °C, the climb takes almost ten hours:

    >>> from kuchka import DeltaCelsius
    >>> from kuchka.units import HOUR
    >>> (DeltaCelsius(980) / firing).to(HOUR)
    9.8 h

    """
    return HeatingRate(to_exact(value) * CELSIUS_PER_HOUR.scale, CELSIUS_PER_HOUR)


def FahrenheitPerSecond(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Fahrenheit per second.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in degrees Fahrenheit per second.

    Returns
    -------
    HeatingRate
        HeatingRate represented in degrees Fahrenheit per second.

    Examples
    --------
    A digital meat thermometer is specified to follow a change of 1 °F/s:

    >>> response = FahrenheitPerSecond(1)
    >>> response
    1 °F/s

    A degree Fahrenheit is exactly 5/9 of a kelvin, so the rate in SI units is:

    >>> from kuchka.units import KELVIN_PER_SECOND
    >>> f"{response.to(KELVIN_PER_SECOND):.3f}"
    '0.556 K/s'

    """
    return HeatingRate(
        to_exact(value) * FAHRENHEIT_PER_SECOND.scale, FAHRENHEIT_PER_SECOND
    )


def FahrenheitPerMinute(value: Numeric) -> HeatingRate:
    """Construct a HeatingRate from a magnitude in degrees Fahrenheit per minute.

    Parameters
    ----------
    value : Numeric
        Heating rate magnitude in degrees Fahrenheit per minute.

    Returns
    -------
    HeatingRate
        HeatingRate represented in degrees Fahrenheit per minute.

    Examples
    --------
    An oven preheats at 20 °F/min:

    >>> preheat = FahrenheitPerMinute(20)
    >>> preheat
    20 °F/min

    Fifteen minutes after starting at 70 °F, it reads:

    >>> from kuchka import Fahrenheit
    >>> from kuchka import Minute
    >>> Fahrenheit(70) + preheat * Minute(15)
    370 °F

    A rate of 9 °F/min is exactly 5 °C/min:

    >>> from kuchka import CelsiusPerMinute
    >>> FahrenheitPerMinute(9) == CelsiusPerMinute(5)
    True

    """
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
