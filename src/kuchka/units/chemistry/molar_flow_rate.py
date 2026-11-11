"""Molar flow rate constructors: moles per second, minute, and hour.

Molar flow rate is the amount of substance that passes a section per unit of time, as a
reactor feed or a gas stream is quoted: `1 mol/s` is the canonical unit.
The minute and hour forms are the ones process work reads off a meter: `mmol/min`,
`mol/min`, `mol/h`, and `kmol/h`.

A catalytic activity (`kat`) has the same dimension and is a `CatalyticActivity`,
reached by its own constructors.

`MOLAR_FLOW_RATE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MolarFlowRate
from kuchka.quantities import UnitDef
from kuchka.units.temporal.time import HOUR
from kuchka.units.temporal.time import MINUTE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

MOLE_PER_SECOND = UnitDef(
    "mole_per_second",
    "mol/s",
    1,
    MOLAR_FLOW_RATE,
    words=("mole per second", "moles per second"),
)
KILOMOLE_PER_SECOND = UnitDef(
    "kilomole_per_second",
    "kmol/s",
    1000,
    MOLAR_FLOW_RATE,
    words=("kilomole per second", "kilomoles per second"),
)
MILLIMOLE_PER_MINUTE = UnitDef(
    "millimole_per_minute",
    "mmol/min",
    1 / (1000 * MINUTE.scale),
    MOLAR_FLOW_RATE,
    words=("millimole per minute", "millimoles per minute"),
)
MOLE_PER_MINUTE = UnitDef(
    "mole_per_minute",
    "mol/min",
    1 / MINUTE.scale,
    MOLAR_FLOW_RATE,
    words=("mole per minute", "moles per minute"),
)
MOLE_PER_HOUR = UnitDef(
    "mole_per_hour",
    "mol/h",
    1 / HOUR.scale,
    MOLAR_FLOW_RATE,
    aliases=("mol/hr",),
    words=("mole per hour", "moles per hour"),
)
KILOMOLE_PER_HOUR = UnitDef(
    "kilomole_per_hour",
    "kmol/h",
    1000 / HOUR.scale,
    MOLAR_FLOW_RATE,
    aliases=("kmol/hr",),
    words=("kilomole per hour", "kilomoles per hour"),
)

MolarFlowRate._canonical_unit = MOLE_PER_SECOND  # noqa: SLF001 -- this module owns MolarFlowRate's canonical unit


def MolePerSecond(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in moles per second.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in mol/s.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in moles per second.

    Examples
    --------
    A feed of 0.5 mol/s runs for a minute:

    >>> from kuchka import Minute
    >>> MolePerSecond(0.5) * Minute(1)
    30 mol

    """
    return MolarFlowRate(to_exact(value) * MOLE_PER_SECOND.scale, MOLE_PER_SECOND)


def KilomolePerSecond(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in kilomoles per second.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in kmol/s.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in kilomoles per second.

    """
    return MolarFlowRate(
        to_exact(value) * KILOMOLE_PER_SECOND.scale, KILOMOLE_PER_SECOND
    )


def MillimolePerMinute(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in millimoles per minute.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in mmol/min.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in millimoles per minute.

    """
    return MolarFlowRate(
        to_exact(value) * MILLIMOLE_PER_MINUTE.scale, MILLIMOLE_PER_MINUTE
    )


def MolePerMinute(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in moles per minute.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in mol/min.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in moles per minute.

    """
    return MolarFlowRate(to_exact(value) * MOLE_PER_MINUTE.scale, MOLE_PER_MINUTE)


def MolePerHour(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in moles per hour.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in mol/h.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in moles per hour.

    """
    return MolarFlowRate(to_exact(value) * MOLE_PER_HOUR.scale, MOLE_PER_HOUR)


def KilomolePerHour(value: Numeric) -> MolarFlowRate:
    """Construct a molar flow rate from a magnitude in kilomoles per hour.

    Parameters
    ----------
    value : Numeric
        Molar flow rate magnitude in kmol/h.

    Returns
    -------
    MolarFlowRate
        Molar flow rate represented in kilomoles per hour.

    Examples
    --------
    A plant that feeds 36 kmol/h of ethanol (46.07 g/mol) moves 0.4607 kg each second:

    >>> from kuchka import GramPerMole
    >>> from kuchka.units import KILOGRAM_PER_SECOND
    >>> (KilomolePerHour(36) * GramPerMole(46.07)).to(KILOGRAM_PER_SECOND)
    0.4607 kg/s

    """
    return MolarFlowRate(to_exact(value) * KILOMOLE_PER_HOUR.scale, KILOMOLE_PER_HOUR)


MOLAR_FLOW_RATE_UNITS: Mapping[str, Callable[[Numeric], MolarFlowRate]] = unit_table(
    "MOLAR_FLOW_RATE_UNITS",
    {
        MILLIMOLE_PER_MINUTE: MillimolePerMinute,
        MOLE_PER_SECOND: MolePerSecond,
        MOLE_PER_MINUTE: MolePerMinute,
        MOLE_PER_HOUR: MolePerHour,
        KILOMOLE_PER_SECOND: KilomolePerSecond,
        KILOMOLE_PER_HOUR: KilomolePerHour,
    },
)

__all__ = [
    "KILOMOLE_PER_HOUR",
    "KILOMOLE_PER_SECOND",
    "MILLIMOLE_PER_MINUTE",
    "MOLAR_FLOW_RATE_UNITS",
    "MOLE_PER_HOUR",
    "MOLE_PER_MINUTE",
    "MOLE_PER_SECOND",
    "KilomolePerHour",
    "KilomolePerSecond",
    "MillimolePerMinute",
    "MolePerHour",
    "MolePerMinute",
    "MolePerSecond",
]
