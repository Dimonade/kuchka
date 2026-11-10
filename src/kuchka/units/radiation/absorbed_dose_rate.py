"""Absorbed dose rate constructors: grays and rads per second, minute, and hour.

    from kuchka import GrayPerMinute, MicrograyPerHour

    field = MicrograyPerHour(0.09)
    beam = GrayPerMinute(2)

`AbsorbedDoseRate` is the absorbed dose delivered per unit time, a role of
`SpecificPower`.
Its canonical unit is the gray per second (`Gy/s`), exactly one watt per kilogram, and
its arithmetic results display in the gray per hour.
The module provides the gray per second, minute, and hour with the multiples
instruments and radiotherapy use, and the rad per hour.

Examples
--------
An environmental gamma dose rate of 90 nGy/h, in microgray per hour:

>>> NanograyPerHour(90).to(MICROGRAY_PER_HOUR)
0.09 µGy/h

A dose rate times a time is an absorbed dose:

>>> from kuchka import Hour
>>> from kuchka.units import NANOGRAY
>>> (MicrograyPerHour(0.09) * Hour(8)).to(NANOGRAY)
720 nGy

`ABSORBED_DOSE_RATE_UNITS` maps symbols such as ``"Gy/s"``, ``"uGy/h"``, and
``"cGy/min"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import AbsorbedDoseRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

GRAY_PER_SECOND = UnitDef(
    "gray_per_second",
    "Gy/s",
    Fraction(1, 1),
    SPECIFIC_POWER,
    words=("grays per second",),
)
MILLIGRAY_PER_SECOND = UnitDef(
    "milligray_per_second",
    "mGy/s",
    Fraction(1, 1000),
    SPECIFIC_POWER,
    words=("milligrays per second",),
)
GRAY_PER_MINUTE = UnitDef(
    "gray_per_minute",
    "Gy/min",
    Fraction(1, 60),
    SPECIFIC_POWER,
    words=("grays per minute",),
)
CENTIGRAY_PER_MINUTE = UnitDef(
    "centigray_per_minute",
    "cGy/min",
    Fraction(1, 6000),
    SPECIFIC_POWER,
    words=("centigrays per minute",),
)
GRAY_PER_HOUR = UnitDef(
    "gray_per_hour",
    "Gy/h",
    Fraction(1, 3600),
    SPECIFIC_POWER,
    aliases=("Gy/hr",),
    words=("grays per hour",),
)
MILLIGRAY_PER_HOUR = UnitDef(
    "milligray_per_hour",
    "mGy/h",
    Fraction(1, 3600000),
    SPECIFIC_POWER,
    aliases=("mGy/hr",),
    words=("milligrays per hour",),
)
MICROGRAY_PER_HOUR = UnitDef(
    "microgray_per_hour",
    "µGy/h",
    Fraction(1, 3600000000),
    SPECIFIC_POWER,
    aliases=("µGy/hr", "uGy/h", "uGy/hr"),
    words=("micrograys per hour",),
)
NANOGRAY_PER_HOUR = UnitDef(
    "nanogray_per_hour",
    "nGy/h",
    Fraction(1, 3600000000000),
    SPECIFIC_POWER,
    aliases=("nGy/hr",),
    words=("nanograys per hour",),
)
RAD_PER_HOUR = UnitDef(
    "rad_per_hour",
    "rad/h",
    Fraction(1, 360000),
    SPECIFIC_POWER,
    aliases=("rad/hr",),
    words=("rads per hour",),
)
MILLIRAD_PER_HOUR = UnitDef(
    "millirad_per_hour",
    "mrad/h",
    Fraction(1, 360000000),
    SPECIFIC_POWER,
    aliases=("mrad/hr",),
    words=("millirads per hour",),
)

AbsorbedDoseRate._canonical_unit = GRAY_PER_SECOND  # noqa: SLF001 -- this module owns AbsorbedDoseRate's canonical unit
AbsorbedDoseRate._result_unit = GRAY_PER_HOUR  # noqa: SLF001 -- and the unit its arithmetic results display in


def GrayPerSecond(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per second.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per second.

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_SECOND.scale, GRAY_PER_SECOND)


def MilligrayPerSecond(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in milligrays per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in milligrays per second.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in milligrays per second.

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIGRAY_PER_SECOND.scale, MILLIGRAY_PER_SECOND
    )


def GrayPerMinute(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per minute.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per minute.

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_MINUTE.scale, GRAY_PER_MINUTE)


def CentigrayPerMinute(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in centigrays per minute.

    Parameters
    ----------
    value : Numeric
        Magnitude in centigrays per minute.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in centigrays per minute.

    """
    return AbsorbedDoseRate(
        to_exact(value) * CENTIGRAY_PER_MINUTE.scale, CENTIGRAY_PER_MINUTE
    )


def GrayPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in grays per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in grays per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in grays per hour.

    """
    return AbsorbedDoseRate(to_exact(value) * GRAY_PER_HOUR.scale, GRAY_PER_HOUR)


def MilligrayPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in milligrays per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in milligrays per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in milligrays per hour.

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIGRAY_PER_HOUR.scale, MILLIGRAY_PER_HOUR
    )


def MicrograyPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in micrograys per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in micrograys per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in micrograys per hour.

    """
    return AbsorbedDoseRate(
        to_exact(value) * MICROGRAY_PER_HOUR.scale, MICROGRAY_PER_HOUR
    )


def NanograyPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in nanograys per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanograys per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in nanograys per hour.

    """
    return AbsorbedDoseRate(
        to_exact(value) * NANOGRAY_PER_HOUR.scale, NANOGRAY_PER_HOUR
    )


def RadPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in rads per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in rads per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in rads per hour.

    """
    return AbsorbedDoseRate(to_exact(value) * RAD_PER_HOUR.scale, RAD_PER_HOUR)


def MilliradPerHour(value: Numeric) -> AbsorbedDoseRate:
    """Construct an AbsorbedDoseRate from a magnitude in millirads per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in millirads per hour.

    Returns
    -------
    AbsorbedDoseRate
        AbsorbedDoseRate represented in millirads per hour.

    """
    return AbsorbedDoseRate(
        to_exact(value) * MILLIRAD_PER_HOUR.scale, MILLIRAD_PER_HOUR
    )


ABSORBED_DOSE_RATE_UNITS: Mapping[str, Callable[[Numeric], AbsorbedDoseRate]] = (
    unit_table(
        "ABSORBED_DOSE_RATE_UNITS",
        {
            GRAY_PER_SECOND: GrayPerSecond,
            MILLIGRAY_PER_SECOND: MilligrayPerSecond,
            GRAY_PER_MINUTE: GrayPerMinute,
            CENTIGRAY_PER_MINUTE: CentigrayPerMinute,
            GRAY_PER_HOUR: GrayPerHour,
            MILLIGRAY_PER_HOUR: MilligrayPerHour,
            MICROGRAY_PER_HOUR: MicrograyPerHour,
            NANOGRAY_PER_HOUR: NanograyPerHour,
            RAD_PER_HOUR: RadPerHour,
            MILLIRAD_PER_HOUR: MilliradPerHour,
        },
    )
)

__all__ = [
    "ABSORBED_DOSE_RATE_UNITS",
    "CENTIGRAY_PER_MINUTE",
    "GRAY_PER_HOUR",
    "GRAY_PER_MINUTE",
    "GRAY_PER_SECOND",
    "MICROGRAY_PER_HOUR",
    "MILLIGRAY_PER_HOUR",
    "MILLIGRAY_PER_SECOND",
    "MILLIRAD_PER_HOUR",
    "NANOGRAY_PER_HOUR",
    "RAD_PER_HOUR",
    "CentigrayPerMinute",
    "GrayPerHour",
    "GrayPerMinute",
    "GrayPerSecond",
    "MicrograyPerHour",
    "MilligrayPerHour",
    "MilligrayPerSecond",
    "MilliradPerHour",
    "NanograyPerHour",
    "RadPerHour",
]
