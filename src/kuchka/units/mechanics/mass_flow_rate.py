"""Mass flow rate constructors: kilograms, grams, tonnes, and pounds per time.

Mass flow rate is the mass that passes a section per unit of time, of a liquid, a gas,
or a solid such as ore on a belt: `1 kg/s` is the canonical unit.
The hour forms are the ones plant throughput is quoted in: `kg/h`, `t/h`, and `lb/h`.

`MASS_FLOW_RATE_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MASS_FLOW_RATE
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import MassFlowRate
from kuchka.quantities import UnitDef
from kuchka.units.mass import GRAM
from kuchka.units.mass import MEGAGRAM
from kuchka.units.mass import POUND
from kuchka.units.temporal.time import HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

KILOGRAM_PER_SECOND = UnitDef(
    "kilogram_per_second",
    "kg/s",
    1,
    MASS_FLOW_RATE,
    words=("kilogram per second", "kilograms per second"),
)
GRAM_PER_SECOND = UnitDef(
    "gram_per_second",
    "g/s",
    GRAM.scale,
    MASS_FLOW_RATE,
)
KILOGRAM_PER_HOUR = UnitDef(
    "kilogram_per_hour",
    "kg/h",
    1 / HOUR.scale,
    MASS_FLOW_RATE,
    aliases=("kg/hr",),
    words=("kilogram per hour", "kilograms per hour"),
)
TONNE_PER_HOUR = UnitDef(
    "tonne_per_hour",
    "t/h",
    MEGAGRAM.scale / HOUR.scale,
    MASS_FLOW_RATE,
    aliases=("t/hr",),
    words=("tonne per hour", "tonnes per hour", "metric ton per hour"),
)
POUND_PER_HOUR = UnitDef(
    "pound_per_hour",
    "lb/h",
    POUND.scale / HOUR.scale,
    MASS_FLOW_RATE,
    aliases=("lb/hr", "lbs/h", "lbs/hr"),
)

MassFlowRate._canonical_unit = KILOGRAM_PER_SECOND  # noqa: SLF001 -- this module owns MassFlowRate's canonical unit


def KilogramPerSecond(value: Numeric) -> MassFlowRate:
    """Construct a mass flow rate from a magnitude expressed in kilograms per second.

    Parameters
    ----------
    value : Numeric
        Mass flow rate magnitude in kg/s.

    Returns
    -------
    MassFlowRate
        Mass flow rate represented in kilograms per second.

    Examples
    --------
    A pump that moves 36 L of fuel of density 800 kg/m³ every second delivers:

    >>> from kuchka import KilogramPerCubicMetre
    >>> from kuchka import LitrePerSecond
    >>> KilogramPerCubicMetre(800) * LitrePerSecond(36)
    28.8 kg/s

    """
    return MassFlowRate(
        to_exact(value) * KILOGRAM_PER_SECOND.scale, KILOGRAM_PER_SECOND
    )


def GramPerSecond(value: Numeric) -> MassFlowRate:
    """Construct a mass flow rate from a magnitude expressed in grams per second.

    Parameters
    ----------
    value : Numeric
        Mass flow rate magnitude in g/s.

    Returns
    -------
    MassFlowRate
        Mass flow rate represented in grams per second.

    """
    return MassFlowRate(to_exact(value) * GRAM_PER_SECOND.scale, GRAM_PER_SECOND)


def KilogramPerHour(value: Numeric) -> MassFlowRate:
    """Construct a mass flow rate from a magnitude expressed in kilograms per hour.

    Parameters
    ----------
    value : Numeric
        Mass flow rate magnitude in kg/h.

    Returns
    -------
    MassFlowRate
        Mass flow rate represented in kilograms per hour.

    Examples
    --------
    A furnace that burns 7.2 kg/h consumes 2 g every second:

    >>> KilogramPerHour(7.2).to(GRAM_PER_SECOND)
    2 g/s

    """
    return MassFlowRate(to_exact(value) * KILOGRAM_PER_HOUR.scale, KILOGRAM_PER_HOUR)


def TonnePerHour(value: Numeric) -> MassFlowRate:
    """Construct a mass flow rate from a magnitude expressed in tonnes per hour.

    Parameters
    ----------
    value : Numeric
        Mass flow rate magnitude in t/h.

    Returns
    -------
    MassFlowRate
        Mass flow rate represented in tonnes per hour.

    Examples
    --------
    A conveyor that carries 180 t/h moves 50 kg every second:

    >>> TonnePerHour(180).to(KILOGRAM_PER_SECOND)
    50 kg/s

    """
    return MassFlowRate(to_exact(value) * TONNE_PER_HOUR.scale, TONNE_PER_HOUR)


def PoundPerHour(value: Numeric) -> MassFlowRate:
    """Construct a mass flow rate from a magnitude expressed in pounds per hour.

    Parameters
    ----------
    value : Numeric
        Mass flow rate magnitude in lb/h.

    Returns
    -------
    MassFlowRate
        Mass flow rate represented in pounds per hour.

    """
    return MassFlowRate(to_exact(value) * POUND_PER_HOUR.scale, POUND_PER_HOUR)


MASS_FLOW_RATE_UNITS: Mapping[str, Callable[[Numeric], MassFlowRate]] = unit_table(
    "MASS_FLOW_RATE_UNITS",
    {
        GRAM_PER_SECOND: GramPerSecond,
        KILOGRAM_PER_SECOND: KilogramPerSecond,
        KILOGRAM_PER_HOUR: KilogramPerHour,
        TONNE_PER_HOUR: TonnePerHour,
        POUND_PER_HOUR: PoundPerHour,
    },
)

MASS_FLOW_RATE_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        GRAM_PER_SECOND,
        KILOGRAM_PER_SECOND,
    ),
)
"""The units `auto_scale` moves a mass flow rate along, smallest first."""

__all__ = [
    "GRAM_PER_SECOND",
    "KILOGRAM_PER_HOUR",
    "KILOGRAM_PER_SECOND",
    "MASS_FLOW_RATE_LADDERS",
    "MASS_FLOW_RATE_UNITS",
    "POUND_PER_HOUR",
    "TONNE_PER_HOUR",
    "GramPerSecond",
    "KilogramPerHour",
    "KilogramPerSecond",
    "PoundPerHour",
    "TonnePerHour",
]
