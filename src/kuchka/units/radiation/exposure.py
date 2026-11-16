"""Exposure constructors: the roentgen and its prefixes.

    from kuchka import Microroentgen
    from kuchka import Milliroentgen
    from kuchka import Roentgen

    survey = Milliroentgen(5)
    background = Microroentgen(10)

`Exposure` is the charge of the ions a photon beam frees in a kilogram of air.
Its SI unit is the coulomb per kilogram (`C/kg`), shared with `SpecificCharge`, and the
roentgen (`R`) is the older unit, defined exactly as 2.58e-4 C/kg.
The module provides the roentgen and its milli- and micro- multiples.
`Exposure.from_specific_charge(CoulombPerKilogram(...))` builds one in the SI unit, and
`EXPOSURE_UNITS["C/kg"]` reads it from text.

Exposure is defined for X-rays and gamma rays in air.
It is not an absorbed dose, and the roentgen is not a unit of one.

Examples
--------
A roentgen in the SI unit:

>>> Roentgen(1).to(COULOMB_PER_KILOGRAM)
0.000258 C/kg

`EXPOSURE_UNITS` maps symbols such as ``"R"``, ``"mR"``, ``"uR"``, and ``"C/kg"`` to
their constructors for boundary code that reads unit labels from external data.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_CHARGE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Exposure
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.specific_charge import COULOMB_PER_KILOGRAM
from kuchka.units.electromagnetics.specific_charge import CoulombPerKilogram

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

ROENTGEN = UnitDef("roentgen", "R", Decimal("0.000258"), SPECIFIC_CHARGE)
MILLIROENTGEN = with_prefix(prefixes.MILLI, ROENTGEN)
MICROROENTGEN = with_prefix(prefixes.MICRO, ROENTGEN)

Exposure._canonical_unit = COULOMB_PER_KILOGRAM  # noqa: SLF001 -- reused from SpecificCharge's own unit


def _coulomb_per_kilogram(value: Numeric) -> Exposure:
    """Construct an Exposure from a magnitude in coulombs per kilogram."""
    return Exposure.from_specific_charge(CoulombPerKilogram(value))


def Roentgen(value: Numeric) -> Exposure:
    """Construct an Exposure from a magnitude in roentgens.

    Parameters
    ----------
    value : Numeric
        Magnitude in roentgens.

    Returns
    -------
    Exposure
        Exposure represented in roentgens.

    """
    return Exposure(to_exact(value) * ROENTGEN.scale, ROENTGEN)


def Milliroentgen(value: Numeric) -> Exposure:
    """Construct an Exposure from a magnitude in milliroentgens.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliroentgens.

    Returns
    -------
    Exposure
        Exposure represented in milliroentgens.

    """
    return Exposure(to_exact(value) * MILLIROENTGEN.scale, MILLIROENTGEN)


def Microroentgen(value: Numeric) -> Exposure:
    """Construct an Exposure from a magnitude in microroentgens.

    Parameters
    ----------
    value : Numeric
        Magnitude in microroentgens.

    Returns
    -------
    Exposure
        Exposure represented in microroentgens.

    """
    return Exposure(to_exact(value) * MICROROENTGEN.scale, MICROROENTGEN)


EXPOSURE_UNITS: Mapping[str, Callable[[Numeric], Exposure]] = unit_table(
    "EXPOSURE_UNITS",
    {
        COULOMB_PER_KILOGRAM: _coulomb_per_kilogram,
        ROENTGEN: Roentgen,
        MILLIROENTGEN: Milliroentgen,
        MICROROENTGEN: Microroentgen,
    },
)

__all__ = [
    "EXPOSURE_UNITS",
    "MICROROENTGEN",
    "MILLIROENTGEN",
    "ROENTGEN",
    "Microroentgen",
    "Milliroentgen",
    "Roentgen",
]
