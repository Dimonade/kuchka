"""Surface charge density constructors: coulombs and ampere-hours per area.

    from kuchka import CoulombPerSquareMetre, MicrocoulombPerSquareCentimetre

    plate = CoulombPerSquareMetre(0.02)
    film = MicrocoulombPerSquareCentimetre(10)

`SurfaceChargeDensity` is electric charge on a surface, `Charge / Area`.
Its canonical unit is the coulomb per square metre (`C/m²`), which is also how an
electric flux density and a polarization density are measured.
The microcoulomb per square centimetre is the unit ferroelectric polarization is quoted
in, and the milliampere-hour per square centimetre is the areal capacity of a battery
electrode: it is exactly 36000 C/m².

Examples
--------
A polarization of 10 µC/cm² is 0.1 C/m²:

>>> MicrocoulombPerSquareCentimetre(10).to(COULOMB_PER_SQUARE_METRE)
0.1 C/m²

A plate holding 2 C/m² over 3 m² holds 6 C:

>>> from kuchka import SquareMetre
>>> CoulombPerSquareMetre(2) * SquareMetre(3)
6 C

`SURFACE_CHARGE_DENSITY_UNITS` maps symbols such as ``"C/m2"`` and ``"uC/cm2"`` to
their constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SURFACE_CHARGE_DENSITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SurfaceChargeDensity
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.charge import COULOMB
from kuchka.units.electromagnetics.charge import MILLIAMPERE_HOUR
from kuchka.units.geometry.area import SQUARE_CENTIMETRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

COULOMB_PER_SQUARE_METRE = UnitDef(
    "coulomb_per_square_metre",
    "C/m²",
    1,
    SURFACE_CHARGE_DENSITY,
    aliases=powered("C/m", 2),
    words=("coulombs per square metre", "coulombs per square meter"),
)
MILLICOULOMB_PER_SQUARE_METRE = with_prefix(prefixes.MILLI, COULOMB_PER_SQUARE_METRE)
MICROCOULOMB_PER_SQUARE_METRE = with_prefix(prefixes.MICRO, COULOMB_PER_SQUARE_METRE)
NANOCOULOMB_PER_SQUARE_METRE = with_prefix(prefixes.NANO, COULOMB_PER_SQUARE_METRE)
COULOMB_PER_SQUARE_CENTIMETRE = UnitDef(
    "coulomb_per_square_centimetre",
    "C/cm²",
    COULOMB.scale / SQUARE_CENTIMETRE.scale,
    SURFACE_CHARGE_DENSITY,
    aliases=powered("C/cm", 2),
    words=("coulombs per square centimetre", "coulombs per square centimeter"),
)
MICROCOULOMB_PER_SQUARE_CENTIMETRE = with_prefix(
    prefixes.MICRO, COULOMB_PER_SQUARE_CENTIMETRE
)
MILLIAMPERE_HOUR_PER_SQUARE_CENTIMETRE = UnitDef(
    "milliampere_hour_per_square_centimetre",
    "mAh/cm²",
    MILLIAMPERE_HOUR.scale / SQUARE_CENTIMETRE.scale,
    SURFACE_CHARGE_DENSITY,
    aliases=powered("mAh/cm", 2),
    words=(
        "milliampere-hours per square centimetre",
        "milliampere-hours per square centimeter",
    ),
)

SurfaceChargeDensity._canonical_unit = COULOMB_PER_SQUARE_METRE  # noqa: SLF001 -- this module owns SurfaceChargeDensity's canonical unit


def CoulombPerSquareMetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from coulombs per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per square metre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in coulombs per square metre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * COULOMB_PER_SQUARE_METRE.scale, COULOMB_PER_SQUARE_METRE
    )


def MillicoulombPerSquareMetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from millicoulombs per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millicoulombs per square metre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in millicoulombs per square metre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * MILLICOULOMB_PER_SQUARE_METRE.scale,
        MILLICOULOMB_PER_SQUARE_METRE,
    )


def MicrocoulombPerSquareMetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from microcoulombs per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcoulombs per square metre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in microcoulombs per square metre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * MICROCOULOMB_PER_SQUARE_METRE.scale,
        MICROCOULOMB_PER_SQUARE_METRE,
    )


def NanocoulombPerSquareMetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from nanocoulombs per square metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanocoulombs per square metre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in nanocoulombs per square metre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * NANOCOULOMB_PER_SQUARE_METRE.scale,
        NANOCOULOMB_PER_SQUARE_METRE,
    )


def CoulombPerSquareCentimetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from coulombs per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per square centimetre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in coulombs per square centimetre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * COULOMB_PER_SQUARE_CENTIMETRE.scale,
        COULOMB_PER_SQUARE_CENTIMETRE,
    )


def MicrocoulombPerSquareCentimetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from microcoulombs per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcoulombs per square centimetre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in microcoulombs per square centimetre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * MICROCOULOMB_PER_SQUARE_CENTIMETRE.scale,
        MICROCOULOMB_PER_SQUARE_CENTIMETRE,
    )


def MilliampereHourPerSquareCentimetre(value: Numeric) -> SurfaceChargeDensity:
    """Construct a SurfaceChargeDensity from milliampere-hours per square centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in milliampere-hours per square centimetre.

    Returns
    -------
    SurfaceChargeDensity
        SurfaceChargeDensity represented in milliampere-hours per square centimetre.

    """
    return SurfaceChargeDensity(
        to_exact(value) * MILLIAMPERE_HOUR_PER_SQUARE_CENTIMETRE.scale,
        MILLIAMPERE_HOUR_PER_SQUARE_CENTIMETRE,
    )


SURFACE_CHARGE_DENSITY_UNITS: Mapping[
    str, Callable[[Numeric], SurfaceChargeDensity]
] = unit_table(
    "SURFACE_CHARGE_DENSITY_UNITS",
    {
        COULOMB_PER_SQUARE_METRE: CoulombPerSquareMetre,
        MILLICOULOMB_PER_SQUARE_METRE: MillicoulombPerSquareMetre,
        MICROCOULOMB_PER_SQUARE_METRE: MicrocoulombPerSquareMetre,
        NANOCOULOMB_PER_SQUARE_METRE: NanocoulombPerSquareMetre,
        COULOMB_PER_SQUARE_CENTIMETRE: CoulombPerSquareCentimetre,
        MICROCOULOMB_PER_SQUARE_CENTIMETRE: MicrocoulombPerSquareCentimetre,
        MILLIAMPERE_HOUR_PER_SQUARE_CENTIMETRE: MilliampereHourPerSquareCentimetre,
    },
)

__all__ = [
    "COULOMB_PER_SQUARE_CENTIMETRE",
    "COULOMB_PER_SQUARE_METRE",
    "MICROCOULOMB_PER_SQUARE_CENTIMETRE",
    "MICROCOULOMB_PER_SQUARE_METRE",
    "MILLIAMPERE_HOUR_PER_SQUARE_CENTIMETRE",
    "MILLICOULOMB_PER_SQUARE_METRE",
    "NANOCOULOMB_PER_SQUARE_METRE",
    "SURFACE_CHARGE_DENSITY_UNITS",
    "CoulombPerSquareCentimetre",
    "CoulombPerSquareMetre",
    "MicrocoulombPerSquareCentimetre",
    "MicrocoulombPerSquareMetre",
    "MilliampereHourPerSquareCentimetre",
    "MillicoulombPerSquareMetre",
    "NanocoulombPerSquareMetre",
]
