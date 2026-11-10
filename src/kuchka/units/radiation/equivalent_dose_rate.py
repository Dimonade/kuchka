"""Equivalent dose rate constructors: sieverts and rems per second and per hour.

    from kuchka import MicrosievertPerHour, SievertPerHour

    reading = MicrosievertPerHour(0.12)
    limit = SievertPerHour(1)

`EquivalentDoseRate` is the equivalent dose delivered per unit time, a role of
`SpecificPower`, and the reading of a survey meter or an area dosimeter.
Its canonical unit is the sievert per second (`Sv/s`), and its arithmetic results
display in the sievert per hour.
The module provides the sievert per second and per hour with the multiples dosimeters
display, and the rem per hour and the millirem per hour.

Examples
--------
A background of 0.12 µSv/h, in nanosieverts per hour:

>>> MicrosievertPerHour(0.12).to(NANOSIEVERT_PER_HOUR)
120 nSv/h

A reading times a working shift is an equivalent dose:

>>> from kuchka import Hour
>>> from kuchka.units import MICROSIEVERT
>>> (MicrosievertPerHour(0.12) * Hour(8)).to(MICROSIEVERT)
0.96 µSv

`EQUIVALENT_DOSE_RATE_UNITS` maps symbols such as ``"Sv/h"``, ``"uSv/h"``, and
``"mrem/h"`` to their constructors for boundary code that reads unit labels from
external data.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import EquivalentDoseRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

SIEVERT_PER_SECOND = UnitDef(
    "sievert_per_second",
    "Sv/s",
    Fraction(1, 1),
    SPECIFIC_POWER,
    words=("sieverts per second",),
)
SIEVERT_PER_HOUR = UnitDef(
    "sievert_per_hour",
    "Sv/h",
    Fraction(1, 3600),
    SPECIFIC_POWER,
    aliases=("Sv/hr",),
    words=("sieverts per hour",),
)
MILLISIEVERT_PER_HOUR = UnitDef(
    "millisievert_per_hour",
    "mSv/h",
    Fraction(1, 3600000),
    SPECIFIC_POWER,
    aliases=("mSv/hr",),
    words=("millisieverts per hour",),
)
MICROSIEVERT_PER_HOUR = UnitDef(
    "microsievert_per_hour",
    "µSv/h",
    Fraction(1, 3600000000),
    SPECIFIC_POWER,
    aliases=("µSv/hr", "uSv/h", "uSv/hr"),
    words=("microsieverts per hour",),
)
NANOSIEVERT_PER_HOUR = UnitDef(
    "nanosievert_per_hour",
    "nSv/h",
    Fraction(1, 3600000000000),
    SPECIFIC_POWER,
    aliases=("nSv/hr",),
    words=("nanosieverts per hour",),
)
REM_PER_HOUR = UnitDef(
    "rem_per_hour",
    "rem/h",
    Fraction(1, 360000),
    SPECIFIC_POWER,
    aliases=("rem/hr",),
    words=("rems per hour",),
)
MILLIREM_PER_HOUR = UnitDef(
    "millirem_per_hour",
    "mrem/h",
    Fraction(1, 360000000),
    SPECIFIC_POWER,
    aliases=("mrem/hr",),
    words=("millirems per hour",),
)

EquivalentDoseRate._canonical_unit = SIEVERT_PER_SECOND  # noqa: SLF001 -- this module owns EquivalentDoseRate's canonical unit
EquivalentDoseRate._result_unit = SIEVERT_PER_HOUR  # noqa: SLF001 -- and the unit its arithmetic results display in


def SievertPerSecond(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in sieverts per second.

    Parameters
    ----------
    value : Numeric
        Magnitude in sieverts per second.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in sieverts per second.

    """
    return EquivalentDoseRate(
        to_exact(value) * SIEVERT_PER_SECOND.scale, SIEVERT_PER_SECOND
    )


def SievertPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in sieverts per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in sieverts per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in sieverts per hour.

    """
    return EquivalentDoseRate(
        to_exact(value) * SIEVERT_PER_HOUR.scale, SIEVERT_PER_HOUR
    )


def MillisievertPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in millisieverts per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in millisieverts per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in millisieverts per hour.

    """
    return EquivalentDoseRate(
        to_exact(value) * MILLISIEVERT_PER_HOUR.scale, MILLISIEVERT_PER_HOUR
    )


def MicrosievertPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in microsieverts per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in microsieverts per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in microsieverts per hour.

    """
    return EquivalentDoseRate(
        to_exact(value) * MICROSIEVERT_PER_HOUR.scale, MICROSIEVERT_PER_HOUR
    )


def NanosievertPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in nanosieverts per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanosieverts per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in nanosieverts per hour.

    """
    return EquivalentDoseRate(
        to_exact(value) * NANOSIEVERT_PER_HOUR.scale, NANOSIEVERT_PER_HOUR
    )


def RemPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in rems per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in rems per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in rems per hour.

    """
    return EquivalentDoseRate(to_exact(value) * REM_PER_HOUR.scale, REM_PER_HOUR)


def MilliremPerHour(value: Numeric) -> EquivalentDoseRate:
    """Construct an EquivalentDoseRate from a magnitude in millirems per hour.

    Parameters
    ----------
    value : Numeric
        Magnitude in millirems per hour.

    Returns
    -------
    EquivalentDoseRate
        EquivalentDoseRate represented in millirems per hour.

    """
    return EquivalentDoseRate(
        to_exact(value) * MILLIREM_PER_HOUR.scale, MILLIREM_PER_HOUR
    )


EQUIVALENT_DOSE_RATE_UNITS: Mapping[str, Callable[[Numeric], EquivalentDoseRate]] = (
    unit_table(
        "EQUIVALENT_DOSE_RATE_UNITS",
        {
            SIEVERT_PER_SECOND: SievertPerSecond,
            SIEVERT_PER_HOUR: SievertPerHour,
            MILLISIEVERT_PER_HOUR: MillisievertPerHour,
            MICROSIEVERT_PER_HOUR: MicrosievertPerHour,
            NANOSIEVERT_PER_HOUR: NanosievertPerHour,
            REM_PER_HOUR: RemPerHour,
            MILLIREM_PER_HOUR: MilliremPerHour,
        },
    )
)

__all__ = [
    "EQUIVALENT_DOSE_RATE_UNITS",
    "MICROSIEVERT_PER_HOUR",
    "MILLIREM_PER_HOUR",
    "MILLISIEVERT_PER_HOUR",
    "NANOSIEVERT_PER_HOUR",
    "REM_PER_HOUR",
    "SIEVERT_PER_HOUR",
    "SIEVERT_PER_SECOND",
    "MicrosievertPerHour",
    "MilliremPerHour",
    "MillisievertPerHour",
    "NanosievertPerHour",
    "RemPerHour",
    "SievertPerHour",
    "SievertPerSecond",
]
