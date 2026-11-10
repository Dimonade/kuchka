"""Specific current constructors: amperes per kilogram, with prefixes.

    from kuchka import AmperePerKilogram, MilliamperePerKilogram

    rate = MilliamperePerKilogram(0.2)

`SpecificCurrent` is electric current per unit mass, `Current / Mass`.
Its canonical unit is the ampere per kilogram (`A/kg`), the same as a coulomb per
kilogram per second, and it is also the unit of the `ExposureRate` role.

Examples
--------
A specific current of 200 µA/kg, in milliamperes per kilogram:

>>> MicroamperePerKilogram(200).to(MILLIAMPERE_PER_KILOGRAM)
0.2 mA/kg

`SPECIFIC_CURRENT_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificCurrent
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

AMPERE_PER_KILOGRAM = UnitDef(
    "ampere_per_kilogram",
    "A/kg",
    1,
    SPECIFIC_CURRENT,
    words=("amperes per kilogram",),
)
MILLIAMPERE_PER_KILOGRAM = UnitDef(
    "milliampere_per_kilogram",
    "mA/kg",
    Fraction(1, 1000),
    SPECIFIC_CURRENT,
    words=("milliamperes per kilogram",),
)
MICROAMPERE_PER_KILOGRAM = UnitDef(
    "microampere_per_kilogram",
    "\u00b5A/kg",
    Fraction(1, 1_000_000),
    SPECIFIC_CURRENT,
    aliases=("uA/kg",),
    words=("microamperes per kilogram",),
)

SpecificCurrent._canonical_unit = AMPERE_PER_KILOGRAM  # noqa: SLF001 -- this module owns SpecificCurrent's canonical unit


def AmperePerKilogram(value: Numeric) -> SpecificCurrent:
    """Construct a SpecificCurrent from a magnitude in amperes per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in amperes per kilogram.

    Returns
    -------
    SpecificCurrent
        SpecificCurrent represented in amperes per kilogram.

    """
    return SpecificCurrent(
        to_exact(value) * AMPERE_PER_KILOGRAM.scale, AMPERE_PER_KILOGRAM
    )


def MilliamperePerKilogram(value: Numeric) -> SpecificCurrent:
    """Construct a SpecificCurrent from a magnitude in milliamperes per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliamperes per kilogram.

    Returns
    -------
    SpecificCurrent
        SpecificCurrent represented in milliamperes per kilogram.

    """
    return SpecificCurrent(
        to_exact(value) * MILLIAMPERE_PER_KILOGRAM.scale, MILLIAMPERE_PER_KILOGRAM
    )


def MicroamperePerKilogram(value: Numeric) -> SpecificCurrent:
    """Construct a SpecificCurrent from a magnitude in microamperes per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in microamperes per kilogram.

    Returns
    -------
    SpecificCurrent
        SpecificCurrent represented in microamperes per kilogram.

    """
    return SpecificCurrent(
        to_exact(value) * MICROAMPERE_PER_KILOGRAM.scale, MICROAMPERE_PER_KILOGRAM
    )


SPECIFIC_CURRENT_UNITS: Mapping[str, Callable[[Numeric], SpecificCurrent]] = unit_table(
    "SPECIFIC_CURRENT_UNITS",
    {
        AMPERE_PER_KILOGRAM: AmperePerKilogram,
        MILLIAMPERE_PER_KILOGRAM: MilliamperePerKilogram,
        MICROAMPERE_PER_KILOGRAM: MicroamperePerKilogram,
    },
)

__all__ = [
    "AMPERE_PER_KILOGRAM",
    "MICROAMPERE_PER_KILOGRAM",
    "MILLIAMPERE_PER_KILOGRAM",
    "SPECIFIC_CURRENT_UNITS",
    "AmperePerKilogram",
    "MicroamperePerKilogram",
    "MilliamperePerKilogram",
]
