"""Unit constructors for thermal conductivity: watts per metre kelvin and its relatives.

    from kuchka import MilliwattPerMetreKelvin, WattPerMetreKelvin

    copper = WattPerMetreKelvin(401)
    aerogel = MilliwattPerMetreKelvin(15)

`ThermalConductivity` is how readily a material conducts heat, `Power / Length /
TemperatureDelta`.
Its canonical unit is the watt per metre kelvin (`W/(m·K)`), and a degree Celsius in the
denominator is a difference, so `W/(m·°C)` is the same unit.

Examples
--------
Copper conducts 401 W/(m·K), or 4.01 W/(cm·K):

>>> WattPerCentimetreKelvin(4.01).to(WATT_PER_METRE_KELVIN)
401 W/(m·K)

An insulating aerogel at 15 mW/(m·K):

>>> MilliwattPerMetreKelvin(15).to(WATT_PER_METRE_KELVIN)
0.015 W/(m·K)

`THERMAL_CONDUCTIVITY_UNITS` maps symbols such as ``"W/(m K)"``, ``"W/mK"``, and
``"mW/(m K)"`` to their constructors, for boundary code that reads a unit as a string
from outside the application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import THERMAL_CONDUCTIVITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ThermalConductivity
from kuchka.quantities import UnitDef
from kuchka.units.length import CENTIMETRE
from kuchka.units.mechanics.power import WATT

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

WATT_PER_METRE_KELVIN = UnitDef(
    "watt_per_metre_kelvin",
    "W/(m·K)",
    1,
    THERMAL_CONDUCTIVITY,
    aliases=(
        "W/(m K)",
        "W/(m*K)",
        "W/m/K",
        "W/mK",
        "W/(m·°C)",
        "W/(m °C)",
        "W/(m*°C)",
        "W/m/°C",
    ),
    words=("watts per metre kelvin", "watts per meter kelvin"),
)
MILLIWATT_PER_METRE_KELVIN = with_prefix(prefixes.MILLI, WATT_PER_METRE_KELVIN)
KILOWATT_PER_METRE_KELVIN = with_prefix(prefixes.KILO, WATT_PER_METRE_KELVIN)
WATT_PER_CENTIMETRE_KELVIN = UnitDef(
    "watt_per_centimetre_kelvin",
    "W/(cm·K)",
    WATT.scale / CENTIMETRE.scale,
    THERMAL_CONDUCTIVITY,
    aliases=(
        "W/(cm K)",
        "W/(cm*K)",
        "W/cm/K",
        "W/cmK",
        "W/(cm·°C)",
        "W/(cm °C)",
        "W/(cm*°C)",
        "W/cm/°C",
    ),
    words=("watts per centimetre kelvin", "watts per centimeter kelvin"),
)

ThermalConductivity._canonical_unit = WATT_PER_METRE_KELVIN  # noqa: SLF001 -- this module owns ThermalConductivity's canonical unit


def WattPerMetreKelvin(value: Numeric) -> ThermalConductivity:
    """Construct a ThermalConductivity from watts per metre kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per metre kelvin.

    Returns
    -------
    ThermalConductivity
        ThermalConductivity represented in watts per metre kelvin.

    """
    return ThermalConductivity(
        to_exact(value) * WATT_PER_METRE_KELVIN.scale, WATT_PER_METRE_KELVIN
    )


def MilliwattPerMetreKelvin(value: Numeric) -> ThermalConductivity:
    """Construct a ThermalConductivity from milliwatts per metre kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliwatts per metre kelvin.

    Returns
    -------
    ThermalConductivity
        ThermalConductivity represented in milliwatts per metre kelvin.

    """
    return ThermalConductivity(
        to_exact(value) * MILLIWATT_PER_METRE_KELVIN.scale, MILLIWATT_PER_METRE_KELVIN
    )


def KilowattPerMetreKelvin(value: Numeric) -> ThermalConductivity:
    """Construct a ThermalConductivity from kilowatts per metre kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilowatts per metre kelvin.

    Returns
    -------
    ThermalConductivity
        ThermalConductivity represented in kilowatts per metre kelvin.

    """
    return ThermalConductivity(
        to_exact(value) * KILOWATT_PER_METRE_KELVIN.scale, KILOWATT_PER_METRE_KELVIN
    )


def WattPerCentimetreKelvin(value: Numeric) -> ThermalConductivity:
    """Construct a ThermalConductivity from watts per centimetre kelvin.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per centimetre kelvin.

    Returns
    -------
    ThermalConductivity
        ThermalConductivity represented in watts per centimetre kelvin.

    """
    return ThermalConductivity(
        to_exact(value) * WATT_PER_CENTIMETRE_KELVIN.scale, WATT_PER_CENTIMETRE_KELVIN
    )


THERMAL_CONDUCTIVITY_UNITS: Mapping[str, Callable[[Numeric], ThermalConductivity]] = (
    unit_table(
        "THERMAL_CONDUCTIVITY_UNITS",
        {
            WATT_PER_METRE_KELVIN: WattPerMetreKelvin,
            MILLIWATT_PER_METRE_KELVIN: MilliwattPerMetreKelvin,
            KILOWATT_PER_METRE_KELVIN: KilowattPerMetreKelvin,
            WATT_PER_CENTIMETRE_KELVIN: WattPerCentimetreKelvin,
        },
    )
)

__all__ = [
    "KILOWATT_PER_METRE_KELVIN",
    "MILLIWATT_PER_METRE_KELVIN",
    "THERMAL_CONDUCTIVITY_UNITS",
    "WATT_PER_CENTIMETRE_KELVIN",
    "WATT_PER_METRE_KELVIN",
    "KilowattPerMetreKelvin",
    "MilliwattPerMetreKelvin",
    "WattPerCentimetreKelvin",
    "WattPerMetreKelvin",
]
