"""Unit constructors for exposure rate: roentgens per second, minute, and hour.

    from kuchka import MilliroentgenPerHour, RoentgenPerHour

    reading = MilliroentgenPerHour(2.5)
    field = RoentgenPerHour(0.1)

`ExposureRate` is the exposure delivered per unit time, a role of `SpecificCurrent`,
and the reading of a survey meter calibrated in roentgens.
Its canonical unit is the ampere per kilogram (`A/kg`), shared with `SpecificCurrent`,
and its arithmetic results display in the roentgen per hour.
`ExposureRate.from_specific_current(AmperePerKilogram(...))` builds one in the SI
unit, and `EXPOSURE_RATE_UNITS["A/kg"]` reads it from text.

Examples
--------
A survey reading of 2.5 mR/h, in microroentgens per hour:

>>> MilliroentgenPerHour(2.5).to(MICROROENTGEN_PER_HOUR)
2500 µR/h

A reading times a time is an exposure:

>>> from kuchka import Hour
>>> from kuchka.units.radiation.exposure import MILLIROENTGEN
>>> (MilliroentgenPerHour(2.5) * Hour(2)).to(MILLIROENTGEN)
5 mR

`EXPOSURE_RATE_UNITS` maps symbols such as ``"R/h"``, ``"mR/h"``, ``"uR/h"``, and
``"A/kg"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ExposureRate
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.specific_current import AMPERE_PER_KILOGRAM
from kuchka.units.electromagnetics.specific_current import AmperePerKilogram

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

ROENTGEN_PER_SECOND = UnitDef(
    "roentgen_per_second",
    "R/s",
    Fraction(129, 500000),
    SPECIFIC_CURRENT,
    words=("roentgens per second",),
)
ROENTGEN_PER_MINUTE = UnitDef(
    "roentgen_per_minute",
    "R/min",
    Fraction(43, 10000000),
    SPECIFIC_CURRENT,
    words=("roentgens per minute",),
)
ROENTGEN_PER_HOUR = UnitDef(
    "roentgen_per_hour",
    "R/h",
    Fraction(43, 600000000),
    SPECIFIC_CURRENT,
    aliases=("R/hr",),
    words=("roentgens per hour",),
)
MILLIROENTGEN_PER_HOUR = UnitDef(
    "milliroentgen_per_hour",
    "mR/h",
    Fraction(43, 600000000000),
    SPECIFIC_CURRENT,
    aliases=("mR/hr",),
    words=("milliroentgens per hour",),
)
MICROROENTGEN_PER_HOUR = UnitDef(
    "microroentgen_per_hour",
    "µR/h",
    Fraction(43, 600000000000000),
    SPECIFIC_CURRENT,
    aliases=("µR/hr", "uR/h", "uR/hr"),
    words=("microroentgens per hour",),
)

ExposureRate._canonical_unit = AMPERE_PER_KILOGRAM  # noqa: SLF001 -- this module owns ExposureRate's canonical unit
ExposureRate._result_unit = ROENTGEN_PER_HOUR  # noqa: SLF001 -- and the unit its arithmetic results display in


def _ampere_per_kilogram(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in amperes per kilogram."""
    return ExposureRate.from_specific_current(AmperePerKilogram(value))


def RoentgenPerSecond(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in roentgens per second.

    Returns
    -------
    ExposureRate
        ExposureRate represented in roentgens per second.

    """
    return ExposureRate(
        to_exact(value) * ROENTGEN_PER_SECOND.scale, ROENTGEN_PER_SECOND
    )


def RoentgenPerMinute(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in roentgens per minute.

    Returns
    -------
    ExposureRate
        ExposureRate represented in roentgens per minute.

    """
    return ExposureRate(
        to_exact(value) * ROENTGEN_PER_MINUTE.scale, ROENTGEN_PER_MINUTE
    )


def RoentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in roentgens per hour.

    Returns
    -------
    ExposureRate
        ExposureRate represented in roentgens per hour.

    """
    return ExposureRate(to_exact(value) * ROENTGEN_PER_HOUR.scale, ROENTGEN_PER_HOUR)


def MilliroentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in milliroentgens per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliroentgens per hour.

    Returns
    -------
    ExposureRate
        ExposureRate represented in milliroentgens per hour.

    """
    return ExposureRate(
        to_exact(value) * MILLIROENTGEN_PER_HOUR.scale, MILLIROENTGEN_PER_HOUR
    )


def MicroroentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in microroentgens per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in microroentgens per hour.

    Returns
    -------
    ExposureRate
        ExposureRate represented in microroentgens per hour.

    """
    return ExposureRate(
        to_exact(value) * MICROROENTGEN_PER_HOUR.scale, MICROROENTGEN_PER_HOUR
    )


EXPOSURE_RATE_UNITS: Mapping[str, Callable[[Numeric], ExposureRate]] = unit_table(
    "EXPOSURE_RATE_UNITS",
    {
        AMPERE_PER_KILOGRAM: _ampere_per_kilogram,
        ROENTGEN_PER_SECOND: RoentgenPerSecond,
        ROENTGEN_PER_MINUTE: RoentgenPerMinute,
        ROENTGEN_PER_HOUR: RoentgenPerHour,
        MILLIROENTGEN_PER_HOUR: MilliroentgenPerHour,
        MICROROENTGEN_PER_HOUR: MicroroentgenPerHour,
    },
)

__all__ = [
    "EXPOSURE_RATE_UNITS",
    "MICROROENTGEN_PER_HOUR",
    "MILLIROENTGEN_PER_HOUR",
    "ROENTGEN_PER_HOUR",
    "ROENTGEN_PER_MINUTE",
    "ROENTGEN_PER_SECOND",
    "MicroroentgenPerHour",
    "MilliroentgenPerHour",
    "RoentgenPerHour",
    "RoentgenPerMinute",
    "RoentgenPerSecond",
]
