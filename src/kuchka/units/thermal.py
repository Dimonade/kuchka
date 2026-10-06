"""Temperature quantities and constructors for Kelvin, Celsius, and Fahrenheit.

`Temperature` represents a thermodynamic temperature reading, a point on a scale.
`TemperatureDelta` represents a difference between two readings.
The kelvin is the canonical SI unit for both.

Kelvin, Celsius, and Fahrenheit readings are all the same `Temperature` type.
Their units differ by a scale and an offset, which `AffineUnitDef` models directly.
Temperature differences have no zero point, so `DeltaKelvin`, `DeltaCelsius`, and
`DeltaFahrenheit` differ by scale only.

Every conversion in this module is exact.
A Fahrenheit degree is exactly 5/9 of a kelvin, and 0 °F is exactly 459.67 x 5/9 K.
A reading such as `Fahrenheit(98.6)` therefore equals `Celsius(37)` with no rounding.

Examples
--------
Water freezes at 0 °C, which is exactly 32 °F and exactly 273.15 K:

>>> freezing = Celsius(0)
>>> freezing == Fahrenheit(32)
True
>>> freezing == Kelvin(273.15)
True

A reading displays in the unit it was constructed with:

>>> Fahrenheit(68)
68 °F

`.to()` changes the display unit and keeps the value:

>>> Celsius(100).to(FAHRENHEIT)
212 °F

The two scales meet at -40:

>>> Fahrenheit(-40) == Celsius(-40)
True

Normal human body temperature, 98.6 °F, is 37 °C:

>>> Fahrenheit(98.6) == Celsius(37)
True

Absolute zero is the same point on every scale:

>>> Fahrenheit(-459.67) == Kelvin(0)
True

Subtracting two readings gives a `TemperatureDelta`.
A difference of 9 °F is a difference of 5 °C:

>>> Fahrenheit(77) - Fahrenheit(68) == DeltaFahrenheit(9)
True
>>> DeltaFahrenheit(9) == DeltaCelsius(5)
True

Adding a delta to a reading shifts it, and the reading keeps its display unit:

>>> Fahrenheit(68) + DeltaFahrenheit(9)
77 °F
>>> Fahrenheit(32) + DeltaCelsius(5)
41 °F

Notes
-----
Adding two readings or scaling a reading by a plain number has no physical meaning,
so `Temperature` defines neither.
A delta supports both.

A reading below absolute zero (0 K, -273.15 °C, -459.67 °F) raises
`InvalidMeasurementError`.

`TEMPERATURE_UNITS` maps the symbols ``"K"``, ``"C"``, and ``"F"`` to their
constructors, and `TEMPERATURE_DELTA_UNITS` maps ``"dK"``, ``"dC"``, and ``"dF"``.
This is intended for boundary code that receives units as external data, such as
configuration files.

See Also
--------
~kuchka.quantities.Temperature
    A point on a temperature scale.
~kuchka.quantities.TemperatureDelta
    A difference between two temperature readings.

"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import TEMPERATURE_DELTA
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AffineUnitDef
from kuchka.quantities import Temperature
from kuchka.quantities import TemperatureDelta
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


def _degree_words(letter: str, name: str) -> tuple[str, ...]:
    """Spoken forms of a temperature scale: `degC`, `degrees C`, `degree Celsius`.

    Words are compared ignoring case, so one lower-case form of each is enough.
    """
    letter = letter.lower()
    return (
        f"{symbols.DEGREE}{letter}",
        f"deg{letter}",
        f"deg {letter}",
        f"degree {letter}",
        f"degrees {letter}",
        f"degree {name}",
        f"degrees {name}",
    )


def _delta_words(
    letter: str, name: str, scale_words: tuple[str, ...]
) -> tuple[str, ...]:
    """Spoken forms of a temperature change: `delta C`, `delta degrees Celsius`."""
    forms = (letter.lower(), name, *scale_words)
    return (f"delta{letter.lower()}", *(f"delta {form}" for form in forms))


_CELSIUS_WORDS = (*_degree_words("C", "celsius"), "celsius", "centigrade")
_FAHRENHEIT_WORDS = _degree_words("F", "fahrenheit")
_KELVIN_WORDS = _degree_words("K", "kelvin")

DELTA_KELVIN = UnitDef(
    "kelvin_delta",
    f"{symbols.DELTA}K",
    Decimal(1),
    TEMPERATURE_DELTA,
    aliases=("dK", "deltaK"),
    words=_delta_words("K", "kelvin", _KELVIN_WORDS),
)
"""A one-degree temperature change.

It is the same size in Celsius and Kelvin:
only the absolute zero point differs, and a delta has no zero point.
"""
DELTA_CELSIUS = UnitDef(
    "celsius_delta",
    f"{symbols.DELTA}{symbols.DEGREE}C",
    Decimal(1),
    TEMPERATURE_DELTA,
    aliases=("dC", f"{symbols.DELTA}C", "deltaC"),
    words=_delta_words("C", "celsius", _CELSIUS_WORDS),
)

DELTA_FAHRENHEIT = UnitDef(
    "fahrenheit_delta",
    f"{symbols.DELTA}{symbols.DEGREE}F",
    Fraction(5, 9),
    TEMPERATURE_DELTA,
    aliases=("dF", f"{symbols.DELTA}F", "deltaF"),
    words=_delta_words("F", "fahrenheit", _FAHRENHEIT_WORDS),
)
"""A one-degree Fahrenheit temperature change, exactly 5/9 of a kelvin."""

TemperatureDelta._canonical_unit = DELTA_KELVIN  # noqa: SLF001 -- this module owns TemperatureDelta's canonical unit


def DeltaKelvin(value: Numeric) -> TemperatureDelta:
    """Construct a temperature difference from a magnitude expressed in kelvin.

    Parameters
    ----------
    value : Numeric
        Temperature difference in kelvin.

    Returns
    -------
    TemperatureDelta
        Temperature difference represented in kelvin.

    Examples
    --------
    A thermal chamber holding its setpoint within 0.5 K:

    >>> tolerance = DeltaKelvin(0.5)
    >>> tolerance
    0.5 ΔK

    A difference is the same size in kelvin and degrees Celsius:

    >>> DeltaKelvin(5) == DeltaCelsius(5)
    True

    """
    return TemperatureDelta(to_exact(value) * DELTA_KELVIN.scale, DELTA_KELVIN)


def DeltaCelsius(value: Numeric) -> TemperatureDelta:
    """Construct a temperature difference from a magnitude expressed in degrees Celsius.

    Parameters
    ----------
    value : Numeric
        Temperature difference in degrees Celsius.

    Returns
    -------
    TemperatureDelta
        Temperature difference represented in degrees Celsius.

    Examples
    --------
    An oven that overshoots its setpoint by 5 °C:

    >>> overshoot = DeltaCelsius(5)
    >>> overshoot
    5 Δ°C

    A delta shifts a reading:

    >>> Celsius(20) + overshoot
    25 °C

    """
    return TemperatureDelta(to_exact(value) * DELTA_CELSIUS.scale, DELTA_CELSIUS)


def DeltaFahrenheit(value: Numeric) -> TemperatureDelta:
    """Construct a temperature difference from a magnitude in degrees Fahrenheit.

    Parameters
    ----------
    value : Numeric
        Temperature difference in degrees Fahrenheit.

    Returns
    -------
    TemperatureDelta
        Temperature difference represented in degrees Fahrenheit.

    Notes
    -----
    One Fahrenheit degree of difference is exactly 5/9 of a kelvin.

    Examples
    --------
    A drop of 9 °F over an evening is a drop of 5 °C:

    >>> evening_drop = DeltaFahrenheit(9)
    >>> evening_drop == DeltaCelsius(5)
    True

    """
    return TemperatureDelta(to_exact(value) * DELTA_FAHRENHEIT.scale, DELTA_FAHRENHEIT)


TEMPERATURE_DELTA_UNITS: Mapping[str, Callable[[Numeric], TemperatureDelta]] = (
    unit_table(
        "TEMPERATURE_DELTA_UNITS",
        {
            DELTA_KELVIN: DeltaKelvin,
            DELTA_CELSIUS: DeltaCelsius,
            DELTA_FAHRENHEIT: DeltaFahrenheit,
        },
    )
)

KELVIN = AffineUnitDef(
    "kelvin",
    "K",
    Decimal(1),
    Decimal(0),
    aliases=(f"{symbols.DEGREE}K",),
    words=_KELVIN_WORDS,
)
"""Kelvin, the canonical temperature unit."""
CELSIUS = AffineUnitDef(
    "celsius",
    f"{symbols.DEGREE}C",
    Decimal(1),
    Decimal("273.15"),
    aliases=("C", f"{symbols.DEGREE} C"),
    words=_CELSIUS_WORDS,
)
"""Degrees Celsius: one degree is 1 K, and 0 °C is 273.15 K."""
FAHRENHEIT = AffineUnitDef(
    "fahrenheit",
    f"{symbols.DEGREE}F",
    Fraction(5, 9),
    Fraction(45967, 100) * Fraction(5, 9),
    aliases=("F", f"{symbols.DEGREE} F"),
    words=_FAHRENHEIT_WORDS,
)
"""Degrees Fahrenheit: one degree is 5/9 K, and 0 degF is 459.67 x 5/9 K."""


Temperature._canonical_unit = KELVIN  # noqa: SLF001 -- this module owns Temperature's canonical unit


def Kelvin(value: Numeric) -> Temperature:
    """Construct a temperature reading from a magnitude expressed in kelvin.

    Parameters
    ----------
    value : Numeric
        Temperature in kelvin, at or above absolute zero (0 K).

    Returns
    -------
    Temperature
        Temperature represented in kelvin.

    Examples
    --------
    Liquid nitrogen boils at about 77 K:

    >>> nitrogen_boiling = Kelvin(77)
    >>> nitrogen_boiling
    77 K

    The cosmic microwave background sits near 2.7 K:

    >>> background = Kelvin(2.7)
    >>> background < nitrogen_boiling
    True

    """
    return Temperature(to_exact(value) * KELVIN.scale + KELVIN.offset, KELVIN)


def Celsius(value: Numeric) -> Temperature:
    """Construct a temperature reading from a magnitude expressed in degrees Celsius.

    Parameters
    ----------
    value : Numeric
        Temperature in degrees Celsius, at or above absolute zero (-273.15 °C).

    Returns
    -------
    Temperature
        Temperature represented in degrees Celsius.

    Notes
    -----
    0 °C is exactly 273.15 K.

    Examples
    --------
    A comfortable room temperature:

    >>> room = Celsius(20)
    >>> room
    20 °C

    The offset from kelvin is exact:

    >>> room == Kelvin(293.15)
    True

    """
    return Temperature(to_exact(value) * CELSIUS.scale + CELSIUS.offset, CELSIUS)


def Fahrenheit(value: Numeric) -> Temperature:
    """Construct a temperature reading from a magnitude expressed in degrees Fahrenheit.

    Parameters
    ----------
    value : Numeric
        Temperature in degrees Fahrenheit, at or above absolute zero (-459.67 °F).

    Returns
    -------
    Temperature
        Temperature represented in degrees Fahrenheit.

    Notes
    -----
    One Fahrenheit degree is exactly 5/9 of a kelvin, and 0 °F is exactly
    459.67 x 5/9 K.

    Examples
    --------
    A US weather forecast of 68 °F:

    >>> forecast = Fahrenheit(68)
    >>> forecast
    68 °F

    The same reading in degrees Celsius:

    >>> forecast.to(CELSIUS)
    20 °C

    Water boils at 212 °F at standard atmospheric pressure:

    >>> Fahrenheit(212) == Celsius(100)
    True

    """
    return Temperature(
        to_exact(value) * FAHRENHEIT.scale + FAHRENHEIT.offset, FAHRENHEIT
    )


TEMPERATURE_UNITS: Mapping[str, Callable[[Numeric], Temperature]] = unit_table(
    "TEMPERATURE_UNITS",
    {
        KELVIN: Kelvin,
        CELSIUS: Celsius,
        FAHRENHEIT: Fahrenheit,
    },
)

__all__ = [
    "CELSIUS",
    "DELTA_CELSIUS",
    "DELTA_FAHRENHEIT",
    "DELTA_KELVIN",
    "FAHRENHEIT",
    "KELVIN",
    "TEMPERATURE_DELTA_UNITS",
    "TEMPERATURE_UNITS",
    "Celsius",
    "DeltaCelsius",
    "DeltaFahrenheit",
    "DeltaKelvin",
    "Fahrenheit",
    "Kelvin",
]
