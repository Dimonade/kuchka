"""Volumetric flow rate constructors: cubic metres, litres, and gallons per time.

Volumetric flow rate is the volume that passes a section per unit of time, of a liquid,
a gas, or a solid such as grain: `1 m³/s` is the canonical unit.
The litre, hour, and minute forms are the ones process and fluid work reads off
pumps, flow meters, and fans: `L/s`, `L/min`, `m³/h`, `m³/min`, and `mL/min`.
The customary pair `gal/min` (the US liquid gallon) and `ft³/min` are exact.

Flow measured at standard or normal conditions (`Nm³/h`, `scfm`) is a different
measurement and not another unit of volume per time, so no spelling of it is accepted.
A bare `gpm` is refused too, because the US and imperial gallons differ.

`VOLUMETRIC_FLOW_RATE_UNITS` maps each symbol to its constructor, for boundary code
that reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import VOLUMETRIC_FLOW_RATE
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import VolumetricFlowRate
from kuchka.units.geometry.volume import CUBIC_FOOT
from kuchka.units.geometry.volume import LITRE
from kuchka.units.geometry.volume import MILLILITRE
from kuchka.units.geometry.volume import US_GALLON
from kuchka.units.temporal.time import HOUR
from kuchka.units.temporal.time import MINUTE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

_CUBED = symbols.SUPERSCRIPT_THREE

CUBIC_METRE_PER_SECOND = UnitDef(
    "cubic_metre_per_second",
    f"m{_CUBED}/s",
    1,
    VOLUMETRIC_FLOW_RATE,
    aliases=("m^3/s", "m**3/s"),
    words=("cubic meter per second", "cubic metre per second"),
)
CUBIC_METRE_PER_MINUTE = UnitDef(
    "cubic_metre_per_minute",
    f"m{_CUBED}/min",
    1 / MINUTE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("m^3/min", "m**3/min"),
    words=("cubic meter per minute", "cubic metre per minute"),
)
CUBIC_METRE_PER_HOUR = UnitDef(
    "cubic_metre_per_hour",
    f"m{_CUBED}/h",
    1 / HOUR.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("m^3/h", "m**3/h", "m^3/hr", "m**3/hr"),
    words=("cubic meter per hour", "cubic metre per hour"),
)
LITRE_PER_SECOND = UnitDef(
    "litre_per_second",
    "L/s",
    LITRE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("l/s",),
    words=(
        "liter per second",
        "litre per second",
        "liters per second",
        "litres per second",
    ),
)
LITRE_PER_MINUTE = UnitDef(
    "litre_per_minute",
    "L/min",
    LITRE.scale / MINUTE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("l/min", "lpm", "LPM"),
    words=(
        "liter per minute",
        "litre per minute",
        "liters per minute",
        "litres per minute",
    ),
)
MILLILITRE_PER_MINUTE = UnitDef(
    "millilitre_per_minute",
    "mL/min",
    MILLILITRE.scale / MINUTE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("ml/min",),
    words=(
        "milliliter per minute",
        "millilitre per minute",
        "milliliters per minute",
        "millilitres per minute",
    ),
)
US_GALLON_PER_MINUTE = UnitDef(
    "us_gallon_per_minute",
    "US gal/min",
    US_GALLON.scale / MINUTE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("gal(US)/min", "gal (US)/min", "USgal/min"),
    words=(
        "us gallon per minute",
        "us liquid gallon per minute",
        "us gallons per minute",
    ),
)
CUBIC_FOOT_PER_MINUTE = UnitDef(
    "cubic_foot_per_minute",
    f"ft{_CUBED}/min",
    CUBIC_FOOT.scale / MINUTE.scale,
    VOLUMETRIC_FLOW_RATE,
    aliases=("ft^3/min", "ft**3/min", "cfm", "CFM"),
    words=("cubic foot per minute", "cubic feet per minute"),
)

VolumetricFlowRate._canonical_unit = CUBIC_METRE_PER_SECOND  # noqa: SLF001 -- this module owns VolumetricFlowRate's canonical unit


def CubicMetrePerSecond(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in cubic metres per second.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in m³/s.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in cubic metres per second.

    Examples
    --------
    A pipe of 0.05 m² cross-section with water moving at 2 m/s carries 0.1 m³/s:

    >>> from kuchka import MetrePerSecond
    >>> from kuchka import SquareMetre
    >>> SquareMetre(0.05) * MetrePerSecond(2)
    0.1 m³/s

    """
    return VolumetricFlowRate(
        to_exact(value) * CUBIC_METRE_PER_SECOND.scale, CUBIC_METRE_PER_SECOND
    )


def CubicMetrePerMinute(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in cubic metres per minute.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in m³/min.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in cubic metres per minute.

    Examples
    --------
    >>> CubicMetrePerMinute(6).to(CUBIC_METRE_PER_SECOND)
    0.1 m³/s

    """
    return VolumetricFlowRate(
        to_exact(value) * CUBIC_METRE_PER_MINUTE.scale, CUBIC_METRE_PER_MINUTE
    )


def CubicMetrePerHour(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in cubic metres per hour.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in m³/h.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in cubic metres per hour.

    Examples
    --------
    A pump rated at 36 m³/h moves 10 L every second:

    >>> CubicMetrePerHour(36).to(LITRE_PER_SECOND)
    10 L/s

    """
    return VolumetricFlowRate(
        to_exact(value) * CUBIC_METRE_PER_HOUR.scale, CUBIC_METRE_PER_HOUR
    )


def LitrePerSecond(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude expressed in litres per second.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in L/s.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in litres per second.

    """
    return VolumetricFlowRate(
        to_exact(value) * LITRE_PER_SECOND.scale, LITRE_PER_SECOND
    )


def LitrePerMinute(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude expressed in litres per minute.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in L/min.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in litres per minute.

    Examples
    --------
    A tap that fills a 10 L bucket in 40 s runs at 15 L/min:

    >>> from kuchka import Litre
    >>> from kuchka import Second
    >>> (Litre(10) / Second(40)).to(LITRE_PER_MINUTE)
    15 L/min

    """
    return VolumetricFlowRate(
        to_exact(value) * LITRE_PER_MINUTE.scale, LITRE_PER_MINUTE
    )


def MillilitrePerMinute(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in millilitres per minute.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in mL/min.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in millilitres per minute.

    Examples
    --------
    An infusion pump set to 125 mL/min runs for ten minutes:

    >>> from kuchka import Minute
    >>> (MillilitrePerMinute(125) * Minute(10)).to(LITRE)
    1.25 L

    """
    return VolumetricFlowRate(
        to_exact(value) * MILLILITRE_PER_MINUTE.scale, MILLILITRE_PER_MINUTE
    )


def UsGallonPerMinute(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in US gallons per minute.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in US gal/min.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in US gallons per minute.

    """
    return VolumetricFlowRate(
        to_exact(value) * US_GALLON_PER_MINUTE.scale, US_GALLON_PER_MINUTE
    )


def CubicFootPerMinute(value: Numeric) -> VolumetricFlowRate:
    """Construct a volumetric flow rate from a magnitude in cubic feet per minute.

    Parameters
    ----------
    value : Numeric
        Volumetric flow rate magnitude in ft³/min.

    Returns
    -------
    VolumetricFlowRate
        Volumetric flow rate represented in cubic feet per minute.

    """
    return VolumetricFlowRate(
        to_exact(value) * CUBIC_FOOT_PER_MINUTE.scale, CUBIC_FOOT_PER_MINUTE
    )


CubicMeterPerSecond = CubicMetrePerSecond
CubicMeterPerMinute = CubicMetrePerMinute
CubicMeterPerHour = CubicMetrePerHour
LiterPerSecond = LitrePerSecond
LiterPerMinute = LitrePerMinute
MilliliterPerMinute = MillilitrePerMinute

VOLUMETRIC_FLOW_RATE_UNITS: Mapping[str, Callable[[Numeric], VolumetricFlowRate]] = (
    unit_table(
        "VOLUMETRIC_FLOW_RATE_UNITS",
        {
            MILLILITRE_PER_MINUTE: MillilitrePerMinute,
            LITRE_PER_SECOND: LitrePerSecond,
            LITRE_PER_MINUTE: LitrePerMinute,
            CUBIC_METRE_PER_SECOND: CubicMetrePerSecond,
            CUBIC_METRE_PER_MINUTE: CubicMetrePerMinute,
            CUBIC_METRE_PER_HOUR: CubicMetrePerHour,
            US_GALLON_PER_MINUTE: UsGallonPerMinute,
            CUBIC_FOOT_PER_MINUTE: CubicFootPerMinute,
        },
    )
)

__all__ = [
    "CUBIC_FOOT_PER_MINUTE",
    "CUBIC_METRE_PER_HOUR",
    "CUBIC_METRE_PER_MINUTE",
    "CUBIC_METRE_PER_SECOND",
    "LITRE_PER_MINUTE",
    "LITRE_PER_SECOND",
    "MILLILITRE_PER_MINUTE",
    "US_GALLON_PER_MINUTE",
    "VOLUMETRIC_FLOW_RATE_UNITS",
    "CubicFootPerMinute",
    "CubicMeterPerHour",
    "CubicMeterPerMinute",
    "CubicMeterPerSecond",
    "CubicMetrePerHour",
    "CubicMetrePerMinute",
    "CubicMetrePerSecond",
    "LiterPerMinute",
    "LiterPerSecond",
    "LitrePerMinute",
    "LitrePerSecond",
    "MilliliterPerMinute",
    "MillilitrePerMinute",
    "UsGallonPerMinute",
]
