"""Heat flux constructors: watts per square metre and per square centimetre.

    from kuchka import KilowattPerSquareMetre, MilliwattPerSquareCentimetre

    sun = KilowattPerSquareMetre(1.361)
    sensor = MilliwattPerSquareCentimetre(100)

`HeatFlux` is the heat that flows through a surface, `Power / Area`.
Its canonical unit is the watt per square metre (`W/m²`), which is also the unit of an
irradiance and of a sound intensity.

Examples
--------
The solar constant over 10 m² is 13.61 kW:

>>> from kuchka import SquareMetre
>>> KilowattPerSquareMetre(1.361) * SquareMetre(10)
13610 W

A 100 mW/cm² flux is 1000 W/m²:

>>> MilliwattPerSquareCentimetre(100).to(WATT_PER_SQUARE_METRE)
1000 W/m²

A power of 600 W through 2 m² is a flux of 300 W/m²:

>>> from kuchka import Watt
>>> Watt(600) / SquareMetre(2)
300 W/m²

`HEAT_FLUX_UNITS` maps symbols such as ``"W/m2"`` and ``"mW/cm2"`` to their
constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import HEAT_FLUX
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import HeatFlux
from kuchka.quantities import UnitDef
from kuchka.units.geometry.area import SQUARE_CENTIMETRE
from kuchka.units.mechanics.power import WATT

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

WATT_PER_SQUARE_METRE = UnitDef(
    "watt_per_square_metre",
    "W/m²",
    1,
    HEAT_FLUX,
    aliases=powered("W/m", 2),
    words=("watts per square metre", "watts per square meter"),
)
MILLIWATT_PER_SQUARE_METRE = with_prefix(prefixes.MILLI, WATT_PER_SQUARE_METRE)
KILOWATT_PER_SQUARE_METRE = with_prefix(prefixes.KILO, WATT_PER_SQUARE_METRE)
MEGAWATT_PER_SQUARE_METRE = with_prefix(prefixes.MEGA, WATT_PER_SQUARE_METRE)
WATT_PER_SQUARE_CENTIMETRE = UnitDef(
    "watt_per_square_centimetre",
    "W/cm²",
    WATT.scale / SQUARE_CENTIMETRE.scale,
    HEAT_FLUX,
    aliases=powered("W/cm", 2),
    words=("watts per square centimetre", "watts per square centimeter"),
)
MILLIWATT_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MILLI, WATT_PER_SQUARE_CENTIMETRE
)
MICROWATT_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MICRO, WATT_PER_SQUARE_CENTIMETRE
)

HeatFlux._canonical_unit = WATT_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns HeatFlux's canonical unit


def WattPerSquareMetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from watts per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per square metre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in watts per square metre.

    """
    return HeatFlux(
        to_exact(value) * WATT_PER_SQUARE_METRE.scale, WATT_PER_SQUARE_METRE
    )


def MilliwattPerSquareMetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from milliwatts per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliwatts per square metre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in milliwatts per square metre.

    """
    return HeatFlux(
        to_exact(value) * MILLIWATT_PER_SQUARE_METRE.scale, MILLIWATT_PER_SQUARE_METRE
    )


def KilowattPerSquareMetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from kilowatts per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilowatts per square metre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in kilowatts per square metre.

    """
    return HeatFlux(
        to_exact(value) * KILOWATT_PER_SQUARE_METRE.scale, KILOWATT_PER_SQUARE_METRE
    )


def MegawattPerSquareMetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from megawatts per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in megawatts per square metre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in megawatts per square metre.

    """
    return HeatFlux(
        to_exact(value) * MEGAWATT_PER_SQUARE_METRE.scale, MEGAWATT_PER_SQUARE_METRE
    )


def WattPerSquareCentimetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from watts per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per square centimetre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in watts per square centimetre.

    """
    return HeatFlux(
        to_exact(value) * WATT_PER_SQUARE_CENTIMETRE.scale, WATT_PER_SQUARE_CENTIMETRE
    )


def MilliwattPerSquareCentimetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from milliwatts per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliwatts per square centimetre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in milliwatts per square centimetre.

    """
    return HeatFlux(
        to_exact(value) * MILLIWATT_PER_SQUARE_CENTIMETRE.scale,
        MILLIWATT_PER_SQUARE_CENTIMETRE,
    )


def MicrowattPerSquareCentimetre(value: Numeric) -> HeatFlux:
    """Construct a HeatFlux from microwatts per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microwatts per square centimetre.

    Returns
    -------
    HeatFlux
        HeatFlux represented in microwatts per square centimetre.

    """
    return HeatFlux(
        to_exact(value) * MICROWATT_PER_SQUARE_CENTIMETRE.scale,
        MICROWATT_PER_SQUARE_CENTIMETRE,
    )


HEAT_FLUX_UNITS: Mapping[str, Callable[[Numeric], HeatFlux]] = unit_table(
    "HEAT_FLUX_UNITS",
    {
        WATT_PER_SQUARE_METRE: WattPerSquareMetre,
        MILLIWATT_PER_SQUARE_METRE: MilliwattPerSquareMetre,
        KILOWATT_PER_SQUARE_METRE: KilowattPerSquareMetre,
        MEGAWATT_PER_SQUARE_METRE: MegawattPerSquareMetre,
        WATT_PER_SQUARE_CENTIMETRE: WattPerSquareCentimetre,
        MILLIWATT_PER_SQUARE_CENTIMETRE: MilliwattPerSquareCentimetre,
        MICROWATT_PER_SQUARE_CENTIMETRE: MicrowattPerSquareCentimetre,
    },
)

__all__ = [
    "HEAT_FLUX_UNITS",
    "KILOWATT_PER_SQUARE_METRE",
    "MEGAWATT_PER_SQUARE_METRE",
    "MICROWATT_PER_SQUARE_CENTIMETRE",
    "MILLIWATT_PER_SQUARE_CENTIMETRE",
    "MILLIWATT_PER_SQUARE_METRE",
    "WATT_PER_SQUARE_CENTIMETRE",
    "WATT_PER_SQUARE_METRE",
    "KilowattPerSquareMetre",
    "MegawattPerSquareMetre",
    "MicrowattPerSquareCentimetre",
    "MilliwattPerSquareCentimetre",
    "MilliwattPerSquareMetre",
    "WattPerSquareCentimetre",
    "WattPerSquareMetre",
]
