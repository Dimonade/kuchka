"""Unit constructors for specific charge: coulombs and ampere-hours per mass.

    from kuchka import AmpereHourPerKilogram, CoulombPerKilogram

    cell = AmpereHourPerKilogram(0.25)
    beam = CoulombPerKilogram(0.0001)

`SpecificCharge` is electric charge per unit mass, `Charge / Mass`.
Its canonical unit is the coulomb per kilogram (`C/kg`), which is also the SI unit of
the `Exposure` role.
The ampere-hour per kilogram (`Ah/kg`) is the unit gravimetric battery capacity is
quoted in, and `mAh/g` is the same quantity: both are exactly 3600 C/kg.

Examples
--------
A cell quoted at 250 mAh/g holds the same charge per mass as one quoted at 250 Ah/kg:

>>> MilliampereHourPerGram(250) == AmpereHourPerKilogram(250)
True

`SPECIFIC_CHARGE_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_CHARGE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SpecificCharge
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.charge import AMPERE_HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

COULOMB_PER_KILOGRAM = UnitDef(
    "coulomb_per_kilogram",
    "C/kg",
    1,
    SPECIFIC_CHARGE,
    words=("coulombs per kilogram",),
)
MILLICOULOMB_PER_KILOGRAM = with_prefix(
    prefixes.MILLI, COULOMB_PER_KILOGRAM, words=("millicoulombs per kilogram",)
)
MICROCOULOMB_PER_KILOGRAM = with_prefix(
    prefixes.MICRO, COULOMB_PER_KILOGRAM, words=("microcoulombs per kilogram",)
)
AMPERE_HOUR_PER_KILOGRAM = UnitDef(
    "ampere_hour_per_kilogram",
    "Ah/kg",
    AMPERE_HOUR.scale,
    SPECIFIC_CHARGE,
    words=("ampere-hours per kilogram",),
)
MILLIAMPERE_HOUR_PER_GRAM = UnitDef(
    "milliampere_hour_per_gram",
    "mAh/g",
    AMPERE_HOUR.scale,
    SPECIFIC_CHARGE,
    words=("milliampere-hours per gram",),
)

SpecificCharge._canonical_unit = COULOMB_PER_KILOGRAM  # noqa: SLF001 -- this module owns SpecificCharge's canonical unit


def CoulombPerKilogram(value: Numeric) -> SpecificCharge:
    """Construct a SpecificCharge from a magnitude in coulombs per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per kilogram.

    Returns
    -------
    SpecificCharge
        SpecificCharge represented in coulombs per kilogram.

    """
    return SpecificCharge(
        to_exact(value) * COULOMB_PER_KILOGRAM.scale, COULOMB_PER_KILOGRAM
    )


def MillicoulombPerKilogram(value: Numeric) -> SpecificCharge:
    """Construct a SpecificCharge from a magnitude in millicoulombs per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in millicoulombs per kilogram.

    Returns
    -------
    SpecificCharge
        SpecificCharge represented in millicoulombs per kilogram.

    """
    return SpecificCharge(
        to_exact(value) * MILLICOULOMB_PER_KILOGRAM.scale, MILLICOULOMB_PER_KILOGRAM
    )


def MicrocoulombPerKilogram(value: Numeric) -> SpecificCharge:
    """Construct a SpecificCharge from a magnitude in microcoulombs per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcoulombs per kilogram.

    Returns
    -------
    SpecificCharge
        SpecificCharge represented in microcoulombs per kilogram.

    """
    return SpecificCharge(
        to_exact(value) * MICROCOULOMB_PER_KILOGRAM.scale, MICROCOULOMB_PER_KILOGRAM
    )


def AmpereHourPerKilogram(value: Numeric) -> SpecificCharge:
    """Construct a SpecificCharge from a magnitude in ampere-hours per kilogram.

    Parameters
    ----------
    value : Numeric
        Magnitude in ampere-hours per kilogram.

    Returns
    -------
    SpecificCharge
        SpecificCharge represented in ampere-hours per kilogram.

    """
    return SpecificCharge(
        to_exact(value) * AMPERE_HOUR_PER_KILOGRAM.scale, AMPERE_HOUR_PER_KILOGRAM
    )


def MilliampereHourPerGram(value: Numeric) -> SpecificCharge:
    """Construct a SpecificCharge from a magnitude in milliampere-hours per gram.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliampere-hours per gram.

    Returns
    -------
    SpecificCharge
        SpecificCharge represented in milliampere-hours per gram.

    """
    return SpecificCharge(
        to_exact(value) * MILLIAMPERE_HOUR_PER_GRAM.scale, MILLIAMPERE_HOUR_PER_GRAM
    )


SPECIFIC_CHARGE_UNITS: Mapping[str, Callable[[Numeric], SpecificCharge]] = unit_table(
    "SPECIFIC_CHARGE_UNITS",
    {
        COULOMB_PER_KILOGRAM: CoulombPerKilogram,
        MILLICOULOMB_PER_KILOGRAM: MillicoulombPerKilogram,
        MICROCOULOMB_PER_KILOGRAM: MicrocoulombPerKilogram,
        AMPERE_HOUR_PER_KILOGRAM: AmpereHourPerKilogram,
        MILLIAMPERE_HOUR_PER_GRAM: MilliampereHourPerGram,
    },
)

__all__ = [
    "AMPERE_HOUR_PER_KILOGRAM",
    "COULOMB_PER_KILOGRAM",
    "MICROCOULOMB_PER_KILOGRAM",
    "MILLIAMPERE_HOUR_PER_GRAM",
    "MILLICOULOMB_PER_KILOGRAM",
    "SPECIFIC_CHARGE_UNITS",
    "AmpereHourPerKilogram",
    "CoulombPerKilogram",
    "MicrocoulombPerKilogram",
    "MilliampereHourPerGram",
    "MillicoulombPerKilogram",
]
