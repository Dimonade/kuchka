"""Specific power constructors: watts per kilogram and per gram.

    from kuchka import KilowattPerKilogram
    from kuchka import WattPerKilogram

    engine = KilowattPerKilogram(2.5)
    limit = WattPerKilogram(2)

`SpecificPower` is power per unit mass, `Power / Mass`.
Its canonical unit is the watt per kilogram (`W/kg`), which is also the unit of specific
absorption rate, and `mW/g` is the same quantity: both are exactly 1 W/kg.
The dose rates are roles of it, with units of their own.

Examples
--------
A limit of 2 W/kg, in the milliwatts per gram a lab report may quote:

>>> WattPerKilogram(2).to(MILLIWATT_PER_GRAM)
2 mW/g

`SPECIFIC_POWER_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificPower
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

WATT_PER_KILOGRAM = UnitDef(
    "watt_per_kilogram",
    "W/kg",
    1,
    SPECIFIC_POWER,
    words=("watts per kilogram",),
)
MILLIWATT_PER_KILOGRAM = UnitDef(
    "milliwatt_per_kilogram",
    "mW/kg",
    Fraction(1, 1000),
    SPECIFIC_POWER,
    words=("milliwatts per kilogram",),
)
KILOWATT_PER_KILOGRAM = UnitDef(
    "kilowatt_per_kilogram",
    "kW/kg",
    1000,
    SPECIFIC_POWER,
    words=("kilowatts per kilogram",),
)
WATT_PER_GRAM = UnitDef(
    "watt_per_gram",
    "W/g",
    1000,
    SPECIFIC_POWER,
    words=("watts per gram",),
)
MILLIWATT_PER_GRAM = UnitDef(
    "milliwatt_per_gram",
    "mW/g",
    1,
    SPECIFIC_POWER,
    words=("milliwatts per gram",),
)

SpecificPower._canonical_unit = WATT_PER_KILOGRAM  # noqa: SLF001 -- this module owns SpecificPower's canonical unit


def WattPerKilogram(value: Numeric) -> SpecificPower:
    """Construct a SpecificPower from a magnitude in watts per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per kilogram.

    Returns
    -------
    SpecificPower
        SpecificPower represented in watts per kilogram.

    """
    return SpecificPower(to_exact(value) * WATT_PER_KILOGRAM.scale, WATT_PER_KILOGRAM)


def MilliwattPerKilogram(value: Numeric) -> SpecificPower:
    """Construct a SpecificPower from a magnitude in milliwatts per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliwatts per kilogram.

    Returns
    -------
    SpecificPower
        SpecificPower represented in milliwatts per kilogram.

    """
    return SpecificPower(
        to_exact(value) * MILLIWATT_PER_KILOGRAM.scale, MILLIWATT_PER_KILOGRAM
    )


def KilowattPerKilogram(value: Numeric) -> SpecificPower:
    """Construct a SpecificPower from a magnitude in kilowatts per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilowatts per kilogram.

    Returns
    -------
    SpecificPower
        SpecificPower represented in kilowatts per kilogram.

    """
    return SpecificPower(
        to_exact(value) * KILOWATT_PER_KILOGRAM.scale, KILOWATT_PER_KILOGRAM
    )


def WattPerGram(value: Numeric) -> SpecificPower:
    """Construct a SpecificPower from a magnitude in watts per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in watts per gram.

    Returns
    -------
    SpecificPower
        SpecificPower represented in watts per gram.

    """
    return SpecificPower(to_exact(value) * WATT_PER_GRAM.scale, WATT_PER_GRAM)


def MilliwattPerGram(value: Numeric) -> SpecificPower:
    """Construct a SpecificPower from a magnitude in milliwatts per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliwatts per gram.

    Returns
    -------
    SpecificPower
        SpecificPower represented in milliwatts per gram.

    """
    return SpecificPower(to_exact(value) * MILLIWATT_PER_GRAM.scale, MILLIWATT_PER_GRAM)


SPECIFIC_POWER_UNITS: Mapping[str, Callable[[Numeric], SpecificPower]] = unit_table(
    "SPECIFIC_POWER_UNITS",
    {
        WATT_PER_KILOGRAM: WattPerKilogram,
        MILLIWATT_PER_KILOGRAM: MilliwattPerKilogram,
        KILOWATT_PER_KILOGRAM: KilowattPerKilogram,
        WATT_PER_GRAM: WattPerGram,
        MILLIWATT_PER_GRAM: MilliwattPerGram,
    },
)

__all__ = [
    "KILOWATT_PER_KILOGRAM",
    "MILLIWATT_PER_GRAM",
    "MILLIWATT_PER_KILOGRAM",
    "SPECIFIC_POWER_UNITS",
    "WATT_PER_GRAM",
    "WATT_PER_KILOGRAM",
    "KilowattPerKilogram",
    "MilliwattPerGram",
    "MilliwattPerKilogram",
    "WattPerGram",
    "WattPerKilogram",
]
