"""Volume charge density constructors: coulombs and ampere-hours per volume.

    from kuchka import AmpereHourPerLitre, CoulombPerCubicMetre

    cloud = CoulombPerCubicMetre(0.000001)
    cell = AmpereHourPerLitre(0.7)

`VolumeChargeDensity` is electric charge in a volume, `Charge / Volume`.
Its canonical unit is the coulomb per cubic metre (`C/m³`).
The ampere-hour per litre is the volumetric capacity of a battery cell: it is exactly
3600000 C/m³.

Examples
--------
A cell quoted at 1 Ah/L holds 3.6 million coulombs in each cubic metre:

>>> AmpereHourPerLitre(1) == CoulombPerCubicMetre(3_600_000)
True

A cloud holding 2 C/m³ over 5 m³ holds 10 C:

>>> from kuchka import CubicMetre
>>> CoulombPerCubicMetre(2) * CubicMetre(5)
10 C

`VOLUME_CHARGE_DENSITY_UNITS` maps symbols such as ``"C/m3"`` and ``"Ah/L"`` to their
constructors, for boundary code that reads a unit as a string from outside the
application.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import VOLUME_CHARGE_DENSITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import VolumeChargeDensity
from kuchka.units.electromagnetics.charge import AMPERE_HOUR
from kuchka.units.electromagnetics.charge import COULOMB
from kuchka.units.geometry.volume import CUBIC_CENTIMETRE
from kuchka.units.geometry.volume import LITRE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

COULOMB_PER_CUBIC_METRE = UnitDef(
    "coulomb_per_cubic_metre",
    "C/m³",
    1,
    VOLUME_CHARGE_DENSITY,
    aliases=powered("C/m", 3),
    words=("coulombs per cubic metre", "coulombs per cubic meter"),
)
MILLICOULOMB_PER_CUBIC_METRE = with_prefix(prefixes.MILLI, COULOMB_PER_CUBIC_METRE)
MICROCOULOMB_PER_CUBIC_METRE = with_prefix(prefixes.MICRO, COULOMB_PER_CUBIC_METRE)
NANOCOULOMB_PER_CUBIC_METRE = with_prefix(prefixes.NANO, COULOMB_PER_CUBIC_METRE)
COULOMB_PER_CUBIC_CENTIMETRE = UnitDef(
    "coulomb_per_cubic_centimetre",
    "C/cm³",
    COULOMB.scale / CUBIC_CENTIMETRE.scale,
    VOLUME_CHARGE_DENSITY,
    aliases=powered("C/cm", 3),
    words=("coulombs per cubic centimetre", "coulombs per cubic centimeter"),
)
AMPERE_HOUR_PER_LITRE = UnitDef(
    "ampere_hour_per_litre",
    "Ah/L",
    AMPERE_HOUR.scale / LITRE.scale,
    VOLUME_CHARGE_DENSITY,
    aliases=("Ah/l",),
    words=("ampere-hours per litre", "ampere-hours per liter"),
)

VolumeChargeDensity._canonical_unit = COULOMB_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns VolumeChargeDensity's canonical unit


def CoulombPerCubicMetre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from coulombs per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per cubic metre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in coulombs per cubic metre.

    """
    return VolumeChargeDensity(
        to_exact(value) * COULOMB_PER_CUBIC_METRE.scale, COULOMB_PER_CUBIC_METRE
    )


def MillicoulombPerCubicMetre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from millicoulombs per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millicoulombs per cubic metre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in millicoulombs per cubic metre.

    """
    return VolumeChargeDensity(
        to_exact(value) * MILLICOULOMB_PER_CUBIC_METRE.scale,
        MILLICOULOMB_PER_CUBIC_METRE,
    )


def MicrocoulombPerCubicMetre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from microcoulombs per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in microcoulombs per cubic metre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in microcoulombs per cubic metre.

    """
    return VolumeChargeDensity(
        to_exact(value) * MICROCOULOMB_PER_CUBIC_METRE.scale,
        MICROCOULOMB_PER_CUBIC_METRE,
    )


def NanocoulombPerCubicMetre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from nanocoulombs per cubic metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in nanocoulombs per cubic metre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in nanocoulombs per cubic metre.

    """
    return VolumeChargeDensity(
        to_exact(value) * NANOCOULOMB_PER_CUBIC_METRE.scale, NANOCOULOMB_PER_CUBIC_METRE
    )


def CoulombPerCubicCentimetre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from coulombs per cubic centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in coulombs per cubic centimetre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in coulombs per cubic centimetre.

    """
    return VolumeChargeDensity(
        to_exact(value) * COULOMB_PER_CUBIC_CENTIMETRE.scale,
        COULOMB_PER_CUBIC_CENTIMETRE,
    )


def AmpereHourPerLitre(value: Numeric) -> VolumeChargeDensity:
    """Construct a VolumeChargeDensity from ampere-hours per litre.

    Parameters
    ----------
    value : Numeric
        Magnitude in ampere-hours per litre.

    Returns
    -------
    VolumeChargeDensity
        VolumeChargeDensity represented in ampere-hours per litre.

    """
    return VolumeChargeDensity(
        to_exact(value) * AMPERE_HOUR_PER_LITRE.scale, AMPERE_HOUR_PER_LITRE
    )


VOLUME_CHARGE_DENSITY_UNITS: Mapping[str, Callable[[Numeric], VolumeChargeDensity]] = (
    unit_table(
        "VOLUME_CHARGE_DENSITY_UNITS",
        {
            COULOMB_PER_CUBIC_METRE: CoulombPerCubicMetre,
            MILLICOULOMB_PER_CUBIC_METRE: MillicoulombPerCubicMetre,
            MICROCOULOMB_PER_CUBIC_METRE: MicrocoulombPerCubicMetre,
            NANOCOULOMB_PER_CUBIC_METRE: NanocoulombPerCubicMetre,
            COULOMB_PER_CUBIC_CENTIMETRE: CoulombPerCubicCentimetre,
            AMPERE_HOUR_PER_LITRE: AmpereHourPerLitre,
        },
    )
)

__all__ = [
    "AMPERE_HOUR_PER_LITRE",
    "COULOMB_PER_CUBIC_CENTIMETRE",
    "COULOMB_PER_CUBIC_METRE",
    "MICROCOULOMB_PER_CUBIC_METRE",
    "MILLICOULOMB_PER_CUBIC_METRE",
    "NANOCOULOMB_PER_CUBIC_METRE",
    "VOLUME_CHARGE_DENSITY_UNITS",
    "AmpereHourPerLitre",
    "CoulombPerCubicCentimetre",
    "CoulombPerCubicMetre",
    "MicrocoulombPerCubicMetre",
    "MillicoulombPerCubicMetre",
    "NanocoulombPerCubicMetre",
]
